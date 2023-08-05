from typing import List

from doujinApi.item.constants import (
    ItemType,
    SortOrder,
    SortOrders,
    SortType,
    SortTypes,
)
from doujinApi.item.parser import (
    parseAuthors,
    parseCharacters,
    parseCircles,
    parseContents,
    parseParodies,
)
from doujinApi.item.request import SearchItemRequest
from doujinApi.typings.tag import Author, Character, Circle, Content, Parody
from doujinApi.utils.session import Session


class SearchItemMethods(Session):
    def __init__(self, apiKey: str) -> None:
        Session.__init__(self, apiKey)

    async def searchCharacterByName(
        self,
        keyword: str,
        sort: SortTypes = SortType.TITLE,
        order: SortOrders = SortOrder.DESC,
    ) -> List[Character]:
        objType = ItemType.CHARACTER
        req = SearchItemRequest(
            S="itemSearch",
            sn=keyword,
            T=objType.value,
            order=sort.value,
            flow=order.value,
        )
        resp = await self.get(req)
        return parseCharacters(resp)

    async def searchParodyByName(
        self,
        keyword: str,
        sort: SortTypes = SortType.TITLE,
        order: SortOrders = SortOrder.DESC,
        page: int = 1,
    ) -> List[Parody]:
        objType = ItemType.PARODY
        req = SearchItemRequest(
            S="itemSearch",
            sn=keyword,
            T=objType.value,
            order=sort.value,
            flow=order.value,
            page=page,
        )
        resp = await self.get(req)
        return parseParodies(resp)

    async def searchAuthorByName(
        self,
        keyword: str,
        sort: SortTypes = SortType.TITLE,
        order: SortOrders = SortOrder.DESC,
        page: int = 1,
    ) -> List[Author]:
        objType = ItemType.AUTHOR
        req = SearchItemRequest(
            S="itemSearch",
            sn=keyword,
            T=objType.value,
            order=sort.value,
            flow=order.value,
            page=page,
        )
        resp = await self.get(req)
        return parseAuthors(resp)

    async def searchCircleByName(
        self,
        keyword: str,
        sort: SortTypes = SortType.TITLE,
        order: SortOrders = SortOrder.DESC,
        page: int = 1,
    ) -> List[Circle]:
        objType = ItemType.CIRCLE
        req = SearchItemRequest(
            S="itemSearch",
            sn=keyword,
            T=objType.value,
            order=sort.value,
            flow=order.value,
            page=page,
        )
        resp = await self.get(req)
        return parseCircles(resp)

    async def searchTagByName(
        self,
        keyword: str,
        sort: SortTypes = SortType.TITLE,
        order: SortOrders = SortOrder.DESC,
        page: int = 1,
    ) -> List[Content]:
        objType = ItemType.CONTENT
        req = SearchItemRequest(
            S="itemSearch",
            sn=keyword,
            T=objType.value,
            order=sort.value,
            flow=order.value,
            page=page,
        )
        resp = await self.get(req)
        return parseContents(resp)
