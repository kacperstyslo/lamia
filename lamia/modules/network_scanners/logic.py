"""
This module stores all the logic of all network scanners. Most of logic is in "NetworkScannersBase"
class, from this class other network scanner modules inherit different functions.
"""

__all__ = (
    "NetworkScannersBase",
    "NetworkScannerQuick",
    "NetworkScannerIntense",
    "NetworksAreasScanner",
)

import asyncio
import platform
import socket
import subprocess
import re
from os import path
from pathlib import Path
from threading import Thread
from functools import partial
from typing import Dict, List, Union, NoReturn, Set

import getmac
from pythonping import ping

from lamia.modules.network_scanners.const import (
    ALL_PORTS_AND_SERVICES,
    OPERATING_SYSTEMS_NAMES,
)
from lamia.modules.network_scanners.view import ui
from lamia.modules.user_information import UserDeviceInformation
from lamia.modules.untils import run_parallel, Text, _Path
from lamia.exceptions import (
    PortNumberToSmallError,
    PortNumberToLargeError,
    InvalidNetworkArea,
    InactiveHostError,
)


class NetworkScannersBase(UserDeviceInformation):
    # pylint: disable=too-many-instance-attributes
    """
    This class provides common (methods, fields) from all Scanners and also have method that
    render menu trough which these scanners can be operated. Names of this scanners below:
    - NetworkScannerQuick (quick scan chosen network area)
    - NetworkScannerIntense (thorough scan selected network area)
    - NetworkScannerSingleTarget (thorough scan selected victim)

    Modules, when they encounter active victims try to obtain various information about them, for
    example:
    ==================================================================================
    |NetworkScannerQuick will get:                                                   |
    |- IP address                                                                    |
    |--------------------------------------------------------------------------------|
    |NetworkScannerIntense && NetworkScannerSingleTarget will get:                   |
    |- IP address                                                                    |
    |- MAC address                                                                   |
    |- Hostname                                                                      |
    |- Operating system name                                                         |
    |- Ports numbers that are open and services names running on these ports         |
    ===================================================================================
    """

    SCANNER_KEY = ""
    SCANNER_MODULES = {}

    __slots__ = (
        "_victims_data",
        "_scanners_base_ui",
        "_coroutines_amount",
        "_victim_ip",
        "_victim_hostname",
        "_victim_mac_address",
        "_victim_operation_system_name",
        "_port_range",
        "_network_area_to_scan",
        "_opened_victim_ports_and_services",
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def __init__(self) -> NoReturn:
        super().__init__()
        self._victims_data = _Path()
        self._scanners_base_ui = ui.NetworkScannerBaseUI()
        self._coroutines_amount: int = 30
        self._victim_ip: str = ""
        self._victim_hostname: str = ""
        self._victim_mac_address: str = ""
        self._victim_operation_system_name: str = ""
        self._port_range: List[int] = []
        self._network_area_to_scan: List[str] = []
        self._opened_victim_ports_and_services: Dict[int, str] = {}

    def __init_subclass__(cls) -> NoReturn:
        NetworkScannersBase.SCANNER_MODULES[cls.SCANNER_KEY] = cls

    @classmethod
    def prepare_scanner(cls) -> NoReturn:
        """
        Just running logic of already chosen Network Scanner modules.
        """
        NetworkScannersBase.SCANNER_MODULES.get(
            cls.SCANNER_KEY
        ).prepare_scanner()

    def chose_network_area_to_scan(self) -> NoReturn:
        """
        This method run forever until user chose correct network area to scan.
        """
        while True:
            self._scanners_base_ui.show_message_while_user_choosing_network_area()
            self._network_area_to_scan = self.__verify_network_area()
            if isinstance(self._network_area_to_scan, list):
                break

    @staticmethod
    def __verify_network_area() -> List[str]:
        ip_to_verify = list(filter(None, str(input("> ")).split(".")))
        if 3 <= len(ip_to_verify) <= 4:
            correct_ip = (
                ".".join(ip_to_verify) + "."
                if len(ip_to_verify) == 3
                else ".".join(ip_to_verify[:-1]) + "."
            )
            return [f"{correct_ip}{num}" for num in range(1, 255)]
        print(InvalidNetworkArea(".".join(ip_to_verify)))

    def set_output_path(
        self, file_name: str, target: Union[str, List[str]]
    ) -> NoReturn:
        """
        Generating output path basing on chosen network area "Network Scanner Intense" or chosen
        victim IP address "Network Scanner Single Target".
        """
        if isinstance(target, list):
            target = ".".join(self._network_area_to_scan[0].split(".")[:3])
        self._victims_data.output_path = f"{file_name}{target}.txt"

    def specify_port_range(self) -> NoReturn:
        """
        It is required to define port range to scan any network area.
        Port ranges:
        min: 10
        max: 9999
        """
        while not self._port_range:
            self._scanners_base_ui.show_message_while_user_specifying_port_range()
            try:
                port_range = int(input("> "))
                if 0 < port_range < 10000:
                    self._port_range = list(range(1, port_range))
                elif port_range > 9999:
                    print(PortNumberToLargeError(port_range))
                elif port_range <= 0:
                    print(PortNumberToSmallError(port_range))
            except ValueError as wrong_input_type:
                raise ValueError(
                    f"The given value is not an {Text.error}int{Text.endc} type!"
                ) from wrong_input_type

    async def scan_victim_generally(self) -> NoReturn:
        """
        This function will call other fnc in NetworkScannerBase to get this below information
        about victim. Function will call:
        - self.quick_check_if_victim_is_active to get victim IP ADDRESS
        - self.__get_victim_hostname to get victim HOSTNAME
        - self.__get_victim_operation_system_name to get victim OPERATING SYSTEM NAME
        - getmac.get_mac_address (third part module) to get victim MAC ADDRESS
        - self.__scan_victim_port_and_get_name_of_running_service_on_this_port to get victim
          open ports and services running on this ports
        """
        (
            self._victim_hostname,
            self._victim_operation_system_name,
            self._victim_mac_address,
        ) = await asyncio.gather(
            self.__get_victim_hostname(),
            self.__get_victim_operation_system_name(),
            self.__get_victim_mac_address(),
        )

        self._scanners_base_ui.show_captured_victim_data(
            victim_ip=self._victim_ip,
            victim_operation_system_name=self._victim_operation_system_name,
            victim_hostname=self._victim_hostname,
            victim_mac_address=self._victim_mac_address,
        )

        while self._port_range:
            await run_parallel(
                *[
                    coroutine()
                    for coroutine in self.__create_port_scanner_coroutines
                ]
            )
            del self._port_range[: self._coroutines_amount]

        self._scanners_base_ui.show_victim_opened_ports_with_services(
            victim_open_ports_and_services=self._opened_victim_ports_and_services,
            victim_ip=self._victim_ip,
            victim_hostname=self._victim_hostname,
        )

        self.__save_captured_victim_data_locally()

    def quick_check_if_victim_is_active(self, victim_ip: str) -> bool:
        """
        Quick check if victim is active, if it active return True.
        """
        if ping(victim_ip, timeout=0.2, count=1).success():
            self._victim_ip = victim_ip
            return True
        return False

    async def __get_victim_mac_address(self) -> str:
        await asyncio.sleep(0.01)
        return getmac.get_mac_address(ip=self._victim_ip)

    async def __get_victim_hostname(self) -> str:
        """
        Just returning victim hostname if Lamia can get it by using socket module.
        """
        await asyncio.sleep(0.01)
        try:
            return socket.gethostbyaddr(self._victim_ip)[0]
        except socket.herror:
            return "Unknown"

    async def __get_victim_operation_system_name(self) -> str:
        """
        This function will try to get victim operating system name by analyzing ICMP response.
        """
        await asyncio.sleep(0.01)
        par_one: str = "-n" if platform.system().lower() == "windows" else "-c"
        par_two: str = "-w" if platform.system().lower() == "windows" else "-c"
        if platform.system().lower() == "windows":
            command_after = [
                "ping",
                par_one,
                "1",
                par_two,
                "100",
                self._victim_ip,
            ]
        else:
            command_after = ["ping", par_one, "1", self._victim_ip]
        try:
            decoded_output: str = subprocess.check_output(
                command_after
            ).decode("UTF-8")
            return OPERATING_SYSTEMS_NAMES.get(
                re.findall(
                    r"\bttl=\b\d{1,3}\b", decoded_output, flags=re.IGNORECASE
                )[0].split("=")[-1],
                "Unknown",
            )
        except subprocess.CalledProcessError:
            return "Host in drop mode!"

    @property
    def __create_port_scanner_coroutines(self):
        """
        This function will create coroutines ("by default 30"). When these 30 coroutines complete
        their tasks, this function will return collected information by this coroutines.
        While port_range exist, scan_victim_generally will call this function again with another
        30 coroutines packages, but this time coroutines will get another ports to check. And this
        process will repeat until port_range exists.
        """
        return [
            partial(
                self.__scan_victim_port_and_get_name_of_running_service_on_this_port,
                port=port,
            )
            for port in self._port_range[: self._coroutines_amount]
        ]

    async def __scan_victim_port_and_get_name_of_running_service_on_this_port(
        self, port: int
    ) -> NoReturn:
        """
        This function will try to find out what victim ports are open. If port will be open module
        will get service name running on this opened port from static "ALL_PORTS_AND_SERVICES".
        """
        await asyncio.sleep(0.001)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.01)
        if not sock.connect_ex((self._victim_ip, port)):
            self._opened_victim_ports_and_services[
                port
            ] = ALL_PORTS_AND_SERVICES.get(port)

    def __save_captured_victim_data_locally(self) -> NoReturn:
        """
        After scanning this function will save all captured output in lamia/modules/output path.
        """
        with open(
            self._victims_data.output_path, "a", encoding="utf-8"
        ) as victim_data:
            victim_data.write(100 * "=" + "\n")
            victim_data.write(
                f"Platform: {self._victim_operation_system_name}\n"
            )
            victim_data.write(f"HOST: {self._victim_hostname}\n")
            victim_data.write(f"IP: {self._victim_ip}\n")
            victim_data.write(f"MAC: {self._victim_mac_address}\n")
            for (
                port,
                service,
            ) in self._opened_victim_ports_and_services.items():
                victim_data.write(
                    f"Open port: {port} with listening service: {service}\n"
                )
            victim_data.write(100 * "=" + "\n")
            self._opened_victim_ports_and_services.clear()


