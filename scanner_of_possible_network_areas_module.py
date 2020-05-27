from threading import Thread

from pythonping import ping

import user_information_module
from automatic_installation_module import *


class PossibleAreaNetworks(user_information_module.UserInfo):
    """
    This module runs in the background and scans for possible subnets which we can later scan using
    one of Network Scanner Modules.
    """

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __call__(self) -> List[str]:
        return self.scanned_networks

    def __init__(self):
        super().__init__()
        self.scanned_networks: List[str] = []
        thread = Thread(target=self.scan_possible_area_networks, args=())
        thread.daemon = True
        thread.start()

    def scan_possible_area_networks(self):
        possible_area: List[str] = []
        parts_ip: List[str] = self.user_ip.split(".")
        for num in range(0, 256):
            if num == 255:
                pass
            ip = f"{parts_ip[0] + '.' + parts_ip[1] + '.'}{num}.1"
            command = ping(f"{ip}", timeout=0.1, count=1)
            if command.success():
                possible_area.append(ip)
        self.scanned_networks = list(dict.fromkeys(possible_area))
