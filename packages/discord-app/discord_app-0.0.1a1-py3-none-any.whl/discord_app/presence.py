
from dataclasses import dataclass
from typing import Optional, List, Tuple

from . import emoji as emoji_module
from . import discord_types
from . import user as user_module


@dataclass
class ActivityTimestamp(discord_types.DiscordDataClass):
    start: Optional[int] = None
    end: Optional[int] = None


ActivityEmoji = emoji_module.Emoji  # Activity Emoji is essentially a subset of Emoji with the same required properties


@dataclass
class ActivityParty(discord_types.DiscordDataClass):
    id: Optional[str] = None
    size: Optional[Tuple[int, int]] = None  # current_size, max_size


@dataclass
class ActivityAsset(discord_types.DiscordDataClass):
    large_image: Optional[str] = None
    large_text: Optional[str] = None
    small_image: Optional[str] = None
    small_text: Optional[str] = None


@dataclass
class ActivitySecret(discord_types.DiscordDataClass):
    join: Optional[str] = None
    spectate: Optional[str] = None
    match: Optional[str] = None


@dataclass
class ActivityButton(discord_types.DiscordDataClass):
    label: str
    url: str


@dataclass
class Activity(discord_types.DiscordDataClass):
    name: str
    type: discord_types.ActivityType
    created_at: int  # Use unix timestamp here (in milliseconds)
    url: Optional[str] = None
    timestamps: Optional[ActivityTimestamp] = None
    application_id: Optional[discord_types.Snowflake] = None
    details: Optional[str] = None
    state: Optional[str] = None
    emoji: Optional[ActivityEmoji] = None
    party: Optional[ActivityParty] = None
    assets: Optional[ActivityAsset] = None
    secrets: Optional[ActivitySecret] = None
    instance: Optional[bool] = None
    flags: Optional[discord_types.ActivityFlag] = None
    buttons: Optional[List[ActivityButton]] = None

    def __post_init__(self) -> None:
        self.type = discord_types.ActivityType(self.type)
        if isinstance(self.timestamps, dict):
            self.timestamps = ActivityTimestamp(**self.timestamps)  # type: ignore[unreachable]
        if isinstance(self.emoji, dict):
            self.emoji = ActivityEmoji(**self.emoji)  # type: ignore[unreachable]
        if isinstance(self.party, dict):
            self.party = ActivityParty(**self.party)  # type: ignore[unreachable]
        if isinstance(self.assets, dict):
            self.assets = ActivityAsset(**self.assets)  # type: ignore[unreachable]
        if isinstance(self.secrets, dict):
            self.secrets = ActivitySecret(**self.secrets)  # type: ignore[unreachable]
        if isinstance(self.flags, int):
            self.flags = discord_types.ActivityFlag(self.flags)
        if isinstance(self.buttons, list):
            self.buttons = [
                ActivityButton(**b) if isinstance(b, dict) else b
                for b in self.buttons
            ]


@dataclass
class ClientStatus(discord_types.DiscordDataClass):
    desktop: Optional[str] = None
    mobile: Optional[str] = None
    web: Optional[str] = None


@dataclass
class PresenceUpdateEvent(discord_types.DiscordDataClass):
    user: 'user_module.User'
    guild_id: discord_types.Snowflake
    status: str
    activities: List[Activity]
    client_status: ClientStatus

    def __post_init__(self) -> None:
        if isinstance(self.user, dict):
            self.user = user_module.User(**self.user)  # type: ignore[unreachable]
        if isinstance(self.activities, list):
            self.activities = [
                Activity(**a) if isinstance(a, dict) else a
                for a in self.activities
            ]
        if isinstance(self.client_status, dict):
            self.client_status = ClientStatus(**self.client_status)  # type: ignore[unreachable]
