import xml.etree.ElementTree as etree
from typing import List, Optional

from doujinApi.book.response import Book
from doujinApi.typings.cast import (
    findAndCastBool,
    findAndCastDate,
    findAndCastElementArray,
    findAndCastInt,
    findAndCastLanguage,
    findAndCastOptionalInt,
    findAndCastOptionalStr,
    findAndCastStr,
)
from doujinApi.utils.parser import (
    filteredTags,
    parseAuthor,
    parseCharacter,
    parseCircle,
    parseContent,
    parseConvention,
    parseParody,
)


def parseBookAsFilename(book: Book) -> str:
    """parse book response model as common filename"""
    event_dict = {
        "コミックマーケット": "C",
        "サンシャインクリエイション": "サンクリ",
        "こみっく☆トレジャー": "こみトレ",
    }
    event = book.event.name_jp.replace(" ", "")
    for k, v in event_dict.items():
        event = event.replace(k, v)
    circle = book.circles[0].name_jp
    authors = ", ".join([a.name_jp for a in book.authors])
    title = book.name_jp
    parody = book.parodies[0].name_jp
    parody = "" if parody == "不詳" else parody
    event = "" if event == "不詳" else event
    if not event and not parody:
        return f"[{circle} ({authors})] {title}"
    if not event:
        return f"[{circle} ({authors})] {title} ({parody})"
    return f"({event}) [{circle} ({authors})] {title} ({parody})"


def parseSimilarity(similarity: Optional[str]) -> Optional[float]:
    if similarity is None:
        return None
    return float(similarity.replace("%", "").replace(",", "."))


def parseBook(elem: etree.Element) -> Book:
    tags = findAndCastElementArray(elem, "LINKS")
    id = int(elem.attrib["ID"][1:])
    similarity = elem.attrib["search"] if "search" in elem.attrib else None
    return Book(
        id=elem.attrib["ID"],
        similarity=parseSimilarity(similarity),
        name_jp=findAndCastStr(elem, "NAME_JP"),
        name_en=findAndCastOptionalStr(elem, "NAME_EN"),
        name_r=findAndCastOptionalStr(elem, "NAME_R"),
        circles=[parseCircle(tag) for tag in filteredTags(tags, "circle")],
        authors=[parseAuthor(tag) for tag in filteredTags(tags, "author")],
        characters=[parseCharacter(tag) for tag in filteredTags(tags, "character")],
        parodies=[parseParody(tag) for tag in filteredTags(tags, "parody")],
        contents=[parseContent(tag) for tag in filteredTags(tags, "contents")],
        date_released=findAndCastDate(elem, "DATE_RELEASED"),
        isbn=findAndCastOptionalInt(elem, "DATA_ISBN"),
        pages=findAndCastInt(elem, "DATA_PAGES"),
        nsfw=findAndCastBool(elem, "DATA_AGE"),
        anthology=findAndCastBool(elem, "DATA_ANTHOLOGY"),
        language=findAndCastLanguage(elem, "DATA_LANGUAGE"),
        copyshi=findAndCastBool(elem, "DATA_COPYSHI"),
        magazine=findAndCastBool(elem, "DATA_MAGAZINE"),
        event=[parseConvention(tag) for tag in filteredTags(tags, "convention")][0],
        image=f"https://img.doujinshi.org/big/{int(id/2000)}/{id}.jpg",
        url=f"https://www.doujinshi.org/book/{id}",
    )


def parseBooks(response: etree.Element) -> List[Book]:
    return [parseBook(child) for child in response if child.tag == "BOOK"]
