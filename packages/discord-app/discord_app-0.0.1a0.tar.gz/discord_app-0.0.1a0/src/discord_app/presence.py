
from dataclasses import dataclass
from typing import Optional, Any

from . import emoji as emoji_module
from . import discord_types
from . import user


@dataclass
class ActivityTimestamp(discord_types.DiscordDataClass):
    start: Optional[int] = None
    end: Optional[int] = None


@dataclass
class Activity(discord_types.DiscordDataClass):
    name: str
    type: discord_types.ActivityType
    created_at: int
    url: Optional[str] = None
    timestamps: Optional[ActivityTimestamp] = None
    application_id: Optional[discord_types.Snowflake] = None
    details: Optional[str] = None
    state: Optional[str] = None
    emoji: Optional[emoji_module.Emoji] = None
    party: Optional[Any] = None
    assets: Optional[Any] = None
    secrets: Optional[Any] = None
    instance: Optional[bool] = None
    flags: Optional[int] = None
    buttons: Optional[Any] = None


@dataclass
class ClientStatus(discord_types.DiscordDataClass):
    desktop: Optional[str] = None
    mobile: Optional[str] = None
    web: Optional[str] = None


@dataclass
class PresenceUpdateEvent(discord_types.DiscordDataClass):
    user: user.User
    guild_id: discord_types.Snowflake
    status: str
    activities: Activity
    client_status: ClientStatus
