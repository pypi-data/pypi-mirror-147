
from dataclasses import dataclass

from . import discord_types
from . import user as user_module
from . import guild as guild_module


@dataclass
class GuildTemplate(discord_types.DiscordDataClass):
    code: str
    name: str
    description: str
    usage_count: int
    creator_id: discord_types.Snowflake
    creator: user_module.User
    created_at: str
    updated_at: str
    source_guild_id: discord_types.Snowflake
    serialized_source_guild: guild_module.PartialGuild
    is_dirty: bool
