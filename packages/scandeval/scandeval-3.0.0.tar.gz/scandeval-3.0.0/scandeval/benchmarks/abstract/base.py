'''Abstract base class for evaluating models'''

from abc import ABC, abstractmethod
from datasets import Dataset
from transformers.models.auto.auto_factory import _BaseAutoModelClass
import transformers.utils.logging as tf_logging
from transformers import (PreTrainedTokenizerBase,
                          AutoTokenizer,
                          AutoConfig,
                          TrainingArguments,
                          Trainer,
                          PrinterCallback,
                          EarlyStoppingCallback,
                          RobertaForSequenceClassification,
                          RobertaForTokenClassification,
                          ProgressCallback)
from typing import Dict, Optional, Tuple, List, Any
import numpy as np
import requests
from bs4 import BeautifulSoup
import subprocess
from tqdm.auto import tqdm
from collections import defaultdict
import warnings
from functools import partial
import gc
import logging
import re
import random
import os

from ...utils import (MODEL_CLASSES, is_module_installed, InvalidBenchmark,
                      TwolabelTrainer, get_all_datasets,
                      NeverLeaveProgressCallback)


logger = logging.getLogger(__name__)


class BaseBenchmark(ABC):
    '''Abstract base class for finetuning and evaluating models.

    Args:
        name (str):
            The name of the dataset.
        task (str):
            The type of task to be benchmarked.
        metric_names (dict):
            A dictionary with the variable names of the metrics used in the
            dataset as keys, and a more human readable name of them as values.
        id2label (list or None, optional):
            A list of all the labels, which is used to convert indices to their
            labels. This will only be used if the pretrained model does not
            already have one. Defaults to None.
        label_synonyms (list of lists of str or None, optional):
            A list of synonyms for each label. Every entry in `label_synonyms`
            is a list of synonyms, where one of the synonyms is contained in
            `id2label`. If None then no synonyms will be used. Defaults to
            None.
        evaluate_train (bool, optional):
            Whether the models should be evaluated on the training scores.
            Defaults to False.
        cache_dir (str, optional):
            Where the downloaded models will be stored. Defaults to
            '.benchmark_models'.
        two_labels (bool, optional):
            Whether two labels should be predicted in the dataset.  If this is
            True then `split_point` has to be set. Defaults to False.
        split_point (int or None, optional):
            When there are two labels to be predicted, this is the index such
            that `id2label[:split_point]` contains the labels for the first
            label, and `id2label[split_point]` contains the labels for the
            second label. Only relevant if `two_labels` is True. Defaults to
            None.
        verbose (bool, optional):
            Whether to print additional output during evaluation. Defaults to
            False.

    Parameters:
        name (str): The name of the dataset.
        task (str): The type of task to be benchmarked.
        metric_names (dict): The names of the metrics.
        id2label (list or None): A list converting indices to labels.
        label2id (dict or None): A dictionary converting labels to indices.
        num_labels (int or None): The number of labels in the dataset.
        label_synonyms (list of lists of str): Synonyms of the dataset labels.
        evaluate_train (bool): Whether the training set should be evaluated.
        cache_dir (str): Directory where models are cached.
        two_labels (bool): Whether two labels should be predicted.
        split_point (int or None): Splitting point of `id2label` into labels.
        verbose (bool): Whether to print additional output.
    '''
    def __init__(self,
                 name: str,
                 task: str,
                 metric_names: Dict[str, str],
                 id2label: Optional[List[str]] = None,
                 label_synonyms: Optional[List[List[str]]] = None,
                 evaluate_train: bool = False,
                 cache_dir: str = '.benchmark_models',
                 two_labels: bool = False,
                 split_point: Optional[int] = None,
                 verbose: bool = False):

        self.short_name = name
        self.name = [long_name
                     for short_name, long_name, _, _ in get_all_datasets()
                     if name == short_name][0]
        self.task = task
        self.metric_names = metric_names
        self.id2label = id2label
        self.label_synonyms = label_synonyms
        self.evaluate_train = evaluate_train
        self.cache_dir = cache_dir
        self.two_labels = two_labels
        self.split_point = split_point
        self.verbose = verbose

        if id2label is not None:

            # Store the number of labels
            self.num_labels = len(id2label)

            # Set default value of label synonyms, if None was given
            if label_synonyms is None:
                self.label_synonyms = [[label] for label in self.id2label]

            # Define the label2id conversion dictionary
            self.label2id = {label: id for id, lbl in enumerate(id2label)
                             for label_syns in self.label_synonyms
                             for label in label_syns
                             if lbl in label_syns}

        # If the id2label conversion list was not given, then set the number of
        # labels to zero and set the label2id conversion dict to None as well
        else:
            self.num_labels = None
            self.label2id = None

        # If verbose is set to True then enable transformers output, which is
        # done by setting it to warning (the default)
        if verbose:
            tf_logging.set_verbosity_warning()

    @staticmethod
    def _get_model_task(task: Optional[str]) -> str:
        '''Get the task of the model.

        Args:
            task (str or None): The task of the model.

        Returns:
            str: The task of the model.
        '''
        pretrained_tasks = ['fill-mask',
                            'sentence-similarity',
                            'feature-extraction']
        if task is None or task in pretrained_tasks:
            return 'fill-mask'
        else:
            return task

    def _get_model_class(self, framework: str) -> _BaseAutoModelClass:
        return MODEL_CLASSES[framework][self.task]

    @staticmethod
    def _get_stats(metrics: Dict[str, List[Dict[str, float]]],
                   metric_name: str) -> Dict[str, Tuple[float, float]]:
        '''Helper function to compute the mean with confidence intervals.

        Args:
            metrics (dict):
                Dictionary with the names of the metrics as keys, of the form
                "<split>_<metric_name>", such as "val_f1", and values the
                metric values.
            metric_name (str):
                The name of the metric. Is used to collect the correct metric
                from `metrics`.

        Returns:
            dict:
                Dictionary with keys among 'train' and 'test', with
                corresponding values being a pair of floats, containing the
                score and the radius of its 95% confidence interval.
        '''
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')

            results = dict()

            if 'train' in metrics.keys():
                train_scores = [dct[f'train_{metric_name}']
                                for dct in metrics['train']]
                train_score = np.mean(train_scores)

                if len(train_scores) > 1:
                    sample_std = np.std(train_scores, ddof=1)
                    train_se = sample_std / np.sqrt(len(train_scores))
                else:
                    train_se = np.nan

                results['train'] = (train_score, 1.96 * train_se)

            if 'test' in metrics.keys():
                test_scores = [dct[f'test_{metric_name}']
                               for dct in metrics['test']]
                test_score = np.mean(test_scores)

                if len(test_scores) > 1:
                    sample_std = np.std(test_scores, ddof=1)
                    test_se = sample_std / np.sqrt(len(test_scores))
                else:
                    test_se = np.nan

                results['test'] = (test_score, 1.96 * test_se)

            return results

    def _load_model(self,
                    model_id: str,
                    revision: Optional[str] = 'main',
                    framework: Optional[str] = None,
                    task: Optional[str] = None) -> Dict[str, Any]:
        '''Load the model.

        Args:
            model_id (str):
                The full HuggingFace Hub path to the pretrained transformer
                model.
            revision (str or None, optional):
                The specific model version to use. It can be a branch name,
                a tag name, or a commit id. Currently only supported for
                HuggingFace models. Defaults to 'main' for latest.
            framework (str or None, optional):
                The framework the model has been built in. Currently supports
                'pytorch', 'jax', and 'spacy'. If None then this will be
                inferred from `model_id`. Defaults to None.
            task (str or None, optional):
                The task for which the model was trained on. If None then this
                will be inferred from `model_id`. Defaults to None.

        Returns:
            dict:
                A dictionary containing at least the key 'model', with the
                value being the model. Can contain other objects related to the
                model, such as its tokenizer.

        Raises:
            RuntimeError: If the framework is not recognized.
        '''
        # Get the name of a framework supported for the model_id
        if framework is None or task is None:
            model_metadata = self._fetch_model_metadata(model_id)
            if framework is None:
                framework = model_metadata['framework']
            if task is None:
                task = model_metadata['task']

        # Ensure that the framework is installed
        from_flax = False
        try:
            if framework in ('pytorch', 'jax'):
                import torch
                import torch.nn as nn
                from torch.nn import Parameter
                if framework == 'jax':
                    from_flax = True
                    import jax  # noqa
                    framework = 'pytorch'
            elif framework == 'spacy':
                import spacy

                # Ignore warnings from SpaCy. This has to be called after the
                # import, as the __init__.py file of SpaCy sets the warning
                # levels of SpaCy warning W036
                import warnings
                warnings.filterwarnings('ignore', module='spacy*')

        except ModuleNotFoundError:
            msg = (f'The model {model_id} is built using the {framework} '
                   f'framework which is not installed. Try installing the '
                   f'ScandEval package as `pip install '
                   f'scandeval[{framework}]`.')
            raise ModuleNotFoundError(msg)

        if framework == 'pytorch':

            if task == 'fill-mask':
                params = dict(num_labels=self.num_labels,
                              id2label=self.id2label,
                              label2id=self.label2id)
            else:
                params = dict()

            try:
                # If the model ID specifies a random model, then load that.
                if model_id.startswith('random'):
                    rnd_id = 'xlm-roberta-base'
                    config = AutoConfig.from_pretrained(rnd_id,
                                                        revision=revision,
                                                        **params)

                    if model_id == 'random-roberta-sequence-clf':
                        model_cls = RobertaForSequenceClassification
                    elif model_id == 'random-roberta-token-clf':
                        model_cls = RobertaForTokenClassification
                    else:
                        raise ValueError(f'A random model was chosen, '
                                         f'"{model_id}", but it was not '
                                         f'recognized.')

                    model = model_cls(config)

                # Otherwise load the pretrained model
                else:
                    config = AutoConfig.from_pretrained(model_id,
                                                        revision=revision,
                                                        **params)
                    model_cls = self._get_model_class(framework=framework)
                    model = model_cls.from_pretrained(model_id,
                                                      revision=revision,
                                                      config=config,
                                                      cache_dir=self.cache_dir,
                                                      from_flax=from_flax)

                # Get the `label2id` and `id2label` conversions from the model
                # config
                try:
                    model_label2id = dict(model.config.label2id)
                except AttributeError:
                    model_label2id = None
                try:
                    try:
                        model_num_labels = len(model.config.id2label)
                        if not isinstance(model.config.id2label, list):
                            model_id2label = dict(model.config.id2label)
                        else:
                            model_id2label = model.config.id2label
                        model_id2label = [model_id2label[idx]
                                          for idx in range(model_num_labels)]
                    except IndexError:
                        raise InvalidBenchmark('There is a gap in the '
                                               'indexing dictionary of the '
                                               'model.')
                except AttributeError:
                    model_id2label = None

                # If one of `label2id` or `id2label` exists in the model
                # config, then define the other one from it
                if model_label2id is not None and model_id2label is None:
                    model_id2label = [label for label in model_label2id.keys()]
                    model.config.id2label = model_id2label
                if model_label2id is None and model_id2label is not None:
                    model_label2id = {lbl: id
                                      for id, lbl in enumerate(model_id2label)}
                    model.config.label2id = model_label2id

                # If the model does not have `label2id` or `id2label`
                # conversions, then use the defaults
                if (task == 'fill-mask' or
                        (model_label2id is None and model_id2label is None)):
                    model.config.label2id = self.label2id
                    model.config.id2label = self.id2label

                # If the model *does* have conversions, then ensure that it can
                # deal with all the labels in the default conversions. This
                # ensures that we can smoothly deal with labels that the model
                # have not been trained on (it will just always get those
                # labels wrong)
                else:

                    # Collect the dataset labels and model labels in the
                    # `model_id2label` conversion list
                    for label in self.id2label:
                        syns = [syn for lst in self.label_synonyms
                                for syn in lst
                                if label in lst]
                        if all([syn not in model_id2label for syn in syns]):
                            model_id2label.append(label)

                    # Ensure that the model_id2label does not contain
                    # duplicates modulo synonyms
                    for idx, label in enumerate(model_id2label):
                        try:
                            canonical_syn = [syn_lst
                                             for syn_lst in self.label_synonyms
                                             if label in syn_lst][0][-1]
                            model_id2label[idx] = canonical_syn

                        # IndexError appears when the label does not appear
                        # within the label_synonyms (i.e. that we added it in
                        # the previous step). In this case, we just skip the
                        # label.
                        except IndexError:
                            continue

                    # Get the synonyms of all the labels, new ones included
                    new_synonyms = self.label_synonyms
                    flat_old_synonyms = [syn for lst in self.label_synonyms
                                         for syn in lst]
                    new_synonyms += [[label] for label in model_id2label
                                     if label not in flat_old_synonyms]

                    # Add all the synonyms of the labels into the label2id
                    # conversion dictionary
                    model_label2id = {label: id
                                      for id, lbl in enumerate(model_id2label)
                                      for label_syns in new_synonyms
                                      for label in label_syns
                                      if lbl in label_syns}

                    # Get the old id2label conversion
                    if not isinstance(model.config.id2label, list):
                        old_id2label = dict(model.config.id2label)
                    else:
                        old_id2label = model.config.id2label

                    # This changes the classification layer in the finetuned
                    # model to be consistent with all the labels in the
                    # dataset. If the model was previously finetuned on a
                    # dataset which left out a label, say, then that label will
                    # be inserted in the model architecture here, but without
                    # the model ever predicting it. This will allow the model
                    # to be benchmarked on such datasets, however.
                    # NOTE: This only works on classification tasks. This code
                    #       needs to be rewritten when we add other types of
                    #       tasks.
                    # NOTE: Only works for pytorch models at the moment
                    if (len(model_id2label) > len(old_id2label)
                            and framework == 'pytorch'):

                        # Count the number of new labels to add to the model
                        num_new_labels = (len(model_id2label) -
                                          len(old_id2label))

                        # If *all* the new labels are new and aren't even
                        # synonyms of the model's labels, then raise an
                        # exception
                        if num_new_labels == self.num_labels:
                            if len(set(flat_old_synonyms)
                                   .intersection(old_id2label)) == 0:
                                msg = ('The model has not been trained on '
                                       'any of the labels in the dataset, or '
                                       'synonyms thereof.')
                                raise InvalidBenchmark(msg)

                        # Load the weights from the model's current
                        # classification layer. This handles both the token
                        # classification case and the sequence classification
                        # case.
                        # NOTE: This might need additional cases (or a general
                        #       solution) when we start dealing with other
                        #       tasks.
                        try:
                            clf_weight = model.classifier.weight.data
                        except AttributeError:
                            try:
                                clf_weight = (model.classifier
                                                   .out_proj
                                                   .weight
                                                   .data)
                            except AttributeError:
                                msg = ('Model does not seem to be a '
                                       'classification model.')
                                raise InvalidBenchmark(msg)

                        # Create the new weights, which have zeros at all the
                        # new entries
                        zeros = torch.zeros(num_new_labels, config.hidden_size)
                        new_clf_weight = torch.cat((clf_weight, zeros), dim=0)
                        new_clf_weight = Parameter(new_clf_weight)

                        # Create the new classification layer
                        new_clf = nn.Linear(config.hidden_size,
                                            len(model_id2label))

                        # Assign the new weights to the new classification
                        # layer, and replace the old classification layer with
                        # this one
                        new_clf.weight = new_clf_weight
                        model.classifier = new_clf

                        # Update the number of labels the model thinks it has.
                        # This is required to avoid exceptions when evaluating
                        model.config.num_labels = len(model_id2label)
                        model.num_labels = len(model_id2label)

                    # Update the model's own conversions with the new ones
                    model.config.id2label = model_id2label
                    model.config.label2id = model_label2id

            except (OSError, ValueError):
                raise InvalidBenchmark(f'The model {model_id} could not be '
                                       f'loaded from the HuggingFace hub')

            # If the model is a subclass of a RoBERTa model then we have to add
            # a prefix space to the tokens, by the way the model is
            # constructed.
            if model_id.startswith('random'):
                params = dict(use_fast=True, add_prefix_space=True)
                tokenizer = AutoTokenizer.from_pretrained(rnd_id,
                                                          revision=revision,
                                                          **params)
            else:
                prefix = 'Roberta' in type(model).__name__
                params = dict(use_fast=True, add_prefix_space=prefix)
                tokenizer = AutoTokenizer.from_pretrained(model_id,
                                                          revision=revision,
                                                          **params)

            # Set the maximal length of the tokenizer to the model's maximal
            # length. This is required for proper truncation
            if (not hasattr(tokenizer, 'model_max_length') or
                    tokenizer.model_max_length > 1_000):

                if hasattr(tokenizer, 'max_model_input_sizes'):
                    all_max_lengths = tokenizer.max_model_input_sizes.values()
                    if len(list(all_max_lengths)) > 0:
                        min_max_length = min(list(all_max_lengths))
                        tokenizer.model_max_length = min_max_length
                    else:
                        tokenizer.model_max_length = 512
                else:
                    tokenizer.model_max_length = 512

            return dict(model=model, tokenizer=tokenizer)

        elif framework == 'spacy':
            local_model_id = model_id.split('/')[-1]

            # Download the model if it has not already been so
            if not is_module_installed(local_model_id):
                url = (f'https://huggingface.co/{model_id}/resolve/main/'
                       f'{local_model_id}-any-py3-none-any.whl')
                logger.info('Model not installed. Downloading model')
                subprocess.run(['pip3', 'install', url, '--quiet'])
                logger.info('Finished downloading model. Resuming benchmark:')

            # Load the model
            try:
                model = spacy.load(local_model_id)
            except OSError:
                raise InvalidBenchmark(f'The model {model_id} could not '
                                       f'be installed from spaCy.')

            return dict(model=model)

        else:
            raise RuntimeError(f'The framework "{framework}" is not '
                               f'supported!')

    @abstractmethod
    def _load_data(self) -> Tuple[Dataset, Dataset]:
        '''Load the datasets.

        Returns:
            A triple of HuggingFace datasets:
                The train and test datasets.
        '''
        pass

    @abstractmethod
    def _preprocess_data(self,
                         dataset: Dataset,
                         framework: str,
                         **kwargs) -> Dataset:
        '''Preprocess a dataset by tokenizing and aligning the labels.

        Args:
            dataset (HuggingFace dataset):
                The dataset to preprocess.
            kwargs:
                Extra keyword arguments containing objects used in
                preprocessing the dataset.

        Returns:
            HuggingFace dataset: The preprocessed dataset.
        '''
        pass

    @abstractmethod
    def _load_data_collator(
            self,
            tokenizer: Optional[PreTrainedTokenizerBase] = None):
        '''Load the data collator used to prepare samples during finetuning.

        Args:
            tokenizer (HuggingFace tokenizer or None, optional):
                A pretrained tokenizer. Can be None if the tokenizer is not
                used in the initialisation of the data collator. Defaults to
                None.

        Returns:
            HuggingFace data collator: The data collator.
        '''
        pass

    @abstractmethod
    def _compute_metrics(self,
                         predictions_and_labels: tuple,
                         id2label: Optional[list] = None) -> Dict[str, float]:
        '''Compute the metrics needed for evaluation.

        Args:
            predictions_and_labels (pair of arrays):
                The first array contains the probability predictions and the
                second array contains the true labels.
            id2label (list or None, optional):
                Conversion of indices to labels. Defaults to None.

        Returns:
            dict:
                A dictionary with the names of the metrics as keys and the
                metric values as values.
        '''
        pass

    def _log_metrics(self,
                     metrics: Dict[str, List[Dict[str, float]]],
                     finetuned: bool,
                     model_id: str) -> Dict[str, dict]:
        '''Log the metrics.

        Args:
            metrics (dict):
                The metrics that are to be logged. This is a dict with keys
                'train' and 'test', with values being lists of dictionaries
                full of metrics.
            finetuned (bool):
                Whether the model is finetuned or not.
            model_id (str):
                The full HuggingFace Hub path to the pretrained transformer
                model.

        Returns:
            dict:
                A dictionary with keys 'raw_metrics' and 'total', with
                'raw_metrics' being identical to `metrics` and 'total' being
                a dictionary with the aggregated metrics (means and standard
                errors).
        '''
        # Initial logging message
        if finetuned:
            msg = (f'Finished finetuning and evaluation of {model_id} on '
                   f'{self.name}.')
        else:
            msg = (f'Finished evaluation of {model_id} on {self.name}.')
        logger.info(msg)

        # Initialise the total dict
        total_dict = dict()

        # Logging of the metric(s)
        for metric_key, metric_name in self.metric_names.items():
            scores = self._get_stats(metrics, metric_key)
            test_score, test_se = scores['test']
            test_score *= 100
            test_se *= 100

            msg = (f'{metric_name}:\n'
                   f'  - Test: {test_score:.2f} ± {test_se:.2f}')

            if 'train' in scores.keys():
                train_score, train_se = scores['train']
                train_score *= 100
                train_se *= 100
                msg += f'\n  - Train: {train_score:.2f} ± {train_se:.2f}'

                # Store the aggregated train metrics
                total_dict[f'train_{metric_key}'] = train_score
                total_dict[f'train_{metric_key}_se'] = train_se

            # Store the aggregated test metrics
            total_dict[f'test_{metric_key}'] = test_score
            total_dict[f'test_{metric_key}_se'] = test_se

            # Log the scores
            logger.info(msg)

        # Define a dict with both the raw metrics and the aggregated metrics
        extended_metrics = dict(raw_metrics=metrics, total=total_dict)

        # Return the extended metrics
        return extended_metrics

    @abstractmethod
    def _get_spacy_predictions_and_labels(self,
                                          model,
                                          dataset: Dataset,
                                          progress_bar: bool) -> tuple:
        '''Get predictions from SpaCy model on dataset.

        Args:
            model (SpaCy model): The model.
            dataset (HuggingFace dataset): The dataset.

        Returns:
            A pair of arrays:
                The first array contains the probability predictions and the
                second array contains the true labels.
        '''
        pass

    def _fetch_model_metadata(self, model_id: str) -> Dict[str, str]:
        '''Fetches metdataof a model from the HuggingFace Hub.

        Args:
            model_id (str):
                The full HuggingFace Hub path to the pretrained transformer
                model.

        Returns:
            dict:
                The keys are names of metadata, with the values being the
                strings that describe the value of that metadata. Keys involve
                'framework' and 'task', where a framework could be 'pytorch'
                and a task could be 'token-classification'.

        Raises:
            RuntimeError: If the extracted framework is not recognized.
        '''
        # If the model ID specifies a random ID, then return a hardcoded
        # metadata dictionary
        if model_id.startswith('random'):
            return dict(task='fill-mask', framework='pytorch')

        # Parse all the anchor tags from the model website
        model_id, *_ = model_id.split('@', 1)
        url = 'https://www.huggingface.co/' + model_id
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        a_tags = soup.find_all('a')
        a_tags_with_class = [a for a in a_tags if a.get('class') is not None]

        # Fetch the frameworks from the model website
        frameworks = [re.sub(r'.*=', '', a['href'])
                      for a in a_tags_with_class
                      if 'tag-white' in a['class'] and 'library' in a['href']]

        # Set up the order of the frameworks
        valid_frameworks = ['pytorch', 'spacy', 'jax']

        # Extract a single valid framework in which the model has been
        # implemented
        for valid_framework in valid_frameworks:
            if valid_framework in frameworks:
                framework = valid_framework
                break
        else:
            msg = f'Cannot detect the framework of {model_id}!'
            raise InvalidBenchmark(msg)

        # Fetch the model tasks from the model website
        tasks = [re.sub(r'.*=', '', a['href'])
                 for a in a_tags_with_class
                 if 'tag-white' in a['class'] and 'pipeline_tag' in a['href']]

        # Extract a single valid task on which the model has been trained. If
        # no task has been specified on the model card then assume that it is
        # 'fill-mask'
        task = self._get_model_task(tasks[0]) if len(tasks) else 'fill-mask'

        return dict(framework=framework, task=task)

    def benchmark(self,
                  model_id: str,
                  progress_bar: bool = True
                  ) -> Dict[str, dict]:
        '''Benchmark a model.

        Args:
            model_id (str):
                The full HuggingFace Hub path to the pretrained transformer
                model. The specific model version to use can be added after
                the suffix '@': "model_id@v1.0.0". It can be a branch name,
                a tag name, or a commit id (currently only supported for
                HuggingFace models, and it defaults to 'main' for latest).
            progress_bar (bool, optional):
                Whether to show a progress bar or not. Defaults to True.

        Returns:
            dict:
                The keys in the dict are 'raw_metrics' and 'total', with all
                the raw metrics in the first dictionary and the aggregated
                metrics in the second.

        Raises:
            RuntimeError: If the extracted framework is not recognized.
        '''
        # Fetch the model metadata
        model_metadata = self._fetch_model_metadata(model_id)
        framework = model_metadata['framework']
        task = model_metadata['task']

        # Extract the revision, if it is specified
        if '@' in model_id:
            model_id, revision = model_id.split('@', 1)
        else:
            revision = 'main'

        # Set random seeds to enforce reproducibility of the randomly
        # initialised weights
        random.seed(4242)
        np.random.seed(4242)
        rng = np.random.default_rng(4242)
        if framework in ('pytorch', 'jax'):
            import torch
            torch.manual_seed(4242)
            torch.cuda.manual_seed_all(4242)
            os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
            os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'
            torch.backends.cudnn.benchmark = False
            torch.backends.cudnn.deterministic = True
            torch.use_deterministic_algorithms(True)

        # Load the model
        model_dict = self._load_model(model_id,
                                      revision=revision,
                                      **model_metadata)

        # Define variable that determines if the model should be finetuned
        finetune = (task == 'fill-mask')

        # Load the dataset
        train, test = self._load_data()

        # Remove empty examples from the datasets
        try:
            train = train.filter(lambda x: len(x['tokens']) > 0)
            test = test.filter(lambda x: len(x['tokens']) > 0)
        except KeyError:
            try:
                train = train.filter(lambda x: len(x['doc']) > 0)
                test = test.filter(lambda x: len(x['doc']) > 0)
            except KeyError:
                pass

        # Get bootstrap sample indices
        test_bidxs = rng.integers(0, len(test), size=(9, len(test)))

        if framework in ('pytorch', 'jax'):
            framework = 'pytorch'

            # Extract the model and tokenizer
            model = model_dict['model']
            tokenizer = model_dict['tokenizer']

            # Preprocess the datasets
            try:
                params = dict(framework=framework,
                              config=model.config,
                              tokenizer=tokenizer)
                if finetune or self.evaluate_train:
                    train = self._preprocess_data(train, **params)
                test = self._preprocess_data(test, **params)
            except ValueError:
                raise InvalidBenchmark('Preprocessing of the dataset could '
                                       'not be done.')

            # Get bootstrapped datasets
            tests = [test]
            tests += [Dataset.from_dict(test[test_bidxs[idx]])
                      for idx in range(test_bidxs.shape[0])]

            # Set up progress bar
            if finetune:
                if progress_bar:
                    itr = tqdm(range(10), desc='Benchmarking')
                else:
                    itr = range(10)
            else:
                itr = [0]

            # Load the data collator
            data_collator = self._load_data_collator(tokenizer)

            # Initialise training arguments
            training_args = TrainingArguments(
                output_dir='.',
                evaluation_strategy='epoch',
                logging_strategy='epoch' if self.verbose else 'no',
                save_strategy='epoch',
                report_to='none',
                save_total_limit=1,
                per_device_train_batch_size=32,
                per_device_eval_batch_size=32,
                learning_rate=2e-5,
                num_train_epochs=1000,
                warmup_steps=((len(train) * 0.9) // 32),
                gradient_accumulation_steps=1,
                load_best_model_at_end=True,
                optim='adamw_torch',
                seed=4242,
            )

            # Manually set `disable_tqdm` to `False` if `progress_bar` is
            # `True`
            if progress_bar:
                training_args.disable_tqdm = False

            metrics = defaultdict(list)
            for idx in itr:
                while True:
                    try:
                        # Set random seeds to enforce reproducibility of the
                        # randomly initialised weights
                        training_args.seed = 4242 + idx
                        random.seed(4242 + idx)
                        np.random.seed(4242 + idx)
                        if framework in ('pytorch', 'jax'):
                            import torch
                            torch.manual_seed(4242 + idx)
                            torch.cuda.manual_seed_all(4242 + idx)

                        # Reinitialise a new model
                        model = self._load_model(model_id,
                                                 revision=revision,
                                                 **model_metadata)['model']

                        # Initialise compute_metrics function
                        compute_metrics = partial(
                            self._compute_metrics,
                            id2label=model.config.id2label
                        )

                        # Initialise early stopping callback
                        patience = 2 + 1000 // len(train)
                        params = dict(early_stopping_patience=patience)
                        early_stopping = EarlyStoppingCallback(**params)

                        # Initialise Trainer
                        split = train.train_test_split(0.1, seed=4242)
                        trainer_args = dict(model=model,
                                            args=training_args,
                                            train_dataset=split['train'],
                                            eval_dataset=split['test'],
                                            tokenizer=tokenizer,
                                            data_collator=data_collator,
                                            compute_metrics=compute_metrics,
                                            callbacks=[early_stopping])
                        if self.two_labels:
                            trainer_args['split_point'] = self.split_point
                            trainer = TwolabelTrainer(**trainer_args)
                        else:
                            trainer = Trainer(**trainer_args)

                        # Set transformers logging back to error
                        tf_logging.set_verbosity_error()

                        # Remove trainer logging
                        trainer.log = lambda _: None

                        # Remove the callback which prints the metrics after
                        # each evaluation
                        if not self.verbose:
                            trainer.remove_callback(PrinterCallback)

                        # Remove the progress bar callback
                        trainer.remove_callback(ProgressCallback)

                        # Add the custom progress callback if `progress_bar` is
                        # True
                        if progress_bar:
                            trainer.add_callback(NeverLeaveProgressCallback)

                        # Finetune the model
                        if finetune:
                            trainer.train()

                        # Log training metrics and save the state
                        if self.evaluate_train:
                            train_metrics = trainer.evaluate(
                                train,
                                metric_key_prefix='train'
                            )
                            metrics['train'].append(train_metrics)

                        # Set up a progress bar for the test datasets if we are
                        # not finetuning
                        if not finetune:
                            if progress_bar:
                                test_itr = tqdm(tests, desc='Benchmarking')
                            else:
                                test_itr = tests
                        else:
                            test_itr = [tests[idx]]

                        # Log test metrics
                        for dataset in test_itr:
                            test_metrics = trainer.evaluate(
                                dataset,
                                metric_key_prefix='test'
                            )
                            metrics['test'].append(test_metrics)

                        break

                    except (RuntimeError, ValueError, IndexError) as e:

                        # We assume that all these CUDA errors are caused by
                        # insufficient GPU memory
                        cuda_errs = [
                            'CUDA out of memory',
                            'CUDA error'
                        ]

                        # If it is an unknown error, then simply report it
                        if all([err not in str(e) for err in cuda_errs]):

                            # Garbage collection, to avoid memory issues
                            try:
                                del model
                            except UnboundLocalError:
                                pass
                            try:
                                del model_dict
                            except UnboundLocalError:
                                pass
                            gc.collect()
                            raise InvalidBenchmark(str(e))

                        # If it is a CUDA memory error, then reduce batch size
                        # and up gradient accumulation
                        bs = training_args.per_device_train_batch_size
                        ga = training_args.gradient_accumulation_steps
                        if bs == 1:
                            raise InvalidBenchmark('CUDA out of memory, even '
                                                   'with a batch size of 1!')
                        training_args.per_device_train_batch_size = bs // 2
                        training_args.per_device_eval_batch_size = bs // 2
                        training_args.gradient_accumulation_steps = ga * 2

                        # Garbage collection, to avoid memory issues
                        try:
                            del model
                        except UnboundLocalError:
                            pass
                        try:
                            del model_dict
                        except UnboundLocalError:
                            pass
                        gc.collect()

            metrics = self._log_metrics(metrics=metrics,
                                        model_id=model_id,
                                        finetuned=finetune)

            # Garbage collection, to avoid memory issues
            try:
                del model, model_dict
            except UnboundLocalError:
                try:
                    del model
                except UnboundLocalError:
                    pass
            gc.collect()

            return metrics

        elif framework == 'spacy':
            # Load the model
            model = model_dict['model']

            # Preprocess the test datasets
            test = self._preprocess_data(test, framework=framework)
            tests = [test]
            tests += [Dataset.from_dict(test[test_bidxs[idx]])
                      for idx in range(test_bidxs.shape[0])]

            # Get the test predictions
            all_test_metrics = list()
            for dataset in tqdm(tests, desc='Benchmarking'):
                preds_labels = self._get_spacy_predictions_and_labels(
                    model=model,
                    dataset=dataset,
                    progress_bar=progress_bar
                )

                # Check if the SpaCy model has been trained on the task at
                # hand. If not, then skip this benchmark.
                sample_preds = preds_labels[0][0]
                pos_ner_test = (isinstance(sample_preds, list) and
                                '' in sample_preds)
                dep_test = (isinstance(sample_preds[0], list) and
                            '' in sample_preds[0])
                if pos_ner_test or dep_test:
                    raise InvalidBenchmark('This SpaCy model have not been '
                                           'trained on this task. Skipping.')

                test_metrics = self._compute_metrics(preds_labels)
                test_metrics = {f'test_{key}': val
                                for key, val in test_metrics.items()}
                all_test_metrics.append(test_metrics)
            metrics = dict(test=all_test_metrics)

            if self.evaluate_train:

                # Preprocess the train datasets
                train = self._preprocess_data(train, framework=framework)

                # Get the train predictions
                all_train_metrics = list()
                for _ in range(10):
                    preds_labels = self._get_spacy_predictions_and_labels(
                        model=model,
                        dataset=train,
                        progress_bar=progress_bar
                    )
                    train_metrics = self._compute_metrics(preds_labels)
                    train_metrics = {f'train_{key}': val
                                     for key, val in train_metrics.items()}

                all_train_metrics.append(train_metrics)
                metrics['train'] = all_train_metrics

            metrics = self._log_metrics(metrics=metrics,
                                        model_id=model_id,
                                        finetuned=False)

            # Garbage collection, to avoid memory issues
            try:
                del model, model_dict
            except UnboundLocalError:
                try:
                    del model
                except UnboundLocalError:
                    pass
            gc.collect()

            return metrics

        else:
            raise RuntimeError(f'The framework "{framework}" is not '
                               f'supported!')

    def __call__(self, *args, **kwargs):
        return self.benchmark(*args, **kwargs)
