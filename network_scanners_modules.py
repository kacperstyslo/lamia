import user_information_module
from automatic_installation_module import *
from ports_and_services import CollectionOfPortsAndServices
from exceptions import PortNumberToSmallError, PortNumberToLargeError


class NetworkScannerModules(user_information_module.UserInfo, CollectionOfPortsAndServices):
    """
    This module I created from scratch allows you to thoroughly scan the network you are connected to.
    By using one of three modules you can get different information about remote computers for
    example:
    -IP address
    -MAC address
    -Hostname
    -Operating system name
    -Opened ports and services names running on this ports
    """

    start_time: float

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __init__(self, scanned_areas):
        super().__init__()
        self.scanned_network_areas: list = scanned_areas
        self.again: int = 0
        self.recommended_network_area_to_scan: str = ".".join(self.user_ip.split(".")[0:3])
        self.ip_of_scanned_pc: str = ""
        self.hostname_of_scanned_pc: str = ""
        self.mac_of_scanned_pc: str = ""
        self.system_of_scanned_pc: str = ""
        self.network_scanner_module_choice = None
        self.port: int = 0
        self.port_range: int = 0
        self.type_of_port_scanning: bool = True
        self.scanner_output_save_path: str = (
            rf"C:\Users\{self.user_hostname}\Desktop\ActiveHosts.txt"
            if os.name == "nt"
            else rf"/root/ActiveHosts.txt"
        )
        self.service: str = ""
        self.network_scanner_module: str = ""
        self.open_ports_and_services: Dict[str, str] = {}
        self.force_exit: bool = False

    def network_scanner_modules_menu(self):
        if self.again == 0:
            network_scanner_load_message = (
                f"{Bcolors.magenta}Network Scanner{Bcolors.endc} is starts up...."
            )
            for char in network_scanner_load_message:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.05)
            time.sleep(1.5)
        Clear.clear()
        print(20 * "-" + f"{Bcolors.magenta}NETWORK SCANNER MENU{Bcolors.endc}" + 20 * "-")
        print(f"{Bcolors.warning}1.QUICK MODULE{Bcolors.endc}")
        print(f"{Bcolors.warning}2.INTENSE MODULE{Bcolors.endc}")
        print(f"{Bcolors.warning}3.SINGLE TARGET MODULE{Bcolors.endc}")
        print(f"{Bcolors.warning}0.BACK TO MAIN MENU{Bcolors.endc}")
        print(60 * "-")
        try:
            network_scanner_menu_options = [1, 2, 3, 0]
            self.network_scanner_module_choice = int(input("> "))
            check_options = [
                option == self.network_scanner_module_choice
                for option in network_scanner_menu_options
            ]
            if not any(check_options):
                print(f"{Bcolors.error_r}WRONG{Bcolors.endc} there is no such option!")
                time.sleep(2)
                self.again = 1
                self.network_scanner_modules_menu()
        except ValueError:
            print(
                f"{Bcolors.error_r}INVALID{Bcolors.endc} input data type! Data type must be "
                f"{Bcolors.warning}int{Bcolors.endc} type."
            )
            time.sleep(2.5)
            self.again = 1
            self.network_scanner_modules_menu()
        Clear.clear()
        if self.network_scanner_module_choice == 1:
            self.force_exit = True
            NetworkScannerModuleQuick(
                self.scanned_network_areas
            ).network_scanner_quick_module_start()
        elif self.network_scanner_module_choice == 2:
            self.force_exit = True
            NetworkScannerModuleIntense().network_scanner_module_intense_start()
        elif self.network_scanner_module_choice == 3:
            print(
                24 * "-"
                + f"{Bcolors.magenta}NETWORK SCANNER SINGLE TARGET MODULE{Bcolors.endc}"
                + 24 * "-"
            )
            print(
                f"This script will thoroughly scan one selected host.\n"
                f"If the host is in the network, the script will receive:\n"
                f"-{Bcolors.warning}IP ADDRESS{Bcolors.endc}\n-{Bcolors.warning}MAC ADDRESS{Bcolors.endc}\n"
                f"-{Bcolors.warning}HOSTNAME{Bcolors.endc}\n-{Bcolors.warning}OPERATING SYSTEM NAME{Bcolors.endc}\n"
                f"Script will also quickly scan 9999 {Bcolors.warning}PORTS{Bcolors.endc}, if any is {Bcolors.pass_g}"
                f"OPEN{Bcolors.endc} it will try to \n"
                f"detect a {Bcolors.warning}SERVICE{Bcolors.endc} running on that port.\n"
            )
            print(f"Do you want to continue? {Bcolors.warning}y/n{Bcolors.endc}")
            print(84 * "-")
            network_scanner_single_target_module_start_choice = str(input("> "))
            Clear.clear()
            if network_scanner_single_target_module_start_choice.lower() == "y":
                self.again = 2
            elif network_scanner_single_target_module_start_choice.lower() == "n":
                self.network_scanner_modules_menu()
            else:
                self.again = 2
                print(f"{Bcolors.error_r}WRONG{Bcolors.endc} option!")
                time.sleep(1)
                self.network_scanner_modules_menu()
        elif not self.network_scanner_module_choice:
            self.force_exit = True

        if not self.force_exit:
            self.type_of_port_scanning = False
            while len(self.ip_of_scanned_pc) != 4:
                Clear.clear()
                print(
                    f"Below enter {Bcolors.warning}IP{Bcolors.endc} of computer what you want to scan"
                )
                print(48 * "-")
                NetworkScannerModuleSingleTarget.target_ip = str(input("> "))
                self.ip_of_scanned_pc = NetworkScannerModuleSingleTarget.target_ip
                self.ip_of_scanned_pc = self.ip_of_scanned_pc.split(".")
                Clear.clear()
                if len(self.ip_of_scanned_pc) != 4:
                    print(f"{Bcolors.error_r}WRONG{Bcolors.endc} IP address!")
                    time.sleep(2)
                else:
                    command = ping(NetworkScannerModuleSingleTarget.target_ip, timeout=0.1, count=1)
                    if not command.success():
                        print(
                            f"{Bcolors.error_r}ERROR{Bcolors.endc} Host with IP: {Bcolors.warning}"
                            f"{NetworkScannerModuleSingleTarget.target_ip}{Bcolors.endc} is down!"
                        )
                        time.sleep(2)
                        self.ip_of_scanned_pc = ""
            self.ip_of_scanned_pc = NetworkScannerModuleSingleTarget.target_ip
            Clear.clear()
            print(
                f"{Bcolors.warning}WAIT{Bcolors.endc} the script scans this {Bcolors.warning}"
                f"{NetworkScannerModuleSingleTarget.target_ip}{Bcolors.endc} IP address\n"
            )
            self.network_scanner_main_scanning_function()
            NetworkScannerModuleSingleTarget().single_target_scanner(777)

    @staticmethod
    def ip_address_verifier() -> List[str]:
        while True:
            ip_to_verify = list(filter(None, str(input("> ")).split(".")))
            if 3 <= len(ip_to_verify) <= 4:
                correct_ip = (
                    ".".join(ip_to_verify) + "."
                    if len(ip_to_verify) == 3
                    else ".".join(ip_to_verify[:-1]) + "."
                )
                return [f"{correct_ip}{num}" for num in range(1, 255)]
            else:
                print(
                    f"You have entered a {Bcolors.error_r}invalid{Bcolors.endc} network area, "
                    f"script can't generate ip addresses to scan!"
                )

    def network_scanner_main_scanning_function(self):
        command = ping(self.ip_of_scanned_pc, timeout=0.1, count=1)
        param = "-n" if platform.system().lower() == "windows" else "-c"
        param2 = "-w" if platform.system().lower() == "windows" else "-c"
        if platform.system().lower() == "windows":
            command_after = ["ping", param, "1", param2, "100", self.ip_of_scanned_pc]
        else:
            command_after = ["ping", param, "1", self.ip_of_scanned_pc]
        try:
            if command.success():
                print(
                    "\n" + 31 * "-" + f"{Bcolors.pass_g}{self.ip_of_scanned_pc}{Bcolors.endc} is "
                    f"{Bcolors.pass_g}ACTIVE{Bcolors.endc}" + 31 * "-"
                )
                print(
                    f"Script will try to get more information about host "
                    f"{Bcolors.warning}{self.ip_of_scanned_pc}{Bcolors.endc} ...."
                )
                if "TTL" in subprocess.check_output(command_after).decode(
                    "UTF-8"
                ) or "ttl" in subprocess.check_output(command_after).decode("UTF-8"):
                    self.mac_of_scanned_pc = getmac.get_mac_address(ip=str(self.ip_of_scanned_pc))
                    self.network_scanner_get_remote_hostname()
                    if not self.mac_of_scanned_pc:
                        self.mac_of_scanned_pc = getmac.get_mac_address()
                    if "128" in subprocess.check_output(command_after).decode("UTF-8"):
                        self.system_of_scanned_pc = "Windows"
                        print(
                            f"{Bcolors.endc}Platform: {Bcolors.warning}{self.system_of_scanned_pc}{Bcolors.endc} "
                            f"Hostname: {Bcolors.warning}{self.hostname_of_scanned_pc}{Bcolors.endc}  "
                            f"IP: {Bcolors.warning}{self.ip_of_scanned_pc}{Bcolors.endc}  "
                            f"MAC: {Bcolors.warning}{self.mac_of_scanned_pc}{Bcolors.endc}"
                        )
                        if self.type_of_port_scanning:
                            self.network_scanner_check_open_ports()
                    elif "64" in subprocess.check_output(command_after).decode("UTF-8"):
                        self.system_of_scanned_pc = "Linux"
                        print(
                            f"{Bcolors.endc}Platform: {Bcolors.warning}{self.system_of_scanned_pc}{Bcolors.endc} "
                            f"Hostname: {Bcolors.warning}{self.hostname_of_scanned_pc}{Bcolors.endc}  "
                            f"IP: {Bcolors.warning}{self.ip_of_scanned_pc}{Bcolors.endc}  "
                            f"MAC: {Bcolors.warning}{self.mac_of_scanned_pc}{Bcolors.endc}"
                        )
                        if self.type_of_port_scanning:
                            self.network_scanner_check_open_ports()
                    if self.type_of_port_scanning:
                        NetworkScannerModuleIntense.network_scanner_module_intense_save_output(self)
                else:
                    print(
                        f"Most likely Device with IP: {self.ip_of_scanned_pc} is {Bcolors.error_r}"
                        f"turned off.{Bcolors.endc}"
                    )
                    print(f"\n")
        except subprocess.CalledProcessError:
            pass

    def network_scanner_check_open_ports(self):
        for self.port in range(1, self.port_range):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.0001)
            result = sock.connect_ex(
                (
                    self.ip_of_scanned_pc,
                    self.port,
                )
            )
            for port, service in self.all_ports_and_services.items():
                if port == self.port:
                    self.service = service
            if not result:
                print(
                    f"Host {Bcolors.warning}{self.hostname_of_scanned_pc}{Bcolors.endc} "
                    f"with IP: {Bcolors.warning}{self.ip_of_scanned_pc}{Bcolors.endc} "
                    f"has an open port number: {Bcolors.warning}{self.port}{Bcolors.endc}. "
                    f"Service: {Bcolors.warning}{self.service}{Bcolors.endc}"
                )
                self.open_ports_and_services.update({f"{self.port}": self.service})
            sock.close()
        print(84 * "=" + "\n")

    def network_scanner_get_remote_hostname(self):
        try:
            self.hostname_of_scanned_pc = socket.gethostbyaddr(self.ip_of_scanned_pc)[0]
        except socket.herror:
            self.hostname_of_scanned_pc = "Unknown"
            print(
                f"Device with IP: {self.ip_of_scanned_pc} is in {Bcolors.error_r}drop mode{Bcolors.endc}. "
                f"Script can't find HOSTNAME"
            )


