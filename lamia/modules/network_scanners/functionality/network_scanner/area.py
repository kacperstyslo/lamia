"""
NetworksAreasScanner (getting all visible areas of the network).
==================================================================================
|NetworksAreasScanner will get:                                                  |
|- IP address                                                                    |
|--------------------------------------------------------------------------------|
"""

__all__ = ("NetworksAreasScanner",)

from os import path
from pathlib import Path
from threading import Thread
from typing import List, Set, NoReturn

from pythonping import ping

from lamia.modules.user_information import UserDeviceInformation


class NetworksAreasScanner(UserDeviceInformation):
    r"""
    This module runs in the background and scans network for others possible network
    areas that user can latter scan more detailed using some of built in modules in
    Lamia. All captured network areas will be saved in
    lamia\output\captured_networks_areas.txt
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def __init__(self) -> None:
        super().__init__()
        self.user_current_network_area: List[str] = self.user_ip.split(".")
        self.ip_octet_one, self.ip_octet_two = (
            self.user_current_network_area[0],
            self.user_current_network_area[1],
        )
        self.output_path: str = path.join(
            Path(__file__).parent.parent.parent.parent,
            "output",
            "captured_networks_areas.txt",
        )
        thread = Thread(target=self.__search_for_active_networks_areas)
        thread.daemon = True
        thread.start()

    def __search_for_active_networks_areas(self) -> NoReturn:
        """
        This module will search for all possible network area that user is able to scan.
        It is enough that one active host will be in some networks area and module will
        save this network area. If user will call Network Scanner module this module
        will return all saved network area where at least one host was active.
        """
        for num in range(0, 255):
            network_area: str = (
                f"{self.ip_octet_one + '.' + self.ip_octet_two + '.'}{num}.1"
            )
            if ping(f"{network_area}", timeout=0.1, count=1).success():
                with open(self.output_path, "a", encoding="utf-8") as captured_networks:
                    captured_networks.write(f"{network_area}\n")

    def __clear_duplicated_networks_areas(self) -> NoReturn:
        """
        This module will clear file "output/captured_networks_areas.txt from duplicated
        networks areas."
        """
        with open(self.output_path, "r+", encoding="utf-8") as file:
            captured_networks: Set[str] = {line.strip() for line in file}
            file.truncate(0)
            file.seek(0)
            for network_area in captured_networks:
                file.write(f"{network_area}\n")

    def get_scanned_networks_areas(self) -> List[str]:
        """
        This module will return all scanned networks areas in List[str] format.
        """
        self.__clear_duplicated_networks_areas()
        with open(self.output_path, encoding="utf-8") as networks_ares:
            return [line.strip() for line in networks_ares]
