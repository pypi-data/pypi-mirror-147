
from dataclasses import dataclass
from typing import List, Optional, Any, Union
from typing_extensions import Self

from . import guild
from . import discord_types
from . import user as user_module
from . import emoji as emoji_module
from . import channel
from . import sticker


@dataclass
class AllowedMentions(discord_types.DiscordDataClass):
    parse: List[discord_types.AllowedMentionType]
    roles: List[discord_types.Snowflake]
    users: List[discord_types.Snowflake]
    replied_user: bool

    def __post_init__(self) -> None:
        self.parse = [
            discord_types.AllowedMentionType(t) if isinstance(t, str) else t
            for t in self.parse
        ]


@dataclass
class ThreadMetadata(discord_types.DiscordDataClass):
    archived: bool
    auto_archive_duration: int
    archive_timestamp: str
    locked: bool
    invitable: Optional[bool] = None
    create_timestamp: Optional[str] = None


@dataclass
class ThreadMember(discord_types.DiscordDataClass):
    join_timestamp: str
    flags: int
    id: Optional[discord_types.Snowflake] = None
    user_id: Optional[discord_types.Snowflake] = None


@dataclass
class Overwrite(discord_types.DiscordDataClass):
    id: discord_types.Snowflake
    type: discord_types.Snowflake
    allow: str
    deny: str


@dataclass
class Channel(discord_types.DiscordDataClass):
    id: discord_types.Snowflake
    type: discord_types.ChannelType
    guild_id: Optional[discord_types.Snowflake] = None
    position: Optional[int] = None
    permission_overwrites: Optional[List[Overwrite]] = None
    name: Optional[str] = None
    topic: Optional[str] = None
    nsfw: Optional[bool] = None
    last_message_id: Optional[discord_types.Snowflake] = None
    bitrate: Optional[int] = None
    user_limit: Optional[int] = None
    rate_limit_per_user: Optional[int] = None
    recipients: Optional[List['user_module.User']] = None
    icon: Optional[str] = None
    owner_id: Optional[discord_types.Snowflake] = None
    application_id: Optional[discord_types.Snowflake] = None
    parent_id: Optional[discord_types.Snowflake] = None
    last_pin_timestamp: Optional[str] = None
    rtc_region: Optional[str] = None
    video_quality_mode: Optional[discord_types.VideoQualityMode] = None
    message_count: Optional[int] = None
    member_count: Optional[int] = None
    thread_metadata: Optional[ThreadMetadata] = None
    member: Optional[ThreadMember] = None
    default_auto_archive_duration: Optional[int] = None
    permissions: Optional[str] = None
    flags: Optional[discord_types.ChannelFlag] = None

    def __post_init__(self) -> None:
        if isinstance(self.recipients, list):
            self.recipients = [user_module.User(**u) if isinstance(u, dict) else u for u in self.recipients]
        if isinstance(self.video_quality_mode, int):
            self.video_quality_mode = discord_types.VideoQualityMode(self.video_quality_mode)
        if isinstance(self.flags, int):
            self.flags = discord_types.ChannelFlag(self.flags)
        if isinstance(self.thread_metadata, dict):
            self.thread_metadata = ThreadMetadata(**self.thread_metadata)  # type: ignore[unreachable]
        if isinstance(self.member, dict):
            self.member = ThreadMember(**self.member)  # type: ignore[unreachable]
        if isinstance(self.permission_overwrites, list):
            self.permission_overwrites = [
                Overwrite(**overwrite) if isinstance(overwrite, dict) else overwrite
                for overwrite in self.permission_overwrites
            ]


PartialChannel = Channel


@dataclass
class ChannelMention(discord_types.DiscordDataClass):
    id: discord_types.Snowflake
    guild_id: discord_types.Snowflake
    type: discord_types.ChannelType
    name: str

    def __post_init__(self) -> None:
        self.type = discord_types.ChannelType(self.type)


@dataclass
class EmbedThumbnail(discord_types.DiscordDataClass):
    url: str
    proxy_url: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None


@dataclass
class EmbedVideo(discord_types.DiscordDataClass):
    url: Optional[str] = None
    proxy_url: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None


