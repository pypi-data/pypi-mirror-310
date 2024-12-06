# django-plugin-kolo

[![PyPI](https://img.shields.io/pypi/v/django-plugin-kolo.svg)](https://pypi.org/project/django-plugin-kolo/)
[![Changelog](https://img.shields.io/github/v/release/fbinz/django-plugin-kolo?include_prereleases&label=changelog)](https://github.com/fbinz/django-plugin-kolo/releases)
[![Tests](https://github.com/fbinz/django-plugin-kolo/workflows/Test/badge.svg)](https://github.com/fbinz/django-plugin-kolo/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/fbinz/django-plugin-kolo/blob/main/LICENSE)

Makes integrating kolo even easier.

## Installation

First configure your Django project [to use DJP](https://djp.readthedocs.io/en/latest/installing_plugins.html).

Then install this plugin in the same environment as your Django application.
```bash
pip install django-plugin-kolo
```
## Usage

Have a look at the [official docs](https://docs.kolo.app/).

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd django-plugin-kolo
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
