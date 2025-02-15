from abc import ABC

from pyOpticwash.py_mdb_terminal.abstract.abc_client import ABCMDBClient
from pyOpticwash.py_mdb_terminal.comamnds.cashless_slave import CommandsCashlessSlave
from pyOpticwash.py_mdb_terminal.comamnds.configuration import CommandsConfiguration
from pyOpticwash.py_mdb_terminal.comamnds.misc import CommandsMisc


class CommandsCommutator(
    CommandsCashlessSlave,
    CommandsConfiguration,
    CommandsMisc,
    ABCMDBClient,
    ABC
):
    """
    The commutator class to merge the commands
    """
    pass
