"""
All "ui" for all network scanners.
"""

__all__ = (
    "NetworkScannerBaseUI",
    "NetworkScannerQuickUI",
    "NetworkScannerSingleTargetUI",
)

# PSL
from inspect import cleandoc
from os import name, system
from typing import List, NoReturn

# Own
from lamia.modules.user_information import UserDeviceInformation
from lamia.modules.untils import clear_terminal, pause_script, Text


class NetworkScannerBaseUI(UserDeviceInformation):
    """
    Networks scanners inherit "ui" mainly from methods built in this class.
    """

    def show_message_while_user_choosing_network_area(self) -> NoReturn:
        clear_terminal()
        print(
            cleandoc(
                f"""
          {100 * "-"}
          Your ip address: {Text.warning}{self.user_ip}{Text.endc}
          If you want to scan your network area type:{Text.warning} {".".join(
                    self.user_ip.split(".")[0:3])}{Text.endc}
          {100 * "-"}
        """
            )
        )

    @staticmethod
    def show_message_while_user_specifying_port_range():
        clear_terminal()
        print(
            cleandoc(
                f"""
                {100 * "-"}
                How many {Text.warning}PORTS{Text.endc} do you want to scan? 1-9999
                {100 * "-"}
                """
            )
        )

    @staticmethod
    def show_output_location(output_location: str) -> NoReturn:
        """
        This method show path to output location where module will save all gathering data about
        victim/victims after scan.
        """
        clear_terminal()
        print(
            cleandoc(
                f"""
                  {100 * "-"}
                  Script will save all results in this location: {Text.warning}{output_location}
                  {Text.endc}
                  {100 * "-"}
                """
            )
        )
        pause_script()

    @staticmethod
    def show_start_up_scanning_message() -> str:
        clear_terminal()
        return f"Module has started scanning! Pleas {Text.warning}wait{Text.endc}...\n"

    @staticmethod
    def show_captured_victim_data(**kwargs) -> NoReturn:
        victim_ip = kwargs["victim_ip"]
        print(
            cleandoc(
                f"""
        {38 * "="}{Text.pass_g} {victim_ip} is {Text.endc}{Text.pass_g}ACTIVE {Text.endc}{38 * "="}
        Platform: {Text.warning}{kwargs['victim_operation_system_name']}{Text.endc}
        Hostname: {Text.warning}{kwargs['victim_hostname']}{Text.endc}
        IP: {Text.warning}{victim_ip}{Text.endc}
        MAC: {Text.warning}{kwargs['victim_mac_address']}{Text.endc}
        """
            )
        )

    @staticmethod
    def show_victim_opened_ports_with_services(**kwargs) -> NoReturn:
        victim_ip: str = kwargs["victim_ip"]
        for port, service in kwargs["victim_open_ports_and_services"].items():
            print(
                f"Host {Text.warning}{kwargs['victim_hostname']}{Text.endc} "
                f"with IP: {Text.warning}{victim_ip}{Text.endc} "
                f"has an open port: {Text.warning}{port}{Text.endc}. "
                f"with listening service: {Text.warning}{service}{Text.endc}"
            )
        print(100 * "=" + "\n")

    @staticmethod
    def show_saved_victims_data(output_location: str) -> NoReturn:
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
        system(fr"more {output_location}") if name == "nt" else system(fr"less {output_location}")
        print(
            cleandoc(
                f"""
            All results are saved here: {Text.pass_g}{output_location}{Text.endc}
            {100 * "-"}
            """
            )
        )
        pause_script()


class NetworkScannerQuickUI:
    """
    Only NetworkScannerQuick will use method in this class.
    """

    @staticmethod
    def show_quick_scan_output(active_victims: List[str]) -> NoReturn:
        for victim in active_victims:
            print(f"Victim with IP: {victim} is {Text.pass_g}ACTIVE!{Text.endc}")
        pause_script()


class NetworkScannerSingleTargetUI:
    """
    Only NetworkScannerSingleTarget will use method in this class.
    """

    @staticmethod
    def generate_chose_victim_ui() -> NoReturn:
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
