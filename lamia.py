# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import user_information_module
import network_scanners_modules
import remote_control_modules
import key_hook_module
import passwords_generators_modules
from automatic_installation_module import *
from scanner_of_possible_network_areas_module import *


class WelcomeMessage:
    """
    Lamia Startup Message.
    """

    init(strip=not sys.stdout.isatty())

    def __init__(self):
        self.load: str = f""
        self.start_up_message: str = figlet_format("Lamia   1 . 2")
        self.check_compatibility: str = "The script checks compatibility..."

    def lamia_load_screen(self):
        for char in self.load:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.1)
        time.sleep(0.1)
        Clear.clear()
        for char in self.start_up_message:
            sys.stdout.write(colored(char, "magenta"))
            sys.stdout.flush()
            time.sleep(0.01)
        time.sleep(3)
        Clear.clear()
        for char in self.check_compatibility:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(1)


class Lamia:
    """
    The class responsible for managing all modules.
    """

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __init__(self, scanned_networks_areas):
        super().__init__()
        self.scanned_networks_areas: List[str] = scanned_networks_areas()

    @staticmethod
    def start_up():
        WelcomeMessage().lamia_load_screen()
        user_information_module.UserInfo().user_information()
        Lamia(scanned_network_areas).lamia_menu()

    def lamia_menu(self):
        while True:
            Clear.clear()
            print(25 * "-" + f"{Bcolors.magenta}LAMIA VERSION 1.2{Bcolors.endc}" + 25 * "-")
            print(f"{Bcolors.warning}1.NETWORK SCANNER{Bcolors.endc}")
            print(f"{Bcolors.warning}2.REMOTE CONTROL{Bcolors.endc}")
            print(f"{Bcolors.warning}3.PASSWORD GENERATOR{Bcolors.endc}")
            if os.name != "nt":
                print(
                    f"{Bcolors.LGRAY}4.KEY-HOOK GENERATOR{Bcolors.endc} {Bcolors.error_r}"
                    f"This module will not work in Linux !{Bcolors.endc}"
                )
            else:
                print(f"{Bcolors.warning}4.KEY-HOOK GENERATOR{Bcolors.endc}")
            print(f"{Bcolors.warning}0.EXIT{Bcolors.endc}")
            print(67 * "-")
            main_menu_choice = int(input("> ")) - 1
            main_menu_choice_options: list = [
                network_scanners_modules.NetworkScannerModules(
                    self.scanned_networks_areas
                ).network_scanner_modules_menu,
                remote_control_modules.RemoteControlModules().remote_control_startup,
                passwords_generators_modules.PasswordsGeneratorModules().password_generator_start,
                key_hook_module.KeyHookModule().key_hook_check_compatibility,
                self.exit_lamia,
            ]

            Clear.clear()
            if main_menu_choice == 3 and os.name != "nt":
                main_menu_choice += 2
            if -1 <= main_menu_choice < 4:
                main_menu_choice_options[main_menu_choice]()
            else:
                print(
                    f"{Bcolors.error_r}Wrong choice or module is not available on this platform or "
                    f"on this python version!{Bcolors.endc}"
                )
                time.sleep(2)

    @staticmethod
    def exit_lamia():
        close_message = "Exit..."
        for char in close_message:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.1)
        print("\n")
        sys.exit(0)


if __name__ == "__main__":
    scanned_network_areas = PossibleAreaNetworks()
    Lamia(scanned_network_areas).start_up()

# VERSION 1.2