@dataclass
class EmbedImage(discord_types.DiscordDataClass):
    url: str
    proxy_url: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None


@dataclass
class EmbedProvider(discord_types.DiscordDataClass):
    name: Optional[str] = None
    url: Optional[str] = None


@dataclass
class EmbedAuthor(discord_types.DiscordDataClass):
    name: str
    url: Optional[str] = None
    icon_url: Optional[str] = None
    proxy_icon_url: Optional[str] = None


@dataclass
class EmbedFooter(discord_types.DiscordDataClass):
    text: str
    icon_url: Optional[str] = None
    proxy_icon_url: Optional[str] = None


@dataclass
class EmbedField(discord_types.DiscordDataClass):
    name: str
    value: str
    inline: Optional[bool] = None


@dataclass
class Embed(discord_types.DiscordDataClass):
    title: Optional[str] = None
    type: Optional[discord_types.EmbedType] = None
    description: Optional[str] = None
    url: Optional[str] = None
    timestamp: Optional[str] = None
    color: Optional[int] = None
    footer: Optional[EmbedFooter] = None
    image: Optional[EmbedImage] = None
    thumbnail: Optional[EmbedThumbnail] = None
    video: Optional[EmbedVideo] = None
    provider: Optional[EmbedProvider] = None
    author: Optional[EmbedAuthor] = None
    fields: Optional[List[EmbedField]] = None

    def __post_init__(self) -> None:
        if isinstance(self.type, str):
            self.type = discord_types.EmbedType(self.type)
        if isinstance(self.footer, dict):
            self.footer = EmbedFooter(**self.footer)  # type: ignore[unreachable]
        if isinstance(self.image, dict):
            self.image = EmbedImage(**self.image)  # type: ignore[unreachable]
        if isinstance(self.thumbnail, dict):
            self.thumbnail = EmbedThumbnail(**self.thumbnail)  # type: ignore[unreachable]
        if isinstance(self.video, dict):
            self.video = EmbedVideo(**self.video)  # type: ignore[unreachable]
        if isinstance(self.provider, dict):
            self.provider = EmbedProvider(**self.provider)  # type: ignore[unreachable]
        if isinstance(self.author, dict):
            self.author = EmbedAuthor(**self.author)  # type: ignore[unreachable]
        if isinstance(self.fields, list):
            self.fields = [
                EmbedField(**field) if isinstance(field, dict) else field
                for field in self.fields
            ]


@dataclass
class PartialAttachment(discord_types.DiscordDataClass):
    id: discord_types.Snowflake
    filename: str
    description: Optional[str] = None
    content_type: Optional[str] = None


@dataclass
class Attachment(discord_types.DiscordDataClass):
    id: discord_types.Snowflake
    filename: str
    size: int
    url: str
    proxy_url: str
    description: Optional[str] = None
    content_type: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None
    ephemeral: Optional[bool] = None


@dataclass
class MessageComponent(discord_types.DiscordDataClass):
    def __new__(cls, *args: Any, **kwargs: Any) -> Union[  # type: ignore[misc]
        'MessageComponentActionRow',
        'MessageComponentButton',
        'MessageComponentSelectMenu',
        'MessageComponentTextInput'
    ]:
        CLASS_MAP = {
            discord_types.MessageComponentType.ACTION_ROW: MessageComponentActionRow,
            discord_types.MessageComponentType.BUTTON: MessageComponentButton,
            discord_types.MessageComponentType.SELECT_MENU: MessageComponentSelectMenu,
            discord_types.MessageComponentType.TEXT_INPUT: MessageComponentTextInput
        }
        target = CLASS_MAP[kwargs['type']]
        if cls is MessageComponent:
            return super(MessageComponent, target).__new__(target)  # type: ignore[misc, no-any-return]
        else:
            return super(MessageComponent, cls).__new__(cls, *args, **kwargs)  # type: ignore[return-value]


