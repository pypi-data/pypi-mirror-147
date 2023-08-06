# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['raspcuterie',
 'raspcuterie.cli',
 'raspcuterie.cli.tests',
 'raspcuterie.config',
 'raspcuterie.config.schema',
 'raspcuterie.config.schema.tests',
 'raspcuterie.config.tests',
 'raspcuterie.dashboard',
 'raspcuterie.dashboard.apexcharts',
 'raspcuterie.dashboard.tests',
 'raspcuterie.db',
 'raspcuterie.devices',
 'raspcuterie.devices.input',
 'raspcuterie.devices.output',
 'raspcuterie.devices.output.tests',
 'raspcuterie.devices.tests']

package_data = \
{'': ['*'], 'raspcuterie.dashboard': ['templates/*']}

install_requires = \
['Flask[async]>=2.1.1,<3.0.0',
 'PyYAML>=6.0,<7.0',
 'Pygments>=2.11.2,<3.0.0',
 'RPi.bme280>=0.2.4,<0.3.0',
 'click>=8.1.2,<9.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'timeout-decorator>=0.5.0,<0.6.0']

extras_require = \
{':sys_platform == "armv6l"': ['RPi.GPIO>=0.7.1,<0.8.0']}

entry_points = \
{'console_scripts': ['raspcuterie = raspcuterie.cli:cli']}

setup_kwargs = {
    'name': 'raspcuterie',
    'version': '1.0.0a0',
    'description': 'Charcuterie dashboard and controller for the Raspberry PI',
    'long_description': None,
    'author': 'jelmert',
    'author_email': 'info@jelmert.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
