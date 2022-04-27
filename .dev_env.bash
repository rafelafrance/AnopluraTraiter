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
python3.10 -m venv .venv
source ./.venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
if [ -f requirements.txt ]; then python -m pip install -r requirements.txt; fi


# ##############################################################################
# Install spacy & a language library for spacy

#pip install -U spacy[cuda111,transformers,lookups]
python -m spacy download en_core_web_sm


# ##############################################################################
# Use the 2nd line if you don't have traiter installed locally

python -m pip install -e ../traiter
# python -m pip install git+https://github.com/rafelafrance/traiter.git@master#egg=traiter


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

python -m pip install -U pynvim
python -m pip install -U 'python-lsp-server[all]'
python -m pip install -U pre-commit pre-commit-hooks
python -m pip install -U autopep8 flake8 isort pylint yapf pydocstyle black
python -m pip install -U jupyter jupyter_nbextensions_configurator
python -m pip install -U jupyterlab
python -m pip install -U jupyterlab_code_formatter
python -m pip install -U jupyterlab-drawio
python -m pip install -U jupyterlab-lsp
python -m pip install -U jupyterlab-spellchecker
python -m pip install -U jupyterlab-git
python -m pip install -U aquirdturtle-collapsible-headings
python -m pip install -U nbdime
python -m pip install -U ipyparallel

jupyter labextension install jupyterlab_onedarkpro
jupyter server extension enable --py jupyterlab_git
jupyter serverextension enable --py jupyterlab_code_formatter


# ##############################################################################
# I Run pre-commit hooks (optional)

pre-commit install
