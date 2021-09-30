# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# PSL
import os
from inspect import cleandoc
from sys import exit
from typing import Callable, Dict, NoReturn

# Third-part
from pyfiglet import figlet_format

# Own
from lamia import GetNetworksAreas
from lamia.exceptions import WrongUserChoiceError
from lamia.modules import clear_terminal, decorate_text, Text
from lamia.modules.user_information import UserDeviceInformation
from lamia.modules import (
    key_hook_generator,
    network_scanners,
    remote_control,
)


class Lamia:
    """
    This class has methods that allows user call modules built in lamia. After executing chosen
    module lamia always will get back here.
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def __init__(self) -> NoReturn:
        self.__lamia_modules: Dict[int, Callable] = {
            1: network_scanners.NetworkScannersBase().show_included_modules,
            2: remote_control.RemoteControlModules().remote_control_startup,
            3: key_hook_generator.KeyHookModule().check_system_compatibility,
            0: self.__exit_lamia,
        }

    @decorate_text(figlet_format("Lamia   2 . 0"))
    def start_up(self):
        """
        When Lamia start's this function call build in Lamia functions in proper order.
        """
        print(UserDeviceInformation().get_user_device_information())
        os.system("pause") if os.name == "nt" else input("Press any key to continue...")
        self.__lamia_menu()

    def __lamia_menu(self) -> NoReturn:
        """
        Render menu until user decide to exit. Allow user to chose module what is built in Lamia by
        using built in Python 'input' command.
        """
        while True:
            clear_terminal()
            print(
                cleandoc(
                    f"""
        {42 * "-"}{Text.blue}LAMIA VER.2.0{Text.endc}{42 * "-"}
        {Text.warning}1.NETWORK SCANNER{Text.endc}
        {Text.warning}2.REMOTE CONTROL{Text.endc}
        {Text.warning}3.KEY-HOOK GENERATOR{Text.endc}
        {Text.warning}0.EXIT{Text.endc}
        {100 * "-"}"""))
            main_menu_choice: int = int(input("> "))
            clear_terminal()
            if main_menu_choice in self.__lamia_modules:
                self.__lamia_modules.get(main_menu_choice)()
            else:
                print(WrongUserChoiceError())

    @staticmethod
    @decorate_text("Gracefully stopping...")
    def __exit_lamia() -> NoReturn:
        """
        Exit lamia with farewell message.
        """
        exit(0)


if __name__ == "__main__":
    GetNetworksAreas()
    Lamia().start_up()

# VERSION 2.0
