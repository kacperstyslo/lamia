from automatic_installation_module import *


class PortNumberToSmallError(Exception, Bcolors):
    def __init__(self, port_value: int):
        self.port_value: int = port_value

    def __str__(self):
        return (
            f"Typed port value: {Bcolors.error_r}{self.port_value}{Bcolors.endc} is too small! "
            f"Minimum port value is {Bcolors.pass_g}1{Bcolors.endc}!"
        )


class PortNumberToLargeError(Exception, Bcolors):
    def __init__(self, port_value: int):
        self.port_value: int = port_value

    def __str__(self):
        return (
            f"Typed port value: {Bcolors.error_r}{self.port_value}{Bcolors.endc} is too big! "
            f"Maximum port value is {Bcolors.pass_g}9999{Bcolors.endc}!"
        )