class NetworkScannerQuick(NetworkScannersBase):
    """
    This module will quickly scan chosen network area to get active hosts.
    """

    SCANNER_KEY: str = "1"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def __init__(self) -> NoReturn:
        super().__init__()
        self._scanner_quick_ui = ui.NetworkScannerQuickUI()

    def prepare_scanner(self) -> NoReturn:
        """
        Preparing module so that can start scanning.
        """
        self.chose_network_area_to_scan()
        self.__run_quick_scan()

    def __run_quick_scan(self) -> NoReturn:
        """
        Here module already have all necessary information and can start quick scan for chosen
        network area.
        """
        active_victims: List[str] = []
        for victim_ip in self._network_area_to_scan:
            if self.quick_check_if_victim_is_active(victim_ip):
                active_victims.append(victim_ip)
        self._scanner_quick_ui.show_quick_scan_output(active_victims)


class NetworkScannerIntense(NetworkScannersBase):
    """
    By using this module you can get below information about targets in chosen network area:
    - IP address
    - MAC address
    - Hostname
    - Operating system name
    - Ports numbers that are open and services names running on these ports
    """

    SCANNER_KEY: str = "2"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def prepare_scanner(self) -> NoReturn:
        """
        Preparing module so that can start scanning.
        """
        self.chose_network_area_to_scan()
        self.set_output_path(
            file_name="scanned_network_area_",
            target=self._network_area_to_scan,
        )
        self.specify_port_range()
        self._scanners_base_ui.show_output_location(
            output_location=self._victims_data.output_path
        )
        self.__run_intense_network_area_scan()

    def __run_intense_network_area_scan(self) -> NoReturn:
        """
        Here module already have all necessary information and can start up all methods, which that
        gathering information about victims for chosen network area.
        """
        print(self._scanners_base_ui.show_start_up_scanning_message())
        for victim_ip in self._network_area_to_scan:
            if self.quick_check_if_victim_is_active(victim_ip):
                asyncio.run(self.scan_victim_generally())
        self._scanners_base_ui.show_saved_victims_data(
            self._victims_data.output_path
        )


