from doujinApi.book.methods import SearchBookMethods
from doujinApi.item.methods import SearchItemMethods


class DoujinApi(SearchItemMethods, SearchBookMethods):
    def __init__(self, apiKey: str) -> None:
        SearchItemMethods.__init__(self, apiKey)
        SearchBookMethods.__init__(self, apiKey)
