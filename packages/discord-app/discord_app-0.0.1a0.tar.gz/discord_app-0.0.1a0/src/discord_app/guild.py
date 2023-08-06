
from dataclasses import dataclass
from typing import List, Optional, Any

from . import discord_types
from . import user as user_module
from . import emoji
from . import channel
from . import voice
from . import sticker


@dataclass
class RoleTags(discord_types.DiscordDataClass):
    bot_id: Optional[discord_types.Snowflake] = None
    integration_id: Optional[discord_types.Snowflake] = None
    # Type of premium_sucscriver is "null" in the documentation
    premium_subscriber: Optional[Any] = None


@dataclass
class Role(discord_types.DiscordDataClass):
    """
        Discord role
    """
    id: discord_types.Snowflake
    name: str
    color: int
    hoist: bool
    position: int
    permissions: str
    managed: bool
    mentionable: bool
    icon: Optional[str] = None
    unicode_emoji: Optional[str] = None
    tags: Optional[RoleTags] = None

    def __post_init__(self) -> None:
        if self.tags is not None and isinstance(self.tags, dict):
            self.tags = RoleTags(**self.tags)


@dataclass
class PartialGuild(discord_types.DiscordDataClass):
    name: str
    roles: List[Role]
    channels: List[channel.Channel]
    verification_level: discord_types.VerificationLevel
    default_message_notifications: discord_types.DefaultMessageNotificationLevel
    explicit_content_filter: discord_types.ExplicitContentFilterLevel


@dataclass
class Guild(PartialGuild):
    id: discord_types.Snowflake
    icon: str
    splash: str
    discovery_splash: str
    owner_id: discord_types.Snowflake
    afk_channel_id: discord_types.Snowflake
    afk_timeout: int
    emojis: List[emoji.Emoji]
    features: List[discord_types.GuildFeature]
    mfa_level: discord_types.MFALevel
    application_id: discord_types.Snowflake
    system_channel_id: discord_types.Snowflake
    system_channel_flags: int
    rules_channel_id: discord_types.Snowflake
    vanity_url_code: str
    description: str
    banner: str
    premium_tier: int
    preferred_locale: str
    public_updates_channel_id: discord_types.Snowflake
    nsfw_level: int
    premium_progress_bar_enabled: bool
    icon_hash: Optional[str] = None
    owner: Optional[bool] = None
    permissions: Optional[str] = None
    region: Optional[str] = None
    widget_enabled: Optional[bool] = None
    widget_channel_id: Optional[discord_types.Snowflake] = None
    joined_at: Optional[str] = None
    large: Optional[bool] = None
    unavailable: Optional[bool] = None
    member_count: Optional[int] = None
    voice_states: Optional[List[voice.VoiceState]] = None
    members: Optional[List['GuildMember']] = None
    threads: Optional[List[channel.Channel]] = None
    presences: Optional[List[Any]] = None
    max_presences: Optional[int] = None
    max_members: Optional[int] = None
    premium_subscription_count: Optional[int] = None
    max_video_channel_users: Optional[int] = None
    approximate_member_count: Optional[int] = None
    approximate_presence_count: Optional[int] = None
    welcome_screen: Optional[Any] = None
    stage_instances: Optional[List[Any]] = None
    stickers: Optional[List[sticker.Sticker]] = None
    guild_scheduled_events: Optional[List[Any]] = None


@dataclass
class GuildPreview(discord_types.DiscordDataClass):
    id: discord_types.Snowflake
    name: str
    icon: str
    splash: str
    discovery_splash: str
    emojis: List[emoji.Emoji]
    features: List[discord_types.GuildFeature]
    approximate_member_count: int
    approximate_presence_count: int
    description: str
    stickers: List[sticker.Sticker]

    def __post_init__(self) -> None:
        self.emojis = [
            emoji.Emoji(**e) if isinstance(e, dict) else e
            for e in self.emojis
        ]
        self.features = [
            discord_types.GuildFeature(feature) if isinstance(feature, str) else feature
            for feature in self.features
        ]
        self.stickers = [
            sticker.Sticker(**s) if isinstance(s, dict) else s
            for s in self.stickers
        ]


@dataclass
class GuildWidgetSettings(discord_types.DiscordDataClass):
    enabled: bool
    channel_id: discord_types.Snowflake


@dataclass
class GetGuildWidget(discord_types.DiscordDataClass):  # The name is not an typo, unless the API documentation is.
    id: discord_types.Snowflake
    name: str
    instant_invite: str
    channels: List[channel.PartialChannel]
    members: List['user_module.PartialUser']
    presence_count: int


@dataclass
class PartialGuildMember(discord_types.DiscordDataClass):
    """
        Guild member but without user, deaf and mute properties.
    """
    joined_at: str
    roles: List[discord_types.Snowflake]
    nick: Optional[str] = None
    avatar: Optional[str] = None
    premium_since: Optional[bool] = None
    pending: Optional[bool] = None
    permissions: Optional[str] = None
    communication_disabled_until: Optional[str] = None

    # The following attributes are undocumented
    flags: Optional[Any] = None
    is_pending: Optional[Any] = None


@dataclass
class GuildMember(PartialGuildMember):
    """
        Guild member
    """
    user: Optional['user_module.User'] = None
    deaf: bool = False
    mute: bool = False

    def __post_init__(self) -> None:
        if isinstance(self.user, dict):
            self.user = user_module.User(**self.user)  # type: ignore[unreachable]


@dataclass
class IntegrationAccount(discord_types.DiscordDataClass):
    id: str
    name: str


@dataclass
class IntegrationApplication(discord_types.DiscordDataClass):
    id: discord_types.Snowflake
    name: str
    icon: str
    description: str
    bot: Optional['user_module.User']


@dataclass
class Integration(discord_types.DiscordDataClass):
    id: discord_types.Snowflake
    name: str
    type: str
    account: IntegrationAccount
    enabled: Optional[bool] = None
    syncing: Optional[bool] = None
    role_id: Optional[discord_types.Snowflake] = None
    enable_emoticons: Optional[bool] = None
    expire_behavior: Optional[discord_types.IntegrationExpireBehavior] = None
    expire_grace_period: Optional[int] = None
    user: Optional['user_module.User'] = None
    synced_at: Optional[str] = None
    subscriber_count: Optional[int] = None
    revoked: Optional[bool] = None
    application: Optional[IntegrationApplication] = None


@dataclass
class Ban(discord_types.DiscordDataClass):
    reason: str
    user: 'user_module.User'


@dataclass
class WelcomeScreenChannel(discord_types.DiscordDataClass):
    channel_id: discord_types.Snowflake
    description: str
    emoji_id: discord_types.Snowflake
    emoji_name: discord_types.Snowflake


@dataclass
class WelcomeScreen(discord_types.DiscordDataClass):
    description: str
    welcome_channels: List[WelcomeScreenChannel]
