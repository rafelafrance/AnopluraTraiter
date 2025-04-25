.PHONY: test install dev venv
.ONESHELL:

test:
	. .venv/bin/activate
	python3.12 -m unittest discover

install:
	test -d .venv || python3.12 -m venv .venv
	. .venv/bin/activate
	python3.12 -m pip install -U pip setuptools wheel
	python3.12 -m pip install git+https://github.com/rafelafrance/traiter.git@master#egg=traiter
	python3.12 -m pip install .
	python3.12 -m spacy download en_core_web_md

dev:
	test -d .venv || python3.12 -m venv .venv
	. .venv/bin/activate
	python3.12 -m pip install -U pip setuptools wheel
	python3.12 -m pip install -e ../../traiter/traiter
	python3.12 -m pip install -e .[dev]
	python3.12 -m spacy download en_core_web_md
	pre-commit install
	cd ./anoplura  # This is so stupid
	ln -s ../traiter/traiter traiter  # the stupid payload

clean:
	rm -rf .venv
	find -iname "*.pyc" -delete
