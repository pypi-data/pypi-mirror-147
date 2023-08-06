
from typing import Optional
from dataclasses import dataclass

from . import discord_types
from . import guild as guild_module


@dataclass
class VoiceState(discord_types.DiscordDataClass):
    channel_id: discord_types.Snowflake
    user_id: discord_types.Snowflake
    session_id: str
    deaf: bool
    mute: bool
    self_deaf: bool
    self_mute: bool
    self_video: bool
    suppress: bool
    request_to_speak_timestamp: str
    guild_id: Optional[discord_types.Snowflake] = None
    member: Optional['guild_module.GuildMember'] = None
    self_stream: Optional[bool] = None
