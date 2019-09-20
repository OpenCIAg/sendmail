#!/usr/bin/env python
import os
import json
from distutils.core import setup

__version__ = (0, 0, 0)


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        return f.read()


pipenv_lock = json.loads(read('Pipfile.lock'))


def is_link(entry):
    name, meta = entry
    return meta.get('git', False)


def n(func):
    def wrapper(*args, **kwargs):
        return not func(*args, **kwargs)

    return wrapper


def dependency_entry_to_requirement(name, meta):
    if 'version' in meta:
        return '{}{}'.format(name, meta.get('version', '==*'))
    return name


def dependency_entry_to_link(name, meta):
    if 'git' in meta:
        return 'git+{}#egg={}'.format(meta.get('git'), name)


def load_requirements():
    for name, meta in pipenv_lock.get("default", {}).items():
        yield dependency_entry_to_requirement(name, meta)


def load_dev_requirements():
    for name, meta in pipenv_lock.get("develop", {}).items():
        yield dependency_entry_to_requirement(name, meta)


def load_dependency_links():
    for name, meta in filter(is_link, pipenv_lock.get("default", {}).items()):
        yield dependency_entry_to_link(name, meta)


str_version = '.'.join(map(str, __version__))


setup(
    name='py-sendmail',
    version=str_version,
    description='A cli to send smtp e-mail',
    author='CIAg',
    author_email='desenv@ciag.org.br',
    entry_points={
        'console_scripts': [
            'sendmail=sendmail:main',
        ]
    },
    packages=[
        'sendmail',
    ],
    install_requires=list(load_requirements()),
    tests_require=list(load_dev_requirements()),
    dependency_links=list(load_dependency_links()),
)