@dataclass
class MessageComponentActionRow(MessageComponent):
    components: List[MessageComponent]
    type: discord_types.MessageComponentType = discord_types.MessageComponentType.ACTION_ROW

    def __post_init__(self) -> None:
        self.components = [
            MessageComponent(component) if isinstance(component, dict) else component
            for component in self.components
        ]
        if self.type != discord_types.MessageComponentType.ACTION_ROW:
            raise ValueError(f"type for {self.__class__.__name__} must be MessageComponentType.ACTION_ROW")
        self.type = discord_types.MessageComponentType.ACTION_ROW


@dataclass
class MessageComponentButton(MessageComponent):
    style: discord_types.MessageComponentButtonStyle
    type: discord_types.MessageComponentType = discord_types.MessageComponentType.BUTTON
    label: Optional[str] = None
    emoji: Optional[emoji_module.Emoji] = None
    custom_id: Optional[str] = None
    url: Optional[str] = None
    disabled: Optional[bool] = None

    def __post_init__(self) -> None:
        self.style = discord_types.MessageComponentButtonStyle(self.style)
        if self.type != discord_types.MessageComponentType.BUTTON:
            raise ValueError(f"type for {self.__class__.__name__} must be MessageComponentType.BUTTON")
        self.type = discord_types.MessageComponentType.BUTTON
        if isinstance(self.emoji, dict):
            self.emoji = emoji_module.Emoji(**self.emoji)  # type: ignore[unreachable]


@dataclass
class MessageComponentSelectOption(discord_types.DiscordDataClass):
    label: str
    value: str
    default: bool = False
    description: Optional[str] = None
    emoji: Optional[emoji_module.Emoji] = None

    def __post_init__(self) -> None:
        if isinstance(self.emoji, dict):
            self.emoji = emoji_module.Emoji(**self.emoji)  # type: ignore[unreachable]


@dataclass
class MessageComponentSelectMenu(MessageComponent):
    custom_id: str
    options: List[MessageComponentSelectOption]
    min_values: int = 1
    max_values: int = 1
    type: discord_types.MessageComponentType = discord_types.MessageComponentType.SELECT_MENU
    disabled: bool = False
    placeholder: Optional[str] = None

    def __post_init__(self) -> None:
        self.options = [
            MessageComponentSelectOption(**option) if isinstance(option, dict) else option
            for option in self.options
        ]
        if self.type != discord_types.MessageComponentType.SELECT_MENU:
            raise ValueError(f"type for {self.__class__.__name__} must be MessageComponentType.SELECT_MENU")
        self.type = discord_types.MessageComponentType.SELECT_MENU


@dataclass
class MessageComponentTextInput(MessageComponent):
    custom_id: str
    style: discord_types.MessageComponentTextInputStyle
    label: str
    type: discord_types.MessageComponentType = discord_types.MessageComponentType.TEXT_INPUT
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    required: bool = True
    value: Optional[str] = None
    placeholder: Optional[str] = None

    def __post_init__(self) -> None:
        self.style = discord_types.MessageComponentTextInputStyle(self.style)
        if self.type != discord_types.MessageComponentType.TEXT_INPUT:
            raise ValueError(f"type for {self.__class__.__name__} must be MessageComponentType.TEXT_INPUT")
        self.type = discord_types.MessageComponentType.TEXT_INPUT


@dataclass
class MessageReference(discord_types.DiscordDataClass):
    message_id: Optional[discord_types.Snowflake] = None
    channel_id: Optional[discord_types.Snowflake] = None
    guild_id: Optional[discord_types.Snowflake] = None
    fail_if_not_exists: Optional[bool] = True


@dataclass
class MessageInteraction(discord_types.DiscordDataClass):
    id: discord_types.Snowflake
    type: discord_types.InteractionType
    name: str
    user: 'user_module.User'
    member: Optional['guild.PartialGuildMember'] = None

    def __post_init__(self) -> None:
        self.type = discord_types.InteractionType(self.type)
        if isinstance(self.user, dict):
            self.user = user_module.User(**self.user)  # type: ignore[unreachable]
        if isinstance(self.member, dict):
            self.member = guild.PartialGuildMember(**self.member)  # type: ignore[unreachable]


@dataclass
class Reaction(discord_types.DiscordDataClass):
    count: int
    me: bool
    emoji: emoji_module.Emoji


@dataclass
class MessageActivity(discord_types.DiscordDataClass):
    type: discord_types.MessageActivityType
    party_id: Optional[str] = None


