"""
All networks scanners types built in Lamia.
"""

__all__ = ("ScannerType",)

from enum import auto, Enum


class ScannerType(Enum):
    """
    Types of network scanners.
    """

    QUICK = auto()
    INTENSE = auto()
    SINGLE_TARGET = auto()
