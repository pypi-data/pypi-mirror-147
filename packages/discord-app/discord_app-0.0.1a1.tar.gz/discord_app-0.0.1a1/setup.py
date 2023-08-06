# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['discord_app']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.1.1,<3.0.0', 'PyNaCl>=1.4.0,<2.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'discord-app',
    'version': '0.0.1a1',
    'description': 'Discord Interaction Application framework for Python',
    'long_description': '# Discord Interaction Application framework for Python\n\n![Tests](https://github.com/jacky9813/discord_app/actions/workflows/tests.yaml/badge.svg) [![Pypi](https://badge.fury.io/py/discord-app.svg)](https://pypi.org/project/discord-app/)\n\n> In early development.\n> \n> The specification and documentation may change without notification.\n> \n> Any new ideas are welcomed.\n\nA [Flask](https://flask.palletsprojects.com/) based Discord Application framework.\n\n## System Requirements\n\n* Python 3.9+\n* (Recommended) [virtualenv](https://virtualenv.pypa.io/en/latest/)\n\n## Install from PyPI\n\nInstall and update using [pip](https://pip.pypa.io/en/stable/getting-started/):\n\n```bash\n $ pip install discord-app\n```\n\n## Known Limitation\n\n* After command specification updated (including new command), Discord clients may require up to an hour to update its command list.\n\n## Sample Server Application\n```python\n#!/usr/bin/env python3\n# app.py\nimport discord_app\n\nfrom . import app_config\n\nPORT = "8080"\n\napp = discord_app.Application.from_basic_data(\n    id=app_config.APPLICATION_ID,\n    public_key=app_config.PUBLIC_KEY,\n    bot_token=app_config.BOT_TOKEN,\n    # Set Discord interaction endpoint URL to http(s)://<YOUR-ADDRESS>:<PORT>/<ENDPOINT>\n    endpoint="/api/discord/command"\n)\n\napp._flask.testing = True\napp._logger.setLevel(logging.DEBUG)\n\n\n@app.application_command(\n    options=discord_app.ApplicationCommand(\n        name="version",\n        name_localizations={\n            "zh-TW": "顯示程式版本"\n        },\n        type=discord_app.ApplicationCommandType.CHAT_INPUT,\n        description="Show application version",\n        description_localizations={\n            "zh-TW": "顯示程式版本"\n        }\n    ),\n    register_on_change=True  # Register command on specification change or is new command.\n)\ndef show_version(_: discord_app.InteractionRequest) -> discord_app.InteractionResponse:\n    return discord_app.InteractionResponse(\n        type=discord_app.InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,\n        data=discord_app.InteractionResponseMessage(\n            content="test application/0.0.1"\n        )\n    )\n\napp.run(\n    host="0.0.0.0",\n    port=PORT\n)\n```\n\n```bash\n $ python3 app.py\n```\n\n## Links\n* [Official API Documentation](https://discord.com/developers/docs/)\n',
    'author': 'JackyCCC',
    'author_email': 'jacky9813@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jacky9813/discord_app',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)
