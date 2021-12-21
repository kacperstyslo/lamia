"""
This classes & functions are here because all lamia modules uses them.
"""

__all__ = (
    "_Path",
    "Text",
    "clear_terminal",
    "pause_script",
    "run_parallel",
    "decorate_text",
)

import asyncio
import sys
from colorama import init
from dataclasses import dataclass
from functools import wraps
from inspect import cleandoc
from os import name, path, system
from pathlib import Path
from time import sleep
from typing import Any, Awaitable, NoReturn


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
class Text:
    """
    All used by Lamia notifications colors.
    """

    endc: str = "\033[0m"
    error: str = "\033[91m"
    pass_g: str = "\033[92m"
    warning: str = "\033[93m"
    blue: str = "\033[94m"


def clear_terminal() -> NoReturn:
    """
    Clear terminal screen after calling.
    """
    system("cls") if name == "nt" else system("clear")


async def run_parallel(*functions: Awaitable[Any]) -> NoReturn:
    await asyncio.gather(*functions)


def pause_script() -> NoReturn:
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
            {30 * "-"}{Text.blue} {module_name} {Text.endc}{30 * "-"}
            {menu_content}
            Do you want to continue? {Text.warning}Y/N{Text.endc}
            {100 * "-"}
            """.strip()
        )
    )


def decorate_text(_text: str):
    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            clear_terminal()
            init(strip=not sys.stdout.isatty())
            for char in _text:
                sys.stdout.write(f"{Text.blue}{char}{Text.endc}")
                sys.stdout.flush()
                if type(_text) is str:
                    sleep(0.05)
                else:
                    sleep(0.01)
            sleep(3)
            method(*args, **kwargs)

        return wrapper

    return decorator
