from abc import ABC

from py_mdb_terminal.abstract.abc_client import ABCMDBClient
from py_mdb_terminal.commands.cashless_master import CommandsCashlessMaster
from py_mdb_terminal.commands.cashless_slave import CommandsCashlessSlave
from py_mdb_terminal.commands.configuration import CommandsConfiguration
from py_mdb_terminal.commands.misc import CommandsMisc


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
