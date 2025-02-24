from abc import ABC

from py_mdb_terminal.abstract.abc_client import ABCMDBClient
from py_mdb_terminal.commands.structures.misc.hardware import Hardware
from py_mdb_terminal.commands.structures.misc.version import Version


class CommandsMisc(ABCMDBClient, ABC):

    def get_version(self) -> Version:
        data = self.send_raw_message_with_response(Version.COMMAND)
        return Version(*data.split(",")[1:])

    def get_hardware_info(self):
        data = self.send_raw_message_with_response(Hardware.COMMAND)
        return Hardware(*data.split(",")[1:])

    def update_software(self):
        self.send_raw_message(b"F,UPDATE")

    def reset_reboot(self):
        self.send_raw_message(b"F,RESET")

    def revert_to_defaults(self):
        self.send_raw_message(b"F,REVERT")

    def set_license_code(self, license_code: str):
        self.send_raw_message(f"F,SET,{license_code}".encode(self.get_encoding()))

    def watchdog(self, time: int, command: int, permanent: int):
        self.send_raw_message(f"W,{time},{command},{permanent}".encode(self.get_encoding()))
