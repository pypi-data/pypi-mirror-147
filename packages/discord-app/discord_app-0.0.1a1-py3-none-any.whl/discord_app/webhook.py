
from dataclasses import dataclass
from typing import Optional

from . import discord_types
from . import user as user_module
from . import guild as guild_module


@dataclass
class Webhook(discord_types.DiscordDataClass):
    id: discord_types.Snowflake
    type: discord_types.WebhookType
    guild_id: discord_types.Snowflake
    channel_id: discord_types.Snowflake
    name: str
    avatar: str
    application_id: discord_types.Snowflake
    user: Optional[user_module.User] = None
    token: Optional[str] = None
    source_guild: Optional[guild_module.PartialGuild] = None
    url: Optional[str] = None

    def __post_init__(self) -> None:
        self.type = discord_types.WebhookType(self.type)
        if isinstance(self.user, dict):
            self.user = user_module.User(**self.user)  # type: ignore[unreachable]
        if isinstance(self.source_guild, dict):
            self.source_guild = guild_module.PartialGuild(**self.source_guild)  # type: ignore[unreachable]
