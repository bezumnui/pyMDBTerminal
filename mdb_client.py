import os.path

import serial
from serial.serialutil import PARITY_NONE

from pyOpticwash.py_mdb_terminal.abstract.abc_client import ABCMDBClient
from pyOpticwash.py_mdb_terminal.comamnds.commands_commutator import CommandsCommutator
from pyOpticwash.py_mdb_terminal.mdb_listener import MDBListener


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
        :param message:
        :raises PortNotOpenError the client is not started
        """
        self.listener.lock_queue()
        self.send_raw_message(message)
        return self.listener.get_last_message(5)

    def send_raw_message(self, message: bytes):
        """
        :param message:
        :raises PortNotOpenError the client is not started
        """
        self.ser.write(message + b"\n")
        self.ser.flush()

    def get_encoding(self):
        return self.encoding

    def get_serial(self):
        return self.ser

