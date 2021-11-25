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

# --------------------------------------------------
class MainProgram:
    def __init__(self):
        # First read the config file
        status, data = jsonHandler.loadSetting()
        if status == False:
            print(colored(">> Error: ", "red") + data)
            print(colored(">> Program will now try to create the default setting!", "white"))
            sleep(0.5)
            status, data = jsonHandler.setDefault()
            if status == False:
                print(colored(">> Error: ", "red") + data)
                print(colored(">> Program fail to create the default setting! Will exit now!", "white"))
                sleep(0.5)
                exit(1)
            else:
                print(colored("Successfully set setting to default!", "green"))
                sleep(0.5)
        
        self.config = data
        # Check if the osu path is correct or not
        if not os.path.exists(self.config["osu_path"]):
            while True:
                clearScreen()
                print(colored('Attention!!', 'red', 'on_grey', ['reverse']))
                print(colored("Looks like your osu folder is not installed on the default path", "yellow"))
                self.config["osu_path"] = input(colored("Please input your Osu! path: ", "yellow"))
                if not os.path.exists(self.config["osu_path"]):
                    print(colored(">> Error: ", "red") + "The path you input is not correct!")
                    print(colored(">> Please input the correct path!", "white"), end="", flush=True)
                    getch()
                    continue
                else:
                    if "osu" not in self.config["osu_path"].lower():
                        signalToGoBack = False
                        print(colored('Attention!!', 'red', 'on_grey', ['reverse']))
                        print(colored(">> It seems like it's not a correct Osu! folder. Are you sure you want to set this as the Osu! path? (Y/N)", "white"), end="", flush=True)
                        while True:
                            ch = ord(getch())
                            if ch == 89 or ch == 121:
                                break
                            elif ch == 78 or ch == 110:
                                print(colored(">> Please Re-enter it correctly the next time!", "green"))
                                sleep(0.5)
                                signalToGoBack = True
                                break
                        if signalToGoBack:
                            continue
                    
                    # Save the setting
                    jsonHandler.writeSetting(self.config)
                    print(colored(">> Successfully set ", "green") + colored(self.config["osu_path"], "yellow") + colored(" as the Osu! path!", "green"))
                    sleep(0.5)
                    break

        self.mainMenuDict = {
            "1": self.menuExtract,
            "2": self.menuSetting,
            "3": self.menuAbout,
            "4": self.menuExit
        }

        self.extractOptionDict = {
            "1": True,
            "2": False,
            "3": False,
            "4": False
        }

    def getOutputPath(self, path, type):
        if path != "auto":
            return path
        else:
            return dir_path + f"\\output\\{type}\\"

    
    def menuExtract(self):
        # Extract the beatmap
        while True:
            clearScreen()
            print(colored("Extract Beatmap", "green"))
            print(colored("Press esc key to go back", "blue"))
            print(colored("=" * 50, "blue"))
            print(colored("Current settings: ", "white"))
            print(colored("Osu! path\t: ", "yellow") + colored(self.config["osu_path"], "green"))
            print(colored("Output path (song)\t: ", "yellow") + self.getOutputPath(colored(self.config["output_path"]['song']), "green"), "song")
            print(colored("Output path (img)\t: ", "yellow") + self.getOutputPath(colored(self.config["output_path"]['img']), "green"), "img")
            print(colored("Output path (video)\t: ", "yellow") + self.getOutputPath(colored(self.config["output_path"]['video']), "green"), "video")
            print(colored("Extract type: ", "white"))
            print(colored("1. Mp3 (.mp3) ✓", "green") if self.extractOptionDict['1'] else colored("1. Mp3 (.mp3) ✗", "red"))
            print(colored("2. Image (.jpg) ✓", "green") if self.extractOptionDict['2'] else colored("2. Image (.jpg) ✗", "red"))
            print(colored("3. Video (.avi) ✓", "green") if self.extractOptionDict['3'] else colored("3. Video (.avi) ✗", "red"))
            print(colored("4. Custom ✓", "green") if self.extractOptionDict['4'] else colored("4. Custom ✗", "red"))
            if self.extractOptionDict['4']:
                print(colored("Custom extract list: ", "white"), end="")
                for item in self.config["custom_extract_list"]:
                    print(colored(item, "green"), end=", ")
                print("\b \b")
            print(colored("=" * 50, "blue"))
            print(colored("1. Extract All Beatmap", "white"))
            print(colored("2. Extract Certain Beatmap", "white"))
            print(colored("3. Change extract type", "white"))
            print(colored(">> ", "yellow"), end="", flush=True)
            ch = ord(getch())
            if ch == 49:
                self.extractAllBeatmap()
            elif ch == 50:
                self.extractCertainBeatmap()
            elif ch == 51:
                self.changeExtractType()
            elif ch == 27:
                break
            else:
                continue

dir_path = os.path.dirname(os.path.realpath(__file__))

path = "C:\Games\Osu\Songs"

beatmapsPath = getSubFolder(path)
print(len(beatmapsPath))

# # Tests
# beatmap_3 = getAllItemsInFolder(beatmapsPath[3])

# extractFiles(beatmapsPath[3], beatmap_3, ".jpg", dir_path + "\\output\\img\\")

if __name__ == "__main__":
    main = MainProgram()
    
    while True:
        clearScreen()
        pass
