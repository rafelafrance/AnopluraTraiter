#!/usr/bin/env bash

# #################################################################################
# Setup the virtual environment for development.
# You may need to "pip install --user virtualenv" globally.
# This is not required but some form of project isolation (conda virtual env etc.)
# is strongly encouraged.

if [[ ! -z "$VIRTUAL_ENV" ]]; then
  echo "'deactivate' before running this script."
  exit 1
fi

rm -rf .venv
virtualenv -p python3.9 .venv
source ./.venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi


# ##############################################################################
# Install spacy & a language library for spacy

pip install -U spacy[cuda111,transformers,lookups]
python -m spacy download en_core_web_sm


# ##############################################################################
# Use the 2nd line if you don't have traiter installed locally

# pip install -e ../traiter
pip install git+https://github.com/rafelafrance/traiter.git@master#egg=traiter


# ##############################################################################
# We need these linux utilities.

# For extracting text from PDFs or converting PDFs to images
sudo apt install poppler-utils

# For extracting text from images
sudo apt install tesseract-ocr


# ##############################################################################
# Some useful directories

mkdir -p data/images
mkdir -p data/output
mkdir -p data/pdfs
mkdir -p data/text


# ##############################################################################
# Dev only installs (optional because they're personal preference)

pip install -U pynvim
pip install -U 'python-lsp-server[all]'
pip install -U pre-commit pre-commit-hooks
pip install -U autopep8 flake8 isort pylint yapf pydocstyle black
pip install -U jupyter jupyter_nbextensions_configurator
pip install -U jupyterlab
pip install -U jupyterlab_code_formatter
pip install -U jupyterlab-drawio
pip install -U jupyterlab-lsp
pip install -U jupyterlab-spellchecker
pip install -U jupyterlab-git
pip install -U aquirdturtle-collapsible-headings
pip install -U nbdime
pip install -U ipyparallel

jupyter labextension install jupyterlab_onedarkpro
jupyter server extension enable --py jupyterlab_git
jupyter serverextension enable --py jupyterlab_code_formatter


# ##############################################################################
# I Run pre-commit hooks (optional)

pre-commit install
