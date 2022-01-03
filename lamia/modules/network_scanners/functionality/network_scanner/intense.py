"""
NetworkScannerIntense (thorough scan selected network area).
|--------------------------------------------------------------------------------|
|NetworkScannerIntense will get:                                                 |
|- IP address                                                                    |
|- MAC address                                                                   |
|- Hostname                                                                      |
|- Operating system name                                                         |
|- Ports numbers that are open and services names running on these ports         |
===================================================================================
"""
__all__ = ("NetworkScannerIntense",)

import asyncio
from typing import NoReturn

from lamia.modules.untils import take_complete_fnc_name
from .base.state import BaseScannerType


class NetworkScannerIntense(BaseScannerType.LAYOUT.value):
    """
    By using this module you can get below information about targets in chosen network
    area:
    - IP address
    - MAC address
    - Hostname
    - Operating system name
    - Ports numbers that are open and services names running on these ports
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def __init__(self, network_scanner_base: BaseScannerType.BASE.value) -> None:
        self._network_scanner_base = network_scanner_base

    def prepare_scanner(self) -> NoReturn:
        """
        Preparing module so that can start scanning.
        """
        self._network_scanner_base.chose_network_area_to_scan()
        self._network_scanner_base.set_output_path(
            file_name="scanned_network_area_",
            target=self._network_scanner_base.network_area_to_scan,
        )
        self._network_scanner_base.specify_port_range()
        self._network_scanner_base.scanners_base_ui.show_output_location(
            output_location=self._network_scanner_base.victims_data.output_path
        )
        self.run_scanner()

    @take_complete_fnc_name("run_intense_network_area_scan")
    def run_scanner(self) -> NoReturn:
        """
        Here module already have all necessary information and can start up all methods,
        which that gathering information about victims for chosen network area.
        """
        print(
            self._network_scanner_base.scanners_base_ui.show_start_up_scanning_message()
        )
        for victim_ip in self._network_scanner_base.network_area_to_scan:
            if self._network_scanner_base.quick_check_if_victim_is_active(victim_ip):
                asyncio.run(self._network_scanner_base.scan_victim_generally())
        self._network_scanner_base.scanners_base_ui.show_saved_victims_data(
            self._network_scanner_base.victims_data.output_path
        )
