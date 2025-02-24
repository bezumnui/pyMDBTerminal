from abc import ABC

from py_mdb_terminal.abstract.abc_client import ABCMDBClient
from py_mdb_terminal.commands.structures.annotations import ValueRange
from py_mdb_terminal.commands.structures.master.cashless_master_parameter import CashlessMasterParameter
from py_mdb_terminal.commands.structures.slave.cashless_slave_parameter import CashlessSlaveParameter


class CommandsConfiguration(ABCMDBClient, ABC):
    """
    Find the documentation there:\n
    https://docs.qibixx.com/mdb-products/api-configuration
    """
    def set_rs232_baundrate(self, baundrate: int = 0):
        """
        Sets the serial port (RS232) Baud rate. Default (0) means serial port disabled.
        The serial port uses the exact same command set which is used on the USB port.
        :param baundrate:
        """
        return self.send_raw_message_with_response(f"F,SERIAL,{baundrate}".encode(self.get_encoding()))

    def set_response_timout(self, timeout: ValueRange(10, 1000) = 1000):
        """
        While in master mode, the MDB interface, will wait this amount of time,
        before it assumes the peripheral does not answer the POLLS and therefore,
        is disconnected. This value, by standard, will be 5ms, but many "modern"
        Peripherals are much slower. The timeout value can be configured in a range from 10 to 1000.

        If you have problems with a peripheral, try to set the value to 1000.
        :param timeout:
        """
        return self.send_raw_message_with_response(f"F,RESPTIMEOUT,{timeout}".encode(self.get_encoding()))

    def disable_cashless_slave_mode(self):
        """
        Once the Cashless Slave is disabled, configurations can be modified by ``set_cashless_slave_parameter``.
        """
        return self.send_raw_message_with_response(b"C,0")

    def enable_cashless_slave_mode(self):
        """
        Once the Cashless Slave is disabled, configurations can be modified by ``set_cashless_slave_parameter``.
        """
        return self.send_raw_message_with_response(b"C,1")

    def set_cashless_slave_parameter(self, parameter: CashlessSlaveParameter, value: str):
        """
        The parameters must be set every time that the interface is powered on.
        :param parameter:
        :param value: check with https://docs.qibixx.com/mdb-products/api-configuration#set-cashless-master-parameter
        """
        return self.send_raw_message_with_response(f"C,SETCONF,{parameter.value}={value}".encode(self.get_encoding()))


    def set_cashless_master_parameter(self, parameter: CashlessMasterParameter, value: str):
        return self.send_raw_message_with_response(f"D,SETCONF,{parameter.value}={value}".encode(self.get_encoding()))


