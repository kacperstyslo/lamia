"""
When the user uses the UI, from here he choosing network scanner modules.
To keep one menu design in the future I created abstract class.
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
from lamia.modules.untils import (
    clear_terminal,
    cast_variable_to_int,
    decorate_text,
    show_menu,
    TextColor,
)

from ..scanners_types import ScannerType
from lamia.modules.network_scanners.functionality import scanners_functionality


class MenuLayout(ABC):
    @classmethod
    @abstractmethod
    def generate_menu_content(cls) -> NoReturn:
        pass


class NetworkScannerBaseMenu:
    """
    Main networks scanners menu.
    """

    _SCANNER_TYPE = {}

    def __init_subclass__(cls, scanner_key: str = "", **kwargs) -> NoReturn:
        super().__init_subclass__(**kwargs)
        if scanner_key:
            cls._SCANNER_TYPE[scanner_key] = cls

    @classmethod
    @decorate_text("NETWORK SCANNER LOADING...")
    def show_modules(cls) -> NoReturn:
        clear_terminal()
        print(
            cleandoc(
                f"""
                {38 * "-"}{TextColor.BLUE} NETWORK SCANNER MODULES {TextColor.ENDC}{38 * "-"}
                {TextColor.WARNING}1.QUICK MODULE {TextColor.ENDC}
                {TextColor.WARNING}2.INTENSE MODULE{TextColor.ENDC}
                {TextColor.WARNING}3.SINGLE TARGET MODULE{TextColor.ENDC}
                {100 * "-"}
            """
            )
        )

        scanner_key: int = cast_variable_to_int(input("> "))
        if scanner_key in cls._SCANNER_TYPE:
            cls._SCANNER_TYPE[scanner_key]().generate_menu_content()
        else:
            print(WrongUserChoiceError())

    @staticmethod
    def run_chosen_scanner(scanner_key: str) -> NoReturn:
        scanners_functionality.NetworkScannerBase._SCANNER_TYPE[
            scanner_key
        ]().prepare_scanner()


class NetworkScannerQuickMenu(
    NetworkScannerBaseMenu, MenuLayout, scanner_key=ScannerType.QUICK.value
):
    """
    Customized menu to NetworkScannerQuick module.
    """

    @classmethod
    def generate_menu_content(cls) -> NoReturn:
        show_menu(
            module_name="NETWORK SCANNER MODULE QUICK",
            menu_content=f"""
            {TextColor.BLUE}QUICK{TextColor.ENDC} module will find all 
            {TextColor.PASS_G}ACTIVE{TextColor.ENDC} hosts in chosen network area and 
            display their {TextColor.WARNING}IP{TextColor.ENDC} address. After scanning 
            chosen network area, output won't be saved!""",
        )
        menu_choice = str(input("> "))
        if menu_choice.upper() == "Y":
            cls.__base__().run_chosen_scanner(1)
        elif not menu_choice.upper() == "N":
            print(WrongUserChoiceError())


class NetworkScannerIntenseMenu(
    NetworkScannerBaseMenu, MenuLayout, scanner_key=ScannerType.INTENSE.value
):
    """
    Customized menu to NetworkScannerIntense module.
    """

    @classmethod
    def generate_menu_content(cls) -> NoReturn:
        show_menu(
            module_name="NETWORK SCANNER INTENSE MODULE",
            menu_content=f"""
           Intense module will search for active hosts in chosen network area, if module 
           find a host, module will try to get as much information as possible about 
           this active host. For example, module will try to find the:
           -{TextColor.WARNING} IP ADDRESS {TextColor.ENDC}
           -{TextColor.WARNING} MAC ADDRESS {TextColor.ENDC}
           -{TextColor.WARNING} HOSTNAME {TextColor.ENDC}
           -{TextColor.WARNING} OPERATING SYSTEM NAME {TextColor.ENDC}
           This script will search for all open ports on this active host, if any are if 
           any are open it will try to find out what services work on these ports.""",
        )
        menu_choice: str = str(input("> "))
        if menu_choice.upper() == "Y":
            cls.__base__().run_chosen_scanner(2)
        elif not menu_choice.upper() == "N":
            print(WrongUserChoiceError())


class NetworkScannerSingleTargetMenu(
    NetworkScannerBaseMenu, MenuLayout, scanner_key=ScannerType.SINGLE_TARGET.value
):
    """
    Customized menu to NetworkScannerSingleTarget module.
    """

    @classmethod
    def generate_menu_content(cls) -> NoReturn:
        show_menu(
            module_name="NETWORK SCANNER SINGLE TARGET MODULE",
            menu_content=f"""
            By using this module you can thoroughly scan one selected host. If host is 
            active, module will receive:
            -{TextColor.WARNING} IP ADDRESS {TextColor.ENDC}
            -{TextColor.WARNING} MAC ADDRESS {TextColor.ENDC}
            -{TextColor.WARNING} HOSTNAME {TextColor.ENDC}
            -{TextColor.WARNING} OPERATING SYSTEM NAME {TextColor.ENDC}
            Script will also quickly scan {TextColor.WARNING}PORTS{TextColor.ENDC}, if 
            host has some ports open module will try to detect what {TextColor.WARNING}
            SERVICES{TextColor.ENDC} running on this ports.""",
        )
        menu_choice: str = str(input("> "))
        if menu_choice.upper() == "Y":
            cls.__base__().run_chosen_scanner(3)
        elif not menu_choice.upper() == "N":
            print(WrongUserChoiceError())