@dataclass
class Message(discord_types.DiscordDataClass):
    id: discord_types.Snowflake
    channel_id: discord_types.Snowflake
    timestamp: str
    tts: bool
    mention_everyone: bool
    mentions: List['user_module.User']
    mention_roles: List['guild.Role']
    attachments: List[Attachment]
    embeds: List[Embed]
    content: str
    type: discord_types.MessageType
    guild_id: Optional[discord_types.Snowflake] = None
    author: Optional['user_module.User'] = None
    member: Optional['guild.PartialGuildMember'] = None
    edited_timestamp: Optional[str] = None
    mention_channels: Optional[List[channel.ChannelMention]] = None
    reactions: Optional[List[Reaction]] = None
    nonce: Optional[Union[int, str]] = None
    activity: Optional[MessageActivity] = None
    application: Optional[Any] = None
    application_id: Optional[discord_types.Snowflake] = None
    message_reference: Optional[MessageReference] = None
    flags: Optional[discord_types.MessageFlags] = None
    # Make mypy ignore "Self if not a type" error
    referenced_message: Optional[Self] = None  # type: ignore
    interaction: Optional[MessageInteraction] = None
    thread: Optional[channel.Channel] = None
    components: Optional[List[MessageComponent]] = None
    sticker_items: Optional[List[sticker.StickerItem]] = None
    stickers: Optional[List[sticker.Sticker]] = None

    def __post_init__(self) -> None:
        self.mentions = [
            user_module.User(**u) if isinstance(u, dict) else u
            for u in self.mentions
        ]
        self.mention_roles = [
            guild.Role(**role) if isinstance(role, dict) else role
            for role in self.mention_roles
        ]
        self.attachments = [
            Attachment(**attachment) if isinstance(attachment, dict) else attachment
            for attachment in self.attachments
        ]
        self.embeds = [
            Embed(**embed) if isinstance(embed, dict) else embed
            for embed in self.embeds
        ]
        self.type = discord_types.MessageType(self.type)
        if isinstance(self.author, dict):
            self.author = user_module.User(**self.author)  # type: ignore[unreachable]
        if isinstance(self.member, dict):
            self.member = guild.PartialGuildMember(**self.member)  # type: ignore[unreachable]
        if isinstance(self.mention_channels, list):
            self.mention_channels = [
                channel.ChannelMention(**cm) if isinstance(cm, dict) else cm
                for cm in self.mention_channels
            ]
        if isinstance(self.reactions, list):
            self.reactions = [
                Reaction(**reaction) if isinstance(reaction, dict) else reaction
                for reaction in self.reactions
            ]
        if isinstance(self.flags, int):
            self.flags = discord_types.MessageFlags(self.flags)
        if isinstance(self.message_reference, dict):
            self.message_reference = MessageReference(**self.message_reference)  # type: ignore[unreachable]
        if isinstance(self.referenced_message, dict):
            self.referenced_message = Message(**self.referenced_message)  # type: ignore[unreachable]
        if isinstance(self.interaction, dict):
            self.interaction = MessageInteraction(**self.interaction)  # type: ignore[unreachable]
        if isinstance(self.thread, dict):
            self.thread = channel.Channel(**self.thread)  # type: ignore[unreachable]
        if isinstance(self.components, list):
            self.components = [
                MessageComponent(**component) if isinstance(component, dict) else component
                for component in self.components
            ]
        if isinstance(self.activity, dict):
            self.activity = MessageActivity(**self.activity)  # type: ignore[unreachable]
        if isinstance(self.sticker_items, list):
            self.sticker_items = [
                sticker.StickerItem(**item) if isinstance(item, dict) else item
                for item in self.sticker_items
            ]
        if isinstance(self.stickers, list):
            self.stickers = [
                sticker.Sticker(**stkr) if isinstance(stkr, dict) else stkr
                for stkr in self.stickers  # name as stkr due to imported mudule name also called sticker
            ]


@dataclass
class FollowedChannel(discord_types.DiscordDataClass):
    channel_id: discord_types.Snowflake
    webhook_id: discord_types.Snowflake
