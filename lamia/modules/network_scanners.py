# PSL
import platform
import sys
import socket
import subprocess
from os import name, path, system
from pathlib import Path
from inspect import cleandoc
from threading import Thread
from typing import Dict, List, NoReturn

# third-party
import getmac
from pythonping import ping

# Own
from . import clear_terminal, decorate_text, pause_script, Text, _Path
from .user_information import UserDeviceInformation
from .ports_and_services import CollectionOfPortsAndServices
from ..exceptions import (
    PortNumberToSmallError,
    PortNumberToLargeError,
    InvalidNetworkArea,
    InactiveHostError,
    WrongUserChoiceError,
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

    MODULE_KEY: str = ""
    SCANNER_MODULES = {}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def __init_subclass__(cls, **kwargs) -> NoReturn:
        NetworkScannersBase.SCANNER_MODULES[cls.MODULE_KEY] = cls

    def __init__(self) -> NoReturn:
        super().__init__()
        self._victims_data = _Path()
        self._port_range: int = 0
        self._victim_ip: str = ""
        self._victim_hostname: str = ""
        self._victim_mac_address: str = ""
        self._victim_operation_system_name: str = ""
        self._network_area_to_scan: List[str] = []
        self._ports_in_percentage: Dict[int, str] = {}
        self._victim_open_ports_and_services: Dict[int, str] = {}

    @classmethod
    @decorate_text("NETWORK SCANNER LOADING...")
    def show_included_modules(cls):
        clear_terminal()
        print(
            cleandoc(
                f"""
                {38 * "-"}{Text.blue} NETWORK SCANNER MODULES {Text.endc}{38 * "-"}
                {Text.warning}1.QUICK MODULE {Text.endc}
                {Text.warning}2.INTENSE MODULE{Text.endc}
                {Text.warning}3.SINGLE TARGET MODULE{Text.endc}
                {Text.warning}0.BACK TO MAIN MENU{Text.endc}
                {100 * "-"}
            """
            )
        )
        module_choice = input("> ")
        clear_terminal()
        if module_choice in cls.SCANNER_MODULES:
            cls.SCANNER_MODULES[module_choice]().show_menu()
        else:
            print(WrongUserChoiceError())

    def chose_network_area_to_scan(self):
        while True:
            clear_terminal()
            print(
                cleandoc(
                    f"""
              {100 * "-"}
              Your ip address: {Text.warning}{self.user_ip}{Text.endc}
              If you want to scan your network type: {Text.warning}{".".join(self.user_ip.split(".")[0:3])}{Text.endc}
              {100 * "-"}
            """
                )
            )
            self._network_area_to_scan = self.verify_network_area()
            if isinstance(self._network_area_to_scan, list):
                break
        self._victims_data.output_path = (
            f"scanned_network_area_{'.'.join(self._network_area_to_scan[0].split('.')[:3])}.txt"
        )
        clear_terminal()

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

    def prepare_module_to_scan(self) -> NoReturn:
        self.specify_port_range()
        self.show_output_location()

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

    def show_output_location(self) -> NoReturn:
        """
        This method show path to output location where module will save all gathering data about
        victim/victims after scan.
        """
        clear_terminal()
        print(
            cleandoc(
                f"""
          {100 * "-"}
          Script will save all results in this location: {Text.warning}{self._victims_data.output_path}{Text.endc}
          {100 * "-"}
        """
            )
        )
        pause_script()

    @staticmethod
    def show_start_up_scanning_message() -> str:
        clear_terminal()
        return f"Module has started scanning! Pleas {Text.warning}wait{Text.endc}..."

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
        print(
            cleandoc(
                f"""
        {38 * "="}{Text.pass_g} {self._victim_ip} is {Text.endc}{Text.pass_g}ACTIVE {Text.endc}{38 * "="}
        Platform: {Text.warning}{self._victim_operation_system_name}{Text.endc}
        Hostname: {Text.warning}{self._victim_hostname}{Text.endc}
        IP: {Text.warning}{self._victim_ip}{Text.endc}
        MAC: {Text.warning}{self._victim_mac_address}{Text.endc}
        """
            )
        )
        self.__get_victim_opened_ports_with_services()
        self.__show_victim_opened_ports_with_services()
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

    def __show_victim_opened_ports_with_services(self) -> NoReturn:
        for port, service in self._victim_open_ports_and_services.items():
            print(
                f"Host {Text.warning}{self._victim_hostname}{Text.endc} "
                f"with IP: {Text.warning}{self._victim_ip}{Text.endc} "
                f"has an open port: {Text.warning}{port}{Text.endc}. "
                f"with listening service: {Text.warning}{service}{Text.endc}"
            )
        print(100 * "=" + "\n")

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

    def show_captured_victims_data(self) -> NoReturn:
        print(
            cleandoc(
                f"""
              {100 * "-"}
              {Text.pass_g}SCANNING IS COMPLETE!{Text.endc}
            """
            )
        )
        pause_script()
        clear_terminal()
        system(fr"more {self._victims_data.output_path}") if name == "nt" else system(
            fr"less {self._victims_data.output_path}"
        )
        print(
            cleandoc(
                f"""
            All results are saved here: {Text.pass_g}{self._victims_data.output_path}{Text.endc}
            {100 * "-"}
            """
            )
        )
        pause_script()


class NetworkScannerQuick(NetworkScannersBase):
    MODULE_KEY: str = "1"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def show_menu(self) -> NoReturn:
        clear_terminal()
        print(
            cleandoc(
                f"""
            {35 * "-"}{Text.blue} NETWORK SCANNER MODULE QUICK {Text.endc}{35 * "-"}
            {Text.blue}QUICK{Text.endc} module will find all {Text.pass_g}ACTIVE{Text.endc}
            hosts in chosen network area and display their {Text.warning}IP{Text.endc} address.
            After scanning chosen network area, output won't be saved!
            Do you want to continue? {Text.warning}Y/N{Text.endc}
            {100 * "-"}
            """
            )
        )
        menu_choice = str(input("> "))
        if menu_choice.upper() == "Y":
            self.chose_network_area_to_scan()
            self.__run_quick_scan()
        elif not menu_choice.upper() == "N":
            print(WrongUserChoiceError())

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
    MODULE_KEY: str = "2"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def show_menu(self) -> NoReturn:
        clear_terminal()
        print(
            cleandoc(
                f"""
    {34 * "-"}{Text.blue} NETWORK SCANNER INTENSE MODULE {Text.endc}{34 * "-"}
    Intense module will search for active hosts in chosen network area, if module find a host, 
    module will try to get as much information as possible about this active host. 
    For example, module will try to find the:
    -{Text.warning} IP ADDRESS {Text.endc}
    -{Text.warning} MAC ADDRESS {Text.endc}
    -{Text.warning} HOSTNAME {Text.endc}
    -{Text.warning} OPERATING SYSTEM NAME {Text.endc}
    This script will search for all open ports on this active host, if any are if any are open it
    will try to find out what services work on these ports.
    Do you want to continue? {Text.warning}Y/N{Text.endc}
    {100 * "-"}"""
            )
        )
        menu_choice: str = str(input("> "))
        if menu_choice.upper() == "Y":
            self.chose_network_area_to_scan()
            self.prepare_module_to_scan()
            self.__run_intense_network_area_scan()
        elif not menu_choice.upper() == "N":
            print(WrongUserChoiceError())
        clear_terminal()

    def __run_intense_network_area_scan(self) -> NoReturn:
        """
        This module start up all methods, which that gathering information about victims for chosen
        network area.
        """
        print(self.show_start_up_scanning_message())
        for victim_ip in self._network_area_to_scan:
            if self.quick_check_if_victim_is_active(victim_ip):
                self.scan_victim_generally()
        print(self.show_captured_victims_data())


class NetworkScannerSingleTarget(NetworkScannersBase):
    MODULE_KEY: str = "3"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def show_menu(self) -> NoReturn:
        print(
            cleandoc(
                f"""
            {31 * "-"}{Text.blue} NETWORK SCANNER SINGLE TARGET MODULE {Text.endc}{31 * "-"}
            By using this module you can thoroughly scan one selected host. If host is active, module will receive:
            -{Text.warning} IP ADDRESS {Text.endc}
            -{Text.warning} MAC ADDRESS {Text.endc}
            -{Text.warning} HOSTNAME {Text.endc}
            -{Text.warning} OPERATING SYSTEM NAME {Text.endc}
            Script will also quickly scan {Text.warning}PORTS{Text.endc}, if host has some
            ports open module will try to detect what {Text.warning}SERVICES{Text.endc} running on this ports.
            Do you want to continue? {Text.warning}Y/N{Text.endc}
            {100 * "-"}
            """
            )
        )
        menu_choice: str = str(input("> "))
        clear_terminal()
        if menu_choice.upper() == "Y":
            self.__chose_victim()
        elif not menu_choice.upper() == "N":
            print(WrongUserChoiceError())

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
            self._victims_data.output_path = f"scanned_victim_{self._victim_ip}.txt"
            self.prepare_module_to_scan()
            self.__run_single_victim_scan()

    def __run_single_victim_scan(self) -> NoReturn:
        print(self.show_start_up_scanning_message())
        self.scan_victim_generally()
        self.show_captured_victims_data()


class NetworksAreasScanner(NetworkScannersBase):
    r"""
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
