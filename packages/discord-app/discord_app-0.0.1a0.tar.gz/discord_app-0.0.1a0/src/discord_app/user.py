
from dataclasses import dataclass
from typing import Optional, Any, List

from . import discord_types
from . import guild as guild_module


@dataclass
class User(discord_types.DiscordDataClass):
    """
        Discord user
    """
    id: discord_types.Snowflake
    username: str
    discriminator: str
    avatar: str
    bot: Optional[bool] = None
    system: Optional[bool] = None
    mfa_enabled: Optional[bool] = None
    banner: Optional[str] = None
    accent_color: Optional[int] = None
    locale: Optional[str] = None
    verified: Optional[bool] = None
    email: Optional[str] = None
    flags: Optional[discord_types.UserFlag] = None
    premium_type: Optional[discord_types.PremiumTypes] = None
    public_flags: Optional[discord_types.UserFlag] = None

    # The following attributes are undocumented
    avatar_decoration: Optional[Any] = None

    def __post_init__(self) -> None:
        if isinstance(self.flags, int):
            self.flags = discord_types.UserFlag(self.flags)
        if isinstance(self.premium_type, int):
            self.premium_type = discord_types.PremiumTypes(self.premium_type)
        if isinstance(self.public_flags, int):
            self.public_flags = discord_types.UserFlag(self.public_flags)


PartialUser = User


@dataclass
class Connection(discord_types.DiscordDataClass):
    id: str
    name: str
    type: str
    verified: bool
    friend_sync: bool
    show_activity: bool
    visibility: discord_types.Visibility
    revoked: Optional[bool] = None
    integrations: Optional[List[guild_module.Integration]] = None
