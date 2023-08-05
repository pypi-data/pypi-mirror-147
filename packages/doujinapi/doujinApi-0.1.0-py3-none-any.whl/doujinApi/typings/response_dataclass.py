from dataclasses import dataclass, field
from typing import Any, List, Optional, Union

from dataclasses_json import config, dataclass_json
from doujinApi.typings.constants import Language

"""
This file is work-in-progress for using dataclasses to parse XML response
Currently unused but it will be used later.
"""


@dataclass_json
@dataclass
class User:
    user_id: str = field(metadata=config(field_name="@id"))
    user_name: str = field(metadata=config(field_name="User"))
    search_queries_left: int = field(metadata=config(field_name="Queries"))
    image_queries_left: int = field(metadata=config(field_name="Image_Queries"))


@dataclass_json
@dataclass
class Book:
    book_id: str = field(metadata=config(field_name="@id"))
    name_jp: str
    name_en: Optional[str]
    name_r: Optional[str]
    authors: List[Any]
    circles: List[Any]
    parodies: List[Any]
    characters: List[Any]
    contents: List[Any]
    date_released: Any
    event: Any
    image: str
    url: str
    pages: int
    nsfw: bool
    anthology: bool
    copyshi: bool
    magazine: bool
    isbn: Optional[int]
    language: Language


@dataclass_json
@dataclass
class Error:
    code: int = field(metadata=config(field_name="CODE"))
    message_short: str = field(metadata=config(field_name="TYPE"))
    message_long: str = field(metadata=config(field_name="EXACT"))


@dataclass_json
@dataclass
class Item:
    id: str


@dataclass_json
@dataclass
class Response:
    data: List[Union[Error, User, Book, Item]] = field(
        metadata=config(field_name="LIST")
    )
