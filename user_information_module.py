from automatic_installation_module import *


class UserInfo:
    """
    This module checks the compatibility of the user's device and saves the necessary data.
    """

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __init__(self):
        super().__init__()
        self.user_hostname: str = getpass.getuser()
        self.user_ip: str = socket.gethostbyname(socket.gethostname())
        self.user_mac: str = getmac.get_mac_address()
        self.user_operating_system_name: str = platform.system() + " " + platform.release()
        self.user_operating_system_version: str = platform.version()
        try:
            self.user_public_ip: str = requests.get("https://api.ipify.org").text
        except requests.exceptions.ConnectionError:
            self.user_public_ip = "Unknown"
        self.city: str = ""
        self.country: str = ""
        self.location: Dict[str, str] = {}
        self.latitude: str = ""
        self.longitude: str = ""

    def user_information(self):
        time.sleep(1)
        Clear.clear()
        if os.name == "posix":
            permissions = os.getuid()
            if permissions != 0:
                print(
                    f"{Bcolors.error_r}ERROR!{Bcolors.endc}You must run script as root! "
                    f"Write: {Bcolors.warning}sudo python3 refactor_file.py{Bcolors.endc}"
                )
                time.sleep(3)
                sys.exit(0)

        if os.name == "nt" and self.user_public_ip != "Unknown":
            reader = geolite2.reader()
            location = reader.get(self.user_public_ip)
            try:
                self.city = location["city"]["names"]["en"]
            except KeyError:
                self.city = "Unknown"
            self.country = location["country"]["names"]["en"]
            self.location = location["location"]
            self.latitude, self.longitude = self.location["latitude"], self.location["longitude"]

            print(19 * "-" + f"{Bcolors.warning}WAIT !{Bcolors.endc}" + 19 * "-")
            time.sleep(0.25)
            print(
                f"Platform: {self.user_operating_system_name}"
                + f"{Bcolors.pass_g} OK!{Bcolors.endc}"
            )
            time.sleep(0.25)
            print(
                f"Version: {self.user_operating_system_version}"
                + f"{Bcolors.pass_g} OK!{Bcolors.endc}"
            )
            time.sleep(0.25)
            if self.user_ip != "127.0.0.1":
                print("IP:", self.user_ip, f"{Bcolors.pass_g} OK!{Bcolors.endc}")
                time.sleep(0.25)
                try:
                    if self.user_public_ip != "Unknown":
                        print(
                            f"Public IP: {self.user_public_ip}",
                            f"{Bcolors.pass_g} OK!{Bcolors.endc}",
                        )
                except AttributeError:
                    print(
                        f"Public IP: {self.user_public_ip}",
                        f"{Bcolors.error_r} CAN'T FIND!{Bcolors.endc}",
                    )

            time.sleep(0.25)
            print("MAC:", self.user_mac + f"{Bcolors.pass_g} OK!{Bcolors.endc}")
            time.sleep(0.25)
            if os.name == "nt" and self.user_public_ip != "Unknown":
                print("Country:", self.country + f"{Bcolors.pass_g} FIND!{Bcolors.endc}")
                time.sleep(0.25)
                if self.city != "Unknown":
                    print("City:", self.city + f"{Bcolors.pass_g} FIND!{Bcolors.endc}")
                    time.sleep(0.25)
                print(
                    f"Latitude: {self.latitude} | Longitude: {self.longitude}"
                    + f"{Bcolors.pass_g} FIND!{Bcolors.endc}"
                )
                time.sleep(0.25)
            print(20 * "-" + f"{Bcolors.pass_g}OK !{Bcolors.endc}" + 20 * "-")
            os.system("pause") if os.name == "nt" else input("Press any key to continue...")
