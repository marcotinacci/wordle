.PHONY: clean clean-temp clean-build clean-pyc clean-test coverage format help lint lint/flake8 lint/black
.DEFAULT_GOAL := help

PROJECT_DIR=wordle
TESTS_DIR=tests
PY = py310

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

init: ## install dependencies
	pip install -r requirements.txt
	pip install -r requirements_dev.txt

format: ## format code with black
	black ${PROJECT_DIR}

lint: lint/flake8 lint/black ## check style

lint/flake8: ## check style with flake8
	flake8 ${PROJECT_DIR} ${TEST_DIR}

lint/black: ## check style with black
	black --check ${PROJECT_DIR} ${TEST_DIR}

test: ## run tests quickly with the default Python
	pytest

test-all: ## run tests on every Python version with tox
	@tox -e $(PY) $(OPTIONS)

coverage: ## check code coverage quickly with the default Python
	coverage run --source ${PROJECT_DIR} -m pytest
	coverage report -m
	coverage xml -o coverage.xml
	coverage html

clean: clean-temp clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-temp: ## remove temporary files
	rm -fr temp/

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -f coverage.xml
	rm -fr htmlcov/
	rm -fr .pytest_cache
