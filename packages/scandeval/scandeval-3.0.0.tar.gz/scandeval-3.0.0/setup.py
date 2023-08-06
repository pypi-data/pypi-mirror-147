from setuptools import setup, find_packages
from pathlib import Path
from bump_version import get_current_version

PYTORCH_REQUIRES = ['torch>=1.9.0']
JAX_REQUIRES = PYTORCH_REQUIRES + ['jaxlib>=0.1.75', 'jax>=0.2.26', 'flax>=0.3.6']
SPACY_REQUIRES = ['spacy>=3.2.0', 'spacy-transformers>=1.1.0']
ALL_REQUIRES = (PYTORCH_REQUIRES +
                JAX_REQUIRES +
                SPACY_REQUIRES)

setup(name='scandeval',
      version=get_current_version(return_tuple=False),
      description='',
      long_description=Path('README.md').read_text(),
      long_description_content_type='text/markdown',
      url='https://github.com/saattrupdan/scandeval',
      author='Dan Saattrup Nielsen',
      author_email='saattrupdan@gmail.com',
      license='MIT',
      classifiers=['License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8'],
      packages=find_packages(exclude=('tests',)),
      include_package_data=True,
      install_requires=['numpy>=1.19.5',
                        'transformers>=4.17.0',
                        'datasets>=2.0.0',
                        'requests>=2.26.0',
                        'tqdm>=4.62.3',
                        'sentencepiece>=0.1.96',
                        'seqeval>=1.2.2',
                        'bs4>=0.0.1',
                        'termcolor>=1.1.0'],
      extras_require=dict(pytorch=PYTORCH_REQUIRES,
                          spacy=SPACY_REQUIRES,
                          jax=JAX_REQUIRES,
                          all=ALL_REQUIRES),
      entry_points=dict(console_scripts=['scandeval=scandeval.cli:benchmark']))
