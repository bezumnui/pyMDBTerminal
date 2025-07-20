import logging
import queue
import threading

from py_mdb_terminal.commands.commands_commutator import CommandsCommutator


class MDBListener:
    def __init__(self, mdb_client: CommandsCommutator):
        self.__client = mdb_client
        self.__queue = queue.Queue(5)
        self.__active = False
        self.__polling_thread: threading.Thread = None
        self.__accepting_lock = threading.Lock()
        self.encoding = "ascii"


    def start(self):
        self.__polling_thread = threading.Thread(target=self.__poll)
        self.__active = True
        self.__polling_thread.start()

    def stop(self, block=True):
        self.__active = False
        if block and self.__polling_thread:
            self.__polling_thread.join()


    def __poll(self):
        serial = self.__client.get_serial()
        while self.__active:
            if serial.in_waiting:
                raw_data = serial.read_all().decode(self.encoding)
                self.log(logging.DEBUG, f"Received a data from polling: {raw_data}")
                if self.__accepting_lock.locked():
                    self.__queue.put(raw_data, False)
                else:
                    self.handle_async_messages(raw_data)

    def handle_async_messages(self, raw_data: bytes):
        self.log(logging.INFO, f"Handling unawaitable data: {raw_data}")

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

    @staticmethod
    def log(level: int, message: str):
        logging.log(level, f"MDBListener: {message}")