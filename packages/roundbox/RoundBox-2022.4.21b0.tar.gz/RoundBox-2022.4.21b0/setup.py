# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['RoundBox',
 'RoundBox.apps',
 'RoundBox.conf',
 'RoundBox.core',
 'RoundBox.core.cache',
 'RoundBox.core.cache.backends',
 'RoundBox.core.checks',
 'RoundBox.core.cliparser',
 'RoundBox.core.cliparser.commands',
 'RoundBox.core.files',
 'RoundBox.core.hass',
 'RoundBox.core.hass.components',
 'RoundBox.core.hass.components.sensor',
 'RoundBox.core.hass.helpers',
 'RoundBox.core.mail',
 'RoundBox.core.mail.backends',
 'RoundBox.dispatch',
 'RoundBox.utils',
 'RoundBox.utils.backports',
 'RoundBox.utils.backports.strenum',
 'RoundBox.utils.log']

package_data = \
{'': ['*'],
 'RoundBox.conf': ['jobs_template/jobs/*',
                   'jobs_template/jobs/daily/*',
                   'jobs_template/jobs/hourly/*',
                   'jobs_template/jobs/minutely/*',
                   'jobs_template/jobs/monthly/*',
                   'jobs_template/jobs/quarter_hourly/*',
                   'jobs_template/jobs/weekly/*',
                   'jobs_template/jobs/yearly/*']}

install_requires = \
['mkdocs-material>=8.2.9']

setup_kwargs = {
    'name': 'roundbox',
    'version': '2022.4.21b0',
    'description': 'A small lightweight framework for IoT applications',
    'long_description': '# ⚡ RoundBox\n\n![PyPI](https://img.shields.io/pypi/v/roundbox?label=RoundBox&style=plastic)\n![GitHub release (latest by date)](https://img.shields.io/github/v/release/soulraven/roundbox?style=plastic)\n[![Build status](https://img.shields.io/github/workflow/status/soulraven/roundbox/merge-to-main?style=plastic)](https://img.shields.io/github/workflow/status/soulraven/roundbox/merge-to-main)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/roundbox?style=plastic)](https://pypi.org/project/roundbox/)\n[![License](https://img.shields.io/github/license/soulraven/roundbox?style=plastic)](https://img.shields.io/github/license/soulraven/roundbox)\n\nA small lightweight framework for IoT applications\n\n### 🎈 Special thanks\nTo build this framework I have used code inspired by the [Django](https://github.com/django/django) project and also\nfrom [Home Assistant](https://github.com/home-assistant/core) project.\n\nBoth projects have a strong code base and lightweight and port on different projects.\n\n### 🖇 Library used\n\n### 📚 Documentation\n\n### 🔧 Installation\n\n### ➿ Variables\n\n- set the ROUNDBOX_COLORS environment variable to specify the palette you want to use. For example,\nto specify the light palette under a Unix or OS/X BASH shell, you would run the following at a command prompt:\n```bash\nexport ROUNDBOX_COLORS="light"\n```\n\n### 🌍 Contributions\n\nContributions of all forms are welcome :)\n\n## 📝 License\n\nThis repository is licensed under the GNU General Public License, version 3 (GPLv3).\n\n## 👀 Author\n\nZaharia Constantin\n\n[View my GitHub profile 💡](https://github.com/soulraven)\n',
    'author': 'Zaharia Constantin',
    'author_email': 'layout.webdesign@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/soulraven/roundbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
