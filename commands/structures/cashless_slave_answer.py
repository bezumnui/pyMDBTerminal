import dataclasses
from enum import Enum
from typing import Type


def answer_prefix(text: str):
    def deco(cls: Type[object]):
        setattr(cls, "__PREFIX", text)
        return cls
    return deco

@answer_prefix("c,UNKNOWN")
class CashlessSlaveAnswer(Enum):

    @classmethod
    def match_message(cls, text: str):
        prefix: str = getattr(cls, "__PREFIX")
        if not text.startswith(prefix):
            return None
        text_array = text.split(",", maxsplit=2)
        if len(text_array) < 3:
            return None
        text = text_array[2]
        for _, instance in cls.__members__.items():
            if instance.value == text:
                return instance
        return None

@answer_prefix("c,ERR")
class CashlessSlaveError(CashlessSlaveAnswer):
    CashlessIsOn = "\"cashless is on\""
    PeripheralDisabled = "\"START -3\""
    DeniedOnCycle = "-3"
    VendingCancelled = "VEND 1"
    VendingFailed = "VEND 3"
    GotReset = "VEND 5"
    InvalidPayload = "\"VEND -2\""
    WrongState = "\"VEND -3\""

@answer_prefix("c,UNKNOWN")
class CashlessSlaveUnknown(CashlessSlaveAnswer):
    BadCommand = "\" C\""

@answer_prefix("c,VEND")
class CashlessSlaveVend(CashlessSlaveAnswer):
    Success = "SUCCESS"

@dataclasses.dataclass
class CashlessSlaveWaitingPayment:
    price: int
    item_number: int

@answer_prefix("c,STATUS")
class CashlessSlaveStatus(CashlessSlaveAnswer):
    Inactive = "INACTIVE"
    Disabled = "DISABLED"
    enabled = "ENABLED"
    idle = "IDLE"
    SessionStartedIdle = "IDLE,"
    WaitingPayment = "VEND,<price>,<item_number>"

    @classmethod
    def match_message(cls, text: str):
        match = super().match_message(text)
        if not match:
            if text.startswith("c,STATUS,VEND,") and text.count(",") == 4:
                return cls.WaitingPayment
        return match

    @classmethod
    def get_waiting_payment(cls, text: str):
        if cls.match_message(text) == cls.WaitingPayment:
            data_split = text.split(",")
            waiting_payment = CashlessSlaveWaitingPayment(int(data_split[-2]), int(data_split[-1]))
            return waiting_payment
        return None

def match_cashless_slave_answer_message(text: str) -> CashlessSlaveAnswer | None:
    enums = (CashlessSlaveError, CashlessSlaveUnknown, CashlessSlaveVend, CashlessSlaveStatus)
    for answer in enums:
        if result := answer.match_message(text):
            return result
    return None


if __name__ == '__main__':
    print(match_cashless_slave_answer_message("c,ERR,\"cashless is on\""))
    print(match_cashless_slave_answer_message("c,STATUS,DISABLED"))
    print(match_cashless_slave_answer_message("c,STATUS,IDLE"))
    print(match_cashless_slave_answer_message("c,ERR,VEND 5"))
    print(match_cashless_slave_answer_message("c,STATUS,VEND,500,0"))
    print(CashlessSlaveStatus.get_waiting_payment("c,STATUS,VEND,500,0"))
