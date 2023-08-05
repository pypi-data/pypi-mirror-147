import xml.etree.ElementTree as etree
from typing import Dict, Union

from doujinApi.book.request import SearchBookRequest
from doujinApi.item.request import SearchItemRequest
from doujinApi.utils.exception import UnauthorizedException
from httpx import AsyncClient


class Session(object):
    ENDPOINT = "https://www.doujinshi.org/api"
    API_KEY = ""

    def __init__(self, apiKey: str) -> None:
        self.API_KEY = apiKey

    async def get(
        self, params: Union[SearchBookRequest, SearchItemRequest]
    ) -> etree.Element:
        async with AsyncClient() as client:
            params_dict: dict = params  # type: ignore
            resp = await client.get(
                f"{self.ENDPOINT}/{self.API_KEY}/", params=params_dict
            )
            tree = etree.fromstring(resp.text.encode("utf-8"))
            for child in tree:
                if child.tag == "ERROR":
                    if child.attrib["code"] == "1":
                        raise UnauthorizedException("Wrong API Key")
            return tree

    async def postImage(self, files: Dict[str, bytes]) -> etree.Element:
        async with AsyncClient() as client:
            resp = await client.post(
                f"{self.ENDPOINT}/{self.API_KEY}/",
                params={"S": "imageSearch"},
                files=files,
            )
            tree = etree.fromstring(resp.text.encode("utf-8"))
            for child in tree:
                if child.tag == "ERROR":
                    if child.attrib["code"] == "1":
                        raise UnauthorizedException("Wrong API Key")
            return tree
