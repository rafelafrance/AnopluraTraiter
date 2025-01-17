.PHONY: test install dev venv
.ONESHELL:

test:
	. .venv/bin/activate
	python3.11 -m unittest discover

install:
	test -d .venv || python3.11 -m venv .venv
	. .venv/bin/activate
	python3.11 -m pip install -U pip setuptools wheel
	python3.11 -m pip install git+https://github.com/rafelafrance/traiter.git@master#egg=traiter
	python3.11 -m pip install .
	python3.11 -m spacy download en_core_web_md

dev:
	test -d .venv || python3.11 -m venv .venv
	. .venv/bin/activate
	python3.11 -m pip install -U pip setuptools wheel
	python3.11 -m pip install -e ../../traiter/traiter
	python3.11 -m pip install -e .[dev]
	python3.11 -m spacy download en_core_web_md
	pre-commit install

clean:
	rm -rf .venv
	find -iname "*.pyc" -delete
