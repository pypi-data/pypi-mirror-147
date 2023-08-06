
from dataclasses import dataclass
from typing import List, Optional, Any

from . import discord_types
from . import user as user_module
from . import emoji
from . import channel
from . import voice
from . import sticker
from . import stage_instance
from . import guild_scheduled_event
from . import presence


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
        if isinstance(self.tags, dict):
            self.tags = RoleTags(**self.tags)  # type: ignore[unreachable]


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

    def __post_init__(self) -> None:
        self.welcome_channels = [
            WelcomeScreenChannel(**wsc) if isinstance(wsc, dict) else wsc
            for wsc in self.welcome_channels
        ]


@dataclass
class PartialGuild(discord_types.DiscordDataClass):
    name: str
    roles: List[Role]
    channels: List[channel.Channel]
    verification_level: discord_types.VerificationLevel
    default_message_notifications: discord_types.DefaultMessageNotificationLevel
    explicit_content_filter: discord_types.ExplicitContentFilterLevel

    def __post_init__(self) -> None:
        self.roles = [
            Role(**r) if isinstance(r, dict) else r
            for r in self.roles
        ]
        self.channels = [
            channel.Channel(**c) if isinstance(c, dict) else c
            for c in self.channels
        ]
        self.verification_level = discord_types.VerificationLevel(self.verification_level)
        self.default_message_notifications = discord_types.DefaultMessageNotificationLevel(self.default_message_notifications)
        self.explicit_content_filter = discord_types.ExplicitContentFilterLevel(self.explicit_content_filter)


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
    system_channel_flags: discord_types.SystemChannelFlags
    rules_channel_id: discord_types.Snowflake
    vanity_url_code: str
    description: str
    banner: str
    premium_tier: discord_types.GuildPremiumTier
    preferred_locale: str
    public_updates_channel_id: discord_types.Snowflake
    nsfw_level: discord_types.GuildNSFWLevel
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
    voice_states: Optional[List[voice.PartialVoiceState]] = None
    members: Optional[List['GuildMember']] = None
    threads: Optional[List[channel.Channel]] = None
    presences: Optional[List[presence.PresenceUpdateEvent]] = None
    max_presences: Optional[int] = None
    max_members: Optional[int] = None
    premium_subscription_count: Optional[int] = None
    max_video_channel_users: Optional[int] = None
    approximate_member_count: Optional[int] = None
    approximate_presence_count: Optional[int] = None
    welcome_screen: Optional[WelcomeScreen] = None
    stage_instances: Optional[List[stage_instance.StageInstance]] = None
    stickers: Optional[List[sticker.Sticker]] = None
    guild_scheduled_events: Optional[List[guild_scheduled_event.GuildScheduledEvent]] = None

    def __post_init__(self) -> None:
        super().__post_init__()
        self.emojis = [
            emoji.Emoji(**e) if isinstance(e, dict) else e
            for e in self.emojis
        ]
        self.features = [
            discord_types.GuildFeature(f) if isinstance(f, str) else f
            for f in self.features
        ]
        self.mfa_level = discord_types.MFALevel(self.mfa_level)
        self.system_channel_flags = discord_types.SystemChannelFlags(self.system_channel_flags)
        self.premium_tier = discord_types.GuildPremiumTier(self.premium_tier)
        self.nsfw_level = discord_types.GuildNSFWLevel(self.nsfw_level)
        if isinstance(self.voice_states, list):
            self.voice_states = [
                voice.PartialVoiceState(**vs) if isinstance(vs, dict) else vs
                for vs in self.voice_states
            ]
        if isinstance(self.members, list):
            self.members = [
                GuildMember(**gm) if isinstance(gm, dict) else gm
                for gm in self.members
            ]
        if isinstance(self.threads, list):
            self.threads = [
                channel.Channel(**t) if isinstance(t, dict) else t
                for t in self.threads
            ]
        if isinstance(self.welcome_screen, dict):
            self.welcome_screen = WelcomeScreen(**self.welcome_screen)  # type: ignore[unreachable]
        if isinstance(self.stage_instances, list):
            self.stage_instances = [
                stage_instance.StageInstance(**si) if isinstance(si, dict) else si
                for si in self.stage_instances
            ]
        if isinstance(self.stickers, list):
            self.stickers = [
                sticker.Sticker(**s) if isinstance(s, dict) else s
                for s in self.stickers
            ]
        if isinstance(self.guild_scheduled_events, list):
            self.guild_scheduled_events = [
                guild_scheduled_event.GuildScheduledEvent(**gse) if isinstance(gse, dict) else gse
                for gse in self.guild_scheduled_events
            ]
        if isinstance(self.presences, list):
            self.presences = [
                presence.PresenceUpdateEvent(**p) if isinstance(p, dict) else p
                for p in self.presences
            ]


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
    members: List['user_module.PartialUser']  # The documentation show here uses partial user for some reason
    presence_count: int

    def __post_init__(self) -> None:
        self.channels = [
            channel.PartialChannel(**c) if isinstance(c, dict) else c
            for c in self.channels
        ]
        self.members = [
            user_module.PartialUser(**m) if isinstance(m, dict) else m
            for m in self.members
        ]


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

    # The following attributes are undocumented in Discord API documentation
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
        # Parent class didn't define __post_init__ function, no need to execute.
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

    def __post_init__(self) -> None:
        if isinstance(self.bot, dict):
            self.bot = user_module.User(**self.bot)  # type: ignore[unreachable]


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

    def __post_init__(self) -> None:
        if isinstance(self.account, dict):
            self.account = IntegrationAccount(**self.account)  # type: ignore[unreachable]
        if isinstance(self.expire_behavior, int):
            self.expire_behavior = discord_types.IntegrationExpireBehavior(self.expire_behavior)
        if isinstance(self.user, dict):
            self.user = user_module.User(**self.user)  # type: ignore[unreachable]
        if isinstance(self.application, dict):
            self.application = IntegrationApplication(**self.application)  # type: ignore[unreachable]


@dataclass
class Ban(discord_types.DiscordDataClass):
    reason: str
    user: 'user_module.User'

    def __post_init__(self) -> None:
        if isinstance(self.user, dict):
            self.user = user_module.User(**self.user)  # type: ignore[unreachable]
