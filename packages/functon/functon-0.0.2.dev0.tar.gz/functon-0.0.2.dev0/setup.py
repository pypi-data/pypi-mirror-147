# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['functon']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'functon',
    'version': '0.0.2.dev0',
    'description': 'True functional programming in Python',
    'long_description': '[![Actions Status](https://github.com/zhivykh/functon/workflows/CI/badge.svg)](https://github.com/zhivykh/functon/actions/)\n[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)\n[![Stable Version](https://img.shields.io/pypi/v/functon?color=blue)](https://pypi.org/project/functon/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n\n# Functon λ [EXPERIMENTAL]\n\n## Installation\n\n```\npython3 -m pip install functon\n```\n\n## Usage\nHello world:\n\n```python\n>>> from functon import fn\n>>> fn(print, "Hello world!")\n\'Hello world!\'\n```\n\n\nTriple the value of a number:\n\n```python\n>>> from functon import defun, fn\n>>> def triple(x: int) -> defun(("*", 3, "x")):\n...     """Compute three times X."""\n>>> fn(triple, 3)\n9\n```\n\nCompute factorials using recursion:\n\n```python\n>>> from functon import defun, fn, IF\n>>> def factorial(N: int) -> defun((IF, ("=", "N", 1), 1, ("*", "N", ("factorial", ("-", "N", 1))))):\n...     """Compute the factorial of N."""\n>>> fn(factorial, 5) \n120\n```',
    'author': 'zhivykh',
    'author_email': 'zivih.n@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zhivykh/functon',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
