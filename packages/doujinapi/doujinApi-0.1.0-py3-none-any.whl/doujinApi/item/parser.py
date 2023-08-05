import xml.etree.ElementTree as etree
from typing import List

from doujinApi.typings.tag import Author, Character, Circle, Content, Convention, Parody
from doujinApi.utils.parser import (
    parseAuthor,
    parseCharacter,
    parseCircle,
    parseContent,
    parseConvention,
    parseParody,
)


def parseCharacters(response: etree.Element) -> List[Character]:
    return [
        parseCharacter(child)
        for child in response
        if child.tag == "ITEM" and child.attrib["TYPE"] == "character"
    ]


def parseAuthors(response: etree.Element) -> List[Author]:
    return [
        parseAuthor(child)
        for child in response
        if child.tag == "ITEM" and child.attrib["TYPE"] == "author"
    ]


def parseCircles(response: etree.Element) -> List[Circle]:
    return [
        parseCircle(child)
        for child in response
        if child.tag == "ITEM" and child.attrib["TYPE"] == "circle"
    ]


def parseContents(response: etree.Element) -> List[Content]:
    return [
        parseContent(child)
        for child in response
        if child.tag == "ITEM" and child.attrib["TYPE"] == "contents"
    ]


def parseEvents(response: etree.Element) -> List[Convention]:
    return [
        parseConvention(child)
        for child in response
        if child.tag == "ITEM" and child.attrib["TYPE"] == "convention"
    ]


def parseParodies(response: etree.Element) -> List[Parody]:
    return [
        parseParody(child)
        for child in response
        if child.tag == "ITEM" and child.attrib["TYPE"] == "parody"
    ]
