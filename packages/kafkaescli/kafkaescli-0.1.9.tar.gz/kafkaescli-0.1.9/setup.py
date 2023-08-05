# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kafkaescli',
 'kafkaescli.core',
 'kafkaescli.core.config',
 'kafkaescli.core.consumer',
 'kafkaescli.core.middleware',
 'kafkaescli.core.producer',
 'kafkaescli.core.shared',
 'kafkaescli.infra',
 'kafkaescli.interface',
 'kafkaescli.interface.web',
 'kafkaescli.lib']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'aiokafka>=0.7.2,<0.8.0',
 'dependency-injector>=4.39.1,<5.0.0',
 'fastapi>=0.75.1,<0.76.0',
 'meiga>=1.3.1,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'pytest-cov>=3.0.0,<4.0.0',
 'typer>=0.4.1,<0.5.0',
 'uvicorn>=0.17.6,<0.18.0']

setup_kwargs = {
    'name': 'kafkaescli',
    'version': '0.1.9',
    'description': 'A magical kafka command line interface.',
    'long_description': '\ufeff\n![Kafkaescli](docs/images/kafkaescli-repository-open-graph-template.png)\n[![Coverage Status](https://coveralls.io/repos/github/jonykalavera/kafkaescli/badge.svg?branch=main)](https://coveralls.io/github/jonykalavera/kafkaescli?branch=main)\n[![CircleCI](https://circleci.com/gh/jonykalavera/kafkaescli/tree/main.svg?style=svg)](https://circleci.com/gh/jonykalavera/kafkaescli/tree/main) [![Join the chat at https://gitter.im/jonykalavera/kafkaescli](https://badges.gitter.im/jonykalavera/kafkaescli.svg)](https://gitter.im/jonykalavera/kafkaescli?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n\n# Install\n\nInstall from [pypi](https://pypi.org/project/kafkaescli/)\n\n```sh\npip install kafkaescli\n```\n\n# Usage\n\n```bash\n# consume from `hello`\nkafkaescli consume hello\n# consume from `hello` showing metadata\nkafkaescli consume hello --metadata\n# produce topic `hello`\nkafkaescli produce hello world\n# produce longer strings\nkafkaescli produce hello "world of kafka"\n# produce from stdin a value per line\ncat values.json | kafkaescli produce hello --stdin\n# produce to topic `world` form the output of a consumer of topic `hello`\nkafkaescli consume hello | kafkaescli produce world --stdin\n# produce `{"foo":"bar"}` to topic `hello`, with middleware\nkafkaescli produce hello \'{"foo":"bar"}\' --middleware \'{"hook_before_produce": "examples.json.hook_before_produce"}\'\n# consume from topic `hello` with middleware\nkafkaescli consume hello --middleware \'{"hook_after_consume": "examples.json.hook_after_consume"}\'\n# run the web api http://localhost:8000/docs\nkafkaescli runserver\n# POST consumed values to WEBHOOK\nkafkaescli consume hello --metadata --webhook https://myendpoint.example.com\n# For more details see\nkafkaescli --help\n```\nThese examples assume a Kafka instance is running at `localhost:9092`\n\n# Contributions\n\n* [Jony Kalavera](https://github.com/jonykalavera)\n\nPull-requests are welcome and will be processed on a best-effort basis.\nFollow the [contributing guide](CONTRIBUTING.md).\n',
    'author': 'Jony Kalavera',
    'author_email': 'mr.jony@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jonykalavera/kafkaescli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
