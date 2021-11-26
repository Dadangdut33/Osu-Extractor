# Internal
import os
from time import sleep
from sys import exit
try:
    from msvcrt import getch, getche
except ImportError:
    def getch():
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    def getche():
        ch = getch()
        print(ch, end='')
        return ch

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

# User lib
from osu_extractor.GetData import getSubFolder, getAllItemsInFolder, getFolderName, extractFiles, createPathIfNotExist, keepCertainListByKeyword
from osu_extractor.Public import jsonHandler

# External
from termcolor import colored

# Local
dir_path = os.path.dirname(os.path.realpath(__file__))

# --------------------------------------------------
class MainProgram:
    def __init__(self):
        # First read the config file
        status, data = jsonHandler.loadSetting()
        if status == False:
            print(colored(">> Error: ", "red") + data)
            sleep(0.5)
            status, data = jsonHandler.setDefault()
            if status == False:
                print(colored(">> Error: ", "red") + data)
                print(colored(">> Program fail to create the default setting! Will exit now!", "white"))
                getch()
                exit(1)
            else:
                print(colored(">> Successfully set setting to default!", "green"))
                sleep(1)
        
        self.config = jsonHandler.loadSetting()[1]
        # Check if the osu path is correct or not
        if not os.path.exists(self.config["osu_path"]) or "osu!.exe" not in getAllItemsInFolder(self.config["osu_path"]):
            while True:
                print(colored('Attention!!', 'red', 'on_grey', ['reverse']))
                print(colored("Looks like your osu folder is not installed on the default path", "yellow"))
                self.config["osu_path"] = input(colored("Please input your Osu! path: ", "yellow")).replace("\\", "/")
                if not os.path.exists(self.config["osu_path"]):
                    print(colored(">> Error: ", "red") + "The path you input is not correct!")
                    print(colored(">> Please input the correct path!", "white"), end="", flush=True)
                    getch()
                    clearScreen()
                    continue
                else:
                    if "osu" not in self.config["osu_path"].lower() or "osu!.exe" not in getAllItemsInFolder(self.config["osu_path"]):
                        signalToGoBack = False
                        print(colored('Attention!!', 'red', 'on_grey', ['reverse']))
                        print(colored(">> It seems like it's not a correct Osu! folder. Are you sure you want to set this as the Osu! path? (Y/N)", "white"), end="", flush=True)
                        while True:
                            ch = ord(getch())
                            if ch == 89 or ch == 121:
                                break
                            elif ch == 78 or ch == 110:
                                print(colored("\n>> Please Re-enter it correctly the next time!", "green"))
                                print(colored("Press any key to continue...", "cyan"), end="", flush=True)
                                getch()
                                signalToGoBack = True
                                break
                        if signalToGoBack:
                            clearScreen()
                            continue
                    
                    # Save the setting
                    jsonHandler.writeSetting(self.config)
                    print(colored("\n>> Successfully set ", "green") + colored(self.config["osu_path"], "yellow") + colored(" as the Osu! path!", "green"))
                    print(colored("Press any key to continue...", "cyan"), end="", flush=True)
                    getch()
                    break

        self.colon = colored(": ", "yellow")

    def getOutputPath(self, path, type):
        if path != "auto":
            return path
        else:
            return dir_path + f"\\output\\{type}\\"

    def menuExtract(self):
        insideMenu = True
        # Extract the beatmap
        while insideMenu:
            clearScreen()
            print(colored("=" * 50, "blue"))
            print(colored(">> Extract Beatmap", "green"))
            print(colored("=" * 50, "blue"))
            
            self.printCurrentSetting()

            print(colored("=" * 50, "blue"))
            print(colored(">> Press esc key if you want to go back", "blue"))
            print(colored(">> Options:", "blue"))
            print(colored("  1. Extract All Beatmap", "white"))
            print(colored("  2. Extract Certain Beatmap", "white"))
            print(colored("  3. Change setting", "white"))
            print(colored("=" * 50, "blue"))
            print(colored(">> ", "yellow"), end="", flush=True)
            while True:
                ch = ord(getch())
                if ch == 49:
                    self.extractAllBeatmap()
                    break
                elif ch == 50:
                    self.extractCertainBeatmap()
                    break
                elif ch == 51:
                    self.menuSetting()
                    break
                elif ch == 27:
                    insideMenu = False
                    break
                else:
                    continue

    def printCurrentSetting(self):
        print(colored(">> Current settings", "green"))
        print(colored("[~] Osu! path\t", "blue") + self.colon + colored(self.config["osu_path"], "green"))
        print(colored("[~] Output path\t", "blue") + self.colon)
        print(colored("    song\t", "yellow") + self.colon + self.getOutputPath(colored(self.config["output_path"]['song']), "green"))
        print(colored("    img\t\t", "yellow") + self.colon + self.getOutputPath(colored(self.config["output_path"]['img']), "green"))
        print(colored("    video\t", "yellow") + self.colon + self.getOutputPath(colored(self.config["output_path"]['video']), "green"))
        print(colored("[~] Extract type", "blue") + self.colon)
        print(colored("    1. Mp3 (.mp3) ✓", "green") if self.config['default_extract']['song'] else colored("    1. Mp3 (.mp3) ✗", "red"))
        print(colored("    2. Image (.jpg) ✓", "green") if self.config['default_extract']['img'] else colored("    2. Image (.jpg) ✗", "red"))
        print(colored("    3. Video (.avi) ✓", "green") if self.config['default_extract']['video'] else colored("    3. Video (.avi) ✗", "red"))
        print(colored("    4. Custom ✓", "green") if self.config['default_extract']['custom'] else colored("    4. Custom ✗", "red"))
        if self.config['default_extract']['custom']:
            print(colored("[~] Custom extract list", "blue") + self.colon)
            print("    ", end="", flush=True)
            for item in self.config["custom_extract_list"]:
                print(colored(item, "green"), end=", ")
            print("\b \b")

    def menuSetting(self):
        insideMenu = True
        # Change the setting
        while insideMenu:
            clearScreen()
            print(colored("=" * 50, "blue"))
            print(colored(">> Change Setting", "green"))
            print(colored("=" * 50, "blue"))
            
            self.printCurrentSetting()

            print(colored("=" * 50, "blue"))
            print(colored(">> Press esc key if you want to go back", "blue"))
            print(colored(">> Options:", "blue"))
            print(colored("  1. Change Osu! path", "white"))
            print(colored("  2. Change Output path (song)", "white"))
            print(colored("  3. Change Output path (img)", "white"))
            print(colored("  4. Change Output path (video)", "white"))
            print(colored("  5. Change extract type value)", "white"))
            print(colored("  6. Reset default options", "white"))
            print(colored("=" * 50, "blue"))
            print(colored(">> ", "yellow"), end="", flush=True)
            while True:
                ch = ord(getch())
                if ch == 27:
                    insideMenu = False
                    break
                else:
                    continue

    def menuAbout(self):
        clearScreen()
        print(colored("=" * 70, "blue"))
        print(colored(">> About", "green"))
        print(colored("=" * 70, "blue"))
        print(colored("A simple Osu! Beatmap extractor. Can be use to extract songs, images,\nand videos from locally installed beatmaps. Made by Dadangdut33\n", "cyan"))
        
        print(colored("Disclaimer: ", "green"), end="") 
        print(colored("""
        \rI do not gain any money from this tool. I do not intend to support
        \rpiracy of any kind. This tool is only made to help extracting song/
        \rimg/videos from a beatmap. You should support the creators of each
        \rsong/images/videos you extract. I recommend tools such as saucenao
        \rand tineye to find the original image and author. You should also 
        \rsupport the original music artist by buying their songs/albums or
        \rby listening their song on official platform.
        """, "white"))
        print(colored("Press any key to go back...", "blue"), end="", flush=True)
        getch()
        
if __name__ == "__main__":
    main = MainProgram()
    running = True
    
    while running:
        clearScreen()
        print(colored("=" * 50, "blue"))
        print(colored(">> Osu! Beatmap Extractor", "green"))
        print(colored("=" * 50, "blue"))
        print(colored(">> Options", "blue"))
        print(colored("  1. Extract"))
        print(colored("  2. Setting"))
        print(colored("  3. About"))
        print(colored("  4. Exit"))
        print(colored("=" * 50, "blue"))
        print(colored(">> ", "yellow"), end="", flush=True)
        while True:
            ch = ord(getch())
            if ch == 49:
                main.menuExtract()
                break
            elif ch == 50:
                main.menuSetting()
                break
            elif ch == 51:
                main.menuAbout()
                break
            elif ch == 52:
                print(colored("Thanks for using this program!", "green"))
                sleep(1)
                clearScreen()
                running = False
                break
            else:
                continue

# Ex
# path = "C:\Games\Osu\Songs"

# beatmapsPath = getSubFolder(path)
# print(len(beatmapsPath))

# # Tests
# beatmap_3 = getAllItemsInFolder(beatmapsPath[3])

# extractFiles(beatmapsPath[3], beatmap_3, ".jpg", dir_path + "\\output\\img\\")
