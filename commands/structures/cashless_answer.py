from enum import Enum
from typing import Type


def answer_prefix(text: str):
    def deco(cls: Type[object]):
        setattr(cls, "__PREFIX", text)
        return cls
    return deco

@answer_prefix(",UNKNOWN")
class CashlessAnswer(Enum):

    @classmethod
    def match_message(cls, text: str):
        prefix: str = getattr(cls, "__PREFIX")
        text = text.lower()
        if not text.startswith(prefix.lower()):
            return None
        text_array = text.split(",", maxsplit=2)
        if len(text_array) < 3:
            return None
        text = text_array[2]
        for _, instance in cls.__members__.items():
            if instance.value.lower() == text[:-2]:
                return instance
        return None