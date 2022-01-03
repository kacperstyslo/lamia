"""
All networks scanners built in Lamia.
"""

__all__ = ("ScannerType",)

from enum import Enum


from . import area, quick, intense, single_target


class ScannerType(Enum):
    """
    Types of network scanners.
    """

    AREA = area.NetworksAreasScanner
    QUICK = quick.NetworkScannerQuick
    INTENSE = intense.NetworkScannerIntense
    SINGLE_TARGET = single_target.NetworkScannerSingleTarget
