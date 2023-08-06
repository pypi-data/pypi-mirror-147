
from dataclasses import dataclass
from typing import Optional, List

from . import discord_types
from . import user as user_module


@dataclass
class Sticker(discord_types.DiscordDataClass):
    id: discord_types.Snowflake
    name: str
    description: str
    tags: str
    type: discord_types.StickerType
    format_type: discord_types.StickerFormatType
    pack_id: Optional[discord_types.Snowflake] = None
    asset: Optional[str] = None  # Deprecated
    available: Optional[bool] = None
    guild_id: Optional[discord_types.Snowflake] = None
    user: Optional['user_module.User'] = None
    sort_value: Optional[int] = None

    def __post_init__(self) -> None:
        self.type = discord_types.StickerType(self.type)
        self.format_type = discord_types.StickerFormatType(self.format_type)
        if isinstance(self.user, dict):
            self.user = user_module.User(**self.user)  # type: ignore[unreachable]


@dataclass
class StickerItem(discord_types.DiscordDataClass):
    id: discord_types.Snowflake
    name: str
    format_type: discord_types.StickerFormatType

    def __post_init__(self) -> None:
        self.format_type = discord_types.StickerFormatType(self.format_type)


@dataclass
class StickerPack(discord_types.DiscordDataClass):
    id: discord_types.Snowflake
    stickers: List[Sticker]
    name: str
    sku_id: discord_types.Snowflake
    description: str
    cover_sticker_id: Optional[discord_types.Snowflake] = None
    banner_asset_id: Optional[discord_types.Snowflake] = None

    def __post_init__(self) -> None:
        self.stickers = [
            Sticker(**sticker) if isinstance(sticker, dict) else sticker
            for sticker in self.stickers
        ]
