
from dataclasses import dataclass
from typing import Dict, List, Optional, Union, Any
from typing_extensions import Self

from . import discord_types
from . import channel
from . import user as user_module
from . import guild as guild_module


@dataclass
class ApplicationCommandOptionChoice(discord_types.DiscordDataClass):
    """
        Related choice for parameter (ApplicationCommandOption)
    """
    name: str
    value: Union[str, int, float]
    name_localizations: Optional[Dict[str, str]] = None


@dataclass
class ApplicationCommandOption(discord_types.DiscordDataClass):
    """
        Parameter for application command.
    """
    name: str
    description: str
    type: Optional[discord_types.ApplicationCommandOptionType] = discord_types.ApplicationCommandOptionType.SUB_COMMAND
    name_localizations: Optional[Dict[str, str]] = None
    description_localizations: Optional[Dict[str, str]] = None
    required: Optional[bool] = False
    choices: Optional[List['ApplicationCommandOptionChoice']] = None
    options: Optional[List['ApplicationCommandOption']] = None
    channel_types: Optional[List[discord_types.ChannelType]] = None
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    autocomplete: Optional[bool] = False

    def __post_init__(self) -> None:
        if isinstance(self.type, int):
            self.type = discord_types.ApplicationCommandOptionType(self.type)
        if isinstance(self.choices, list):
            self.choices = [ApplicationCommandOptionChoice(**choice) if isinstance(choice, dict) else choice for choice in self.choices]
        if isinstance(self.options, list):
            self.options = [ApplicationCommandOption(**option) if isinstance(option, dict) else option for option in self.options]
        if isinstance(self.channel_types, list):
            self.channel_types = [
                discord_types.ChannelType(channel_type) if isinstance(channel_type, discord_types.ChannelType) else channel_type
                for channel_type in self.channel_types
            ]


@dataclass
class ApplicationCommand(discord_types.DiscordDataClass):
    """
        The specification for the custom Discord command.
    """
    name: str
    description: str
    name_localizations: Optional[Dict[str, str]] = None
    description_localizations: Optional[Dict[str, str]] = None
    id: Optional[discord_types.Snowflake] = None
    type: Optional[discord_types.ApplicationCommandType] = discord_types.ApplicationCommandType.CHAT_INPUT
    application_id: Optional[discord_types.Snowflake] = None
    guild_id: Optional[discord_types.Snowflake] = None
    options: Optional[List['ApplicationCommandOption']] = None
    default_permission: Optional[bool] = None
    version: Optional[discord_types.Snowflake] = None

    # The following attribute are undocumented
    default_member_permissions: Optional[Any] = None
    dm_permission: Optional[Any] = None

    def __post_init__(self) -> None:
        if isinstance(self.type, int):
            self.type = discord_types.ApplicationCommandType(self.type)
        if isinstance(self.options, list):
            self.options = [ApplicationCommandOption(**option) if isinstance(option, dict) else option for option in self.options]


@dataclass
class InteractionResponseData(discord_types.DiscordDataClass):
    def __new__(cls, *args: Any, **kwargs: Any) -> Union[  # type: ignore[misc]
        'InteractionResponseMessage',
        'InteractionResponseAutocomplete',
        'InteractionResponseModal'
    ]:
        target: Any = InteractionResponseMessage
        if "choices" in kwargs:
            target = InteractionResponseAutocomplete
        if "title" in kwargs or "custom_id" in kwargs:
            target = InteractionResponseModal
        if cls is InteractionResponseData:
            return super(InteractionResponseData, target).__new__(target, *args, **kwargs)  # type: ignore[misc, no-any-return]
        else:
            return super(InteractionResponseData, cls).__new__(cls)  # type: ignore[return-value]


