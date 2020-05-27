"""
All build in lamia exceptions.
"""

# PSL
from inspect import cleandoc
from time import sleep
from typing import NoReturn

# Own
from lamia.modules.untils import Text


class LamiaError(Exception):
    """
    Base class for Lamia errors.
    """

    def __init__(self, error_msg: str) -> NoReturn:
        super().__init__()
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
        super().__init__(
            f"Typed port value: {Text.error}{to_small_port_value}{Text.endc} "
            f"is too small!\n Minimal port value is 1!"
        )


class PortNumberToLargeError(LamiaError):
    """
    Caller: network_scanners
    Raise this exception when user tries to scan port over 9999.
    """

    def __init__(self, to_large_port_value: int) -> NoReturn:
        super().__init__(
            f"Typed port value: {Text.error}{to_large_port_value}"
            f"{Text.endc} is too big!\n Maximum port value is 9999!"
        )


class WrongUserChoiceError(LamiaError):
    """
    Caller: Anywhere
    Raise this exception when user choose option that is not available in which user is located.
    """

    def __init__(self) -> NoReturn:
        super().__init__("Chosen option is not available in this module!")


class LocalSaveError(LamiaError):
    """
    Caller: Anywhere
    Raise this exception when Lamia can't save file on user device.
    """

    def __init__(self) -> NoReturn:
        super().__init__("Lamia can't save the file locally! Try again!")


class NotCompatibleSystemYetError(LamiaError):
    """
    Caller: Anywhere
    Raise this exception when user system is not compatible with Lamia.
    """

    def __init__(self, not_supported_system: str) -> NoReturn:
        super().__init__(f"This module is not yet ready for {not_supported_system} system!")


class InactiveHostError(LamiaError):
    """
    Caller: Networks Scanners (all)
    Raise this exception when user chose inactive host.
    """

    def __init__(self, inactive_victim: str) -> NoReturn:
        super().__init__(f"Selected host: {inactive_victim} is inactive!")


class InvalidNetworkArea(LamiaError):
    """
    Caller: Networks Scanners (all)
    Raise this exception when user typed network area incorrectly.
    """

    def __init__(self, wrong_network_area: str) -> NoReturn:
        super().__init__(f"Typed network area: {wrong_network_area} is incorrect!")


class WrongEmailCredentials(LamiaError):
    """
    Caller: Key hook generator
    Raise this exception when user provides wrong credentials to sender email.
    """

    def __init__(self) -> NoReturn:
        super().__init__("Wrong credentials!")
