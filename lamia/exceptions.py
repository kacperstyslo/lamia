# PSL
from inspect import cleandoc
from time import sleep
from typing import NoReturn

# Own
from lamia.modules import Text


class LamiaError(Exception):
    """
    Base class for Lamia errors.
    """

    def __init__(self, error_msg: str) -> NoReturn:
        self._error_msg: str = error_msg

    def __str__(self) -> str:
        print(
            cleandoc(
                f"""
                {46 * f"{Text.error}-{Text.endc}"}{Text.error} ERROR! {Text.endc}{46 * f"{Text.error}-{Text.endc}"}
                {self._error_msg}
                {100 * f"{Text.error}-{Text.endc}"}
                """
            )
        )
        sleep(3)
        return ""

class PortNumberToSmallError(LamiaError):
    """
    Caller: network_scanners
    Raise this exception when user trys to scan port under 1.
    """

    def __init__(self, to_small_port_value: int) -> NoReturn:
        self._error_msg: str = f"Typed port value: {Text.error}{to_small_port_value}{Text.endc}"
        f"is too small!\n Minimal port value is 1!"

    def __str__(self) -> str:
        return LamiaError(self._error_msg).__str__()


class PortNumberToLargeError(LamiaError):
    """
    Caller: network_scanners
    Raise this exception when user tries to scan port over 9999.
    """

    def __init__(self, to_large_port_value: int) -> NoReturn:
        self._error_msg: str = f"Typed port value: {Text.error}{to_large_port_value}"
        f"{Text.endc} is too small!\n Maximum port value is 9999!"

    def __str__(self) -> str:
        return LamiaError(self._error_msg).__str__()


class WrongUserChoiceError(LamiaError):
    """
    Caller: Anywhere
    Raise this exception when user choose option that is not available in which user is located.
    """

    def __init__(self) -> NoReturn:
        self._error_msg: str = "Chosen option is not available in this module!"

    def __str__(self) -> str:
        return LamiaError(self._error_msg).__str__()


class LocalSaveError(LamiaError):
    """
    Caller: Anywhere
    Raise this exception when Lamia can't save file on user device.
    """

    def __init__(self) -> NoReturn:
        self._error_msg: str = "Lamia can't save the file locally! Try again!"

    def __str__(self) -> str:
        return LamiaError(self._error_msg).__str__()


class NotCompatibleSystemYetError(LamiaError):
    """
    Caller: Anywhere
    Raise this exception when user system is not compatible with Lamia.
    """

    def __init__(self, not_supported_system: str) -> NoReturn:
        self._error_msg: str = f"This module is not yet ready for {not_supported_system} system!"

    def __str__(self) -> str:
        return LamiaError(self._error_msg).__str__()


class InactiveHostError(LamiaError):
    """
    Caller: Networks Scanners (all)
    Raise this exception when user chose inactive host.
    """

    def __init__(self, inactive_victim: str) -> NoReturn:
        self._error_msg: str = f"Selected host: {inactive_victim} is inactive!"

    def __str__(self) -> str:
        return LamiaError(self._error_msg).__str__()


class InvalidNetworkArea(LamiaError):
    """
    Caller: Networks Scanners (all)
    Raise this exception when user typed network area incorrectly.
    """

    def __init__(self, wrong_network_area: str) -> NoReturn:
        self._error_msg: str = f"Typed network area: {wrong_network_area} is incorrect!"

    def __str__(self) -> str:
        return LamiaError(self._error_msg).__str__()


class WrongEmailCredentials(LamiaError):
    """
    Caller: Key hook generator
    Raise this exception when user provides wrong credentials to sender email.
    """

    def __init__(self) -> NoReturn:
        self._error_msg: str = "Wrong credentials!"

    def __str__(self) -> str:
        return LamiaError(self._error_msg).__str__()