@dataclass
class InteractionResponseMessage(InteractionResponseData):
    tts: Optional[bool] = None
    content: Optional[str] = None
    embeds: Optional[List[channel.Embed]] = None
    allowed_mentions: Optional[channel.AllowedMentions] = None
    flags: Optional[discord_types.MessageFlags] = None
    components: Optional[List[channel.MessageComponent]] = None
    attachments: Optional[List[channel.PartialAttachment]] = None

    def __post_init__(self) -> None:
        if isinstance(self.embeds, list):
            self.embeds = [
                channel.Embed(**e) if isinstance(e, dict) else e
                for e in self.embeds
            ]
        if isinstance(self.allowed_mentions, dict):
            self.allowed_mentions = channel.AllowedMentions(**self.allowed_mentions)  # type: ignore[unreachable]
        if isinstance(self.flags, int):
            self.flags = discord_types.MessageFlags(self.flags)
        if isinstance(self.components, list):
            self.components = [
                channel.MessageComponent(**component) if isinstance(component, dict) else component
                for component in self.components
            ]
        if isinstance(self.attachments, list):
            self.attachments = [
                channel.PartialAttachment(**attachment) if isinstance(attachment, dict) else attachment
                for attachment in self.attachments
            ]


@dataclass
class InteractionResponseAutocomplete(InteractionResponseData):
    choices: List[ApplicationCommandOptionChoice]

    def __post_init__(self) -> None:
        self.choices = [
            ApplicationCommandOptionChoice(**choice) if isinstance(choice, dict) else choice
            for choice in self.choices
        ]


@dataclass
class InteractionResponseModal(InteractionResponseData):
    custom_id: str
    title: str
    components: List[channel.MessageComponent]

    def __post_init__(self) -> None:
        self.components = [
            channel.MessageComponent(**component) if isinstance(component, dict) else component
            for component in self.components
        ]


@dataclass
class InteractionResponse(discord_types.DiscordDataClass):
    """
        Response object for handling incoming interaction.
    """
    type: discord_types.InteractionResponseType
    data: Optional[InteractionResponseData] = None

    def __post_init__(self) -> None:
        if isinstance(self.type, int):
            self.type = discord_types.InteractionResponseType(self.type)
        if isinstance(self.data, dict):
            # TODO: The corresponding data may related to the response type. But I'm not sure if deciding data type here is a good idea.
            DATA_TYPES = {  # type: ignore[unreachable]
                discord_types.InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE: InteractionResponseMessage,
                discord_types.InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE: InteractionResponseMessage,
                discord_types.InteractionResponseType.DEFFERED_UPDATE_MESSAGE: InteractionResponseMessage,
                discord_types.InteractionResponseType.UPDATE_MESSAGE: InteractionResponseMessage,
                discord_types.InteractionResponseType.MODAL: InteractionResponseModal,
                discord_types.InteractionResponseType.APPLICATION_AUTOCOMPLETE_RESULT: InteractionResponseAutocomplete,
                discord_types.InteractionResponseType.PONG: None
            }
            target_cls = DATA_TYPES[self.type]
            if target_cls is None:
                # Response to ping shouldn't have data
                self.data = None
            else:
                self.data = target_cls(**self.data)


@dataclass
class InteractionResolvedData(discord_types.DiscordDataClass):
    """
        Interaction Resolve Data
    """
    users: Optional[Dict[discord_types.Snowflake, user_module.User]] = None
    members: Optional[Dict[discord_types.Snowflake, guild_module.PartialGuildMember]] = None
    roles: Optional[Dict[discord_types.Snowflake, guild_module.Role]] = None
    channels: Optional[Dict[discord_types.Snowflake, channel.PartialChannel]] = None
    messages: Optional[Dict[discord_types.Snowflake, channel.Message]] = None
    attachments: Optional[Dict[discord_types.Snowflake, channel.Attachment]] = None

    def __post_init__(self) -> None:
        if isinstance(self.users, dict):
            self.users = {
                discord_types.Snowflake(k): user_module.User(**v) if isinstance(v, dict) else v
                for (k, v) in self.users.items()
            }
        if isinstance(self.members, dict):
            self.members = {
                discord_types.Snowflake(k): guild_module.PartialGuildMember(**v) if isinstance(v, dict) else v
                for (k, v) in self.members.items()
            }
        if isinstance(self.roles, dict):
            self.roles = {
                discord_types.Snowflake(k): guild_module.Role(**v) if isinstance(v, dict) else v
                for (k, v) in self.roles.items()
            }
        if isinstance(self.channels, dict):
            self.channels = {
                discord_types.Snowflake(k): channel.Channel(**v) if isinstance(v, dict) else v
                for (k, v) in self.channels.items()
            }
        if isinstance(self.messages, dict):
            self.messages = {
                discord_types.Snowflake(k): channel.Message(**v) if isinstance(v, dict) else v
                for (k, v) in self.messages.items()
            }
        if isinstance(self.attachments, dict):
            self.attachments = {
                discord_types.Snowflake(k): channel.Attachment(**v) if isinstance(v, dict) else v
                for (k, v) in self.attachments.items()
            }


