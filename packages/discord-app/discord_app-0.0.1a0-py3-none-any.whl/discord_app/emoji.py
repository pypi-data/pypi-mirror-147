
from dataclasses import dataclass
from typing import List, Optional
from . import discord_types
from . import user as user_module


@dataclass
class Emoji(discord_types.DiscordDataClass):
    id: discord_types.Snowflake
    name: Optional[str] = None
    roles: Optional[List[discord_types.Snowflake]] = None
    user: Optional['user_module.User'] = None
    require_colons: Optional[bool] = None
    managed: Optional[bool] = None
    animated: Optional[bool] = None
    available: Optional[bool] = None

    def __post_init__(self) -> None:
        if isinstance(self.user, dict):
            self.user = user_module.User(**self.user)  # type: ignore[unreachable]
