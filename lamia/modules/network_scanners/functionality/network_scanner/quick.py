"""
NetworkScannerQuick (quick scan chosen network area).
==================================================================================
|NetworkScannerQuick will get:                                                   |
|- IP address                                                                    |
|--------------------------------------------------------------------------------|
"""
__all__ = ("NetworkScannerQuick",)

from typing import List, NoReturn

from lamia.modules.network_scanners.view import ui
from lamia.modules.untils import take_complete_fnc_name
from .base.state import BaseScannerType


class NetworkScannerQuick(BaseScannerType.LAYOUT.value):
    """
    This module will quickly scan chosen network area to get active hosts.
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def __init__(self, network_scanner_base: BaseScannerType.BASE.value) -> None:
        self._network_scanner_base = network_scanner_base
        self._scanner_quick_ui = ui.NetworkScannerQuickUI()

    def prepare_scanner(self) -> NoReturn:
        """
        Preparing module so that can start scanning.
        """
        self._network_scanner_base.chose_network_area_to_scan()
        self.run_scanner()

    @take_complete_fnc_name("run_quick_scan")
    def run_scanner(self) -> NoReturn:
        active_victims: List[str] = []
        for victim_ip in self._network_scanner_base.network_area_to_scan:
            if self._network_scanner_base.quick_check_if_victim_is_active(victim_ip):
                active_victims.append(victim_ip)
        self._scanner_quick_ui.show_quick_scan_output(active_victims)
