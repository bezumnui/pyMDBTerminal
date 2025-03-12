import logging
from abc import ABC

from py_mdb_terminal.abstract.abc_client import ABCMDBClient
from py_mdb_terminal.commands.structures.master.cashless_master_answer import \
    match_cashless_master_answer_message


class CommandsCashlessMaster(ABCMDBClient, ABC):

    def master_disable(self):
        """
        Prior to initiating transactions with the MDB Bus, it is necessary to Enable the Cashless Master.
         Specifically for Cashless Devices, in addition to "Idle" Mode, it is also possible
         to enable the Device in "Always Idle" Mode.
        """
        return self.__send_message_and_handle_result(f"D,0".encode(self.get_encoding()))

    def master_enable_authorise_first(self):
        """
        "Authorization First" First Mode- Vending sessions are initiated by the Cashless Peripherals
         (Meaning that in a real terminal, the user would first have to swipe his card
          to pre-authorize a certain amount, and then select the product. Further information in Cashless Slave).
        """
        return self.__send_message_and_handle_result(f"D,1".encode(self.get_encoding()))

    def master_enable_always_idle(self):
        """
        "Always Idle"/Selection First Mode (direct vend), the Master can request the credit to the Cashless
        Slave first and therefore it will start the session (In a real terminal, the user would select the
        product first on the machine, and then swipe the card to confirm the requested amount).
        """
        return self.__send_message_and_handle_result(f"D,2".encode(self.get_encoding()))


    def master_start_polling(self):
        """
        Once the Master and Slave are enabled (please see instructions to enable Slave Peripherals in Cashless Slave),
         the master can start polling the Cashless Reader, by issuing the command.
        """
        return self.__send_message_and_handle_result(b"D,READER,1")

    def master_stop_polling(self):
        return self.__send_message_and_handle_result(b"D,READER,0")

    def master_request_credit(self, amount: str, product: str):
        """
        The following command is used to send a request to the Cashless Slave. When the Cashless Master
        is configured in "Idle" Mode, this command should be preceded by a start session command
        (further info in Cashless Slave ). If the Cashless Master is configured in "Always Idle" Mode,
         the instruction below will trigger a "Start" operation on the slave.
        :param amount: is a floating number, e.g. 1.50
        :param product:
        :return:
        """

        # amount = "{0:.2f}".format(amount)
        return self.__send_message_and_handle_result(f"D,REQ,{amount},{product}".encode(self.get_encoding()))


    def master_cancel_pending_request_credit(self):
        """
        This command is used to cancel a pending request to the Cashless Slave.
        """
        return self.__send_message_and_handle_result(b"D,REQ,-1")

    def master_end_transaction(self, product_id: int | None = None):
        """
        **THE product_id PARAMETER WORKS FROM THE VERSION 3.8.0.0** \n
        End transaction with Defined/Undefined Product ID.\
        :return:
        """

        version_supported = self.current_version_is_or_above("3.8.0.0")


        if product_id and version_supported:
            return self.__send_message_and_handle_result(f"D,END,{product_id}".encode(self.get_encoding()))
        if product_id and not version_supported:
            logging.error("Product ID is not supported in this version. Proceeding without it.")
            return self.__send_message_and_handle_result(b"D,END")
        return self.__send_message_and_handle_result(b"D,END")


    def send_raw(self, data: bytes):
        """
        Send a raw command to the Cashless Master
        """
        return self.__send_message_and_handle_result(data)

    def master_end_and_revert_transaction(self):
        """
        Used, for example, if a product was not dispensed
        """
        return self.__send_message_and_handle_result(b"D,END,-1")


    def __send_message_and_handle_result(self, data: bytes):
        res = self.send_raw_message_with_response(data)
        answer = match_cashless_master_answer_message(res)
        logging.debug(f"Got response: {answer}")
        return answer, res
