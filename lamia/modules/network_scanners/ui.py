# PSL
from inspect import cleandoc
from os import name, system
from typing import NoReturn

# Own
from lamia.modules.network_scanners import scanners
from lamia.exceptions import WrongUserChoiceError
from lamia.modules.user_information import UserDeviceInformation
from lamia.modules.untils import clear_terminal, decorate_text, show_menu, pause_script, Text


class NetworkScannerBaseView(UserDeviceInformation):
    SCANNER_KEY: str = ""
    SCANNER_MODULES = {}

    def __init_subclass__(cls, **kwargs) -> NoReturn:
        NetworkScannerBaseView.SCANNER_MODULES[cls.SCANNER_KEY] = cls

    @classmethod
    @decorate_text("NETWORK SCANNER LOADING...")
    def show_modules(cls):
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
        if module_choice in cls.SCANNER_MODULES:
            cls.SCANNER_MODULES[module_choice]().generate_menu_content()
        else:
            print(WrongUserChoiceError())

    @staticmethod
    def run_chosen_scanner(scanner_key: str) -> NoReturn:
        scanners.NetworkScannersBase.SCANNER_MODULES[scanner_key](port_range=0, victim_ip="",
                                                                  victim_hostname="", victim_mac_address="",
                                                                  victim_operation_system_name="").prepare()

    def show_communicate_while_user_choosing_network_area(self) -> NoReturn:
        clear_terminal()
        print(
            cleandoc(
                f"""
          {100 * "-"}
          Your ip address: {Text.warning}{self.user_ip}{Text.endc}
          If you want to scan your network area type: {Text.warning}{".".join(self.user_ip.split(".")[0:3])}{Text.endc}
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
                  Script will save all results in this location: {Text.warning}{output_location}{Text.endc}
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
        victim_ip = kwargs['victim_ip']
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
        for port, service in kwargs['victim_open_ports_and_services'].items():
            print(
                f"Host {Text.warning}{kwargs['victim_hostname']}{Text.endc} "
                f"with IP: {Text.warning}{kwargs['victim_ip']}{Text.endc} "
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


class NetworkScannerQuickView(NetworkScannerBaseView):
    SCANNER_KEY = "1"

    @classmethod
    def generate_menu_content(cls) -> NoReturn:
        show_menu(
            module_name="NETWORK SCANNER MODULE QUICK",
            menu_content=f"""
            {Text.blue}QUICK{Text.endc} module will find all {Text.pass_g}ACTIVE{Text.endc} hosts in chosen network 
            area and display their {Text.warning}IP{Text.endc} address. After scanning chosen network area, 
            output won't be saved!""",
        )
        menu_choice = str(input("> "))
        if menu_choice.upper() == "Y":
            cls.__base__().run_chosen_scanner(scanner_key=cls.SCANNER_KEY)
        elif not menu_choice.upper() == "N":
            print(WrongUserChoiceError())


class NetworkScannerIntenseView(NetworkScannerBaseView):
    SCANNER_KEY = "2"

    @classmethod
    def generate_menu_content(cls) -> NoReturn:
        show_menu(
            module_name="NETWORK SCANNER INTENSE MODULE",
            menu_content=f"""
           Intense module will search for active hosts in chosen network area, if module find a host, 
           module will try to get as much information as possible about this active host. 
           For example, module will try to find the:
           -{Text.warning} IP ADDRESS {Text.endc}
           -{Text.warning} MAC ADDRESS {Text.endc}
           -{Text.warning} HOSTNAME {Text.endc}
           -{Text.warning} OPERATING SYSTEM NAME {Text.endc}
           This script will search for all open ports on this active host, if any are if any are open it
           will try to find out what services work on these ports.""",
        )
        menu_choice: str = str(input("> "))
        if menu_choice.upper() == "Y":
            cls.__base__().run_chosen_scanner(scanner_key=cls.SCANNER_KEY)
        elif not menu_choice.upper() == "N":
            print(WrongUserChoiceError())


class NetworkScannerSingleTargetView(NetworkScannerBaseView):
    SCANNER_KEY = "3"

    @classmethod
    def generate_menu_content(cls) -> NoReturn:
        show_menu(
            module_name="NETWORK SCANNER SINGLE TARGET MODULE",
            menu_content=f"""
            By using this module you can thoroughly scan one selected host. If host is active, module will receive:
            -{Text.warning} IP ADDRESS {Text.endc}
            -{Text.warning} MAC ADDRESS {Text.endc}
            -{Text.warning} HOSTNAME {Text.endc}
            -{Text.warning} OPERATING SYSTEM NAME {Text.endc}
            Script will also quickly scan {Text.warning}PORTS{Text.endc}, if host has some
            ports open module will try to detect what {Text.warning}SERVICES{Text.endc} running on this ports.""",
        )
        menu_choice: str = str(input("> "))
        if menu_choice.upper() == "Y":
            cls.__base__().run_chosen_scanner(scanner_key=cls.SCANNER_KEY)
        elif not menu_choice.upper() == "N":
            print(WrongUserChoiceError())
