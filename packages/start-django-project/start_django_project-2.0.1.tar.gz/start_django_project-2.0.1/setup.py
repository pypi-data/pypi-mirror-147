# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['start_django_project',
 'start_django_project.django-template.code.web',
 'start_django_project.django-template.code.web.app',
 'start_django_project.django-template.code.web.app.management.commands',
 'start_django_project.django-template.code.web.app.migrations',
 'start_django_project.django-template.code.web.project']

package_data = \
{'': ['*'],
 'start_django_project': ['django-template/*',
                          'django-template/.vscode/*',
                          'django-template/code/*',
                          'django-template/nginx/*'],
 'start_django_project.django-template.code.web': ['static/images/*',
                                                   'static/style/*'],
 'start_django_project.django-template.code.web.app': ['templates/*',
                                                       'templates/app/*']}

entry_points = \
{'console_scripts': ['start-django-project = start_django_project.cli:cli']}

setup_kwargs = {
    'name': 'start-django-project',
    'version': '2.0.1',
    'description': 'Init a new django project with a simple bootstrap layout',
    'long_description': '# make-django-app\nTo download:\n\n`pip install make-django-project`\n\nTo use:\n\n`start-django-project ./path_of_your_project`\n\nOr to init inside a folder:\n\n`start-django-project ./`',
    'author': 'TechHeart',
    'author_email': 'contact@TechHeart.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
