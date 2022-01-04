"""
From here lamia call all modules.
"""
# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from os import name, system
from inspect import cleandoc
from sys import exit
from typing import Callable, Dict, NoReturn

try:
    __import__("imp").find_module("maxminddb-geolite2")
except ImportError:
    from lamia.modules.automatic_installation import (
        install_missing_third_party_modules,
    )
    from elevate import elevate
    from pyfiglet import figlet_format

from lamia.exceptions import WrongUserChoiceError
from lamia.modules.untils import clear_terminal, decorate_text, TextColor
from lamia.modules.user_information import UserDeviceInformation
from lamia.modules import key_hook_generator, remote_control
from lamia.modules import network_scanners


class Lamia:
    """
    This class has methods that allows user call modules built in lamia. After
    executing chosen module lamia always will get back here.
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def __init__(self) -> None:
        self.__lamia_modules: Dict[int, Callable[[None], None]] = {
            1: network_scanners.ScannersView.show_network_scanners,
            2: remote_control.RemoteControlModules().remote_control_startup,
            3: key_hook_generator.KeyHookModule().check_system_compatibility,
            0: self.__exit_lamia,
        }

    @decorate_text(figlet_format("Lamia   2 . 4"))
    def start_up(self):
        """
        When Lamia start's this function call build in Lamia functions in proper order.
        """
        print(UserDeviceInformation().get_user_device_information())
        system("pause") if name == "nt" else input("Press any key to continue...")
        self.__lamia_menu()

    def __lamia_menu(self) -> NoReturn:
        """
        Render menu until user decide to exit. Allow user to chose module what is built
        in Lamia by using built in Python 'input' command.
        """
        while True:
            clear_terminal()
            print(
                cleandoc(
                    f"""
        {42 * "-"}{TextColor.BLUE}LAMIA VER.2.4{TextColor.ENDC}{42 * "-"}
        {TextColor.WARNING}1.NETWORK SCANNER{TextColor.ENDC}
        {TextColor.WARNING}2.REMOTE CONTROL{TextColor.ENDC}
        {TextColor.WARNING}3.KEY-HOOK GENERATOR{TextColor.ENDC}
        {TextColor.WARNING}0.EXIT{TextColor.ENDC}
        {100 * "-"}"""
                )
            )
            main_menu_choice: int = int(input("> "))
            clear_terminal()
            if main_menu_choice in self.__lamia_modules:
                self.__lamia_modules.get(main_menu_choice)()
            else:
                print(WrongUserChoiceError())

    @staticmethod
    @decorate_text("Gracefully stopping...")
    def __exit_lamia() -> None:
        """
        Exit lamia with farewell message.
        """
        exit(0)


if __name__ == "__main__":
    elevate() if name == "nt" else elevate(graphical=False)
    network_scanners.GetNetworksAreas()
    Lamia().start_up()

# VERSION 2.4
