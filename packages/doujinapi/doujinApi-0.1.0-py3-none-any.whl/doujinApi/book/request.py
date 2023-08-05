from __future__ import annotations

from typing import Literal, TypedDict

from doujinApi.typings.constants import Code


class SearchBookRequest(TypedDict, total=False):
    S: Literal["objectSearch"]
    sn: str
    slist: str
    page: int


class SearchBookRequestFilterParams(TypedDict, total=False):
    B: str
    C: str
    A: str
    P: str
    H: str
    N: str
    O: str
    K: str
    G: str
    T: str
    L: str
    I: str


class SearchBookRequestFilter:
    def __init__(self) -> None:
        self.PARAMS = SearchBookRequestFilterParams()

    def event(self, eventName: str) -> SearchBookRequestFilter:
        """
        実施されたイベント名で絞り込みます

        Parameters
        ----------
        eventName: str
            イベント名

        Returns
        -------
        self
            メソッドチェーン用
        """
        self.PARAMS[Code.CONVENTION.value] = eventName  # type: ignore
        return self

    def series(self, seriesName: str) -> SearchBookRequestFilter:
        """
        作品のシリーズ名で絞り込みます

        Parameters
        ----------
        seriesName: str
            シリーズ名

        Returns
        -------
        self
            メソッドチェーン用
        """
        self.PARAMS[Code.COLLECTIONS.value] = seriesName  # type: ignore
        return self

    def parody(self, parodyName: str) -> SearchBookRequestFilter:
        """
        作品の原作名で絞り込みます

        Parameters
        ----------
        parodyName: str
            原作名

        Returns
        -------
        self
            メソッドチェーン用
        """
        self.PARAMS[Code.PARODY.value] = parodyName  # type: ignore
        return self

    def genre(self, genreName: str) -> SearchBookRequestFilter:
        """
        作品のジャンルで絞り込みます

        Parameters
        ----------
        genreName: str
            ジャンル名

        Returns
        -------
        self
            メソッドチェーン用
        """
        self.PARAMS[Code.GENRE.value] = genreName  # type: ignore
        return self

    def author(self, authorName: str) -> SearchBookRequestFilter:
        """
        作品の発行絵師名で絞り込みます

        Parameters
        ----------
        authorName: str
            発行絵師名

        Returns
        -------
        self
            メソッドチェーン用
        """
        self.PARAMS[Code.AUTHOR.value] = authorName  # type: ignore
        return self

    def circle(self, circleName: str) -> SearchBookRequestFilter:
        """
        作品の発行サークル名で絞り込みます

        Parameters
        ----------
        circleName: str
            発行サークル名

        Returns
        -------
        self
            メソッドチェーン用
        """
        self.PARAMS[Code.CIRCLE.value] = circleName  # type: ignore
        return self

    def imprint(self, labelName: str) -> SearchBookRequestFilter:
        self.PARAMS[Code.IMPRINT.value] = labelName  # type: ignore
        return self

    def character(self, characterName: str) -> SearchBookRequestFilter:
        """
        作品に登場するキャラクター名で絞り込みます

        Parameters
        ----------
        characterName: str
            キャラクター名

        Returns
        -------
        self
            メソッドチェーン用
        """
        self.PARAMS[Code.CHARACTER.value] = characterName  # type: ignore
        return self

    def publisher(self, publisherName: str) -> SearchBookRequestFilter:
        """
        作品の発行社名で絞り込みます

        Parameters
        ----------
        publisherName: str
            発行サークル名

        Returns
        -------
        self
            メソッドチェーン用
        """
        self.PARAMS[Code.PUBLISHER.value] = publisherName  # type: ignore
        return self

    def tag(self, tagName: str) -> SearchBookRequestFilter:
        """
        作品のタグで絞り込みます

        Parameters
        ----------
        tagName: str
            タグ名称

        Returns
        -------
        self
            メソッドチェーン用
        """
        self.PARAMS[Code.CONTENT.value] = tagName  # type: ignore
        return self

    def __str__(self) -> str:
        resp = "|".join(
            [f"{k}:{self.PARAMS[k]}" for k in self.PARAMS.keys()]  # type: ignore
        )
        return resp