class NetworkScannerSingleTarget(NetworkScannersBase):
    """
    By using this module you can get below information about chosen victim:
    - IP address
    - MAC address
    - Hostname
    - Operating system name
    - Ports numbers that are open and services names running on these ports
    """

    SCANNER_KEY: str = "3"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def __init__(self) -> NoReturn:
        super().__init__()
        self._scanner_single_target_ui = ui.NetworkScannerSingleTargetUI()

    def prepare_scanner(self) -> NoReturn:
        """
        Preparing module so that can start scanning.
        """
        if self.__chose_victim():
            self.specify_port_range()
            self.__run_single_victim_scan()

    def __chose_victim(self) -> bool:
        """
        Choosing victim, it is important that chosen victim must be active.
        """
        self._scanner_single_target_ui.generate_chose_victim_ui()
        host_to_check_is_active = str(input("> "))
        if len(
            host_to_check_is_active.split(".")
        ) != 4 or not self.quick_check_if_victim_is_active(
            host_to_check_is_active
        ):
            print(InactiveHostError(host_to_check_is_active))
        elif self.quick_check_if_victim_is_active(host_to_check_is_active):
            self.set_output_path(
                file_name="scanned_victim_", target=self._victim_ip
            )
            self._scanners_base_ui.show_output_location(
                output_location=self._victims_data.output_path
            )
            return True

    def __run_single_victim_scan(self) -> NoReturn:
        """
        Here module already have all necessary information and can start scanning chosen victim.
        """
        print(self._scanners_base_ui.show_start_up_scanning_message())
        asyncio.run(self.scan_victim_generally())
        self._scanners_base_ui.show_saved_victims_data(
            self._victims_data.output_path
        )


