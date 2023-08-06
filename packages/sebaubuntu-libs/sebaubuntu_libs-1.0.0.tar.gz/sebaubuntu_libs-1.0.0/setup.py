# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sebaubuntu_libs',
 'sebaubuntu_libs.libaik',
 'sebaubuntu_libs.libandroid',
 'sebaubuntu_libs.libexception',
 'sebaubuntu_libs.libgofile',
 'sebaubuntu_libs.libgofile.raw_api',
 'sebaubuntu_libs.liblineage',
 'sebaubuntu_libs.liblocale',
 'sebaubuntu_libs.liblogging',
 'sebaubuntu_libs.libnekobin',
 'sebaubuntu_libs.libprop',
 'sebaubuntu_libs.libtyping',
 'sebaubuntu_libs.libvintf']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sebaubuntu-libs',
    'version': '1.0.0',
    'description': "SebaUbuntu's shared libs",
    'long_description': '# sebaubuntu_libs\n\nA collection of code shared between my projects\n',
    'author': 'Sebastiano Barezzi',
    'author_email': 'barezzisebastiano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SebaUbuntu/sebaubuntu_libs',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
