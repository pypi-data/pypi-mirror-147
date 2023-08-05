# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiotdlib',
 'aiotdlib.api',
 'aiotdlib.api.errors',
 'aiotdlib.api.functions',
 'aiotdlib.api.types',
 'aiotdlib_generator',
 'aiotdlib_generator.parser']

package_data = \
{'': ['*'], 'aiotdlib': ['tdlib/*'], 'aiotdlib_generator': ['templates/*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0',
 'sortedcontainers>=2.4.0,<3.0.0',
 'ujson>=5.2.0,<6.0.0']

entry_points = \
{'console_scripts': ['aiotdlib_generator = aiotdlib_generator.__main__:main']}

setup_kwargs = {
    'name': 'aiotdlib',
    'version': '0.18.0',
    'description': 'Python asyncio Telegram client based on TDLib',
    'long_description': '# aiotdlib - Python asyncio Telegram client based on [TDLib](https://github.com/tdlib/td)\n\n[![PyPI version shields.io](https://img.shields.io/pypi/v/aiotdlib.svg)](https://pypi.python.org/pypi/aiotdlib/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/aiotdlib.svg)](https://pypi.python.org/pypi/aiotdlib/)\n[![PyPI license](https://img.shields.io/pypi/l/aiotdlib.svg)](https://pypi.python.org/pypi/aiotdlib/)\n\n> This wrapper is actual for **[TDLib v1.8.3 (f295ef3)](https://github.com/pylakey/td/commit/f295ef3a0d3545970bfd658c3443496be3d28397)**\n>\n> This package includes prebuilt TDLib binaries for macOS (arm64) and Debian Bullseye (amd64).\n> You can use your own binary by passing `library_path` argument to `Client` class constructor. Make sure it\'s built from [this commit](https://github.com/tdlib/td/commit/f295ef3a0d3545970bfd658c3443496be3d28397). Compatibility with other versions of library is not guaranteed.\n\n## Features\n\n* All types and functions are generated automatically\n  from [tl schema](https://github.com/tdlib/td/blob/f295ef3a0d3545970bfd658c3443496be3d28397/td/generate/scheme/td_api.tl)\n* All types and functions come with validation and good IDE type hinting (thanks\n  to [Pydantic](https://github.com/samuelcolvin/pydantic))\n* A set of high-level API methods which makes work with tdlib much simpler\n\n## Requirements\n\n* Python 3.9+\n* Get your **api_id** and **api_hash**. Read more\n  in [Telegram docs](https://core.telegram.org/api/obtaining_api_id#obtaining-api-id)\n\n## Installation\n\n### PyPI\n\n```shell\npip install aiotdlib\n```\n\nor if you use [Poetry](https://python-poetry.org)\n\n```shell\npoetry add aiotdlib\n```\n\n### Docker\n\nYou can use [this Docker image](https://hub.docker.com/r/pylakey/aiotdlib) as a base for your own image.\n\nAny parameter of Client class could be set via environment variables.\n\n#### Example\n\nmain.py\n\n```python\nfrom aiotdlib import Client\n\nclient = Client()\nclient.run()\n```\n\nand run it like this:\n\n```shell\nexport AIOTDLIB_API_ID=123456\nexport AIOTDLIB_API_HASH=<my_api_hash>\nexport AIOTDLIB_BOT_TOKEN=<my_bot_token>\npython main.py\n```\n\n## Examples\n\n### Base example\n\n```python\nimport asyncio\nimport logging\n\nfrom aiotdlib import Client\n\nAPI_ID = 123456\nAPI_HASH = ""\nPHONE_NUMBER = ""\n\n\nasync def main():\n    client = Client(\n        api_id=API_ID,\n        api_hash=API_HASH,\n        phone_number=PHONE_NUMBER\n    )\n\n    async with client:\n        me = await client.api.get_me()\n        logging.info(f"Successfully logged in as {me.json()}")\n\n\nif __name__ == \'__main__\':\n    logging.basicConfig(level=logging.INFO)\n    asyncio.run(main())\n```\n\n### Events handlers\n\n```python\nimport asyncio\nimport logging\n\nfrom aiotdlib import Client\nfrom aiotdlib.api import API, BaseObject, UpdateNewMessage\n\nAPI_ID = 123456\nAPI_HASH = ""\nPHONE_NUMBER = ""\n\n\nasync def on_update_new_message(client: Client, update: UpdateNewMessage):\n    chat_id = update.message.chat_id\n\n    # api field of client instance contains all TDLib functions, for example get_chat\n    chat = await client.api.get_chat(chat_id)\n    logging.info(f\'Message received in chat {chat.title}\')\n\n\nasync def any_event_handler(client: Client, update: BaseObject):\n    logging.info(f\'Event of type {update.ID} received\')\n\n\nasync def main():\n    client = Client(\n        api_id=API_ID,\n        api_hash=API_HASH,\n        phone_number=PHONE_NUMBER\n    )\n\n    # Registering event handler for \'updateNewMessage\' event\n    # You can register many handlers for certain event type\n    client.add_event_handler(on_update_new_message, update_type=API.Types.UPDATE_NEW_MESSAGE)\n\n    # You can register handler for special event type "*". \n    # It will be called for each received event\n    client.add_event_handler(any_event_handler, update_type=API.Types.ANY)\n\n    async with client:\n        # idle() will run client until it\'s stopped\n        await client.idle()\n\n\nif __name__ == \'__main__\':\n    logging.basicConfig(level=logging.INFO)\n    asyncio.run(main())\n```\n\n### Bot command handler\n\n```python\nimport logging\n\nfrom aiotdlib import Client\nfrom aiotdlib.api import UpdateNewMessage\n\nAPI_ID = 123456\nAPI_HASH = ""\nBOT_TOKEN = ""\n\nbot = Client(api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)\n\n\n# Note: bot_command_handler method is universal and can be used directly or as decorator\n# Registering handler for \'/help\' command\n@bot.bot_command_handler(command=\'help\')\nasync def on_help_command(client: Client, update: UpdateNewMessage):\n    # Each command handler registered with this method will update update.EXTRA field\n    # with command related data: {\'bot_command\': \'help\', \'bot_command_args\': []}\n    await client.send_text(update.message.chat_id, "I will help you!")\n\n\nasync def on_start_command(client: Client, update: UpdateNewMessage):\n    # So this will print "{\'bot_command\': \'help\', \'bot_command_args\': []}"\n    print(update.EXTRA)\n    await client.send_text(update.message.chat_id, "Have a good day! :)")\n\n\nasync def on_custom_command(client: Client, update: UpdateNewMessage):\n    # So when you send a message "/custom 1 2 3 test" \n    # So this will print "{\'bot_command\': \'custom\', \'bot_command_args\': [\'1\', \'2\', \'3\', \'test\']}"\n    print(update.EXTRA)\n\n\nif __name__ == \'__main__\':\n    logging.basicConfig(level=logging.INFO)\n    # Registering handler for \'/start\' command\n    bot.bot_command_handler(on_start_command, command=\'start\')\n    bot.bot_command_handler(on_custom_command, command=\'custom\')\n    bot.run()\n```\n\n### Proxy\n\n```python\n\nimport asyncio\nimport logging\n\nfrom aiotdlib import Client, ClientProxySettings, ClientProxyType\n\nAPI_ID = 123456\nAPI_HASH = ""\nPHONE_NUMBER = ""\n\n\nasync def main():\n    client = Client(\n        api_id=API_ID,\n        api_hash=API_HASH,\n        phone_number=PHONE_NUMBER,\n        proxy_settings=ClientProxySettings(\n            host="10.0.0.1",\n            port=3333,\n            type=ClientProxyType.SOCKS5,\n            username="aiotdlib",\n            password="somepassword",\n        )\n    )\n\n    async with client:\n        await client.idle()\n\n\nif __name__ == \'__main__\':\n    logging.basicConfig(level=logging.INFO)\n    asyncio.run(main())\n```\n\n### Middlewares\n\n```python\n\nimport asyncio\nimport logging\n\nfrom aiotdlib import Client, HandlerCallable\nfrom aiotdlib.api import API, BaseObject, UpdateNewMessage\n\nAPI_ID = 12345\nAPI_HASH = ""\nPHONE_NUMBER = ""\n\n\nasync def some_pre_updates_work(event: BaseObject):\n    logging.info(f"Before call all update handlers for event {event.ID}")\n\n\nasync def some_post_updates_work(event: BaseObject):\n    logging.info(f"After call all update handlers for event {event.ID}")\n\n\n# Note that call_next argument would always be passed as keyword argument,\n# so it should be called "call_next" only.\nasync def my_middleware(client: Client, event: BaseObject, *, call_next: HandlerCallable):\n    # Middlewares useful for opening database connections for example\n    await some_pre_updates_work(event)\n\n    try:\n        await call_next(client, event)\n    finally:\n        await some_post_updates_work(event)\n\n\nasync def on_update_new_message(client: Client, update: UpdateNewMessage):\n    logging.info(\'on_update_new_message handler called\')\n\n\nasync def main():\n    client = Client(\n        api_id=API_ID,\n        api_hash=API_HASH,\n        phone_number=PHONE_NUMBER\n    )\n\n    client.add_event_handler(on_update_new_message, update_type=API.Types.UPDATE_NEW_MESSAGE)\n\n    # Registering middleware.\n    # Note that middleware would be called for EVERY EVENT.\n    # Don\'t use them for long-running tasks as it could be heavy performance hit\n    # You can add as much middlewares as you want. \n    # They would be called in order you\'ve added them\n    client.add_middleware(my_middleware)\n\n    async with client:\n        await client.idle()\n\n\nif __name__ == \'__main__\':\n    logging.basicConfig(level=logging.INFO)\n    asyncio.run(main())\n```\n\n## LICENSE\n\nThis project is licensed under the terms of the [MIT](https://github.com/pylakey/aiotdlib/blob/master/LICENSE) license.\n',
    'author': 'pylakey',
    'author_email': 'pylakey@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pylakey/aiotdlib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
