"""
    Data types used by Discord Interaction model

    Mostly enumerates and flags.
"""
from dataclasses import dataclass
from enum import Enum, IntEnum, IntFlag


#############################################################
#   Global
#############################################################


Snowflake = str  # I know this is an int, but API returns as a str


@dataclass
class DiscordDataClass():
    pass


#############################################################
#   Interaction
#############################################################

class ApplicationFlags(IntFlag):
    """
        Application flags
    """
    GATEWAY_PRESENCE = 1 << 12
    GATEWAY_PRESENCE_LIMITED = 1 << 13
    GATEWAY_GUILD_MEMBERS = 1 << 14
    GATEWAY_GUILD_MEMBERS_LIMITED = 1 << 15
    VERIFICATION_PENDING_GUILD_LIMIT = 1 << 16
    EMBEDDED = 1 << 17
    GATEWAY_MESSAGE_CONTENT = 1 << 18
    GATEWAY_MESSAGE_CONTENT_LIMITED = 1 << 19


class ApplicationCommandType(IntEnum):
    """
        Application Command Type

        Controls how the command will be invoked.
    """
    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3


class ApplicationCommandOptionType(IntEnum):
    """
        Application Command Option Type

        Specify the parameter data type for the command.
    """
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10
    ATTACHMEHT = 11


class InteractionType(IntEnum):
    """
        Interaction Type

        Interaction behavior identificator.
    """
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5


class InteractionCallbackType(IntEnum):
    """
        Interaction Callback Type

        Use when responding an interaction.
    """
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    DEFFERED_UPDATE_MESSAGE = 6
    UPDATE_MESSAGE = 7
    APPLICATION_AUTOCOMPLETE_RESULT = 8
    MODAL = 9


InteractionResponseType = InteractionCallbackType


class MessageComponentType(IntEnum):
    """
        Message component type
    """
    ACTION_ROW = 1
    BUTTON = 2
    SELECT_MENU = 3
    TEXT_INPUT = 4


#############################################################
#   Channel (including messages, embed)
#############################################################


class ChannelType(IntEnum):
    """
        Channel Type
    """
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_NEWS = 5

    # These three only available in API v9
    GUILD_NEWS_THREAD = 10
    GUILD_PUBLIC_THREAD = 11
    GUILD_PRIVATE_THREAD = 12

    GUILD_STAGE_VOICE = 13
    GUILD_DIRECTORY = 14
    GUILD_FORUM = 15


class VideoQualityMode(IntEnum):
    """
        Video quality mode
    """
    AUTO = 1
    FULL = 2


class ChannelFlag(IntFlag):
    """
        Channel flag
    """
    PINNED = 1 << 1


class AllowedMentionType(str, Enum):
    """
        Allowed mention type
    """
    ROLE = "roles"
    USER = "users"
    EVERYONE = "everyone"


class MessageType(IntEnum):
    """
        Message type
    """
    DEFAULT = 0
    RECIPIENT_ADD = 1
    RECIPIENT_REMOVE = 2
    CALL = 3
    CHANNEL_NAME_CHANGE = 4
    CHANNEL_ICON_CHANGE = 5
    CHANNEL_PINNED_MESSAGE = 6
    GUILD_MEMBER_JOIN = 7
    USER_PREMIUM_GUILD_SUBSCRIPTION = 8
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_1 = 9
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_2 = 10
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_3 = 11
    CHANNEL_FOLLOW_ADD = 12
    GUILD_DISCOVERY_DISQUALIFIED = 14
    GUILD_DISCOVERY_REQUALIFIED = 15
    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
    THREAD_CREATED = 18
    REPLY = 19
    CHAT_INPUT_COMMAND = 20
    THREAD_STARTER_MESSAGE = 21
    GUILD_INVITE_REMINDER = 22
    CONTEXT_MENU_COMMAND = 23


class MessageActivityType(IntEnum):
    """
        Message activity type
    """
    JOIN = 1
    SPECTATE = 2
    LISTEN = 3
    JOIN_REQUEST = 5


class MessageFlags(IntFlag):
    """
        Message flags
    """
    CROSSPOSTED = 1 << 0
    IS_CROSSPOST = 1 << 1
    SUPPRESS_EMBEDS = 1 << 2
    SOURCE_MESSAGE_DELETED = 1 << 3
    URGENT = 1 << 4
    HAS_THREAD = 1 << 5
    EPHEMERAL = 1 << 6
    LOADING = 1 << 7
    FAILED_TO_MENTION_SOME_ROLES_IN_THREAD = 1 << 8


class MessageComponentButtonStyle(IntEnum):
    """
        Button style
    """
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5


class MessageComponentTextInputStyle(IntEnum):
    """
        Text input style
    """
    SHORT = 1
    PARAGRAPH = 2


class EmbedType(str, Enum):
    """
        Embed content type
    """
    RICH = "rich"
    IMAGE = "image"
    VIDEO = "video"
    GIFV = "gifv"
    ARTICLE = "article"
    LINK = "link"


#############################################################
#   Guild
#############################################################


class DefaultMessageNotificationLevel(IntEnum):
    """
        Default message notification level
    """
    ALL_MESSAGES = 0
    ONLY_MENTIONS = 1


class ExplicitContentFilterLevel(IntEnum):
    """
        Explicit content filter level
    """
    DISABLED = 0
    MEMBERS_WITHOUT_ROLES = 1
    ALL_MEMBERS = 2


class MFALevel(IntEnum):
    """
        Multi-Factor Authentication Level
    """
    NONE = 0
    ELEVATED = 1


