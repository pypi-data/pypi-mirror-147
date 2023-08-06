
from dataclasses import dataclass
from typing import Optional, List

from . import discord_types
from . import guild as guild_module
from . import channel as channel_module
from . import user as user_module
from . import application as application_module
from . import guild_scheduled_event as gse_module


@dataclass
class InviteStageInstance(discord_types.DiscordDataClass):
    members: List[guild_module.PartialGuildMember]
    participant_count: int
    speaker_count: int
    topic: str

    def __post_init__(self) -> None:
        self.members = [
            guild_module.PartialGuildMember(**m) if isinstance(m, dict) else m
            for m in self.members
        ]


@dataclass
class Invite(discord_types.DiscordDataClass):
    code: str
    channel: channel_module.PartialChannel
    guild: Optional[guild_module.PartialGuild] = None
    inviter: Optional[user_module.User] = None
    target_type: Optional[discord_types.InviteTargetType] = None
    target_user: Optional[user_module.User] = None
    target_application: Optional[application_module.PartialApplication] = None
    approximate_presence_count: Optional[int] = None
    approximate_member_count: Optional[int] = None
    expires_at: Optional[str] = None
    stage_instance: Optional[InviteStageInstance] = None
    guild_scheduled_event: Optional[gse_module.GuildScheduledEvent] = None

    def __post_init__(self) -> None:
        if isinstance(self.channel, dict):
            self.channel = channel_module.PartialChannel(**self.channel)  # type: ignore[unreachable]
        if isinstance(self.guild, dict):
            self.guild = guild_module.PartialGuild(**self.guild)  # type: ignore[unreachable]
        if isinstance(self.inviter, dict):
            self.inviter = user_module.User(**self.inviter)  # type: ignore[unreachable]
        if isinstance(self.target_type, int):
            self.target_type = discord_types.InviteTargetType(self.target_type)
        if isinstance(self.target_user, dict):
            self.target_user = user_module.User(**self.target_user)  # type: ignore[unreachable]
        if isinstance(self.target_application, dict):
            self.target_application = application_module.PartialApplication(**self.target_application)  # type: ignore[unreachable]
        if isinstance(self.stage_instance, dict):
            self.stage_instance = InviteStageInstance(**self.stage_instance)  # type: ignore[unreachable]
        if isinstance(self.guild_scheduled_event, dict):
            self.guild_scheduled_event = gse_module.GuildScheduledEvent(**self.guild_scheduled_event)  # type: ignore[unreachable]


@dataclass
class InviteMetadata(discord_types.DiscordDataClass):
    uses: int
    max_uses: int
    max_age: int
    temporary: bool
    created_at: str
