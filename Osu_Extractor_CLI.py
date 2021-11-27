# Internal
import os
import sys
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
        createNew = False
        if status == False:
            clearScreen()
            print(colored(">> Error: ", "red") + data)
            sleep(0.5)
            print(colored(">> Trying to create a default setting file...", "green"))
            status, data = jsonHandler.setDefault()
            if status == False:
                print(colored(">> Error: ", "red") + data)
                print(colored(">> Program fail to create the default setting! Will exit now!", "white"))
                getch()
                exit(1)
            else:
                print(colored(">> Successfully set setting to default!\n", "green"))
                createNew = True
                sleep(0.7)
        
        self.config = jsonHandler.loadSetting()[1]
        # Check if the osu path is on default path or not
        if not os.path.exists(self.config["osu_path"]) or "osu!.exe" not in getAllItemsInFolder(self.config["osu_path"]):
            if not createNew: clearScreen()
            while True:
                print(colored('Attention!!', 'red', 'on_grey', ['reverse']))
                if createNew: 
                    print(colored("Looks like your osu folder is not installed on the default path", "yellow"))
                else: 
                    print(colored("Couldn't found Osu!.exe in your osu path!", "yellow"))
                
                # Ask to input the correct path
                self.config["osu_path"] = input(colored("Please input the correct Osu! path: ", "yellow")).replace("/", "\\")
                
                # Check whether the path is correct or not
                if not os.path.exists(self.config["osu_path"]):
                    print(colored(">> Error: ", "red") + "The path you input is not correct!")
                    print(colored(">> Please input the correct path!", "white"), end="")
                    input()
                    # Remove all the line starting from attention,
                    for i in range(0, 5):
                        sys.stdout.write("\033[F") # Go up 1 line
                        sys.stdout.write("\033[K") # Clear to the end of line
                else:
                    if "osu" not in self.config["osu_path"].lower() or "osu!.exe" not in getAllItemsInFolder(self.config["osu_path"]):
                        signalToGoBack = False
                        print(colored('Attention!!', 'red', 'on_grey', ['reverse']))
                        print(colored(">> It seems like it's not a correct Osu! folder. Are you sure you want to set this as the Osu! path? (Y/N)", "white"), end="", flush=True)
                        while True:
                            ch = ord(getch())
                            if ch == 89 or ch == 121: # Y
                                break
                            elif ch == 78 or ch == 110: # N
                                signalToGoBack = True
                                break
                        if signalToGoBack:
                            print('\0')
                            for i in range(0, 5):
                                sys.stdout.write("\033[F") # Go up 1 line
                                sys.stdout.write("\033[K") # Clear to the end of line
                            continue
                    
                    # Save the setting
                    jsonHandler.writeSetting(self.config)
                    print(colored("\n>> Successfully set ", "green") + colored(self.config["osu_path"], "yellow") + colored(" as the Osu! path!", "green"))
                    print(colored("Press any key to continue...", "cyan"), end="", flush=True)
                    getch()
                    break

        self.colon = colored(": ", "yellow")
        self.settingMenuOpt = {
            1: lambda: self.changeOsuPath(),
            2: lambda: self.changeOutputPath("song"),
            3: lambda: self.changeOutputPath("img"),
            4: lambda: self.changeOutputPath("video"),
            5: lambda: self.changeExtractType(),
            6: lambda: self.resetDefault()
        }

    def changeOsuPath(self):
        while True:
            clearScreen()
            print(colored("=" * 70, "blue"))
            print(colored(">> Change Osu! path", "green"))
            print(colored("=" * 70, "blue"))
            print(colored(">> Press", "blue") + colored(' ctrl + c', 'red') + colored(" to cancel, press", "blue")  + colored(' enter ', 'yellow') + colored("to confirm", "blue"))
            print(colored(">> Input ", "blue") + colored("default", "yellow") + colored(" if you want to use the default path", "blue"))
            print(colored(">> Set:", "blue"))
            print(colored("   Current path\t: ", "yellow") + colored(self.config["osu_path"], "cyan"))
            try:
                path = input(colored("   Into\t\t: ", "yellow"))
            except KeyboardInterrupt:
                break
            
            path = path.strip()
            print()
            if not os.path.exists(path) and path.lower().strip() != "default":
                print(colored(">> Error: ", "red") + "The path you input is not correct!")
                print(colored(">> Please input the correct path!", "white"), end="", flush=True)
                getch()
            else:
                if path == "default":
                    path = jsonHandler.default_Setting['osu_path']
                
                if "osu!.exe" not in getAllItemsInFolder(path):
                    signalToGoBack = False
                    print(colored('Attention!!', 'red', 'on_grey', ['reverse']))
                    print(colored(">> It seems like it's not a correct Osu! folder. Are you sure you want to set this as the Osu! path? (Y/N)", "white"), end="", flush=True)
                    while True:
                        ch = ord(getch())
                        if ch == 89 or ch == 121: # Y
                            break
                        elif ch == 78 or ch == 110: # N
                            signalToGoBack = True
                            break
                    if signalToGoBack:
                        continue

                self.config["osu_path"] = path
                jsonHandler.writeSetting(self.config)
                print(colored(">> Successfully set ", "green") + colored(self.config["osu_path"], "yellow") + colored(" as the Osu! path!", "green"))
                print(colored("Press any key to continue...", "cyan"), end="", flush=True)
                getch()
                break

    def changeOutputPath(self, changeType):
        """Change the output path

        Args:
            changeType (str): type of the output (song, img, video)
        """
        while True:
            clearScreen()
            print(colored("=" * 70, "blue"))
            print(colored(f">> Change output path ({changeType})", "green"))
            print(colored("=" * 70, "blue"))
            print(colored(">> Press", "blue") + colored(' ctrl + c', 'red') + colored(" to cancel, press", "blue")  + colored(' enter ', 'yellow') + colored("to confirm", "blue"))
            print(colored(">> Input ", "blue") + colored("default", "yellow") + colored(" if you want to use the default path", "blue"))
            print(colored(">> Set:", "blue"))
            print(colored("   Current path\t: ", "yellow") + colored(self.getOutputPath(self.config["output_path"][changeType], changeType), "cyan"))
            
            try:
                path = input(colored("   Into\t\t: ", "yellow"))
            except KeyboardInterrupt:
                break
            
            path = path.strip()
            print()
            if not os.path.exists(path) and path.lower() != "default":
                print(colored(">> Error: ", "red") + "The path you input is not correct!")
                print(colored(">> Please input the correct path!", "white"), end="", flush=True)
                getch()
            else:
                self.config["output_path"][changeType] = path.lower() if "default" in path.lower() else path
                jsonHandler.writeSetting(self.config)
                print(colored(">> Successfully set ", "green") + colored(self.getOutputPath(self.config["output_path"][changeType], changeType), "yellow") + colored(" as the output path!", "green"))
                print(colored("Press any key to continue...", "cyan"), end="", flush=True)
                getch()
                break

    def changeExtractType(self):
        insideMenu = True
        while insideMenu:
            clearScreen()
            print(colored("=" * 70, "blue"))
            print(colored(">> Change extract type", "green"))
            print(colored("=" * 70, "blue"))
            print(colored(">> Press", "blue") + colored(" esc ", "red") + colored("if you want to go back", "blue"))
            print(colored(">> Enable/Disable:", "blue"))
            print(colored(f"    1. Mp3 (.mp3) (Y)", "green") if self.config['default_extract']['song'] else colored("    1. Mp3 (.mp3) (N)", "red"))
            print(colored(f"    2. Image (.jpg) (Y)", "green") if self.config['default_extract']['img'] else colored("    2. Image (.jpg) (N)", "red"))
            print(colored(f"    3. Video (.avi) (Y)", "green") if self.config['default_extract']['video'] else colored("    3. Video (.avi) (N)", "red"))
            print(colored(f"    4. Custom (Y)", "green") if self.config['default_extract']['custom'] else colored("    4. Custom (N)", "red"))
            print(colored("[~] 5. Custom extract list:", "blue"))
            print("    ", end="", flush=True)
            for item in self.config["default_extract"]["custom_list"]:
                print(colored(item, "green" if self.config['default_extract']['custom'] else "red"), end=" ")
            print()
            print(colored(">> ", "yellow"), end="", flush=True)

            while True:
                ch = ord(getch())
                if ch == 27: # ESC
                    insideMenu = False
                    break
                
                if ch == 49: # 1
                    self.config['default_extract']['song'] = not self.config['default_extract']['song']
                    break
                elif ch == 50: # 2
                    self.config['default_extract']['img'] = not self.config['default_extract']['img']
                    break
                elif ch == 51: # 3
                    self.config['default_extract']['video'] = not self.config['default_extract']['video']
                    break
                elif ch == 52: # 4
                    self.config['default_extract']['custom'] = not self.config['default_extract']['custom']
                    break
                elif ch == 53: # 5
                    self.askForCustomExtractList()
                    break

        # Save setting
        jsonHandler.writeSetting(self.config)

    def askForCustomExtractList(self):
        strCustom = ""
        for item in self.config["default_extract"]["custom_list"]:
            strCustom += item + " "

        strCustom = strCustom.strip()

        while True:
            clearScreen()
            print(colored("=" * 70, "blue"))
            print(colored(">> Press", "blue") + colored(' esc ', 'red') + colored("to cancel, press", "blue")  + colored(' enter ', 'yellow') + colored("to confirm", "blue"))
            print(colored(">> Input the file format with dot and separated by space, ex: .mp3 .jpg", "green"))
            print(colored("   Set\t: ", "yellow"))
            print("   ", end="", flush=True)
            print(colored(strCustom, "green" if self.config['default_extract']['custom'] else "red"), end="", flush=True)

            ch = ord(getch())
            # if backspace delete 1
            if ch == 8:
                strCustom = strCustom[:-1]
            else:
                strCustom += chr(ch)                

            if ch == 27: # ESC
                break
            if ch == 13: # enter
                self.config["default_extract"]["custom_list"] = strCustom.strip().split(" ") if strCustom.strip() != "" else [strCustom]

                if self.config["default_extract"]["custom_list"] == ['\r']:
                    self.config["default_extract"]["custom_list"] = []

                print(colored("\n>> Successfully set \"", "green") + colored(strCustom.strip(), "yellow") + colored("\" as the custom extract list!", "green"))
                print(colored("   Press any key to continue...", "cyan"), end="", flush=True)
                getch()
                break

    def resetDefault(self):
        clearScreen()
        print(colored("=" * 70, "blue"))
        print(colored(">> Reset to default", "green"))
        print(colored("=" * 70, "blue"))
        print(colored(">> Are you sure you want to reset to default? (Y/N) ", "white"), end="", flush=True)
        while True:
            ch = ord(getch())

            if ch == 89 or ch == 121: # Y
                print("Y")
                resetStatus, statusStr = jsonHandler.setDefault()
                if resetStatus:
                    self.config = jsonHandler.loadSetting()[1]
                    print(colored(">> Successfully reset to default!", "green"))
                    print(colored("Press any key to continue...", "cyan"), end="", flush=True)
                    getch()
                    break
                else:
                    print(colored(">> Error: ", "red") + statusStr)
                    print(colored("Press any key to continue...", "cyan"), end="", flush=True)
                    getch()
                    break
            elif ch == 78 or ch == 110: # N
                return

    def getOutputPath(self, path, type):
        if path.lower() == "default":
            return f"{dir_path}\\output\\{type}\\"
        else:
            return path

    def menuExtract(self):
        insideMenu = True
        # Extract the beatmap
        while insideMenu:
            clearScreen()
            print(colored("=" * 70, "blue"))
            print(colored(">> Extract Beatmap", "green"))
            print(colored("=" * 70, "blue"))
            
            self.printCurrentSetting()

            print(colored("=" * 70, "blue"))
            print(colored(">> Press", "blue") + colored(" esc ", "red") + colored("if you want to go back", "blue"))
            print(colored(">> Options:", "blue"))
            print(colored("  1. Extract All Beatmap", "white"))
            print(colored("  2. Extract Certain Beatmap", "white"))
            print(colored("  3. Change setting", "white"))
            print(colored("=" * 70, "blue"))
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
                elif ch == 27: # esc
                    insideMenu = False
                    break
                else:
                    continue

    def printCurrentSetting(self):
        print(colored(">> Current settings", "green"))
        print(colored("[~] Osu! path\t", "blue") + self.colon + colored(self.config["osu_path"], "green"))
        print(colored("[~] Output path\t", "blue") + self.colon)
        print(colored("    song\t", "yellow") + self.colon + colored(self.getOutputPath(self.config["output_path"]['song'], "song"), "cyan"))
        print(colored("    img\t\t", "yellow") + self.colon + colored(self.getOutputPath(self.config["output_path"]['img'], "img"), "cyan"))
        print(colored("    video\t", "yellow") + self.colon + colored(self.getOutputPath(self.config["output_path"]['video'], "video"), "cyan"))
        print(colored("[~] Extract type", "blue") + self.colon)
        print(colored(f"    1. Mp3 (.mp3) (Y)", "green") if self.config['default_extract']['song'] else colored("    1. Mp3 (.mp3) (N)", "red"))
        print(colored(f"    2. Image (.jpg) (Y)", "green") if self.config['default_extract']['img'] else colored("    2. Image (.jpg) (N)", "red"))
        print(colored(f"    3. Video (.avi) (Y)", "green") if self.config['default_extract']['video'] else colored("    3. Video (.avi) (N)", "red"))
        print(colored(f"    4. Custom (Y)", "green") if self.config['default_extract']['custom'] else colored("    4. Custom (N)", "red"))
        print(colored("[~] Custom extract list", "blue") + self.colon)
        print("    ", end="", flush=True)
        for item in self.config["default_extract"]["custom_list"]:
            print(colored(item, "green" if self.config['default_extract']['custom'] else "red"), end=" ")
        print()


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
            print(colored(">> Press", "blue") + colored(" esc ", "red") + colored("if you want to go back", "blue"))
            print(colored(">> Options:", "blue"))
            print(colored("  1. Change Osu! path", "white"))
            print(colored("  2. Change Output path (song)", "white"))
            print(colored("  3. Change Output path (img)", "white"))
            print(colored("  4. Change Output path (video)", "white"))
            print(colored("  5. Change extract type value", "white"))
            print(colored("  6. Reset default options", "white"))
            print(colored("=" * 50, "blue"))
            print(colored(">> ", "yellow"), end="", flush=True)
            while True:
                ch = ord(getch())
                if ch == 27:
                    insideMenu = False
                    break
                else:
                    if ch - 48 in self.settingMenuOpt:
                        self.settingMenuOpt[ch - 48]()
                        break

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
