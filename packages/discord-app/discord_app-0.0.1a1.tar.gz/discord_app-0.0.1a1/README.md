# Discord Interaction Application framework for Python

![Tests](https://github.com/jacky9813/discord_app/actions/workflows/tests.yaml/badge.svg) [![Pypi](https://badge.fury.io/py/discord-app.svg)](https://pypi.org/project/discord-app/)

> In early development.
> 
> The specification and documentation may change without notification.
> 
> Any new ideas are welcomed.

A [Flask](https://flask.palletsprojects.com/) based Discord Application framework.

## System Requirements

* Python 3.9+
* (Recommended) [virtualenv](https://virtualenv.pypa.io/en/latest/)

## Install from PyPI

Install and update using [pip](https://pip.pypa.io/en/stable/getting-started/):

```bash
 $ pip install discord-app
```

## Known Limitation

* After command specification updated (including new command), Discord clients may require up to an hour to update its command list.

## Sample Server Application
```python
#!/usr/bin/env python3
# app.py
import discord_app

from . import app_config

PORT = "8080"

app = discord_app.Application.from_basic_data(
    id=app_config.APPLICATION_ID,
    public_key=app_config.PUBLIC_KEY,
    bot_token=app_config.BOT_TOKEN,
    # Set Discord interaction endpoint URL to http(s)://<YOUR-ADDRESS>:<PORT>/<ENDPOINT>
    endpoint="/api/discord/command"
)

app._flask.testing = True
app._logger.setLevel(logging.DEBUG)


@app.application_command(
    options=discord_app.ApplicationCommand(
        name="version",
        name_localizations={
            "zh-TW": "顯示程式版本"
        },
        type=discord_app.ApplicationCommandType.CHAT_INPUT,
        description="Show application version",
        description_localizations={
            "zh-TW": "顯示程式版本"
        }
    ),
    register_on_change=True  # Register command on specification change or is new command.
)
def show_version(_: discord_app.InteractionRequest) -> discord_app.InteractionResponse:
    return discord_app.InteractionResponse(
        type=discord_app.InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        data=discord_app.InteractionResponseMessage(
            content="test application/0.0.1"
        )
    )

app.run(
    host="0.0.0.0",
    port=PORT
)
```

```bash
 $ python3 app.py
```

## Links
* [Official API Documentation](https://discord.com/developers/docs/)
