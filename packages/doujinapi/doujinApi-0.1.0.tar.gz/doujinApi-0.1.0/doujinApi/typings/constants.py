from enum import Enum


class Frequency(Enum):
    NOT_SET = 0
    VERY_FEW = 1
    SOME = 2
    MANY = 3
    MOST = 4
    ALL = 5


class FrequencyAuthorAndCircle(Enum):
    NOT_SET = 0
    GUEST = 1
    MAIN = 2


class Code(Enum):
    BOOK = "B"
    CIRCLE = "C"
    AUTHOR = "A"
    PARODY = "P"
    CHARACTER = "H"
    CONVENTION = "N"
    COLLECTIONS = "O"
    CONTENT = "K"
    GENRE = "G"
    TYPE = "T"
    PUBLISHER = "L"
    IMPRINT = "I"


class Language(Enum):
    UNKNOWN = 1
    ENGLISH = 2
    JAPANESE = 3
    CHINESE = 4
    KOREAN = 5
    FRENCH = 6
    GERMAN = 7
    SPANISH = 8
    ITALIAN = 9
    RUSSIAN = 10


class Sex(Enum):
    UNKNOWN = 0
    MALE = 1
    FEMALE = 2
    OTHER = 3
