# PSL
import platform
import sys
import socket
import subprocess
from os import path
from pathlib import Path
from inspect import cleandoc
from threading import Thread
from typing import Dict, List, Union, NoReturn

# third-party
import getmac
from pythonping import ping

# Own
from lamia.modules.network_scanners import ui
from lamia.modules.untils import clear_terminal, pause_script, Text, _Path
from lamia.modules.user_information import UserDeviceInformation
from lamia.modules.ports_and_services import CollectionOfPortsAndServices
from lamia.exceptions import (
    PortNumberToSmallError,
    PortNumberToLargeError,
    InvalidNetworkArea,
    InactiveHostError,
)


class NetworkScannersBase(UserDeviceInformation, CollectionOfPortsAndServices):
    """
    This class provides common (methods, fields) from all Scanners and also have method that
    render menu trough which these scanners can be operated. Names of this scanners below:
    - NetworkScannerQuick
    - NetworkScannerIntense
    - NetworkScannerSingleTarget

    By using one of this three modules you can get different information about remote hosts for
    example you can get:
    - IP address
    - MAC address
    - Hostname
    - Operating system name
    - Opened ports and services names running on this ports
    """

    SCANNER_KEY: str = ""
    SCANNER_MODULES = {}

    __slots__ = ['port_range', 'victim_ip', 'victim_hostname', 'victim_mac_address',
                 'victim_operation_system_name']

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def __init__(self, **kwargs) -> NoReturn:
        print(self.__slots__)
        super().__init__()
        self._victims_data = _Path()
        self._scanners_view = ui.NetworkScannerBaseView()
        self._port_range: int = kwargs['port_range']
        self._victim_ip: str = kwargs['victim_ip']
        self._victim_hostname: str = kwargs["victim_hostname"]
        self._victim_mac_address: str = kwargs["victim_mac_address"]
        self._victim_operation_system_name: str = kwargs["victim_operation_system_name"]
        self._network_area_to_scan: List[str] = []
        self._ports_in_percentage: Dict[int, str] = {}
        self._victim_open_ports_and_services: Dict[int, str] = {}

    def __init_subclass__(cls, **kwargs) -> NoReturn:
        NetworkScannersBase.SCANNER_MODULES[cls.SCANNER_KEY] = cls

    @classmethod
    def prepare(cls) -> NoReturn:
        NetworkScannersBase.SCANNER_MODULES.get(cls.SCANNER_KEY).prepare()

    def chose_network_area_to_scan(self) -> NoReturn:
        while True:
            self._scanners_view.show_communicate_while_user_choosing_network_area()
            self._network_area_to_scan = self.verify_network_area()
            if isinstance(self._network_area_to_scan, list):
                break

    @staticmethod
    def verify_network_area() -> List[str]:
        ip_to_verify = list(filter(None, str(input("> ")).split(".")))
        if 3 <= len(ip_to_verify) <= 4:
            correct_ip = (
                ".".join(ip_to_verify) + "."
                if len(ip_to_verify) == 3
                else ".".join(ip_to_verify[:-1]) + "."
            )
            return [f"{correct_ip}{num}" for num in range(1, 255)]
        print(InvalidNetworkArea(".".join(ip_to_verify)))

    def set_output_path(self, file_name: str, target: Union[str, List[str]]) -> NoReturn:
        if isinstance(target, list):
            target = ".".join(self._network_area_to_scan[0].split(".")[:3])
        self._victims_data.output_path = f"{file_name}{target}.txt"

    def specify_port_range(self) -> NoReturn:
        """
        It is required to define port range to scan any network area.
        Port ranges -> min: 10, max: 9999
        """
        clear_terminal()
        while True:
            print(
                cleandoc(
                    f"""
              {34 * "-"}{Text.blue} NETWORK SCANNER INTENSE MODULE {Text.endc}{34 * "-"}
              How many {Text.warning}PORTS{Text.endc} do you want to scan? 1-9999
              {100 * "-"}
            """
                )
            )
            try:
                self._port_range = int(input("> "))
                if 0 < self._port_range < 10000:
                    break
                elif self._port_range > 9999:
                    print(PortNumberToLargeError(self._port_range))
                elif self._port_range <= 0:
                    print(PortNumberToSmallError(self._port_range))
            except ValueError:
                raise ValueError(f"The given value is not an {Text.error}int{Text.endc} type!")
            clear_terminal()

    def scan_victim_generally(self) -> NoReturn:
        """
        This method will get the below information about chosen victim.
        - OPERATING SYSTEM NAME
        - IP ADDRESS
        - MAC ADDRESS
        - HOSTNAME
        """
        if not self._ports_in_percentage:
            self.__generate_port_number_scale_in_percentage()
        self._victim_hostname: str = self.__get_victim_hostname()
        self._victim_mac_address: str = getmac.get_mac_address(ip=self._victim_ip)
        self._victim_operation_system_name: str = self.__get_victim_operation_system_name()
        self._scanners_view.show_captured_victim_data(
            victim_ip=self._victim_ip,
            victim_operation_system_name=self._victim_operation_system_name,
            victim_hostname=self._victim_hostname,
            victim_mac_address=self._victim_mac_address,
        )
        self.__get_victim_opened_ports_with_services()
        self._scanners_view.show_victim_opened_ports_with_services(
            victim_open_ports_and_services=self._victim_open_ports_and_services, victim_ip=self._victim_ip,
            victim_hostname=self._victim_hostname)
        self.__save_captured_victim_data_locally()

    def __generate_port_number_scale_in_percentage(self) -> NoReturn:
        for num in range(1, 10):
            self._ports_in_percentage[int(self._port_range * float(f"0.{num}"))] = f"{num}0 %"

    def quick_check_if_victim_is_active(self, victim_ip: str) -> bool:
        if ping(victim_ip, timeout=0.1, count=1).success():
            self._victim_ip = victim_ip
            return True

    def __get_victim_hostname(self) -> str:
        try:
            return socket.gethostbyaddr(self._victim_ip)[0]
        except socket.herror:
            return "Unknown"

    def __get_victim_operation_system_name(self) -> str:
        par_one: str = "-n" if platform.system().lower() == "windows" else "-c"
        par_two: str = "-w" if platform.system().lower() == "windows" else "-c"
        if platform.system().lower() == "windows":
            command_after = ["ping", par_one, "1", par_two, "100", self._victim_ip]
        else:
            command_after = ["ping", par_one, "1", self._victim_ip]
        try:
            decoded_output: str = subprocess.check_output(command_after).decode("UTF-8")
            if "ttl" or "TTL" in decoded_output:
                if "128" in decoded_output:
                    return "Windows"
                elif "64" in decoded_output:
                    return "Linux"
        except subprocess.CalledProcessError:
            return "Drop mode!"
        return "Unknown"

    @staticmethod
    def __restart_line_current_line() -> NoReturn:
        sys.stdout.write("\r")
        sys.stdout.flush()

    def __get_victim_opened_ports_with_services(self) -> NoReturn:
        for port in range(1, self._port_range):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.0001)
            result = sock.connect_ex((self._victim_ip, port))
            if port in self._ports_in_percentage:
                sys.stdout.write(f"{self._ports_in_percentage.get(port)} of ports is scanned!")
                sys.stdout.flush()
                self.__restart_line_current_line()
            if not result:
                self._victim_open_ports_and_services[port] = self._all_ports_and_services.get(
                    port
                )  # port: service
            sock.close()

    def __save_captured_victim_data_locally(self) -> NoReturn:
        with open(self._victims_data.output_path, "a", encoding="utf-8") as victim_data:
            victim_data.write(100 * "=" + "\n")
            victim_data.write(f"Platform: {self._victim_operation_system_name}\n")
            victim_data.write(f"HOST: {self._victim_hostname}\n")
            victim_data.write(f"IP: {self._victim_ip}\n")
            victim_data.write(f"MAC: {self._victim_mac_address}\n")
            for port, service in self._victim_open_ports_and_services.items():
                victim_data.write(f"Open port: {port} with listening service: {service}\n")
            victim_data.write(100 * "=" + "\n")
            self._victim_open_ports_and_services.clear(), self._ports_in_percentage.clear()