@dataclass
class InteractionDataOption(discord_types.DiscordDataClass):
    """
        When incoming interaction message is application command,
        this object is to deliver the command parameter.
    """
    name: str
    type: discord_types.ApplicationCommandOptionType
    value: Optional[Union[int, float, str]] = None
    # Make mypy ignore "Self if not a type" error
    options: Optional[List[Self]] = None  # type: ignore
    focused: Optional[bool] = None

    def __post_init__(self) -> None:
        if isinstance(self.type, int):
            self.type = discord_types.ApplicationCommandOptionType(self.type)
        if isinstance(self.options, list):
            self.options = [
                InteractionDataOption(**option) if isinstance(option, dict) else option
                for option in self.options
            ]


@dataclass
class InteractionData(discord_types.DiscordDataClass):
    """
        Additional data for incoming interaction message
    """
    id: discord_types.Snowflake
    name: str
    type: discord_types.ApplicationCommandType
    resolved: Optional[InteractionResolvedData] = None
    options: Optional[List[InteractionDataOption]] = None
    guild_id: Optional[discord_types.Snowflake] = None
    custom_id: Optional[str] = None
    component_type: Optional[discord_types.MessageComponentType] = None
    values: Optional[List[channel.MessageComponentSelectOption]] = None
    target_id: Optional[discord_types.Snowflake] = None
    components: Optional[List[channel.MessageComponent]] = None

    def __post_init__(self) -> None:
        if isinstance(self.type, int):
            self.type = discord_types.ApplicationCommandType(self.type)
        if isinstance(self.resolved, dict):
            self.resolved = InteractionResolvedData(**self.resolved)  # type: ignore[unreachable]
        if isinstance(self.options, list):
            self.options = [
                InteractionDataOption(**option) if isinstance(option, dict) else option
                for option in self.options
            ]
        if isinstance(self.component_type, int):
            self.component_type = discord_types.MessageComponentType(self.component_type)
        if isinstance(self.values, list):
            self.values = [
                channel.MessageComponentSelectOption(**option) if isinstance(option, dict) else option
                for option in self.values
            ]
        if isinstance(self.components, list):
            self.components = [
                channel.MessageComponent(**component) if isinstance(component, dict) else component
                for component in self.components
            ]


@dataclass
class InteractionRequest(discord_types.DiscordDataClass):
    """
        Incoming interaction message
    """
    id: discord_types.Snowflake
    application_id: discord_types.Snowflake
    type: discord_types.InteractionType
    token: str
    version: int = 1
    data: Optional[InteractionData] = None
    guild_id: Optional[discord_types.Snowflake] = None
    channel_id: Optional[discord_types.Snowflake] = None
    member: Optional[guild_module.GuildMember] = None
    user: Optional[user_module.User] = None
    message: Optional[channel.Message] = None
    locale: Optional[str] = None
    guild_locale: Optional[str] = None

    # Internal use only
    _app: Optional[Any] = None

    def __post_init__(self) -> None:
        if isinstance(self.type, int):
            self.type = discord_types.InteractionType(self.type)
        if isinstance(self.data, dict):  # type: ignore[unreachable]
            self.data = InteractionData(**self.data)  # type: ignore[unreachable]
        if isinstance(self.member, dict):
            self.member = guild_module.GuildMember(**self.member)  # type: ignore[unreachable]
        if isinstance(self.user, dict):
            self.user = user_module.User(**self.user)  # type: ignore[unreachable]
        if isinstance(self.message, dict):
            self.message = channel.Message(**self.message)  # type: ignore[unreachable]

    def get_channel(self) -> Optional[channel.Channel]:
        if self.channel_id and self._app:
            channel_data, _ = self._app.call_api(  # type: ignore[misc]
                "GET",
                f"/channels/{self.channel_id}"
            )
            return channel.Channel(**channel_data)
        else:
            return None
