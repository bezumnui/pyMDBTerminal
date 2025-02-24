from py_mdb_terminal.commands.structures.cashless_answer import answer_prefix, CashlessAnswer


@answer_prefix("d,ERR")
class CashlessMasterError(CashlessAnswer):
    # D,ERR,"cashless master is on"	Master instance was already ON
    InstanceAlreadyOn = "\"cashless master is on\" "
    # d,ERR,-1	Command not applicable in current state
    CommandNotApplicable = "-1"


@answer_prefix("d,STATUS")
class CashlessMasterStatus(CashlessAnswer):
    # d,STATUS,RESET	Master/VMC instance was initialized and there are no peripherals connected to it
    Reset = "RESET"
    # d,STATUS,INIT,1	There is a peripheral on the bus and the master instance is polling it
    Initialized = "INIT,1"
    # d,STATUS,IDLE    There is a peripheral on the bus and the master instance is idle
    Idle = "IDLE"
    # d,STATUS,CREDIT,-1	The peripheral has started the session and a payment method with has been inserted
    Credit = "CREDIT,-1"
    # d,STATUS,RESULT,-1	The terminal has denied the vending session. E.g. due to lack of funds in the credit card.
    Result = "RESULT,-1"
    # d,STATUS,VEND	A vending request has been made by the master instance and it is waiting for the slave to accept it
    Vending = "VEND"
    # d,STATUS,RESULT,1,1.50    The terminal has accepted the vending session and the amount of 1.50 has been deducted from the credit card
    ResultAmount = "RESULT,1,{amount}"

    @classmethod
    def match_message(cls, text: str):
        match = super().match_message(text)
        text = text.lower()
        if not match:
            if text.startswith("d,RESULT,1") and text.count(",") == 4:
                return cls.ResultAmount
        return match


def match_cashless_master_answer_message(text: str) -> CashlessAnswer | None:
    enums = (CashlessMasterError, CashlessMasterStatus)
    for answer in enums:
        if result := answer.match_message(text):
            return result
    return None

