"""
When the user uses the UI, from here he choosing network scanner modules. To keep one menu design in
the future I created abstract class.
"""

__all__ = (
    "MenuLayout",
    "NetworkScannerBaseMenu",
    "NetworkScannerQuickMenu",
    "NetworkScannerIntenseMenu",
    "NetworkScannerSingleTargetMenu",
)

from abc import ABC, abstractmethod
from inspect import cleandoc
from typing import NoReturn

from lamia.exceptions import WrongUserChoiceError
from lamia.modules.untils import decorate_text, show_menu, Text, clear_terminal
from lamia.modules.network_scanners import logic


class MenuLayout(ABC):
    @classmethod
    @abstractmethod
    def generate_menu_content(cls) -> NoReturn:
        pass


class NetworkScannerBaseMenu:
    """
    Main networks scanners menu.
    """

    SCANNER_KEY: str = ""
    SCANNER_MODULES = {}

    def __init_subclass__(cls, **kwargs) -> NoReturn:
        NetworkScannerBaseMenu.SCANNER_MODULES[cls.SCANNER_KEY] = cls

    @classmethod
    @decorate_text("NETWORK SCANNER LOADING...")
    def show_modules(cls) -> NoReturn:
        clear_terminal()
        print(
            cleandoc(
                f"""
                {38 * "-"}{Text.blue} NETWORK SCANNER MODULES {Text.endc}{38 * "-"}
                {Text.warning}1.QUICK MODULE {Text.endc}
                {Text.warning}2.INTENSE MODULE{Text.endc}
                {Text.warning}3.SINGLE TARGET MODULE{Text.endc}
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
        logic.NetworkScannersBase.SCANNER_MODULES[
            scanner_key
        ]().prepare_scanner()


class NetworkScannerQuickMenu(NetworkScannerBaseMenu, MenuLayout):
    """
    Customized menu to NetworkScannerQuick module.
    """

    SCANNER_KEY: str = "1"

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


class NetworkScannerIntenseMenu(NetworkScannerBaseMenu, MenuLayout):
    """
    Customized menu to NetworkScannerIntense module.
    """

    SCANNER_KEY: str = "2"

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


class NetworkScannerSingleTargetMenu(NetworkScannerBaseMenu, MenuLayout):
    """
    Customized menu to NetworkScannerSingleTarget module.
    """

    SCANNER_KEY: str = "3"

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
