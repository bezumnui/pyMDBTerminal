import abc
import logging
from abc import ABC

import serial


class ABCMDBClient(ABC):


    @abc.abstractmethod
    def start(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def stop(self, block=True):
        raise NotImplementedError()

    @abc.abstractmethod
    def send_raw_message_with_response(self, message: bytes) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def send_raw_message(self, message: bytes):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_encoding(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_serial(self) -> serial.Serial:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_software_version(self) -> str:
        raise NotImplementedError()

    def current_version_is_or_above(self, cmp_version: str) -> bool:
        current = self.get_software_version().split(".")
        cmp = cmp_version.split(".")
        if len(current) != len(cmp):
            raise ValueError("Versions have different lengths.")
        for i in range(len(current)):
            if int(current[i]) > int(cmp[i]):
                return True
            if int(current[i]) < int(cmp[i]):
                return False

        return True


    @staticmethod
    def log(level: int, message: str):
        logging.log(level, f"ABCMDBClient: {message}")