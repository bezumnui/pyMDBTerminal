from abc import ABC
from typing import Annotated

from pyOpticwash.py_mdb_terminal.abstract.abc_client import ABCMDBClient
from pyOpticwash.py_mdb_terminal.comamnds.structures.annotations import MaxLen
from pyOpticwash.py_mdb_terminal.comamnds.structures.cashless_slave_answer import match_cashless_slave_answer_message


class CommandsCashlessSlave(ABCMDBClient, ABC):

    def start_session(self, amount: int):
        """
        If the VMC does not support always idle vend, the vending session has to be started by the peripheral .
        If the cashless Master (VMC) has not activated the peripheral yet, this command will throw an error.

        :param amount:
        """
        return self.__send_message_and_handle_result(f"C,START,{amount}".encode(self.get_encoding()))

    def approve_vending_request(self, amount: int):
        """
        After this command, the VMC must finish the vend cycle and the cashless peripheral
        will go back to IDLE (waiting for session start)

        :param amount:
        """
        return self.__send_message_and_handle_result(f"C,VEND,{amount}".encode(self.get_encoding()))

    def stop_inactive_vend_session(self):
        """
        An Inactive Vend Session means that it was initiated by the Peripheral (only occurs
        in Idle/Authorization First mode) but was not followed up by the VMC,
        meaning that the credit was still not requested from the Cashless Peripheral.
        """
        return self.__send_message_and_handle_result(b"C,STOP")

    def stop_active_vend_session(self):
        """
        (Deny Credit Request)
        An active vend session means that the Credit has already been requested by the Master, but not confirmed by the peripheral.
        """
        return self.__send_message_and_handle_result(b"C,VEND,-1")

    def accept_revalue(self):
        """
        In certain situations, the VMC might send a Revalue request to the peripheral.
        This can be triggered for whatever reason that may need the VMC to restore some
        funds to the card (like charging pre-paid cards with physical money).
        Once the Revalue is requested to the Cashless Peripheral,
        the VMC expects only an Accept or a Deny response.
        """
        return self.__send_message_and_handle_result(b"C,REVALUE,1")

    def deny_revalue(self):
       return  self.__send_message_and_handle_result(b"C,REVALUE,0")

    def display_message(self, text: Annotated[str, MaxLen(32)]):
        """
        Some vending machines, allow connected Cashless Devices to send display requests to them, in
        response to polling. When this happens, it is possible to use the Cashless Terminal API to send a
        display request, if the cashless is in the Enabled state. To send a display request to the vending
        machine, the following command must be issued in the console
        :param text:
        """
        assert len(text) <= 32
        return self.send_raw_message(f"C,DISPLAY,{text}".encode(self.get_encoding()))

    def report_cash_sale(self, value: float, product_id: int):
        value = "{0:.2f}".format(value)
        return self.send_raw_message(f"C,SALE,{value},{product_id}".encode(self.get_encoding()))

    def __send_message_and_handle_result(self, data: bytes):
        res = self.send_raw_message_with_response(data)
        answer = match_cashless_slave_answer_message(res)
        return answer, res
