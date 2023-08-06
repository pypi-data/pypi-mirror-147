
from dataclasses import dataclass

from . import discord_types


@dataclass
class StageInstance(discord_types.DiscordDataClass):
    id: discord_types.Snowflake
    guild_id: discord_types.Snowflake
    channel_id: discord_types.Snowflake
    topic: str
    privacy_level: int
    discoverable_disabled: bool
    guild_scheduled_event_id: discord_types.Snowflake
