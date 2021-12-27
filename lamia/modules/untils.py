"""
This classes & functions are here because all lamia modules uses them.
"""

__all__ = (
    "cast_variable_to_int",
    "take_complete_fnc_name",
    "clear_terminal",
    "decorate_text",
    "pause_script",
    "run_concurrently",
    "show_menu",
    "TextColor",
    "_Path",
)

import asyncio
import sys
from dataclasses import dataclass
from functools import wraps
from inspect import cleandoc
from os import name, path, system
from pathlib import Path
from time import sleep
from typing import Any, Awaitable, NoReturn, Union

from colorama import init


class _Path:
    def __init__(self) -> NoReturn:
        self._output_path: str = ""
        self._script_path: str = ""

    @property
    def output_path(self) -> str:
        return self._output_path

    @output_path.setter
    def output_path(self, _file_name: str) -> NoReturn:
        self._output_path = path.join(
            Path(__file__).parent.parent,
            "output",
            _file_name,
        )

    @property
    def script_path(self) -> str:
        return self._script_path

    @script_path.setter
    def script_path(self, _file_name: str) -> NoReturn:
        self._script_path = path.join(
            Path(__file__).parent.parent,
            "generated_scripts",
            _file_name,
        )


@dataclass
class TextColor:
    """
    All used by Lamia notifications colors.
    """

    BLUE: str = "\033[94m"
    ERROR: str = "\033[91m"
    ENDC: str = "\033[0m"
    PASS_G: str = "\033[92m"
    WARNING: str = "\033[93m"


def clear_terminal() -> NoReturn:
    """
    Clear terminal screen after calling.
    """
    system("cls") if name == "nt" else system("clear")


def cast_variable_to_int(variable: Union[float, str]) -> Union[int, None]:
    """
    Cast value to int without error.
    :param variable: number in float or string value type that will be cast to int value
    """
    return int(variable) if variable.isdigit() else None


async def run_concurrently(*functions: Awaitable[Any]) -> NoReturn:
    """
    Run tasks concurrently. This module is used in network scanners.
    """
    await asyncio.gather(*functions)


def pause_script() -> NoReturn:
    """
    Pause lamia in any situation.
    """
    system("pause") if name == "nt" else input("Press any key to continue...")


def show_menu(module_name: str, menu_content: str) -> NoReturn:
    """
    Printing formatted and colored module menu.
    :param module_name: name of calling module
    :param menu_content: already prepared menu in str format
    """
    clear_terminal()
    print(
        cleandoc(
            f"""
            {30 * "-"}{TextColor.BLUE} {module_name} {TextColor.ENDC}{30 * "-"}
            {menu_content}
            Do you want to continue? {TextColor.WARNING}Y/N{TextColor.ENDC}
            {100 * "-"}
            """.strip()
        )
    )


def decorate_text(_text: str):
    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            """
            This decorator will create the impression of writing text on the screen.
            """
            clear_terminal()
            init(strip=not sys.stdout.isatty())
            for char in _text:
                sys.stdout.write(f"{TextColor.BLUE}{char}{TextColor.ENDC}")
                sys.stdout.flush()
                if isinstance(_text, str):
                    sleep(0.05)
                else:
                    sleep(0.01)
            sleep(3)
            method(*args, **kwargs)

        return wrapper

    return decorator


def take_complete_fnc_name(full_fnc_name: str):
    """
    Take full function name, if it too long.
    :param full_fnc_name: long, descriptive function name
    """
    def actual_decorator(fnc):
        @wraps(fnc)
        def wrapper(*args, **kwargs):
            fnc.__name__ = full_fnc_name
            return fnc(*args, **kwargs)

        return wrapper

    return actual_decorator
