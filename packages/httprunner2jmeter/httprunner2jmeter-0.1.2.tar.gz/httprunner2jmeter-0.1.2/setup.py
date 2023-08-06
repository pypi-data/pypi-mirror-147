# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['httprunner2jmeter',
 'httprunner2jmeter.builtin',
 'httprunner2jmeter.ext',
 'httprunner2jmeter.ext.har2case',
 'httprunner2jmeter.ext.locust',
 'httprunner2jmeter.ext.uploader']

package_data = \
{'': ['*']}

install_requires = \
['jmespath>=0.9.5,<0.10.0', 'pyjmeter>=0.5,<0.6', 'pyyaml>=5.1.2,<6.0.0']

entry_points = \
{'console_scripts': ['hr2jmeter = httprunner2jmeter.cli:main']}

setup_kwargs = {
    'name': 'httprunner2jmeter',
    'version': '0.1.2',
    'description': 'Make httprunner scripts to jmeter scripts.',
    'long_description': '\n# HttpRunner2Jmeter\n\nMake httprunner scripts to jmeter scripts\n\n# How run\n\n`hr2jmeter /path/to/yaml/file`',
    'author': '贝克街的捉虫师',
    'author_email': 'forpeng@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BSTester/httprunner2jmeter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
