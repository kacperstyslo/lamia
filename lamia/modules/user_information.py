"""
This module will get important data from user device to correctly run lamia.
"""
import os
import platform
import sys
import socket
from inspect import cleandoc
from time import sleep
from typing import Dict, NoReturn

import getpass
import getmac
import requests
from geolite2 import geolite2

from .untils import clear_terminal, TextColor


class UserDeviceInformation:
    """
    This module checks the compatibility of the user's device with Lamia and saves the
    necessary user data.
    """

    __slots__ = (
        "_city",
        "_country",
        "_latitude",
        "_longitude",
        "_user_ip",
        "_user_public_ip",
        "_user_hostname",
        "_user_mac",
        "_user_operating_system_version",
        "_user_operating_system_name",
        "_location",
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def __init__(self) -> None:
        self._city: str = ""
        self._country: str = ""
        self._latitude: str = ""
        self._longitude: str = ""
        self._user_ip: str = ""
        self._user_public_ip: str = ""
        self._user_hostname: str = getpass.getuser()
        self._user_mac: str = getmac.get_mac_address()
        self._user_operating_system_version: str = platform.version()
        self._user_operating_system_name: str = (
            platform.system() + " " + platform.release()
        )
        self._location: Dict[str, str] = {}

    @property
    def user_ip(self) -> str:
        _socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _socket.connect(("8.8.8.8", 80))
        self._user_ip = _socket.getsockname()[0]
        _socket.close()
        return self._user_ip

    @staticmethod
    def __get_posix_root_privileges() -> NoReturn:
        permissions = os.getuid()
        if permissions != 0:
            print(
                cleandoc(
                    f"""
                {100 * f"{TextColor.ERROR}-{TextColor.ENDC}"}
                {TextColor.ERROR} ERROR! {TextColor.ENDC}You must run script as root!
                Write: {TextColor.WARNING} sudo python3 refactor_file.py {TextColor.ENDC}
                {100 * f"{TextColor.ERROR}-{TextColor.ENDC}"}
                """
                )
            )
            sys.exit(0)

    def __get_user_public_ip(self) -> NoReturn:
        try:
            self._user_public_ip: str = requests.get("https://api.ipify.org").text
        except requests.exceptions.ConnectionError:
            self._user_public_ip: str = "Unknown"

    def __show_user_public_ip(self) -> str:
        try:
            if self._user_public_ip != "Unknown":
                return (
                    f"Public IP: {self._user_public_ip} {TextColor.PASS_G} "
                    f"OK!{TextColor.ENDC}"
                )
        except AttributeError:
            return (
                f"Public IP: {self._user_public_ip} {TextColor.ERROR} "
                f"CAN'T FIND!{TextColor.ENDC}"
            )

    def __get_user_device_location(self) -> NoReturn:
        reader = geolite2.reader()
        location = reader.get(self._user_public_ip)
        try:
            self._city = location["city"]["names"]["en"]
        except KeyError:
            self._city = "Unknown"
        self._country = location["country"]["names"]["en"]
        self._location = location["location"]
        self._latitude, self._longitude = (
            self._location["latitude"],
            self._location["longitude"],
        )

    def get_user_device_information(self) -> str:
        """
        Caller: run.Lamia.start_up
        This function call other functions in this module to prepare information about
        user device.
        """
        sleep(1)
        clear_terminal()
        self.__get_user_public_ip()
        self.__get_user_device_location()
        return cleandoc(
            f"""
        {47 * "-"}{TextColor.WARNING} WAIT {TextColor.ENDC}{47 * "-"}
        Platform: {self._user_operating_system_name} {TextColor.PASS_G} OK! {TextColor.ENDC}
        Version: {self._user_operating_system_version} {TextColor.PASS_G} OK! {TextColor.ENDC}
        IP: {self.user_ip} {TextColor.PASS_G} OK! {TextColor.ENDC}
        {self.__show_user_public_ip()}
        MAC: {self._user_mac} {TextColor.PASS_G} OK! {TextColor.ENDC}
        Country: {self._country} {"FOUND!" if self._user_public_ip != "Unknown" else "Can't Find"}
        City: {self._city} {"FOUND!" if self._city != "Unknown" else "Can't Find"}
        Longitude: {self._longitude} {"FOUND!" if self._city != "Unknown" else "Can't Find"}
        Latitude: {self._latitude} {"FOUND!" if self._city != "Unknown" else "Can't Find"}
        {48 * "-"} {TextColor.PASS_G} OK {TextColor.ENDC} {48 * "-"}
            """
        )
