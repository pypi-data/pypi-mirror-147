# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djunk',
 'djunk.apps',
 'djunk.apps.core',
 'djunk.apps.core.management',
 'djunk.apps.core.management.commands',
 'djunk.apps.core.tests',
 'djunk.apps.templating',
 'djunk.apps.templating.templatetags',
 'djunk.apps.templating.tests',
 'djunk.settings']

package_data = \
{'': ['*'],
 'djunk.apps.core.management.commands': ['app_template/__init__.py-tpl',
                                         'app_template/__init__.py-tpl',
                                         'app_template/__init__.py-tpl',
                                         'app_template/__init__.py-tpl',
                                         'app_template/__init__.py-tpl',
                                         'app_template/admin.py-tpl',
                                         'app_template/admin.py-tpl',
                                         'app_template/admin.py-tpl',
                                         'app_template/admin.py-tpl',
                                         'app_template/admin.py-tpl',
                                         'app_template/apps.py-tpl',
                                         'app_template/apps.py-tpl',
                                         'app_template/apps.py-tpl',
                                         'app_template/apps.py-tpl',
                                         'app_template/apps.py-tpl',
                                         'app_template/factories.py-tpl',
                                         'app_template/factories.py-tpl',
                                         'app_template/factories.py-tpl',
                                         'app_template/factories.py-tpl',
                                         'app_template/factories.py-tpl',
                                         'app_template/migrations/*',
                                         'app_template/models.py-tpl',
                                         'app_template/models.py-tpl',
                                         'app_template/models.py-tpl',
                                         'app_template/models.py-tpl',
                                         'app_template/models.py-tpl',
                                         'app_template/tests/*'],
 'djunk.apps.templating': ['templates/templating/*']}

install_requires = \
['Django>=4.0.4,<5.0.0']

setup_kwargs = {
    'name': 'djunk',
    'version': '0.2.0',
    'description': "My personal 'junk drawer' of reusable Django apps and related snippets.",
    'long_description': None,
    'author': 'Jordan Eremieff',
    'author_email': 'jordan@eremieff.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