class NetworkScannerQuick(NetworkScannersBase):
    SCANNER_KEY: str = "1"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def prepare(self) -> NoReturn:
        self.chose_network_area_to_scan()
        self.__run_quick_scan()

    def __run_quick_scan(self) -> NoReturn:
        active_victims: List[str] = []
        for victim_ip in self._network_area_to_scan:
            if self.quick_check_if_victim_is_active(victim_ip):
                active_victims.append(victim_ip)
        self.__show_quick_scan_output(active_victims)

    @staticmethod
    def __show_quick_scan_output(active_victims: List[str]) -> NoReturn:
        for victim in active_victims:
            print(f"Victim with IP: {victim} is {Text.pass_g}ACTIVE!{Text.endc}")
        pause_script()


class NetworkScannerIntense(NetworkScannersBase):
    SCANNER_KEY: str = "2"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def prepare(self) -> NoReturn:
        print("here")
        self.chose_network_area_to_scan()
        self.set_output_path(
            file_name="scanned_network_area_",
            target=self._network_area_to_scan,
        )
        self.specify_port_range()
        self._scanners_view.show_output_location(
            output_location=self._victims_data.output_path
        )
        self.__run_intense_network_area_scan()

    def __run_intense_network_area_scan(self) -> NoReturn:
        """
        This module start up all methods, which that gathering information about victims for chosen
        network area.
        """
        print(self._scanners_view.show_start_up_scanning_message())
        for victim_ip in self._network_area_to_scan:
            if self.quick_check_if_victim_is_active(victim_ip):
                self.scan_victim_generally()
        self._scanners_view.show_saved_victims_data(self._victims_data.output_path)