class VerificationLevel(IntEnum):
    """
        The verification level a user must comply before joining as a guild member.
    """
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4


class GuildNSFWLevel(IntEnum):
    """
        Identify how Not-Safe-For-Work (NSFW) a guild is.
    """
    DEFAULT = 0
    EXPLICIT = 1
    SAFE = 2
    AGE_RESTRICTED = 3


class GuildPremiumTier(IntEnum):
    """
        Guild Nitro tier
    """
    NONE = 0
    TIER_1 = 1
    TIER_2 = 2
    TIER_3 = 3


class SystemChannelFlags(IntFlag):
    """
        System channel flags
    """
    SUPPRESS_JOIN_NOTIFICATIONS = 1 << 0
    SUPPRESS_PREMIUM_SUBSCRIPTIONS = 1 << 1
    SUPPRESS_GUILD_REMINDER_NOTIFICATIONS = 1 << 2
    SUPPRESS_JOIN_NOTIFICATION_REPLIES = 1 << 3


class GuildFeature(str, Enum):
    """
        Guild features
    """
    ANIMATED_BANNER = "ANIMATED_BANNER"
    ANIMATED_ICON = "ANIMATED_ICON"
    BANNER = "BANNER"
    COMMERCE = "COMMERCE"
    COMMUNITY = "COMMUNITY"
    DISCOVERABLE = "DISCOVERABLE"
    FEATURABLE = "FEATURABLE"
    INVITE_SPLASH = "INVITE_SPLASH"
    MEMBER_VERIFICATION_GATE_ENABLED = "MEMBER_VERIFICATION_GATE_ENABLED"
    MONETIZATION_ENABLED = "MONETIZATION_ENABLED"
    MORE_STICKERS = "MORE_STICKERS"
    NEWS = "NEWS"
    PARTNERED = "PARTNERED"
    PREVIEW_ENABLED = "PREVIEW_ENABLED"
    PRIVATE_THREADS = "PRIVATE_THREADS"
    ROLE_ICONS = "ROLE_ICONS"
    SEVEN_DAY_THREAD_ARCHIVE = "SEVEN_DAY_THREAD_ARCHIVE"
    THREE_DAY_THREAD_ARCHIVE = "THREE_DAY_THREAD_ARCHIVE"
    TICKETED_EVENTS_ENABLED = "TICKETED_EVENTS_ENABLED"
    VANITY_URL = "VANITY_URL"
    VERIFIED = "VERIFIED"
    VIP_REGIONS = "VIP_REGIONS"
    WELCOME_SCREEN_ENABLED = "WELCOME_SCREEN_ENABLED"


class IntegrationExpireBehavior(IntEnum):
    REMOVE_ROLE = 0
    KICK = 1


#############################################################
#   Guild Scheduled Event
#############################################################


class GuildScheduledEventEntityType(IntEnum):
    """
        Guild scheduled event Entity type
    """
    STAGE_INSTANCE = 1
    VOICE = 2
    EXTERNAL = 3


class GuildScheduledEventStatus(IntEnum):
    """
        Guild scheduled event Status
    """
    SCHEDULED = 1
    ACTIVE = 2
    COMPLERED = 3
    CANCELED = 4


#############################################################
#   Stage Instance
#############################################################


class PrivacyLevel(IntEnum):
    """
        Privacy level
    """
    PUBLIC = 1  # Deprecated
    GUILD_ONLY = 2


GuildScheduledEventPrivacyLevel = PrivacyLevel


#############################################################
#   Invite
#############################################################


class InviteTargetType(IntEnum):
    """
        Invite target type
    """
    STREAM = 1
    EMBEDDED_APPLICATION = 2


#############################################################
#   User
#############################################################


class UserFlag(IntFlag):
    """
        User flag
    """
    STAFF = 1 << 0
    PARTNER = 1 << 1
    HYPESQUAD = 1 << 2
    BUG_HUNTER_LEVEL_1 = 1 << 3
    HYPESQUAD_ONLINE_HOUSE_1 = 1 << 6
    HYPESQUAD_ONLINE_HOUSE_2 = 1 << 7
    HYPESQUAD_ONLINE_HOUSE_3 = 1 << 8
    PREMIUM_EARLY_SUPPORTER = 1 << 9
    TEAM_PSEUDO_USER = 1 << 10
    BUG_HUNTER_LEVEL_2 = 1 << 14
    VERIFIED_BOT = 1 << 16
    VERIFIED_DEVELOPER = 1 << 17
    CERTIFIED_MODERATOR = 1 << 18
    BOT_HTTP_INTERACTIONS = 1 << 19


class PremiumTypes(IntEnum):
    """
        Nitro subscription level
    """
    NONE = 0
    NITRO_CLASSIC = 1
    NITRO = 2


class Visibility(IntEnum):
    """
        Connection visibility
    """
    NONE = 0
    EVERYONE = 1


#############################################################
#   Sticker
#############################################################


class StickerFormatType(IntEnum):
    """
        Sticker format
    """
    PNG = 1
    APNG = 2
    LOTTIE = 3


class StickerType(IntEnum):
    """
        Source of the sticker
    """
    STANDARD = 1
    GUILD = 2


#############################################################
#   Webhook
#############################################################


class WebhookType(IntEnum):
    """
        Webhook type
    """
    INCOMING = 1
    CHANNEL_FOLLOWER = 2
    APPLICATION = 3


#############################################################
#   Activity
#############################################################


class ActivityType(IntEnum):
    """
        User activity presence
    """
    GAME = 0
    STREAMING = 1
    LISTENING = 2
    WATCHING = 3
    CUSTOM = 4
    COMPETING = 5
