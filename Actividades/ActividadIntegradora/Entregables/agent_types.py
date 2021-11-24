"""Agent Type Enum

This script avoids the usage of isinstance() or type() by returning
a member from an enum with the name of the different agent types that
exist in the Robot Model.

This file can also be imported as a module and contains the following class:

    * AgentType - grants access to the different agent types within the model"""

__author__ = "Raúl Youthan Irigoyen Osorio"

from enum import Enum, auto


class AgentType(Enum):
    ROBOT = auto()
    BOX = auto()
    DEPOT = auto()