class NetworksAreasScanner(NetworkScannersBase):
    r"""
    This module runs in the background and scans network for others possible network areas that user
    can latter scan more detailed using some of built in modules in Lamia. All captured network
    areas will be saved in lamia\output\captured_networks_areas.txt
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def __init__(self) -> NoReturn:
        super().__init__()
        self.user_current_network_area: List[str] = self.user_ip.split(".")
        self.ip_octet_one, self.ip_octet_two = (
            self.user_current_network_area[0],
            self.user_current_network_area[1],
        )
        self.output_path: str = path.join(
            Path(__file__).parent.parent.parent,
            "output",
            "captured_networks_areas.txt",
        )
        thread = Thread(target=self.__search_for_active_networks_areas)
        thread.daemon = True
        thread.start()

    def __search_for_active_networks_areas(self) -> NoReturn:
        """
        This module will search for all possible network area that user is able to scan. It is
        enough that one active host will be in some networks area and module will save this
        network area. If user will call Network Scanner module this module will return all saved
        network area where at least one host was active.
        """
        for num in range(0, 255):
            network_area: str = (
                f"{self.ip_octet_one + '.' + self.ip_octet_two + '.'}{num}.1"
            )
            if ping(f"{network_area}", timeout=0.1, count=1).success():
                with open(
                    self.output_path, "a", encoding="utf-8"
                ) as captured_networks:
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
