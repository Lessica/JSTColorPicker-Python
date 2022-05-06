"""
Extract JSTColorPicker annotation data models from metadata of bitmap images.
"""

import dataclasses
from typing import Optional
from collections import namedtuple
from bpylist2.archive_types import DataclassArchiver


__version__ = '0.1.0'


@dataclasses.dataclass
class Content(DataclassArchiver):
    items: list = dataclasses.field(default_factory=list)

    def __json__(self):
        return self.__dict__


@dataclasses.dataclass
class ContentItem(DataclassArchiver):
    id: int = dataclasses.field(default=0)
    similarity: float = dataclasses.field(default=1)
    userInfo: dict = dataclasses.field(default_factory=dict)
    userInfoKeys: list[str] = dataclasses.field(default_factory=list)
    userInfoValues: list[str] = dataclasses.field(default_factory=list)
    tags: list = dataclasses.field(default_factory=list)

    @property
    def user_info(self) -> dict[str, str]:
        user_info = self.userInfo or {}
        for user_idx, user_key in enumerate(self.userInfoKeys):
            user_info[str(user_key)] = str(self.userInfoValues[user_idx])
        return user_info

    @property
    def first_tag(self) -> Optional[str]:
        if len(self.tags) == 0:
            return None
        return self.tags[0]

    def __json__(self):
        return self.__dict__


@dataclasses.dataclass
class JSTPixelColor(DataclassArchiver):
    red: int = dataclasses.field(default=0)
    green: int = dataclasses.field(default=0)
    blue: int = dataclasses.field(default=0)
    alpha: int = dataclasses.field(default=0)

    def __json__(self):
        return self.__dict__


Rect = namedtuple('Rect', ['x', 'y', 'width', 'height'])


@dataclasses.dataclass
class PixelArea(ContentItem):
    rectOriginX: int = dataclasses.field(default=0)
    rectOriginY: int = dataclasses.field(default=0)
    rectSizeWidth: int = dataclasses.field(default=0)
    rectSizeHeight: int = dataclasses.field(default=0)

    @property
    def rect(self) -> Rect:
        return Rect(x=self.rectOriginX, y=self.rectOriginY, width=self.rectSizeWidth, height=self.rectSizeHeight)

    def __json__(self):
        return self.__dict__


@dataclasses.dataclass
class PixelColor(ContentItem):
    coordinateX: int = dataclasses.field(default=0)
    coordinateY: int = dataclasses.field(default=0)
    pixelColorRep: JSTPixelColor = dataclasses.field(default=0)

    def __json__(self):
        return self.__dict__

