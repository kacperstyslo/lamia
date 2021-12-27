"""
All "ui" for all network scanners.
"""

__all__ = (
    "NetworkScannerBaseUI",
    "NetworkScannerQuickUI",
    "NetworkScannerSingleTargetUI",
)

from inspect import cleandoc
from os import name, system
from typing import List, NoReturn

from lamia.modules.user_information import UserDeviceInformation
from lamia.modules.untils import clear_terminal, pause_script, TextColor


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
          Your ip address: {TextColor.WARNING}{self.user_ip}{TextColor.ENDC}
          If you want to scan your network area type:{TextColor.WARNING} {".".join(
          self.user_ip.split(".")[0:3])}{TextColor.ENDC}
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
                How many {TextColor.WARNING}PORTS{TextColor.ENDC} do you want to scan? 1-9999
                {100 * "-"}
                """
            )
        )

    @staticmethod
    def show_output_location(output_location: str) -> NoReturn:
        """
        This method show path to output location where module will save all gathering
        data about victim/victims after scan.
        """
        clear_terminal()
        print(
            cleandoc(
                f"""
                  {100 * "-"}
                  Script will save all results in this location: {TextColor.WARNING}
                  {output_location}{TextColor.ENDC}
                  {100 * "-"}
                """
            )
        )
        pause_script()

    @staticmethod
    def show_start_up_scanning_message() -> str:
        clear_terminal()
        return (
            f"Module has started scanning! Pleas {TextColor.WARNING}wait"
            f"{TextColor.ENDC}...\n"
        )

    @staticmethod
    def show_captured_victim_data(**kwargs) -> NoReturn:
        victim_ip = kwargs["victim_ip"]
        print(
            cleandoc(
                f"""
        {38 * "="}{TextColor.PASS_G} {victim_ip} is {TextColor.ENDC}{TextColor.PASS_G}ACTIVE {TextColor.ENDC}{38 * "="}
        Platform: {TextColor.WARNING}{kwargs['victim_operation_system_name']}{TextColor.ENDC}
        Hostname: {TextColor.WARNING}{kwargs['victim_hostname']}{TextColor.ENDC}
        IP: {TextColor.WARNING}{victim_ip}{TextColor.ENDC}
        MAC: {TextColor.WARNING}{kwargs['victim_mac_address']}{TextColor.ENDC}
        """
            )
        )

    @staticmethod
    def show_victim_opened_ports_with_services(**kwargs) -> NoReturn:
        victim_ip: str = kwargs["victim_ip"]
        for port, service in kwargs["victim_open_ports_and_services"].items():
            print(
                f"Host {TextColor.WARNING}{kwargs['victim_hostname']}{TextColor.ENDC} "
                f"with IP: {TextColor.WARNING}{victim_ip}{TextColor.ENDC} "
                f"has an open port: {TextColor.WARNING}{port}{TextColor.ENDC}. "
                f"with listening service: {TextColor.WARNING}{service}{TextColor.ENDC}"
            )
        print(100 * "=" + "\n")

    @staticmethod
    def show_saved_victims_data(output_location: str) -> NoReturn:
        print(
            cleandoc(
                f"""
              {100 * "-"}
              {TextColor.PASS_G}SCANNING IS COMPLETE!{TextColor.ENDC}
            """
            )
        )
        pause_script()
        clear_terminal()
        system(fr"more {output_location}") if name == "nt" else system(
            fr"less {output_location}"
        )
        print(
            cleandoc(
                f"""
            All results are saved here: {TextColor.PASS_G}{output_location}{TextColor.ENDC}
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
            print(
                f"Victim with IP: {victim} is {TextColor.PASS_G}ACTIVE!{TextColor.ENDC}"
            )
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
                    {31 * "-"}{TextColor.BLUE} NETWORK SCANNER SINGLE TARGET MODULE {TextColor.ENDC}{31 * "-"} 
                    Below enter {TextColor.WARNING}IP{TextColor.ENDC} of computer what you want to scan.
                    {100 * "-"}
                    """
            )
        )
