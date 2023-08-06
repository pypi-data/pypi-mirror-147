'''
'''

from os import (
    environ as env
)
from pathlib import Path
import setuptools
import yaml


with open('./env.yml', 'r', encoding='utf-8') as vars_file:
    conf = yaml.safe_load(vars_file)

NAMESPACE = conf['NAMESPACE']
GIT_URL = env.get('CI_PROJECT_URL', 'http://localhost')

kwargs = {
    'name': f'{NAMESPACE.replace(".", "-")}',
    'version': f'{conf["VERSION"]}{env.get("BUILD_SUFIX", ".")}{env.get("CI_PIPELINE_IID", "0")}',
    'author': conf['AUTHOR'],
    'author_email': conf['EMAIL'],
    'description': conf['DESCR'],
    'url': conf['NOTION'],
    'keywords': conf['KEYWORDS'],
    'project_urls': {
        'Source Code': GIT_URL,
        'Bug Tracker': f'{GIT_URL}/-/issues',
    },
    'package_dir': {"": "src"},
    'packages': conf['MODULES'],
    'namespace_modules': conf['NAMESPACE'],
    'python_requires': conf['PYTHON_REQ'],
    'classifiers': conf['CLASSIFIERS'],
    'install_requires': []
}

if Path('README.md').is_file():

    with open('README.md', 'r', encoding='utf-8') as md:
        long_description = md.read()

    if len(long_description) > 0:
        kwargs['long_description_content_type'] = 'text/markdown'
        kwargs['long_description'] = long_description

setuptools.setup(**kwargs)
