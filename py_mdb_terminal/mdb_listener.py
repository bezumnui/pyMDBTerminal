import logging
import os
import queue
import threading
from datetime import datetime
from logging.handlers import RotatingFileHandler

from py_mdb_terminal.commands.commands_commutator import CommandsCommutator


class MDBListener:
    def __init__(self, mdb_client: CommandsCommutator):
        self.__client = mdb_client
        self.__queue = queue.Queue(5)
        self.__active = False
        self.__polling_thread: threading.Thread = None
        self.__accepting_lock = threading.Lock()
        self.encoding = "ascii"
        self.__logger = logging.getLogger(name=MDBListener.__class__.__name__)
        self.__setup_logging()


    def start(self):
        self.__polling_thread = threading.Thread(target=self.__poll)
        self.__active = True
        self.__polling_thread.start()

    def stop(self, block=True):
        self.__active = False
        if block and self.__polling_thread:
            self.__polling_thread.join()

    def __setup_logging(self):
        self.__logger.setLevel(logging.DEBUG)

        if not os.path.exists("log"):
            os.mkdir("log")

        file_handler = RotatingFileHandler(
            filename=datetime.now().strftime("log/mdb_listener_log_%d.%m.%Y_%H.%M.%S"),
            maxBytes=5 * 1024 * 1024,
            backupCount=5
        )

        stream_handler = logging.StreamHandler()

        file_handler.setLevel(logging.DEBUG)
        stream_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        self.__logger.addHandler(file_handler)
        self.__logger.addHandler(stream_handler)

    def __poll(self):
        serial = self.__client.get_serial()
        while self.__active:
            if serial.closed:
                self.__logger.log(logging.CRITICAL, f"MDB adapter has closed the connection.")
                self.stop(True)

            elif serial.in_waiting:
                raw_data = serial.read_all().decode(self.encoding)
                self.__logger.log(logging.DEBUG, f"Received data from polling: {raw_data}")

                if raw_data.startswith("x"):
                    self.log_telemetry(raw_data)
                elif self.__accepting_lock.locked():
                    self.__queue.put(raw_data, False)
                else:
                    self.handle_async_messages(raw_data)

    def handle_async_messages(self, raw_data: str):
        self.__logger.log(logging.INFO, f"Handling unawaitable data: {raw_data}")

    def log_telemetry(self, raw_data: str):
        self.__logger.info(raw_data)

    def lock_queue(self):
        """
        MUST be called BEFORE the ``get_last_message`` to prepare the queue.
        Queue will be unlocked after ``get_last_message``. Use the following format to read incoming messages:

        ``lock_queue()``\n
        ``sendMessage()``\n
        ``get_last_message()``\n

        """
        self.__accepting_lock.acquire_lock(True, 5)

    def get_last_message(self, timeout = 10) -> str:
        data = self.__queue.get(timeout=timeout)
        self.__accepting_lock.release_lock()
        return data
