import os
import json
import sys
import winreg
import shutil
from datetime import datetime
from colorama import Style, Fore, init

init()


class JourneyRobeChanger:
    def __init__(self):
        self.default = {
            "SteamID3": None,
            "create_backup": True,
            "clear_backup": False,
            "ask_restore": True,
            "ask_clear": True
        }

        self.error_file = "error.txt"
        self.config_file = "config.json"
        self.id = self.read("SteamID3", int)
        self.create_backup = self.read("create_backup", bool)
        self.clear_backup = self.read("clear_backup", bool)
        self.ask_restore = self.read("ask_restore", bool)
        self.ask_clear = self.read("ask_clear", bool)

        self.annapurna_path = self.get_annapurna_path()
        self.steam_path = self.get_steam_id()
        self.start()

    def start(self):
        if self.clear_backup:
            self.delete_backup()
        if self.create_backup:
            self.auto_backup()
        self.update_robe()

    def read(self, key, t):
        if os.path.isfile(self.config_file):
            try:
                data = json.load(open(self.config_file))
                value = data[key]
                if isinstance(value, t):
                    return value
                else:
                    self.write(key, self.default[key])
            except json.decoder.JSONDecodeError:
                self.write_default()
            except KeyError:
                self.write(key, self.default)
        else:
            self.write_default()
            return self.default[key]

    def write(self, key, value):
        if os.path.isfile(self.config_file):
            with open(self.config_file, "r+") as file:
                try:
                    data = json.load(file)
                except json.decoder.JSONDecodeError:
                    self.write_default()
                    print("write")
                    self.write(key, value)
                    return
                try:
                    data[key] = value
                except KeyError:
                    data.update({key: value})
                json.dump(data, open(self.config_file, "w"), indent=2)
                return
        self.write_default()
        self.write(key, value)

    def write_default(self):
        print("An error was encountered while reading config.json. Resetting file to default.")
        json.dump(self.default, open(self.config_file, "w"), indent=2)

    @staticmethod
    def get_number(msg, lower, upper):
        while True:
            try:
                number = int(input(msg))
                if not (lower <= number <= upper):
                    raise ValueError
                return number
            except ValueError:
                print(f"Please input a number between {lower} and {upper}.")

    def level_select(self):
        print("""
You will start from your selected level as a T4 WR, with all symbols from previous levels collected.
These are your options:
0: Broken Bridge (BB)
1: Pink Desert   (PD)
2: Sunken City   (SC)
3: Underground   (UG)
4: Tower
5: Snow""")
        number = self.get_number("Please select. (0-5): ", 0, 5)
        level = {
            0: "CS.BIN",
            1: "PD.BIN",
            2: "SC.BIN",
            3: "UG.BIN",
            4: "TO.BIN",
            5: "SN.BIN",
        }[number]
        self.do_copy(f".\\presets\\{level}")

    def update_robe(self):
        print("""These are your options:
    0: RR (start from the very beginning)
    1: RR (start from BB)
    2: WR (CS)
    3: WR (CS)
    4: WR (CS)
    5: Level Select""")
        number = self.get_number("Please select. (0-5): ", 0, 5)
        robe = {
            0: None,
            1: "T1.BIN",
            2: "T2.BIN",
            3: "T3.BIN",
            4: "T4.BIN",
            5: None
        }[number]
        self.delete_save(self.annapurna_path)
        self.delete_save(self.steam_path)
        if 5 > number > 0:
            self.do_copy(f".\\presets\\{robe}")
        elif number == 5:
            self.level_select()

    @staticmethod
    def get_annapurna_path():
        return os.path.abspath(
            os.getenv('APPDATA').replace("\\Roaming", "") + "\\Local\\Annapurna Interactive\\Journey\\Steam")

    def get_steam_path(self):  # https://stackoverflow.com/a/58389125
        try:
            hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\WOW6432Node\\Valve\\Steam")
            steam = winreg.QueryValueEx(hkey, "InstallPath")[0]
            winreg.CloseKey(hkey)
            if not os.path.exists(steam):
                raise ValueError(f"Steam dir {steam} wasn't found after extracting from hkey.")
            return os.path.abspath(steam + "\\userdata\\")

        except Exception as e:
            self.handle_error(e)

    def get_steam_id(self):
        steam = self.get_steam_path()  # get the general path
        dirs = [x for x in os.listdir(steam)]
        if len(dirs) == 1:  # count dirs, if there's just one default to that
            user_id = dirs[0]
        else:
            if self.id is not None and os.path.exists(steam + f"\\{self.id}\\"):
                user_id = self.id
            else:
                print("""Please input your SteamID3.
Go to your steam profile page. Right-click on your profile picture, then select
"Copy Page URL". Then go to https://steamid.xyz/ and paste it into the search bar. Hit submit. 
The entry second from the top should be "Steam ID3". Copy this entry (it looks like U:1:XXXXXXXX).
Then paste this here using CTRL+V. Then press enter.""")
                user_id = input("SteamID3: ").replace("[", "").replace("]", "").replace("U:1:", "")  # get ID from user
                if os.path.exists(steam + f"\\{user_id}\\"):
                    self.write("SteamID3", int(user_id))  # write to file for future use
                else:
                    print("It seems this ID doesn't exist on this PC. Have you pasted the right one? The ID has to be "
                          "in the format of U:1:XXXXXX, do not paste it with this part only partially visible ("
                          "1:XXXXXX would be invalid). If the issue persists, follow the message below.")
                    # user probably entered the wrong ID
                    self.handle_error(f"ID {user_id} doesn't exist on this PC, aborting.")
        if os.path.exists(steam + f"\\{user_id}\\638230\\remote"):
            return steam + f"\\{user_id}\\638230\\remote"
        else:
            print("Could not find the Journey game directory. Please check if the game is installed.")
            self.handle_error("Faulty path: " + steam + f"\\{user_id}\\638230\\remote")

    @staticmethod
    def delete_save(path):
        if os.path.isfile(path + "\\SAVE.BIN"):
            os.remove(path + "\\SAVE.BIN")

    @staticmethod
    def delete_backup():
        if os.path.isfile(".\\presets\\BACKUP.BIN"):
            os.remove(".\\presets\\BACKUP.BIN")

    def do_copy(self, src):
        shutil.copyfile(src, self.steam_path + "\\SAVE.BIN")
        shutil.copyfile(src, self.annapurna_path + "\\SAVE.BIN")

    def auto_backup(self):
        files = [x for x in os.listdir("./presets")]
        if "BACKUP.BIN" not in files:  # if backup does not exist:
            st = self.steam_path + "\\SAVE.BIN"
            an = self.annapurna_path + "\\SAVE.BIN"
            src = st if os.path.isfile(st) else an if os.path.isfile(an) else None
            if src:
                shutil.copyfile(src, ".\\presets\\BACKUP.BIN")
                # if there was a save found copy it and rename it to 'backup.bin'
        else:
            if self.ask_restore:
                print(f"{Fore.RED}Backup detected.{Style.RESET_ALL} Do you wish to restore?")
                while True:
                    res = input("Restore? [y/n]: ").lower()
                    if res in ("yes", "y", "no", "n"):
                        if res in ("yes", "y"):
                            self.do_copy(".\\presets\\BACKUP.BIN")  # restore
                        break
                    else:
                        print("Invalid input.")
            if self.ask_clear:
                print("Do you wish to clear the current backup?")
                while True:
                    res = input("Clear? [y/n]: ")
                    if res in ("yes", "y", "no", "n"):
                        if res in ("yes", "y"):
                            os.remove(".\\presets\\BACKUP.BIN")  # clear
                        break
                    else:
                        print("Invalid input.")

    def handle_error(self, error):
        dt = datetime.now().strftime("[ %d.%m.%Y | %H:%M:%S ] ")
        with open(self.error_file, "a") as file:
            file.write(dt + str(error) + "\n")
        print("An error has been encountered. Please contact me through GitHub or Discord (arckoor#5871) and send me"
              "the file 'error.txt' that has been created in the your install directory for this tool, along with a "
              "description of what you were doing.")
        input("Enter to exit: ")
        sys.exit()


JourneyRobeChanger()
