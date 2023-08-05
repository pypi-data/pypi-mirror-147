import xml.etree.ElementTree as etree
from datetime import date, datetime
from typing import List, Optional, cast

from doujinApi.typings.constants import Language, Sex


def findAndCastOptionalStr(elem: etree.Element, tag: str) -> Optional[str]:
    text = findAndCastStr(elem, tag)
    return text if text != "None" else None


def findAndCastOptionalInt(elem: etree.Element, tag: str) -> Optional[int]:
    text = findAndCastStr(elem, tag)
    return findAndCastInt(elem, tag) if text != "None" else None


def findAndCastStr(elem: etree.Element, field: str) -> str:
    return str(cast(etree.Element, elem.find(field)).text)


def findAndCastInt(elem: etree.Element, field: str) -> int:
    return int(findAndCastStr(elem, field))


def findAndCastBool(elem: etree.Element, field: str) -> bool:
    return bool(findAndCastInt(elem, field))


def findAndCastDate(elem: etree.Element, field: str) -> date:
    date_str = findAndCastStr(elem, field)
    if date_str == "0000-00-00":
        return date.min
    return datetime.strptime(findAndCastStr(elem, field), "%Y-%m-%d").date()


def findAndCastElementArray(elem: etree.Element, field: str) -> List[etree.Element]:
    return cast(List[etree.Element], elem.find(field))


def findAndCastOptionalSex(elem: etree.Element, field: str) -> Optional[Sex]:
    text = findAndCastStr(elem, field)
    return Sex(findAndCastInt(elem, field)) if text != "None" else None


def findAndCastLanguage(elem: etree.Element, field: str) -> Language:
    return Language(findAndCastInt(elem, field))
