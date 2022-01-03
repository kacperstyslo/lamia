"""
NetworkScannerSingleTarget (thorough scan selected victim).
|--------------------------------------------------------------------------------|
|NetworkScannerSingleTarget will get:                                            |
|- IP address                                                                    |
|- MAC address                                                                   |
|- Hostname                                                                      |
|- Operating system name                                                         |
|- Ports numbers that are open and services names running on these ports         |
===================================================================================
"""

__all__ = ("NetworkScannerSingleTarget",)

import asyncio
from typing import NoReturn


from lamia.exceptions import InactiveHostError
from lamia.modules.network_scanners.view import ui
from lamia.modules.untils import take_complete_fnc_name
from .base.state import BaseScannerType


class NetworkScannerSingleTarget(BaseScannerType.LAYOUT.value):
    """
    By using this module you can get below information about chosen victim:
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
        self._scanner_single_target_ui = ui.NetworkScannerSingleTargetUI()

    def prepare_scanner(self) -> NoReturn:
        """
        Preparing module so that can start scanning.
        """
        if self.__chose_victim():
            self._network_scanner_base.specify_port_range()
            self.run_scanner()

    def __chose_victim(self) -> bool:
        """
        Choosing victim, it is important that chosen victim must be active.
        """
        self._scanner_single_target_ui.generate_chose_victim_ui()
        host_to_check_is_active = str(input("> "))
        if len(
            host_to_check_is_active.split(".")
        ) != 4 or not self._network_scanner_base.quick_check_if_victim_is_active(
            host_to_check_is_active
        ):
            print(InactiveHostError(host_to_check_is_active))
        elif self._network_scanner_base.quick_check_if_victim_is_active(
            host_to_check_is_active
        ):
            self._network_scanner_base.set_output_path(
                file_name="scanned_victim_",
                target=self._network_scanner_base.victim_ip,
            )
            self._network_scanner_base.scanners_base_ui.show_output_location(
                output_location=self._network_scanner_base.victims_data.output_path
            )
            return True

    @take_complete_fnc_name("run_single_victim_scan")
    def run_scanner(self) -> NoReturn:
        """
        Here module already have all necessary information and can start scanning chosen
        victim.
        """
        print(
            self._network_scanner_base.scanners_base_ui.show_start_up_scanning_message()
        )
        asyncio.run(self._network_scanner_base.scan_victim_generally())
        self._network_scanner_base.scanners_base_ui.show_saved_victims_data(
            self._network_scanner_base.victims_data.output_path
        )
