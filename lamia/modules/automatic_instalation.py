# PSL
import os
import sys
import subprocess
from time import sleep

required_packages = ["pythonping", "getmac", "paramiko", "colorama", "termcolor", "pyfiglet"]
packages = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
installed_packages = [r.decode().split("==")[0] for r in packages.split()]
missing_package = False
nt_elevate_missing_package = False

for package in required_packages:
    if package not in installed_packages:
        missing_package = True
        print(
            "Missing required package! Lamia will install the missing packages automatically\nWait..."
        )
        sleep(0.5)

try:
    if os.name == "nt":
        from elevate import elevate

        # TODO elevate()
except ModuleNotFoundError:
    nt_elevate_missing_package = True
    subprocess.call(
        "pip install elevate==0.1.3", stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL
    )
except OSError:
    print("Exit...")
    sys.exit(0)

try:
    import requests
except (ImportError, ModuleNotFoundError):
    subprocess.call(
        "pip install requests==2.26.0", stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL
    )

try:
    from pythonping import ping
except (NameError, ModuleNotFoundError):
    subprocess.call(
        "pip install pythonping==1.1.0", stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL
    ) if os.name == "nt" else subprocess.call(
        "pip3 install pythonping==1.1.0",
        shell=True,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )
try:
    import getmac
except (ImportError, ModuleNotFoundError):
    subprocess.call(
        "pip install getmac==0.8.2", stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL
    ) if os.name == "nt" else subprocess.call(
        "pip3 install getmac==0.8.2",
        shell=True,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )
try:
    import paramiko
except (ImportError, ModuleNotFoundError):
    subprocess.call(
        "pip install paramiko==2.7.2", stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL
    ) if os.name == "nt" else subprocess.call(
        "pip3 install paramiko==2.7.2",
        shell=True,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )
try:
    from colorama import init
except (ImportError, ModuleNotFoundError):
    subprocess.call(
        "pip install colorama==0.4.4", stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL
    ) if os.name == "nt" else subprocess.call(
        "pip3 install colorama==0.4.4",
        shell=True,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )
try:
    from pyfiglet import figlet_format
except (ImportError, ModuleNotFoundError):
    subprocess.call(
        "pip install pyfiglet==0.8.post1", stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL
    ) if os.name == "nt" else subprocess.call(
        "pip3 install pyfiglet==0.8.post1",
        shell=True,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )
try:
    from frozendict import frozendict
except (ImportError, ModuleNotFoundError):
    subprocess.call(
        "pip install frozendict==1.2", stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL
    ) if os.name == "nt" else subprocess.call(
        "pip3 install frozendict==1.2",
        shell=True,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )

if os.name == "nt":
    try:
        import pynput
    except (ImportError, ModuleNotFoundError):
        subprocess.call(
            "pip install pynput==1.7.3", stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL
        )
    try:
        import pythoncom
    except (ImportError, ModuleNotFoundError):
        subprocess.call(
            "pip install pywin32==227", stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL
        )
    try:
        from geolite2 import geolite2
    except (ImportError, ModuleNotFoundError):
        subprocess.call(
            "pip install maxminddb-geolite2==2018.703",
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )

if missing_package or nt_elevate_missing_package:
    os.execv(
        sys.executable, ["python3"] + [os.path.basename(__file__)]
    ) if os.name != "nt" else os.execv(sys.executable, ["python"] + [sys.argv[0]])
