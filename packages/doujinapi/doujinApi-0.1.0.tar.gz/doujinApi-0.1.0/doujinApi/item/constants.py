from enum import Enum
from typing import Literal


class SortOrder(Enum):
    ASC = "asc"
    DESC = "desc"


SortOrders = Literal[
    SortOrder.ASC,
    SortOrder.DESC,
]


class ItemType(Enum):
    CIRCLE = "circle"
    AUTHOR = "author"
    PARODY = "parody"
    CHARACTER = "character"
    CONTENT = "contents"
    GENRE = "genre"
    CONVENTION = "convention"
    COLLECTION = "collections"
    PUBLISHER = "publisher"
    IMPRINT = "imprint"


ItemTypes = Literal[
    ItemType.CIRCLE,
    ItemType.AUTHOR,
    ItemType.PARODY,
    ItemType.CHARACTER,
    ItemType.CONTENT,
    ItemType.GENRE,
    ItemType.CONVENTION,
    ItemType.COLLECTION,
    ItemType.PUBLISHER,
    ItemType.IMPRINT,
]


class SortType(Enum):
    TITLE = "title"
    TITLE_J = "jtitle"
    DATE = "date"
    ADDED = "added"
    UPDATED = "changed"
    PAGES = "pages"
    VIEWS = "pages_views"
    SCORE = "score"


SortTypes = Literal[
    SortType.TITLE,
    SortType.TITLE_J,
    SortType.DATE,
    SortType.ADDED,
    SortType.UPDATED,
    SortType.PAGES,
    SortType.VIEWS,
    SortType.SCORE,
]
