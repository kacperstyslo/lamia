"""
All the basic classes that are needed to create new network scanners.
"""

__all__ = ("BaseScannerType",)

from enum import Enum

from .base import NetworkScannerBase, NetworkScannerLayout


class BaseScannerType(Enum):
    """
    Basic classes for creating new network scanners.
    """

    LAYOUT = NetworkScannerLayout
    BASE = NetworkScannerBase
