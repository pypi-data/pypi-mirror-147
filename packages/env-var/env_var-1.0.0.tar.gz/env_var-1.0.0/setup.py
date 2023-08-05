# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['env_var', 'env_var._transformers']

package_data = \
{'': ['*']}

install_requires = \
['isoduration>=20.11.0,<21.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'rfc3339-validator>=0.1.4,<0.2.0',
 'rfc3986-validator>=0.1.1,<0.2.0',
 'validators>=0.18.2,<0.19.0']

setup_kwargs = {
    'name': 'env-var',
    'version': '1.0.0',
    'description': 'simple utility to parse and validate environment variables',
    'long_description': '# env_var\n\nA simple utility for working with environment variables. The main goal was to provide proper type check.\n\n```python\nfrom env_var import env\n\nminio_port = env(\'MINIO_PORT\').as_port_number().default(9000).required() # port type hint is `int`\nminio_host = env(\'MINIO_HOST\').as_hostname().optional() # minio_host type hint is `str | None`\nminio_secure = env(\'MINIO_SECURE\').as_bool().required() # minio_host type hint is `bool`\n```\n\nSetting `default` will result in always returning a value, so it makes little sense to use it with `optional`.\n\n\nIt might be useful to gather all environment variables that are used in an application to a separate file.\n\n```python\nfrom enum import Enum\nfrom env_var import env\n\nclass SomeImportantOption(Enum):\n  option_a = "a"\n  option_b = "b"\n  option_c = "c"\n\nPG_HOST = env(\'PG_HOST\').as_hostname().required()\nPG_PORT = env(\'PG_PORT\').as_port_number().default(5432).required()\nPG_DB = env(\'PG_DB\').as_string().required()\nPG_USER = env(\'PG_USER\').as_string().required()\nPG_PASSWORD = env(\'PG_PASSWORD\').as_string().required()\n\nIMPORTANT_OPTION = env(\'IMPORTANT_OPTION\').as_enum(SomeImportantOption).required()\n```\nSometimes it might happen that some variables will be required only in specific circumstances, in such cases calling `required` can be postponed until the variable is actually needed.\n\n```python\nUPDATE_URL = env(\'UPDATE_URL\').as_url()\n"""required only when some condition is met"""\n\n# elsewhere in the code\ndef send_update(status: str):\n  url = UPDATE_URL.required()\n  requests.post(url, dict(status=status))\n```\n\nIt\'s also possible to pass custom transformers/validators.\n\n```python\n@dataclass\nclass MyOwnClass:\n    initial: str\n\ninitial_class = env("INITIAL").custom_transformer(MyOwnClass).required() # intial_class is of type MyOwnClass\n```\n',
    'author': 'Sebastian Banaszkiewicz',
    'author_email': 'banaszkiewicz.sebastian@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/seba-ban/env-var',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
