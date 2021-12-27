"""
This module will install all missing third part modules.
"""
from os import name
from subprocess import call
from typing import NoReturn


def install_missing_third_party_modules() -> NoReturn:
    """
    Install all third-part python packages that lamia will use in modules.
    """
    call("pip install -r requirements.txt") if name == "nt" else call(
        "cat requirements.txt | sudo xargs -n 1 pip3 install"
    )


install_missing_third_party_modules()
