"""
All networks scanners views built in Lamia.
"""

__all__ = ("ScannerView",)

from enum import auto, Enum


class ScannerView(Enum):
    """
    Types of network scanners.
    """

    QUICK = auto()
    INTENSE = auto()
    SINGLE_TARGET = auto()
