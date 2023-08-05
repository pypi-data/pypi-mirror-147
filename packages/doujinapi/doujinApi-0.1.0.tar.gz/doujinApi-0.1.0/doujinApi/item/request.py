from __future__ import annotations

import datetime
from typing import Literal, TypedDict

from doujinApi.item.constants import ItemTypes, SortOrders, SortTypes


class SearchItemRequest(TypedDict, total=False):
    """
    アイテムを検索する際使用するリクエスト

    Attributes
    ----------
    sn: str
        検索キーワード
    S : str
        検索種別(itemSearch固定)
    T : str
        検索対象(circle, author等)
    order: Optional[str]
        ソート方法(title, title_j, date等)
    flow: Optional[str]
        ソート方向(ASC, DESC)
    date: Optional[datetime.date]
        (任意)登録された日付
    cont: Optional[str]
        (任意)投稿者
    page: Optional[int]
        ページ番号(デフォルト1)
    """

    sn: str
    S: Literal["itemSearch"]
    T: ItemTypes
    order: SortTypes
    flow: SortOrders
    date: datetime.date
    cont: str
    page: int
