"""
All the components that are needed to create a new network scanners.
"""

__all__ = (
    "NetworkScannerBase",
    "NetworkScannerLayout",
)

import asyncio
import platform
import socket
import subprocess
import re

from abc import abstractmethod, ABC
from functools import partial
from typing import Callable, Dict, List, Union, Optional, NoReturn

import getmac
from pythonping import ping

from lamia.modules.network_scanners.const import (
    ALL_PORTS_AND_SERVICES,
    OPERATING_SYSTEMS_NAMES,
)
from lamia.modules.network_scanners.view import ui
from lamia.modules.user_information import UserDeviceInformation
from lamia.modules.untils import (
    run_concurrently,
    take_complete_fnc_name,
    TextColor,
    _Path,
)
from lamia.exceptions import (
    PortNumberToSmallError,
    PortNumberToLargeError,
    InvalidNetworkArea,
)


class NetworkScannerLayout(ABC):
    """
    This two function must be included in every new network scanner. In this functions
    we can call ready-made functions from NetworkScannerBase in different ways to get
    different network scanners.
    """

    @abstractmethod
    def prepare_scanner(self, scanner_type: Optional[Callable]) -> NoReturn:
        """
        Prepare any of network scanner to able to scan.
        """

    @abstractmethod
    def run_scanner(self) -> NoReturn:
        """
        Launch any network scanner made of modules embedded in NetworkScannerBase.
        """


