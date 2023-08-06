
from dataclasses import dataclass
from typing import Optional

from . import discord_types
from . import user as user_module
from . import guild as guild_module


@dataclass
class GuildScheduledEventEntityMetadata(discord_types.DiscordDataClass):
    location: Optional[str] = None


@dataclass
class GuildScheduledEvent(discord_types.DiscordDataClass):
    id: discord_types.Snowflake
    guild_id: discord_types.Snowflake
    name: str
    scheduled_start_time: str
    privacy_level: discord_types.GuildScheduledEventPrivacyLevel
    status: discord_types.GuildScheduledEventStatus
    entity_type: discord_types.GuildScheduledEventEntityType
    creator_id: Optional[discord_types.Snowflake] = None
    description: Optional[str] = None
    creator: Optional[user_module.User] = None
    user_count: Optional[int] = None
    image: Optional[str] = None

    # Required for STAGE_INSTANCE and VOICE
    channel_id: Optional[discord_types.Snowflake] = None

    # Required for EXTERNAL
    entity_metadata: Optional[GuildScheduledEventEntityMetadata] = None
    scheduled_end_time: Optional[str] = None


@dataclass
class GuildScheduledEventUser(discord_types.DiscordDataClass):
    guild_scheduled_event_id: discord_types.Snowflake
    user: user_module.User
    member: Optional[guild_module.GuildMember]
