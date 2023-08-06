
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


@dataclass
class InviteMetadata(discord_types.DiscordDataClass):
    uses: int
    max_uses: int
    max_age: int
    temporary: bool
    created_at: str
