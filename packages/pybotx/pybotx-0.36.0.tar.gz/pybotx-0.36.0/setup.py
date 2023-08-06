# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybotx',
 'pybotx.bot',
 'pybotx.bot.api',
 'pybotx.bot.api.responses',
 'pybotx.bot.middlewares',
 'pybotx.client',
 'pybotx.client.bots_api',
 'pybotx.client.chats_api',
 'pybotx.client.events_api',
 'pybotx.client.exceptions',
 'pybotx.client.files_api',
 'pybotx.client.notifications_api',
 'pybotx.client.smartapps_api',
 'pybotx.client.stickers_api',
 'pybotx.client.users_api',
 'pybotx.models',
 'pybotx.models.message',
 'pybotx.models.system_events']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.7.0,<0.9.0',
 'httpx>=0.18.0,<0.22.0',
 'loguru>=0.6.0,<0.7.0',
 'mypy-extensions>=0.2.0,<0.5.0',
 'pydantic>=1.6.0,<1.9.0',
 'typing-extensions>=3.7.4,<5.0.0']

setup_kwargs = {
    'name': 'pybotx',
    'version': '0.36.0',
    'description': 'A python library for interacting with eXpress BotX API',
    'long_description': '# pybotx\n\n*Библиотека для создания чат-ботов и SmartApps для мессенджера eXpress*\n\n[![PyPI version](https://badge.fury.io/py/botx.svg)](https://badge.fury.io/py/pybotx)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pybotx)\n[![Coverage](https://codecov.io/gh/ExpressApp/pybotx/branch/master/graph/badge.svg)](https://codecov.io/gh/ExpressApp/pybotx/branch/master)\n[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n\n## Особенности\n\n* Простая для использования\n* Поддерживает коллбэки BotX\n* Легко интегрируется с асинхронными веб-фреймворками\n* Полное покрытие тестами\n* Полное покрытие аннотациями типов\n\n\n## Установка\n\nИспользуя `pip`:\n\n```bash\npip install git+https://github.com/ExpressApp/pybotx.git\n```\n\n**Предупреждение:** Данный проект находится в активной разработке (`0.y.z`) и\nего API может быть изменён при повышении минорной версии.\n',
    'author': 'Sidnev Nikolay',
    'author_email': 'nsidnev@ccsteam.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ExpressApp/pybotx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
