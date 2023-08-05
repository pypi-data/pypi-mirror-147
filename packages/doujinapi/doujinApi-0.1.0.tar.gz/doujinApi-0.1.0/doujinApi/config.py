class DoujinApiConfig:
    ENDPOINT = "https://www.doujinshi.org/api/"
    OLD_ENDPOINT = "http://doujinshi.mugimugi.org/api/"
    API_KEY = ""

    def __init__(self, apiKey: str) -> None:
        self.API_KEY = apiKey
