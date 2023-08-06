# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['envcast', 'envcast.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'envcast',
    'version': '1.2.0',
    'description': 'This module helps to cast environment variables to desired types. It may be very useful for 12factor app usage.',
    'long_description': '# envcast\n![Build and publish](https://github.com/xfenix/envcast/workflows/Build%20and%20publish/badge.svg)\n[![PyPI version](https://badge.fury.io/py/envcast.svg)](https://badge.fury.io/py/envcast)\n[![codecov](https://codecov.io/gh/xfenix/envcast/branch/master/graph/badge.svg)](https://codecov.io/gh/xfenix/envcast)\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n[![Imports: isort](https://img.shields.io/badge/imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)\n\nPackage for environment variables parsing with type casting. Why do you need it? Because you can\'t just grab environment variables as is, you need to cast them to desired types for your application (for example like bool variable: how to cast strings `False`, `""`, `0` to bool without boilerplaite?).  \nThis packages just cast needed environment variables to desired types with syntax very familiar to `os.getenv` users.  \nPlus this package has good test coverage and quality codebase.  \nWritten in modern python 3.7+ with full support of:\n\n- https://www.python.org/dev/peps/pep-0526/\n- https://www.python.org/dev/peps/pep-0484/\n- https://www.python.org/dev/peps/pep-0008/\n- https://www.python.org/dev/peps/pep-0257/\n- https://www.python.org/dev/peps/pep-0518/\n- https://www.python.org/dev/peps/pep-0585/\n\n# TL;DR\nIt behaves very similar to `os.getenv`:\n```python\nimport envcast\n\n\n# result will be casted to str\nenvcast.env(\'SOME_ENV_VAR\', \'defaultvalue\', type_cast=str)\n\n# result will be casted to bool (if it like 1 or on or true/True -> if will be python True)\n# BUT, if there is no value, default value is None will be casted to bool, so it will be False\nenvcast.env(\'SOME_BOOL_ENV_VAR\', type_cast=bool)\n```\n\n# Usage, API, more details and examples\nSignature of env and dotenv absolutely similar and looks like this:\n```python\n# var_name is desired variable name\n# default_value going through type casting, so it must be in desired type\n# type_cast — desired variable type casting function\n# list_type_cast applies if type_cast is list, tuple\nenvcast.env(var_name: str, default_value: typing.Any = None,\n            type_cast: type = str, list_type_cast: type = str)\n```\n\n### From environment variables\nFor casting good old plain env variables you will need do following:\n```python\nimport envcast\n\n\nthis_will_be_bool: bool = envcast.env(\'SOME_ENV_VARIABLE\', \'false\', type_cast=bool))\nor_this_is_string_by_default: str = envcast.env(\'OTHER_ENV_VAR\')\nthis_is_int: int = envcast.env(\'MORE_ENV\', type_cast=int)\n```\n\n### From .env file\nIf your are using .env file, you can do it too:\n```python\nimport envcast\n\n\nenvcast.set_dotenv_path(\'.\')\n# Can be any of the following :\n# envcast.set_dotenv_path(\'~/some/.env\')\n# envcast.set_dotenv_path(\'/tmp/.env\')\n# envcast.set_dotenv_path(\'/tmp/\')\nthis_will_be_bool: bool = envcast.dotenv(\'SOME_ENV_VARIABLE\', \'false\', type_cast=bool))\nor_this_is_string_by_default: str = envcast.dotenv(\'OTHER_ENV_VAR\')\nthis_is_int: int = envcast.dotenv(\'MORE_ENV\', type_cast=int)\n```\nDont worry, file will be readed and parsed only once.\n\n### Exceptions\n- envcast.exceptions.IncorrectDotenvPath\n- envcast.exceptions.NotSettedDotenvPath\n- envcast.exceptions.BrokenDotenvStructure\n\n### Supported casting types\nYou can pass to `type_cast` or `list_type_cast` any desired type casting callables.\nIt may be any builtin type, of Decimal, Path, or any other callable.\n\n### Listing values\nIf you want to parse and cast environment variable with list of values:\n```\nMY_FANCY_VAR=True, On, Ok, False, Disabled, 0\n```\nYou will need expression like this:\n```python\nenvcast.env(\'MY_FANCY_VAR\', type_cast=bool, list_type_cast=list)\n```\nIf you cares about what exactly can be separator for list values: it can be `,`, ` ` (space) or `|`.\n\n# Changelog\nYou can check https://github.com/xfenix/envcast/releases/ release page.\n',
    'author': 'Denis Anikin',
    'author_email': 'ad@xfenix.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xfenix/envcast/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
