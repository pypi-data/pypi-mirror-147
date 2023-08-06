
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
    creator: Optional['user_module.User'] = None
    user_count: Optional[int] = None
    image: Optional[str] = None

    # Required for STAGE_INSTANCE and VOICE type
    channel_id: Optional[discord_types.Snowflake] = None

    # Required for EXTERNAL type
    entity_metadata: Optional[GuildScheduledEventEntityMetadata] = None
    scheduled_end_time: Optional[str] = None

    def __post_init__(self) -> None:
        self.privacy_level = discord_types.GuildScheduledEventPrivacyLevel(self.privacy_level)
        self.status = discord_types.GuildScheduledEventStatus(self.status)
        self.entity_type = discord_types.GuildScheduledEventEntityType(self.entity_type)
        if isinstance(self.creator, dict):
            self.creator = user_module.User(**self.creator)  # type: ignore[unreachable]

        if self.entity_type is discord_types.GuildScheduledEventEntityType.EXTERNAL:
            if self.entity_metadata is None or self.scheduled_end_time is None:
                raise AttributeError("entity_metadata and scheduled_end_time is required for EXTERNAL event type.")
            if isinstance(self.entity_metadata, dict):
                self.entity_metadata = GuildScheduledEventEntityMetadata(**self.entity_metadata)  # type: ignore[unreachable]
        else:
            if self.channel_id is None:
                raise AttributeError(f"entity_metadata and scheduled_end_time is required for {self.entity_type.name} event type.")


@dataclass
class GuildScheduledEventUser(discord_types.DiscordDataClass):
    guild_scheduled_event_id: discord_types.Snowflake
    user: 'user_module.User'
    member: Optional['guild_module.GuildMember']

    def __post_init__(self) -> None:
        if isinstance(self.user, dict):
            self.user = user_module.User(**self.user)  # type: ignore[unreachable]
        if isinstance(self.member, dict):
            self.member = guild_module.GuildMember(**self.member)  # type: ignore[unreachable]