class NetworkScannerModuleQuick(NetworkScannerModules):
    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __init__(self, scanned_areas):
        super().__init__(scanned_areas)
        self.scanned_network_areas = scanned_areas

    def network_scanner_quick_module_start(self):
        Clear.clear()
        print(28 * "-" + f"{Bcolors.magenta}NETWORK SCANNER QUICK MODULE{Bcolors.endc}" + 28 * "-")
        print(
            f"{Bcolors.magenta}QUICK{Bcolors.endc} module will find all {Bcolors.pass_g}ACTIVE{Bcolors.endc} "
            f"hosts in chosen network and display\nthier {Bcolors.warning}IP{Bcolors.endc} address.\n"
        )
        print(f"Do you want to continue? {Bcolors.warning}y/n{Bcolors.endc}")
        print(84 * "-")
        network_scanner_quick_module_start_choice = str(input("> "))
        Clear.clear()
        if network_scanner_quick_module_start_choice.lower() == "y":
            NetworkScannerModuleQuick(
                self.scanned_network_areas
            ).network_scanner_quick_module_scanner()
        elif network_scanner_quick_module_start_choice.lower() == "n":
            self.again = 1
            self.network_scanner_modules_menu()
        else:
            print(f"{Bcolors.error_r}Wrong{Bcolors.endc} option!")
            time.sleep(2)
            self.network_scanner_quick_module_start()

    def network_scanner_quick_module_scanner(self):
        print(28 * "-" + f"{Bcolors.magenta}NETWORK SCANNER QUICK MODULE{Bcolors.endc}" + 28 * "-")
        if self.scanned_network_areas.__len__() > 0:
            print(
                f"Script found networks areas where probably work devices with\n"
                f"internet connection. Do you want to see this network areas? {Bcolors.warning}y/n{Bcolors.endc}"
            )
            print(84 * "-")
            show_possible_networks = str(input("> "))
            if show_possible_networks.upper() == "Y":
                for possible_n in self.scanned_network_areas:
                    print(
                        f"Possible network area with active devices: {Bcolors.warning}{possible_n}{Bcolors.endc}"
                    )
                print(84 * "-")
            else:
                Clear.clear()
                print(
                    28 * "-"
                    + f"{Bcolors.magenta}NETWORK SCANNER QUICK MODULE{Bcolors.endc}"
                    + 28 * "-"
                )
        print(f"YOUR IP ADDRESS: {Bcolors.warning}{self.user_ip}{Bcolors.endc}")
        print(
            f"{Bcolors.warning}RECOMMENDED{Bcolors.endc} If you want to scan your network enter "
            f"{Bcolors.warning}{self.recommended_network_area_to_scan}{Bcolors.endc}\n"
            f"If you want to scan other network area just enter IP address from other network area."
        )
        print(84 * "-")
        pool_of_ip_addresses_to_scanned = self.ip_address_verifier()
        self.start_time = time.time()
        ip_active: List[str] = []
        try:
            for single_target in pool_of_ip_addresses_to_scanned:
                if single_target == pool_of_ip_addresses_to_scanned[-1]:
                    print()
                    if len(ip_active) < 5:
                        print(
                            f"The script will try to find more hosts, {Bcolors.warning}WAIT{Bcolors.endc}...\n"
                        )
                        for another_single_target in pool_of_ip_addresses_to_scanned:
                            if another_single_target == pool_of_ip_addresses_to_scanned[-1]:
                                print()
                                if not ip_active:
                                    print(
                                        f"Script can't find any active host in given network area. Use"
                                        f"{Bcolors.magenta}INTENSE MODULE{Bcolors.endc} or scan other network area."
                                    )
                                    os.system("pause") if os.name == "nt" else input(
                                        "Press enter to continue..."
                                    )
                                else:
                                    print(f"{Bcolors.pass_g}FINISHED SCAN!{Bcolors.endc}")
                                    print(
                                        f"Execution time: {Bcolors.warning}%s{Bcolors.endc} seconds"
                                        % round((time.time() - self.start_time), 2)
                                    )
                                    os.system("pause") if os.name == "nt" else input(
                                        "Press enter to continue..."
                                    )

                            command = ping(f"{another_single_target}", timeout=0.1, count=1)
                            if command.success():
                                ip_active.append(another_single_target)
                                print(
                                    f"Host with IP:{Bcolors.warning} {another_single_target}{Bcolors.endc} "
                                    f"is {Bcolors.pass_g}ACTIVE.{Bcolors.endc}"
                                )
                    else:
                        print(f"{Bcolors.pass_g}FINISHED SCAN!{Bcolors.endc}")
                        print(
                            f"Execution time: {Bcolors.warning}%s{Bcolors.endc} seconds"
                            % round((time.time() - self.start_time), 2)
                        )
                        os.system("pause") if os.name == "nt" else input(
                            "Press enter to continue..."
                        )

                command = ping(f"{single_target}", timeout=0.01, count=1)
                if command.success():
                    ip_active.append(single_target)
                    print(
                        f"Host with IP:{Bcolors.warning} {single_target}{Bcolors.endc} "
                        f"is {Bcolors.pass_g}ACTIVE.{Bcolors.endc}"
                    )
        finally:
            Clear.clear()
            if ip_active.__len__() != 0:
                print(
                    27 * "-"
                    + f"{Bcolors.magenta}ALL DISCOVERED ACTIVE DEVICES{Bcolors.endc}"
                    + 27 * "-"
                )
                ip_active = sorted(list(dict.fromkeys(ip_active)))
                while ip_active:
                    print(
                        f"Host with IP: {Bcolors.warning}{[active_host for active_host in ip_active][0]}"
                        f"{Bcolors.endc} is {Bcolors.pass_g}ACTIVE.{Bcolors.endc}"
                    )
                    del ip_active[0]
                print(83 * "-")
                os.system("pause") if os.name == "nt" else input("Press enter to continue...")


