from enum import Enum


class CharacterType(Enum):
    ALPHA = "alpha"
    NUMERIC = "numeric"
    NON_ALPHANUMERIC = "non-alphanumeric"
    END_OF_FILE = "end-of-file"