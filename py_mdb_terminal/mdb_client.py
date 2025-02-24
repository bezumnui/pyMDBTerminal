import logging
import os.path
from asyncio import QueueEmpty

import serial
from serial.serialutil import PARITY_NONE

from py_mdb_terminal.abstract.abc_client import ABCMDBClient
from py_mdb_terminal.commands.commands_commutator import CommandsCommutator
from py_mdb_terminal.commands.structures.master.cashless_master_parameter import CashlessMasterParameter
from py_mdb_terminal.mdb_listener import MDBListener


class MDBClient(CommandsCommutator, ABCMDBClient):
    BAUNDRATE = 115200
    DATABITS = 8
    STOPBITS = 1
    PARITY = PARITY_NONE

    def __init__(self, port: str = "/dev/ttyACM0"):
        super().__init__()
        self.listener = MDBListener(self)
        self.port = port
        self.ser = serial.Serial(None, self.BAUNDRATE, self.DATABITS, self.PARITY, self.STOPBITS)
        self.ser.port = port
        self.running = False
        self.encoding = "ascii"
        self.software_version: str = ""

    def check_port_availability(self):
        return os.path.exists(self.port)

    def start(self):
        """
       :raises SerialException if the port cannot be opened.\
       :raises ValueError if the serial is already opened.
       """
        if self.running:
            raise ValueError("The serial is already opened.")
        self.running = True
        self.ser.open()
        self.listener.start()
        self.software_version = self.get_version().software_version


    def stop(self, block=True):
        """
        :param block: should block the thread on listen thread stop.\
        :raises ValueError if the serial is not in use.
        """
        if not self.running:
            raise ValueError("The serial is not in use.")
        self.listener.stop(block=block)
        self.ser.close()

    def send_raw_message_with_response(self, message: bytes) -> str:
        """
        :param message:\
        :raises PortNotOpenError the client is not started.
        """
        self.listener.lock_queue()
        self.send_raw_message(message)
        try:
            return self.listener.get_last_message(5)
        except QueueEmpty as e:
            raise TimeoutError("Failed to receive a response from the MDB device") from e

    def send_raw_message(self, message: bytes):
        """
        :param message:\
        :raises PortNotOpenError the client is not started.
        """
        self.ser.write(message + b"\n")
        self.ser.flush()

    def get_software_version(self) -> str:
        return self.software_version

    def get_encoding(self):
        return self.encoding

    def get_serial(self):
        return self.ser


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    client = MDBClient("/dev/tty.usbmodem01")
    if not client.check_port_availability():
        print("Port is not available.")
        exit(1)

    logging.info(f"Port {client.port} is available. Starting the client.")
    client.start()
    logging.info(f"Connection PC-MDB established. Software version: {client.software_version}")
    logging.info("Requesting the HW version...")

    hw = client.get_hardware_info()
    logging.info(f"SW: {client.software_version}, HW: {hw.hardware_version}")

    client.set_response_timout(1000)
    client.set_cashless_master_parameter(CashlessMasterParameter.VMCSlaveAddress, "0x10")
    initialize_answer, initialize_response = client.master_enable_always_idle()
    # if initialize_answer != CashlessMasterStatus.Initialized:
    #     logging.error(f"Failed to initialize the device. Response: {initialize_answer}")
    #
    #     exit(1)

    client.master_request_credit(10, 1)
    # input("Press enter to stop the client\n")
    input("Press enter to stop the client\n")
    client.master_disable()
    logging.info("Stopping the client.")

    client.stop()
