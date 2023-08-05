from dataclasses import dataclass
from datetime import date
from typing import List, Optional

from doujinApi.typings.constants import Language
from doujinApi.typings.tag import Author, Character, Circle, Content, Convention, Parody


@dataclass
class Book:
    id: str
    name_jp: str
    name_en: Optional[str]
    name_r: Optional[str]
    authors: List[Author]
    circles: List[Circle]
    parodies: List[Parody]
    characters: List[Character]
    contents: List[Content]
    date_released: date
    event: Convention
    image: str
    url: str
    pages: int
    nsfw: bool
    anthology: bool
    copyshi: bool
    magazine: bool
    isbn: Optional[int]
    language: Language
    similarity: Optional[float]
