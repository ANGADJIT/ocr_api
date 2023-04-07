from enum import Enum


class TextType(Enum):
    NUMBER = 'NUMBER'
    PLAIN_TEXT = 'PLAIN_TEXT'
    EMAIL = 'EMAIL'
    URL = 'URL'

    def __str__(self) -> str:
        return self.value
