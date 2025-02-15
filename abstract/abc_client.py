import abc
import logging
from abc import ABC



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
    def get_encoding(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_serial(self):
        raise NotImplementedError()

    @staticmethod
    def log(level: int, message: str):
        logging.log(level, f"ABCMDBClient: {message}")