class NetworkScannerModuleIntense(NetworkScannerModules):
    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __init__(self):
        super().__init__(NetworkScannerModules)

    def network_scanner_module_intense_start(self):
        Clear.clear()
        print(
            27 * "-" + f"{Bcolors.magenta}NETWORK SCANNER INTENSE MODULE{Bcolors.endc}" + 27 * "-"
        )
        print(
            f"{Bcolors.magenta}INTENSE{Bcolors.endc} module will search for {Bcolors.pass_g}ACTIVE{Bcolors.endc}"
            f" hosts  in chosen network, if it\nhits the {Bcolors.pass_g}ACTIVE{Bcolors.endc} host,it will try\n"
            f"to get as much information as possible about this active host."
        )
        print(
            f"For example, this script will try to find the:\n"
            f"-{Bcolors.warning}IP ADDRESS{Bcolors.endc}\n-{Bcolors.warning}MAC ADDRESS{Bcolors.endc}\n"
            f"-{Bcolors.warning}HOSTNAME{Bcolors.endc}\n-{Bcolors.warning}OPERATING SYSTEM NAME{Bcolors.endc}\n"
            f"This script will search for all {Bcolors.pass_g}OPEN {Bcolors.endc}{Bcolors.warning}PORTS{Bcolors.endc}"
            f" on this {Bcolors.pass_g}ACTIVE{Bcolors.endc} host,\n"
            f"if any are {Bcolors.pass_g}OPEN{Bcolors.endc} it will try to find out what {Bcolors.warning}"
            f"SERVICES{Bcolors.endc} work on these ports.\n"
        )
        print(f"Do you want to continue? {Bcolors.warning}Y/N{Bcolors.endc}")
        print(84 * "-")
        network_scanner_module_intense_start_choice = str(input("> "))
        Clear.clear()
        if network_scanner_module_intense_start_choice.lower() == "y":
            print(
                27 * "-"
                + f"{Bcolors.magenta}NETWORK SCANNER INTENSE MODULE{Bcolors.endc}"
                + 27 * "-"
            )
            print(
                f"Script will save all results in this location: {Bcolors.warning}{self.scanner_output_save_path}"
                f"{Bcolors.endc}{Bcolors.endc}\n"
            )
            os.system("pause") if os.name == "nt" else input("Press enter to continue...")
            NetworkScannerModuleIntense().network_scanner_module_intense_scanner()
        elif network_scanner_module_intense_start_choice.lower() == "n":
            self.again = 1
            self.network_scanner_modules_menu()
        else:
            print(f"{Bcolors.error_r}Wrong{Bcolors.endc} option!")
            time.sleep(2)
            self.network_scanner_module_intense_start()

    def network_scanner_module_intense_save_output(self):
        with open(self.scanner_output_save_path, "a") as fp:
            fp.write(38 * "=" + "\n")
            fp.write(f"Platform: {self.system_of_scanned_pc}" + "\n")
            fp.write(f"HOST: {self.hostname_of_scanned_pc}" + "\n")
            fp.write(f"IP: {self.ip_of_scanned_pc}" + "\n")
            fp.write(f"MAC: {self.mac_of_scanned_pc}" + "\n")
            for self.port in self.open_ports_and_services:
                fp.write(
                    f"Port: {self.port}"
                    + " "
                    + " Service: "
                    + self.open_ports_and_services[self.port]
                    + "\n"
                )
            self.open_ports_and_services.clear()

    def network_scanner_module_intense_get_port_range(self):
        while True:
            print(
                27 * "-"
                + f"{Bcolors.magenta}NETWORK SCANNER INTENSE MODULE{Bcolors.endc}"
                + 27 * "-"
            )
            print(f"How many {Bcolors.warning}PORTS{Bcolors.endc} do you want to scan? 1-9999")
            try:
                print(84 * "-")
                self.port_range: int = int(input("> "))
                if 0 < self.port_range < 10000:
                    break
                elif self.port_range > 9999:
                    print(PortNumberToLargeError(self.port_range))
                elif self.port_range <= 0:
                    print(PortNumberToSmallError(self.port_range))
            except ValueError:
                print(f"The given value is not an {Bcolors.error_r}int{Bcolors.endc} type !")
            time.sleep(2.5)
            Clear.clear()

    def network_scanner_module_intense_scanner(self):
        Clear.clear()
        self.network_scanner_module_intense_get_port_range()
        Clear.clear()
        print(
            27 * "-" + f"{Bcolors.magenta}NETWORK SCANNER INTENSE MODULE{Bcolors.endc}" + 27 * "-"
        )
        print(f"YOUR IP ADDRESS: {Bcolors.warning}{self.user_ip}{Bcolors.endc}")
        print(
            f"{Bcolors.warning}RECOMMENDED{Bcolors.endc} If you want to scan your network type "
            f"{Bcolors.warning}{self.recommended_network_area_to_scan}{Bcolors.endc}"
        )
        self.start_time = time.time()
        pool_of_ip_addresses_to_scanned = self.ip_address_verifier()

        for self.ip_of_scanned_pc in pool_of_ip_addresses_to_scanned:
            if self.ip_of_scanned_pc == pool_of_ip_addresses_to_scanned[-1]:
                print()
                print(f"{Bcolors.pass_g}FINISHED SCAN!{Bcolors.endc}")
                print(
                    f"Execution time: {Bcolors.warning}%s{Bcolors.endc} seconds"
                    % round((time.time() - self.start_time), 2)
                )
                os.system("pause") if os.name == "nt" else input("Press enter to continue...")
                Clear.clear()
                os.system(
                    fr"more {self.scanner_output_save_path}"
                ) if os.name == "nt" else os.system(fr"less {self.scanner_output_save_path}")
                print(
                    f"\nAll results are saved here: {Bcolors.pass_g}{self.scanner_output_save_path}{Bcolors.endc}"
                )
                input("Press enter to continue...")
                input()
            self.network_scanner_main_scanning_function()


