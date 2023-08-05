import xml.etree.ElementTree as etree
from typing import List, Optional

from doujinApi.typings.cast import (
    findAndCastDate,
    findAndCastInt,
    findAndCastOptionalSex,
    findAndCastOptionalStr,
    findAndCastStr,
)
from doujinApi.typings.tag import Author, Character, Circle, Content, Convention, Parody


def filteredTags(tags: List[etree.Element], key: str) -> List[etree.Element]:
    return [tag for tag in tags if tag.attrib["TYPE"] == key]


def parseCircle(elem: etree.Element) -> Circle:
    tags = elem.findall("ITEM")
    return Circle(
        id=elem.attrib["ID"],
        name_jp=findAndCastStr(elem, "NAME_JP"),
        name_en=findAndCastOptionalStr(elem, "NAME_EN"),
        name_r=findAndCastStr(elem, "NAME_R"),
        name_alt=[str(t.text) for t in elem.findall("NAME_ALT")],
        count=findAndCastInt(elem, "OBJECTS"),
        authors=[parseAuthor(t) for t in filteredTags(tags, "author")],
    )


def parseAuthor(elem: etree.Element) -> Author:
    return Author(
        id=elem.attrib["ID"],
        name_jp=findAndCastStr(elem, "NAME_JP"),
        name_en=findAndCastOptionalStr(elem, "NAME_EN"),
        name_r=findAndCastStr(elem, "NAME_R"),
        name_alt=[str(t.text) for t in elem.findall("NAME_ALT")],
        count=findAndCastInt(elem, "OBJECTS"),
    )


def parseAge(age: Optional[str]) -> Optional[int]:
    """because of this api sometimes returns '13-14' as age..."""
    if age is None:
        return None
    if "-" in age:
        return int(age.split("-")[1])
    return int(age)


def parseCharacter(elem: etree.Element) -> Character:
    tags = elem.findall("ITEM")
    return Character(
        id=elem.attrib["ID"],
        name_jp=findAndCastStr(elem, "NAME_JP"),
        name_en=findAndCastOptionalStr(elem, "NAME_EN"),
        name_r=findAndCastStr(elem, "NAME_R"),
        name_alt=[str(t.text) for t in elem.findall("NAME_ALT")],
        count=findAndCastInt(elem, "OBJECTS"),
        sex=findAndCastOptionalSex(elem, "DATA_SEX"),
        age=parseAge(findAndCastOptionalStr(elem, "DATA_AGE")),
        contents=[parseContent(t) for t in filteredTags(tags, "contents")],
    )


def parseParody(elem: etree.Element) -> Parody:
    tags = elem.findall("ITEM")
    return Parody(
        id=elem.attrib["ID"],
        name_jp=findAndCastStr(elem, "NAME_JP"),
        name_en=findAndCastOptionalStr(elem, "NAME_EN"),
        name_r=findAndCastStr(elem, "NAME_R"),
        name_alt=[str(t.text) for t in elem.findall("NAME_ALT")],
        count=findAndCastInt(elem, "OBJECTS"),
        contents=[parseContent(t) for t in filteredTags(tags, "contents")],
        characters=[parseCharacter(t) for t in filteredTags(tags, "character")],
    )


def parseContent(elem: etree.Element) -> Content:
    return Content(
        id=elem.attrib["ID"],
        name_jp=findAndCastStr(elem, "NAME_JP"),
        name_en=findAndCastOptionalStr(elem, "NAME_EN"),
        name_r=findAndCastStr(elem, "NAME_R"),
        name_alt=[str(t.text) for t in elem.findall("NAME_ALT")],
        count=findAndCastInt(elem, "OBJECTS"),
    )


def parseConvention(elem: etree.Element) -> Convention:
    return Convention(
        id=elem.attrib["ID"],
        name_jp=findAndCastStr(elem, "NAME_JP"),
        name_en=findAndCastOptionalStr(elem, "NAME_EN"),
        name_r=findAndCastStr(elem, "NAME_R"),
        name_alt=[str(t.text) for t in elem.findall("NAME_ALT")],
        count=findAndCastInt(elem, "OBJECTS"),
        date_start=findAndCastDate(elem, "DATE_START"),
        date_end=findAndCastDate(elem, "DATE_END"),
    )
