# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drf_rockstar_extensions',
 'drf_rockstar_extensions.fields',
 'drf_rockstar_extensions.fields.fetcher_field']

package_data = \
{'': ['*']}

install_requires = \
['djangorestframework>=3.13.0,<4.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'drf-rockstar-extensions',
    'version': '0.0.4',
    'description': 'Extensions that help your project become rockstar',
    'long_description': 'DRF Rockstar Extensions\n===============================\n[![Test](https://github.com/agung96tm/drf_rockstar_extensions/workflows/Test/badge.svg)](https://github.com/agung96tm/drf_rockstar_extensions/actions)\n[![Docs](https://readthedocs.org/projects/django-rest-framework-simplejwt/badge/?version=latest)](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)\n\n\nExtensions that help your project become rockstar\n\n\nDRF Rockstar Extensions is available on PyPI:\n\n```console\n$ python -m pip install drf-rockstar-extensions\n```\n\n### Docs\n<a href="https://drf-rockstar-extensions.readthedocs.io/en/latest/" target="_blank">https://drf-rockstar-extensions.readthedocs.io</a>\n\n\n### Contributors\n<table>\n  <tr>\n    <td align="center">\n      <a href="https://agung96tm.com/">\n        <img src="https://avatars.githubusercontent.com/u/1901484?v=4" width="100px;" alt=""/><br />\n        <b>Agung Yuliyanto</b><br>\n      </a>\n      <div>💻</div>\n    </td>\n  </tr>\n</table>',
    'author': 'Agung Yuliyanto',
    'author_email': 'agung.96tm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://drf-rockstar-extensions.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
