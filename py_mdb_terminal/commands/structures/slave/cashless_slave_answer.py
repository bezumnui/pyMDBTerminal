import dataclasses
from py_mdb_terminal.commands.structures.cashless_answer import CashlessAnswer, answer_prefix


@answer_prefix("c,ERR")
class CashlessError(CashlessAnswer):
    CashlessIsOn = "\"cashless is on\""
    PeripheralDisabled = "\"START -3\""
    DeniedOnCycle = "-3"
    VendingCancelled = "VEND 1"
    VendingFailed = "VEND 3"
    GotReset = "VEND 5"
    InvalidPayload = "\"VEND -2\""
    WrongState = "\"VEND -3\""

@answer_prefix("c,UNKNOWN")
class CashlessUnknown(CashlessAnswer):
    BadCommand = "\" C\""

@answer_prefix("c,VEND")
class CashlessVend(CashlessAnswer):
    Success = "SUCCESS"

@dataclasses.dataclass
class CashlessSlaveWaitingPayment:
    price: int
    item_number: int

@answer_prefix("c,STATUS")
class CashlessStatus(CashlessAnswer):
    Inactive = "INACTIVE"
    Disabled = "DISABLED"
    enabled = "ENABLED"
    idle = "IDLE"
    SessionStartedIdle = "IDLE,"
    WaitingPayment = "VEND,{price},{item_number}"

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

def match_cashless_slave_answer_message(text: str) -> CashlessAnswer | None:
    enums = (CashlessError, CashlessUnknown, CashlessVend, CashlessStatus)
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
    print(CashlessStatus.get_waiting_payment("c,STATUS,VEND,500,0"))
