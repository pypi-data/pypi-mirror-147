from dataclasses import dataclass
from datetime import date
from typing import List, Optional

from doujinApi.typings.constants import Sex


@dataclass
class Tag:
    id: str
    name_jp: str
    name_en: Optional[str]
    name_r: Optional[str]
    name_alt: Optional[List[str]]
    count: Optional[int]


@dataclass
class Content(Tag):
    pass


@dataclass
class Character(Tag):
    sex: Optional[Sex]
    age: Optional[int]
    contents: Optional[List[Content]]


@dataclass
class Convention(Tag):
    date_start: date
    date_end: date


@dataclass
class Collection(Tag):
    pass


@dataclass
class Type(Tag):
    pass


@dataclass
class Parody(Tag):
    contents: Optional[List[Content]]
    characters: Optional[List[Character]]


@dataclass
class Author(Tag):
    pass


@dataclass
class Circle(Tag):
    authors: Optional[List[Author]]


@dataclass
class Genre(Tag):
    pass


@dataclass
class Imprint(Tag):
    pass


@dataclass
class Publisher(Tag):
    pass