class NetworkScannerBase(UserDeviceInformation, NetworkScannerLayout):
    # pylint: disable=too-many-instance-attributes
    """
    This class has fields and methods that you can use to create a new network scanner.
    For example by using methods embedded in this class, I built three network scanners:
    - NetworkScannerQuick
    - NetworkScannerIntense
    - NetworkScannerSingleTarget

    All of this above network scanners when encounter active victims and try to obtain
    various information about them, for example:
    ==================================================================================
    |- IP address                                                                    |
    |- MAC address                                                                   |
    |- Hostname                                                                      |
    |- Operating system name                                                         |
    |- Ports numbers that are open and services names running on these ports         |
    ===================================================================================
    """

    __slots__ = (
        "victim_ip",
        "victims_data",
        "scanners_base_ui",
        "network_area_to_scan",
        "_coroutines_amount",
        "_victim_hostname",
        "_victim_mac_address",
        "_victim_operation_system_name",
        "_port_range",
        "_opened_victim_ports_and_services",
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def __init__(self) -> None:
        super().__init__()
        self.victim_ip: str = ""
        self.victims_data = _Path()
        self.scanners_base_ui = ui.NetworkScannerBaseUI()
        self.network_area_to_scan: Optional[List[str]] = None
        self._coroutines_amount: int = 30
        self._victim_hostname: str = ""
        self._victim_mac_address: str = ""
        self._victim_operation_system_name: str = ""
        self._port_range: List[int] = []
        self._opened_victim_ports_and_services: Dict[int, str] = {}

    def prepare_scanner(self, scanner_type) -> NoReturn:
        """
        Just running logic of already chosen Network Scanner.
        Also dependency injection is performed (NetworkScannerBase to any NetworkScanner).
        :param scanner_type: instance of some network scanner
        :type scanner_type: Callable
        """
        scanner_type(NetworkScannerBase()).prepare_scanner()

    def run_scanner(self) -> NoReturn:
        ...

    def chose_network_area_to_scan(self) -> NoReturn:
        """
        This method run forever until user chose correct network area to scan.
        """
        while not isinstance(self.network_area_to_scan, list):
            self.scanners_base_ui.show_message_while_user_choosing_network_area()
            self.network_area_to_scan = self.__verify_network_area()

    @staticmethod
    def __verify_network_area() -> Union[List[str], None]:
        """
        Check if provided network area is correct.
        :return: List of all possible victims in given network area.
        :rtype: List of strings
        """
        ip_to_verify = list(filter(None, str(input("> ")).split(".")))
        if 3 <= len(ip_to_verify) <= 4:
            correct_ip = (
                ".".join(ip_to_verify) + "."
                if len(ip_to_verify) == 3
                else ".".join(ip_to_verify[:-1]) + "."
            )
            return [f"{correct_ip}{num}" for num in range(1, 255)]
        print(InvalidNetworkArea(".".join(ip_to_verify)))
        return None

    def set_output_path(
        self, file_name: str, target: Union[str, List[str]]
    ) -> NoReturn:
        """
        Generating output path basing on chosen network area "Network Scanner Intense"
        or chosen victim IP address "Network Scanner Single Target".
        :param file_name: Output file_name
        :type file_name: str
        :param target: network Area or single victim which will be scanned
        :type target: string or List of strings
        """
        if isinstance(target, list):
            target = ".".join(self.network_area_to_scan[0].split(".")[:3])
        self.victims_data.output_path = f"{file_name}{target}.txt"

    def specify_port_range(self) -> NoReturn:
        """
        It is required to define port range to scan any network area.
        Port ranges:
        min: 10
        max: 9999
        """
        while not self._port_range:
            self.scanners_base_ui.show_message_while_user_specifying_port_range()
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
                    f"The given value is not an {TextColor.ERROR}int{TextColor.ENDC} type!"
                ) from wrong_input_type

    async def scan_victim_generally(self) -> NoReturn:
        """
        This function will call other fnc in NetworkScannerBase to get this below
        information about victim. Function will call:
        - self.quick_check_if_victim_is_active to get victim IP ADDRESS
        - self.__get_victim_hostname to get victim HOSTNAME
        - self.__get_victim_operation_system_name to get victim OPERATING SYSTEM NAME
        - getmac.get_mac_address (third part module) to get victim MAC ADDRESS
        - self.__get_victim_port_and_service to get victim open ports and services
          running on this ports
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

        self.scanners_base_ui.show_captured_victim_data(
            victim_ip=self.victim_ip,
            victim_operation_system_name=self._victim_operation_system_name,
            victim_hostname=self._victim_hostname,
            victim_mac_address=self._victim_mac_address,
        )

        while self._port_range:
            await run_concurrently(
                *[coroutine() for coroutine in self.__create_port_scanner_coroutines]
            )
            del self._port_range[: self._coroutines_amount]

        self.scanners_base_ui.show_victim_opened_ports_with_services(
            victim_open_ports_and_services=self._opened_victim_ports_and_services,
            victim_ip=self.victim_ip,
            victim_hostname=self._victim_hostname,
        )

        self.__save_captured_victim_data_locally()

    def quick_check_if_victim_is_active(self, victim_ip: str) -> bool:
        """
        Quick check if victim is active, if it active return True.
        :param victim_ip: IP address of currently scanned victim.
        :type victim_ip: str
        :return: True if victim is active otherwise False is not active.
        :rtype: bool
        """
        if ping(victim_ip, timeout=0.2, count=1).success():
            self.victim_ip = victim_ip
            return True
        return False

    async def __get_victim_mac_address(self) -> str:
        """
        Get victim mac address.
        :return: Victim MAC address or string 'Unknown'
        :rtype: str
        """
        await asyncio.sleep(0.01)
        return getmac.get_mac_address(ip=self.victim_ip)

    async def __get_victim_hostname(self) -> str:
        """
        Just returning victim hostname if Lamia can get it by using socket module.
        :return: Victim hostname
        :rtype: str
        """
        await asyncio.sleep(0.01)
        try:
            return socket.gethostbyaddr(self.victim_ip)[0]
        except socket.herror:
            return "Unknown"

    async def __get_victim_operation_system_name(self) -> str:
        """
        This function will try to get victim operating system name by analyzing ICMP
        response.
        :return: Name of victim operating system
        :rtype: str
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
                self.victim_ip,
            ]
        else:
            command_after = ["ping", par_one, "1", self.victim_ip]
        try:
            decoded_output: str = subprocess.check_output(command_after).decode("UTF-8")
            return OPERATING_SYSTEMS_NAMES.get(
                re.findall(r"\bttl=\b\d{1,3}\b", decoded_output, flags=re.IGNORECASE)[
                    0
                ].split("=")[-1],
                "Unknown",
            )
        except subprocess.CalledProcessError:
            return "Host in drop mode!"

    @property
    def __create_port_scanner_coroutines(self):
        """
        This function will create coroutines ("by default 30"). When these 30 coroutines
        complete their tasks, this function will return collected information by this
        coroutines. While port_range exist, scan_victim_generally will call this
        function again with another 30 coroutines packages, but this time coroutines
        will get another ports to check. And this process will repeat until port_range
        exists.
        """
        return [
            partial(
                self.__get_victim_port_and_service,
                port=port,
            )
            for port in self._port_range[: self._coroutines_amount]
        ]

    @take_complete_fnc_name(
        "scan_victim_port_and_get_name_of_running_service_on_this_port"
    )
    async def __get_victim_port_and_service(self, port: int) -> NoReturn:
        """
        This function will try to find out what victim ports are open. If port will be
        open module will get service name running on this opened port from static
        variable named "ALL_PORTS_AND_SERVICES".
        :param port: Currently scanned port on victim device
        :type port: int
        """
        await asyncio.sleep(0.001)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.01)
        if not sock.connect_ex((self.victim_ip, port)):
            self._opened_victim_ports_and_services[port] = ALL_PORTS_AND_SERVICES.get(
                port
            )

    def __save_captured_victim_data_locally(self) -> NoReturn:
        """
        After scanning this function will save all captured output in
        lamia/modules/output path.
        """
        with open(self.victims_data.output_path, "a", encoding="utf-8") as victim_data:
            victim_data.write(100 * "=" + "\n")
            victim_data.write(f"Platform: {self._victim_operation_system_name}\n")
            victim_data.write(f"HOST: {self._victim_hostname}\n")
            victim_data.write(f"IP: {self.victim_ip}\n")
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
