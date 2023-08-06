# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logging518']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.11"': ['tomli>=2.0.1,<3.0.0']}

setup_kwargs = {
    'name': 'logging518',
    'version': '1.0.0',
    'description': "Configure Python's native logging module using pyproject.toml",
    'long_description': '# \U0001fab5 logging518\n\n[![PyPI version](https://badge.fury.io/py/logging518.svg)](https://badge.fury.io/py/logging518) ![PyPI - Downloads](https://img.shields.io/pypi/dm/logging518) [![Test Matrix](https://github.com/mharrisb1/logging518/actions/workflows/test_matrix.yml/badge.svg)](https://github.com/mharrisb1/logging518/actions/workflows/test_matrix.yml)\n\nUse your pyproject.toml (or any other TOML file) to configure Python\'s native logging module\n\n## Usage\n\nYou can use `logging518.config.fileConfig` the same way you would use `logging.config.fileConfig` but instead of passing a ConfigParser-form file, you can pass in a TOML-form file.\n\n```python\nimport logging\nimport logging518.config  # instead of logging.config\n\nlogging518.config.fileConfig("pyproject.toml")\nlogger = logging.get_logger("project")\n\nlogger.info("Hello, log!")\n```\n\n## Configure\n\n`logging518.config.fileConfig` simply deserializes the TOML file you pass in (using `tomli`/`tomlib`) and passes the contents to `logging.config.dictConfig`.\n\n`logging518.config.fileConfig` uses the [tool table](https://peps.python.org/pep-0518/#tool-table) in your TOML file to look up the configuration. All logging config should be defined under `tool.logging` in the tool table.\n\n```toml\n[tool.logging]\nversion = 1\ndisable_existing_loggers = true\n\n[tool.logging.loggers.project]\nlevel = "WARNING"\n\n[tool.logging.loggers.project.foo_module]\nlevel = "DEBUG"\n```\n\nThis config would be the same as:\n\n```python\nimport logging.config\n\nLOGGING_CONFIG = {\n    "version": 1,\n    "disable_existing_loggers": True,\n    "loggers": {\n        "project": {\n            "level": "WARNING"\n        },\n        "project.foo_module": {\n            "level": "DEBUG"\n        }\n    }\n}\n\nlogging.config.dictConfig(LOGGING_CONFIG)\n```\n\nMore examples can be found in the 👩\u200d🍳 [Cookbook](https://mharrisb1.github.io/logging518/)\n',
    'author': 'Michael Harris',
    'author_email': 'michael.harrisru@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mharrisb1/logging518',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
