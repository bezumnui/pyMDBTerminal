from abc import ABC

from pyOpticwash.py_mdb_terminal.abstract.abc_client import ABCMDBClient
from pyOpticwash.py_mdb_terminal.commands.cashless_master import CommandsCashlessMaster
from pyOpticwash.py_mdb_terminal.commands.cashless_slave import CommandsCashlessSlave
from pyOpticwash.py_mdb_terminal.commands.configuration import CommandsConfiguration
from pyOpticwash.py_mdb_terminal.commands.misc import CommandsMisc


class CommandsCommutator(
    CommandsCashlessSlave,
    CommandsCashlessMaster,
    CommandsConfiguration,
    CommandsMisc,
    ABCMDBClient,
    ABC
):
    """
    The commutator class to merge the commands
    """
    pass
