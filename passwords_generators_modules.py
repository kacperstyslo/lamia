import user_information_module
from automatic_installation_module import *


class PasswordsGeneratorModules(user_information_module.UserInfo):
    """
    Using this module you can create all combination of PIN's and also creating random passwords
    for brute force attack.
    """

    start_time: float

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __init__(self):
        super().__init__()
        self.check_default_choice_pin: str = ""
        self.PIN: str = (
            rf"C:\Users\{self.user_hostname}\Desktop\PIN.txt"
            if os.name == "nt"
            else rf"/root/PIN.txt"
        )
        self.password_save: str = (
            rf"C:\Users\{self.user_hostname}\Desktop\PASSWORDS.txt"
            if os.name == "nt"
            else rf"/root/PASSWORDS.txt"
        )

    def password_generator_start(self):
        print(70 * "-")
        print(
            f"This module allows you to {Bcolors.warning}GENERATE ALL PASSWORD COMBINATION{Bcolors.endc}\n"
            f"of the symbols given. Do you want to continue {Bcolors.warning}y/n{Bcolors.endc}?"
        )
        print(70 * "-")
        password_generator_start_choice = str(input("> "))
        if password_generator_start_choice.lower() == "y":
            self.passwords_generator_modules_menu()
        elif not password_generator_start_choice.lower() == "n":
            print(f"{Bcolors.error_r}WRONG OPTION!{Bcolors.endc}")
            time.sleep(1.5)

    @staticmethod
    def passwords_generator_modules_menu():
        Clear.clear()
        print(22 * "-" + f"{Bcolors.magenta}PASSWORD GENERATOR MODULE{Bcolors.endc}" + 22 * "-")
        print(f"{Bcolors.warning}1.Password generator{Bcolors.endc}")
        print(f"{Bcolors.warning}2.PIN generator{Bcolors.endc}")
        print(f"{Bcolors.warning}0.BACK TO MAIN MENU{Bcolors.endc}")
        print(70 * "-")
        password_generator_menu_choice = int(input("> ")) - 1
        password_generator_choice_options: list = [
            PasswordsGeneratorModules().password_generator_characters_choice,
            PasswordsGeneratorModules().pin_generator,
        ]
        if -1 < password_generator_menu_choice < 2:
            password_generator_choice_options[password_generator_menu_choice]()

    def password_generator_characters_choice(self):
        Clear.clear()
        print(
            20 * "-" + f"{Bcolors.magenta}PASSWORD GENERATOR MODULE MENU{Bcolors.endc}" + 20 * "-"
        )
        print("Select the characters of which the password will consist")
        print(
            f"{Bcolors.warning}1. [{','.join([letter for letter in ascii_lowercase])}]{Bcolors.endc}\n"
        )
        print(
            f"{Bcolors.warning}2.[{','.join([letter for letter in ascii_lowercase])}"
            f"!,@,#,$,%,^,&,\n*,(,),=,+,.,?,~]{Bcolors.endc}\n"
        )
        print(
            f"{Bcolors.warning}3.[{','.join([letter for letter in ascii_uppercase])}]{Bcolors.endc}\n"
        )
        print(
            f"{Bcolors.warning}4.[{','.join([letter for letter in ascii_lowercase])}\n"
            f"{','.join([letter for letter in ascii_uppercase])}"
            f"!,@,#,$,%,^,&,\n*,(,),=,+,.,?,~]{Bcolors.endc}\n"
        )
        print(
            f"{Bcolors.warning}5.[{','.join([letter for letter in ascii_lowercase])}\n"
            f"{','.join([letter for letter in ascii_uppercase])}!,@,#,$,%,^,&,*,(,),=,+,.,?,~]{Bcolors.endc}\n"
        )
        print(f"{Bcolors.warning}0.BACK TO MAIN MENU{Bcolors.endc}")
        print(70 * "-")
        password_characters_choice = int(input("> "))
        collection_of_characters: Dict[int, str] = {
            0: None,
            1: f"{ascii_lowercase}",
            2: f"{ascii_lowercase}!@#$%^&*()=+.?~",
            3: f"{ascii_uppercase}",
            4: f"{ascii_uppercase}!@#$%^&*()=+,.?~",
            5: f"{ascii_letters}@#$%^&*()=+,.?~",
        }
        Clear.clear()
        if password_characters_choice:
            try:
                selected_characters = collection_of_characters[password_characters_choice]
                print("Enter the password length [number]: ", end="")
                password_length = int(input())
                if password_length > 25:
                    Clear.clear()
                    print(f"{Bcolors.error_r}ERROR!{Bcolors.endc} To long!\n")
                    os.system("pause") if os.name == "nt" else input("Press enter to continue...")
                    self.password_generator_characters_choice()
                print("Enter the numbers of password [number]: ", end="")
                number_of_passwords = int(input())
                self.generating_passwords_from_chosen_combination(
                    characters=selected_characters,
                    length=password_length,
                    how_many=number_of_passwords,
                )
            except KeyError:
                print(f"{Bcolors.error_r}ERROR!{Bcolors.endc} Wrong option!")
                time.sleep(1)
                self.password_generator_characters_choice()

    def add_execution_time(data_generating_function):
        def wrapper(self, **kwargs):
            start_time = time.time()
            data_generating_function(self, **kwargs)
            if len(kwargs):
                print(
                    f"{Bcolors.pass_g}\nSuccess!{Bcolors.endc} "
                    f"Script save output here {Bcolors.warning}{self.password_save}{Bcolors.endc}"
                )
                print(
                    f"Number of generated passwords: {Bcolors.warning}{kwargs['how_many']}{Bcolors.endc}"
                )
            else:
                print(
                    f"{Bcolors.pass_g}Success!{Bcolors.endc} "
                    f"Script save output here {Bcolors.warning}{self.PIN}{Bcolors.endc}"
                )
                print(f"Numbers of generated items: {Bcolors.warning}{self.c}{Bcolors.endc}")
            print(
                f"Execution time: {Bcolors.warning}%s{Bcolors.endc} seconds"
                % round((time.time() - start_time), 2)
            )
            input("Press enter to continue...")
            self.passwords_generator_modules_menu()

        return wrapper

    @add_execution_time
    def generating_passwords_from_chosen_combination(self, **kwargs):
        with open(self.password_save, "w") as f:
            [
                f.write(
                    str((random.sample(kwargs["characters"], kwargs["length"])))
                    .replace(",", "")
                    .replace("'", "")
                    .replace(" ", "")[1:-1]
                    + str(f"\n")
                )
                for _ in range(kwargs["how_many"])
            ]

    @add_execution_time
    def pin_generator(self):
        with open(self.PIN, "w") as f:
            for self.c, self.pin in enumerate(list(product(range(10), repeat=4)), 1):
                f.write(str("%s%s%s%s" % self.pin) + str(f"\n"))