class NetworkScannerSingleTarget(NetworkScannersBase):
    SCANNER_KEY: str = "3"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def prepare(self) -> NoReturn:
        self.specify_port_range()
        self.__chose_victim()

    def __chose_victim(self) -> NoReturn:
        clear_terminal()
        print(
            cleandoc(
                f"""
            {31 * "-"}{Text.blue} NETWORK SCANNER SINGLE TARGET MODULE {Text.endc}{31 * "-"}
            Below enter {Text.warning}IP{Text.endc} of computer what you want to scan.
            {100 * "-"}
            """
            )
        )
        host_to_check_is_active = str(input("> "))
        if len(host_to_check_is_active.split(".")) != 4 or not self.quick_check_if_victim_is_active(
                host_to_check_is_active
        ):
            InactiveHostError(host_to_check_is_active)
        elif self.quick_check_if_victim_is_active(host_to_check_is_active):
            self.set_output_path(file_name="scanned_victim_", target=self._victim_ip)
            self._scanners_view.show_output_location(
                output_location=self._victims_data.output_path
            )
            self.__run_single_victim_scan()

    def __run_single_victim_scan(self) -> NoReturn:
        print(self._scanners_view.show_start_up_scanning_message())
        self.scan_victim_generally()
        self._scanners_view.show_saved_victims_data(self._victims_data.output_path)


class NetworksAreasScanner(NetworkScannersBase):
    """
    This module runs in the background and scans network for others possible network areas that
    user can latter scan more detailed using some of built in modules in Lamia. All
    captured network areas will be saved in lamia\saved_data\captured_networks_areas.txt
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def __init__(self) -> NoReturn:
        self.user_current_network_area: List[str] = self.user_ip.split(".")
        self.ip_octet_one, self.ip_octet_two = (
            self.user_current_network_area[0],
            self.user_current_network_area[1],
        )
        self.output_path: str = path.join(
            Path(__file__).parent.parent, "output", "captured_networks_areas.txt"
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
            network_area: str = f"{self.ip_octet_one + '.' + self.ip_octet_two + '.'}{num}.1"
            if ping(f"{network_area}", timeout=0.1, count=1).success():
                with open(self.output_path, "a", encoding="utf-8") as captured_networks:
                    captured_networks.write(f"{network_area}\n")

    def __clear_duplicated_networks_areas(self) -> NoReturn:
        """
        This module will clear file "output/captured_networks_areas.txt from duplicated
        networks areas."
        """
        with open(self.output_path, "r+", encoding="utf-8") as file:
            captured_networks = set([line.strip() for line in file])
            file.truncate(0), file.seek(0)
            for network_area in captured_networks:
                file.write(f"{network_area}\n")

    def get_scanned_networks_areas(self) -> List[str]:
        """
        This module will return all scanned networks areas in List[str] format.
        """
        self.__clear_duplicated_networks_areas()
        with open(self.output_path, "r", encoding="utf-8") as networks_ares:
            return [line.strip() for line in networks_ares]