class NetworkScannerModuleSingleTarget(NetworkScannerModules):
    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __init__(self):
        super(NetworkScannerModules, self).__init__()

    queue: Queue = Queue()
    single_target_open_ports: List[int] = []
    target_ip: str = ""
    ports_percentage: Dict[int, str] = {
        999: "10%",
        1999: "20%",
        2999: "30%",
        3999: "40%",
        4999: "50%",
        5999: "60%",
        6999: "70%",
        7999: "80%",
        8999: "90%",
    }

    @staticmethod
    def single_target_restart_line():
        sys.stdout.write("\r")
        sys.stdout.flush()

    @staticmethod
    def single_target_port_scan_with_threads(port):
        for key, value in NetworkScannerModuleSingleTarget.ports_percentage.items():
            if port == key:
                sys.stdout.write(f"{value} of all ports is scanned!")
                sys.stdout.flush()
                NetworkScannerModuleSingleTarget.single_target_restart_line()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((NetworkScannerModuleSingleTarget.target_ip, port))
            sock.settimeout(0.5)
            return True
        except (ConnectionRefusedError, OSError):
            pass

    @staticmethod
    def single_target_get_ports():
        for port in range(1, 9999):
            NetworkScannerModuleSingleTarget.queue.put(port)

    @staticmethod
    def single_target_worker():
        while not NetworkScannerModuleSingleTarget.queue.empty():
            port = NetworkScannerModuleSingleTarget.queue.get()
            if NetworkScannerModuleSingleTarget.single_target_port_scan_with_threads(port):
                NetworkScannerModuleSingleTarget.single_target_open_ports.append(port)

    @staticmethod
    def single_target_scanner(threads):

        NetworkScannerModuleSingleTarget.single_target_get_ports()
        thread_list = []

        for _ in range(threads):
            thread = Thread(target=NetworkScannerModuleSingleTarget.single_target_worker)
            thread_list.append(thread)

        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()

        NetworkScannerModuleSingleTarget().single_target_port_output()

    def single_target_port_output(self):
        while len(NetworkScannerModuleSingleTarget.single_target_open_ports):
            port_and_service = next(
                (
                    (port, service)
                    for port, service in self.all_ports_and_services.items()
                    if port == NetworkScannerModuleSingleTarget.single_target_open_ports[0]
                ),
                None,
            )
            if port_and_service is None:
                port, service = (
                    NetworkScannerModuleSingleTarget.single_target_open_ports[0],
                    "Unknown",
                )
            else:
                port, service = port_and_service
            print(
                f"Host {Bcolors.warning}HOSTNAME{Bcolors.endc} with IP: "
                f"{Bcolors.warning}{NetworkScannerModuleSingleTarget.target_ip}{Bcolors.endc} has an open port number: "
                f"{Bcolors.warning}{port}{Bcolors.endc}. Service: {Bcolors.warning}{service}{Bcolors.endc}"
            )
            del NetworkScannerModuleSingleTarget.single_target_open_ports[0]
        print()
        os.system("pause") if os.name == "nt" else input("Press any key to continue...")
