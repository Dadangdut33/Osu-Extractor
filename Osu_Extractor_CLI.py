# Internal
import os
import sys
import time
import subprocess
from time import sleep
from sys import exit
try:
    from msvcrt import getch
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

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

# User lib
from osu_extractor.GetData import getSubFolder, getAllItemsInFolder, getFolderName, extractFiles, createPathIfNotExist, keepCertainListByKeyword
from osu_extractor.Public import jsonHandler, version

# External
from termcolor import colored
from tqdm import tqdm

# Local
dir_path = os.path.dirname(os.path.realpath(__file__))
def startfile(filename):
    """
    Open a folder or file in the default application.
    """
    createPathIfNotExist(filename)
    try:
        os.startfile(filename)
    except FileNotFoundError:
        print("Cannot find the file specified.")
    except Exception:
        try:
            subprocess.Popen(['xdg-open', filename])
        except FileNotFoundError:
            print("Cannot open the file specified.")
        except Exception as e:
            print("Error: " + str(e))

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
            2: lambda: self.menuChangeOutputPath(),
            3: lambda: self.changeExtractType(),
            4: lambda: self.resetDefault()
        }

    def changeOsuPath(self):
        while True:
            clearScreen()
            print(colored("=" * 100, "blue"))
            print(colored(">> Change Osu! path", "green"))
            print(colored("=" * 100, "blue"))
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
                print(colored("\n>> Successfully set ", "green") + colored(self.config["osu_path"], "yellow") + colored(" as the Osu! path!", "green"))
                print(colored("Press any key to continue...", "cyan"), end="", flush=True)
                getch()
                break

    def menuChangeOutputPath(self):
        optChangeOutputPath = { 
            1: lambda: self.changeOutputPath("song"),
            2: lambda: self.changeOutputPath("img"),
            3: lambda: self.changeOutputPath("video"),
            4: lambda: self.changeOutputPath("custom"),
        }
        insideMenu = True
        while insideMenu:
            clearScreen()
            print(colored("=" * 100, "blue"))
            print(colored(">> Change output path", "green"))
            print(colored("=" * 100, "blue"))
            print(colored(">> Press", "blue") + colored(' esc ', 'red') + colored("if you want to go back", "blue"))
            print(colored(">> Set:", "blue"))
            print(colored(" 1. Song\t", "yellow") + self.colon + colored(self.getOutputPath(self.config["output_path"]['song'], "song"), "cyan"))
            print(colored(" 2. Img\t\t", "yellow") + self.colon + colored(self.getOutputPath(self.config["output_path"]['img'], "img"), "cyan"))
            print(colored(" 3. Video\t", "yellow") + self.colon + colored(self.getOutputPath(self.config["output_path"]['video'], "video"), "cyan"))
            print(colored(" 4. Custom\t", "yellow") + self.colon + colored(self.getOutputPath(self.config["output_path"]["custom"], "custom"), "cyan"))
            print(colored("=" * 100, "blue"))
            print(colored(">> ", "yellow"), end="", flush=True)

            while True:
                ch = ord(getch())
                if ch == 27: # ESC
                    insideMenu = False
                    break

                if ch - 48 in optChangeOutputPath.keys():
                    optChangeOutputPath[ch - 48]()
                    break

    def changeOutputPath(self, changeType):
        """Change the output path

        Args:
            changeType (str): type of the output (song, img, video)
        """
        while True:
            clearScreen()
            print(colored("=" * 100, "blue"))
            print(colored(f">> Change output path ({changeType})", "green"))
            print(colored("=" * 100, "blue"))
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
            print(colored("=" * 100, "blue"))
            print(colored(">> Change extract type", "green"))
            print(colored("=" * 100, "blue"))
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
            print(colored("=" * 100, "blue"))
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
                # Split input to array by space
                toSave = strCustom.strip().split(" ") if strCustom.strip() != "" else [strCustom]

                # If empty
                if toSave == ['\r']:
                    toSave = []

                # Check if the format is correct
                correct = True
                if len(toSave) > 0:
                    for item in toSave:
                        if not item.startswith(".") or len(item) < 2:
                            correct = False
                            print(colored("\n>> Error: ", "red") + "The format is not correct!")
                            print(colored(">> Please input the correct format!", "white"), end="", flush=True)
                            getch()
                            break
                
                if not correct:
                    continue
                
                # Save
                self.config["default_extract"]["custom_list"] = toSave
                print(colored("\n>> Successfully set \"", "green") + colored(strCustom.strip(), "yellow") + colored("\" as the custom extract list!", "green"))
                print(colored("   Press any key to continue...", "cyan"), end="", flush=True)
                getch()
                break

    def resetDefault(self):
        clearScreen()
        print(colored("=" * 100, "blue"))
        print(colored(">> Reset to default", "green"))
        print(colored("=" * 100, "blue"))
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

    def getOutputPath(self, path, fileFormat):
        if path.lower() == "default":
            return f"{dir_path}\\output\\{fileFormat}\\"
        else:
            return path

    def extractCertainBeatmap(self):        
        while True:
            clearScreen()
            print(colored("=" * 100, "blue"))
            print(colored(">> Extract certain beatmap", "green"))
            print(colored("=" * 100, "blue"))
            print(colored(">> Press", "blue") + colored(' ctrl + c', 'red') + colored(" to cancel and go back to extract menu", "blue"))
            
            try:
                query = input(colored(">> Beatmap name: ", "yellow"))
                
                if query.strip() == "":
                    continue
                else:
                    self.extractBeatmaps(query)
                    break

            except KeyboardInterrupt:
                break

    def extractBeatmaps(self, searchFor=None):
        continueExtract = False
        insideMenu = True
        # Get the beatmaps list
        path = f"{self.config['osu_path']}\Songs"
        beatmapsPath = getSubFolder(path)
        totals = len(beatmapsPath)

        if searchFor:
            beatmapsPath = keepCertainListByKeyword(beatmapsPath, searchFor)
            totals = len(beatmapsPath)
            # Added "" for display
            searchFor = ' named ' + colored(f'"{searchFor}"', "yellow")

        # If no beatmaps found
        if totals == 0:
            print(colored("No beatmaps found!", "red"))
            print(colored("Press any key to continue...", "cyan"), end="", flush=True)
            getch()
            if searchFor: self.extractCertainBeatmap()
            return

        while insideMenu:
            clearScreen()
            print(colored("=" * 100, "blue"))
            print(colored(">> Extract all beatmap" if searchFor is None else f">> Extract beatmaps{searchFor}", "green"))
            print(colored("=" * 100, "blue"))
            if searchFor:
                print(colored("Found ", "blue") + colored(str(totals), "yellow") + colored(" beatmaps", "blue") + searchFor)
            else:
                print(colored("Found ", "blue") + colored(str(totals), "yellow") + colored(" beatmaps", "blue"))
            print(colored(">> Are you sure you want to extract it with the current setting ", "blue") + colored("(Y/N)", "yellow") + colored(":", "blue"))
            print(colored(">> ", "yellow"), end="", flush=True)

            while True:
                ch = ord(getch())
                if ch == 89 or ch == 121: # Y
                    continueExtract = True
                    insideMenu = False
                    break
                elif ch == 78 or ch == 110: # N
                    insideMenu = False
                    break

        if not continueExtract:
            return

        # Extract all beatmaps
        totalExtracted = 0
        # Get start time
        startTime = time.time()
        # Extracting
        try:
            clearScreen()
            print(colored("=" * 100, "blue"))
            print(colored(">> Extract all beatmap", "green"))
            print(colored("=" * 100, "blue"))
            print(colored(">> Press", "blue") + colored(' ctrl + c', 'red') + colored(" to stopped the process midway", "blue"))
            print(colored("Extracting beatmaps" + searchFor + "..." if searchFor else "Extracting all beatmaps...", "green"))

            with tqdm(total=totals, colour="blue", ncols=100) as pbar:
                for item in beatmapsPath:
                    theFile = getAllItemsInFolder(item)
                    # Check extract type
                    if self.config['default_extract']['song']:
                        extractFiles(item, theFile, ".mp3", self.getOutputPath(self.config['output_path']['song'], "song"), getFolderName(item))
                    if self.config['default_extract']['img']:
                        extractFiles(item, theFile, ".jpg", self.getOutputPath(self.config['output_path']['img'], "img"), getFolderName(item))
                    if self.config['default_extract']['video']:
                        extractFiles(item, theFile, ".avi", self.getOutputPath(self.config['output_path']['video'], "video"), getFolderName(item))
                    if self.config['default_extract']['custom']:
                        for custom in self.config['default_extract']['custom_list']:
                            extractFiles(item, theFile, custom, self.getOutputPath(self.config['output_path']['custom'], "custom"), getFolderName(item))

                    pbar.update(1)
                    totalExtracted += 1
            print()
            # get end time
            endTime = time.time()

        except KeyboardInterrupt:
            # get end time
            endTime = time.time()
            print()
            print(colored(">> Process stopped by user", "red"))

        # Display how much beatmaps are extracted
        print(colored(">> Successfully extracted ", "green") + colored(str(totalExtracted), "yellow") + colored(" beatmaps", "green"))
        # Print total time taken
        print(colored(">> Total time taken: ", "green") + colored(str(round(endTime - startTime, 2)), "yellow") + colored(" seconds", "green"))

        # Ask if user want to open the output folder or not
        print(colored(">> Do you want to open the output folder? (Y/N)", "blue"))
        print(colored(">> ", "yellow"), end="", flush=True)
        while True:
            ch = ord(getch())
            if ch == 89 or ch == 121: # Y
                if self.config['default_extract']['song']:
                    startfile(self.getOutputPath(self.config['output_path']['song'], "song"))
                if self.config['default_extract']['img']:
                    startfile(self.getOutputPath(self.config['output_path']['img'], "img"))
                if self.config['default_extract']['video']:
                    startfile(self.getOutputPath(self.config['output_path']['video'], "video"))
                if self.config['default_extract']['custom']:
                    startfile(self.getOutputPath(self.config['output_path']['custom'], "custom"))
                
                print(colored("Opening output folder...", "green"))
                sleep(1)
                break
            elif ch == 78 or ch == 110: # N
                break

    def printCurrentSetting(self):
        print(colored(">> Current settings", "green"))
        print(colored("[~] Osu! path\t", "blue") + self.colon + colored(self.config["osu_path"], "green"))
        print(colored("[~] Output path\t", "blue") + self.colon)
        print(colored("    song\t", "yellow") + self.colon + colored(self.getOutputPath(self.config["output_path"]['song'], "song"), "cyan"))
        print(colored("    img\t\t", "yellow") + self.colon + colored(self.getOutputPath(self.config["output_path"]['img'], "img"), "cyan"))
        print(colored("    video\t", "yellow") + self.colon + colored(self.getOutputPath(self.config["output_path"]['video'], "video"), "cyan"))
        print(colored("    custom\t", "yellow") + self.colon + colored(self.getOutputPath(self.config["output_path"]["custom"], "custom"), "cyan"))
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

    def menuExtract(self):
        insideMenu = True
        # Extract the beatmap
        while insideMenu:
            clearScreen()
            print(colored("=" * 100, "blue"))
            print(colored(">> Extract Beatmap", "green"))
            print(colored("=" * 100, "blue"))
            
            self.printCurrentSetting()

            print(colored("=" * 100, "blue"))
            print(colored(">> Press", "blue") + colored(" esc ", "red") + colored("if you want to go back", "blue"))
            print(colored(">> Options:", "blue"))
            print(colored("  1. Extract All Beatmap", "white"))
            print(colored("  2. Extract Certain Beatmap", "white"))
            print(colored("  3. Change setting", "white"))
            print(colored("=" * 100, "blue"))
            print(colored(">> ", "yellow"), end="", flush=True)
            while True:
                ch = ord(getch())
                if ch == 49:
                    # Check extract options, if all is disabled
                    if not self.config['default_extract']['song'] and not self.config['default_extract']['img'] and not self.config['default_extract']['video'] and not self.config['default_extract']['custom']:
                        print(colored("You need to atleast set 1 extract types in the setting!", "red"))
                        print(colored(">> Press any key to continue...", "yellow"), end="", flush=True)
                        getch()
                        break

                    self.extractBeatmaps()
                    break
                elif ch == 50:
                    # Check extract options, if all is disabled
                    if not self.config['default_extract']['song'] and not self.config['default_extract']['img'] and not self.config['default_extract']['video'] and not self.config['default_extract']['custom']:
                        print(colored("You need to atleast set 1 extract types in the setting!", "red"))
                        print(colored(">> Press any key to continue...", "yellow"), end="", flush=True)
                        getch()
                        break

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

    def menuSetting(self):
        insideMenu = True
        # Change the setting
        while insideMenu:
            clearScreen()
            print(colored("=" * 100, "blue"))
            print(colored(">> Change Setting", "green"))
            print(colored("=" * 100, "blue"))
            
            self.printCurrentSetting()

            print(colored("=" * 100, "blue"))
            print(colored(">> Press", "blue") + colored(" esc ", "red") + colored("if you want to go back", "blue"))
            print(colored(">> Options:", "blue"))
            print(colored("  1. Change Osu! path", "white"))
            print(colored("  2. Change Output path", "white"))
            print(colored("  3. Change extract type value", "white"))
            print(colored("  4. Reset default options", "white"))
            print(colored("=" * 100, "blue"))
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
        print(colored("=" * 100, "blue"))
        print(colored(">> About", "green"))
        print(colored("=" * 100, "blue"))
        print(colored("A simple Osu! Beatmap extractor. Can be use to extract songs, images,\nand videos from locally installed beatmaps. Made by Dadangdut33\n", "cyan"))
        
        print(colored("Disclaimer: ", "green"), end="") 
        print(colored("""
        \rI do not gain any money from this tool. I do not intend to support
        \rpiracy of any kind. This tool is only made to help extracting (copying)
        \rsong/img/videos from a beatmap. You should support the creators of each
        \rsong/img/videos you extract. I recommend tools such as saucenao and
        \rtineye to find the original image and author. You should also support
        \rthe original music artist by buying their songs/albums or by listening
        \rtheir song on official platform.
        """, "white"))
        print(colored("Press any key to go back...", "blue"), end="", flush=True)
        getch()

    def openOutputFolder(self):
        insideMenu = True
        while insideMenu:
            clearScreen()
            print(colored("=" * 51, "blue"))
            print(colored(">> Open Output Folder", "green"))
            print(colored("=" * 51, "blue"))
            print(colored(">> Choose which output folder that you want to open", "green"))
            print(colored(">> Press", "blue") + colored(' esc ', 'red') + colored("if you want to go back", "blue"))
            print(colored(">> Options:", "blue"))
            print(colored("  1. Song folder", "white"))
            print(colored("  2. Image folder", "white"))
            print(colored("  3. Video folder", "white"))
            print(colored("  4. Custom folder", "white"))
            print(colored("=" * 51, "blue"))
            print(colored(">> ", "yellow"), end="", flush=True)
            while True:
                ch = ord(getch())
                if ch == 49:
                    startfile(self.getOutputPath(self.config['output_path']['song'], "song"))
                    print(colored("Opening song folder...", "green"))
                    sleep(0.5)
                    break
                elif ch == 50:
                    startfile(self.getOutputPath(self.config['output_path']['img'], "img"))
                    print(colored("Opening image folder...", "green"))
                    sleep(0.5)
                    break
                elif ch == 51:
                    startfile(self.getOutputPath(self.config['output_path']['video'], "video"))
                    print(colored("Opening video folder...", "green"))
                    sleep(0.5)
                    break
                elif ch == 52:
                    startfile(self.getOutputPath(self.config['output_path']['custom'], "custom"))
                    print(colored("Opening custom folder...", "green"))
                    sleep(0.5)
                    break
                elif ch == 27:
                    insideMenu = False
                    break
                else:
                    continue
        
if __name__ == "__main__":
    main = MainProgram()
    running = True
    
    while running:
        clearScreen()
        print(colored("=" * 50, "blue"))
        print(colored(f">> Osu! Beatmap Extractor V{version}", "green"))
        print(colored("=" * 50, "blue"))
        print(colored(">> Options", "blue"))
        print(colored("  1. Extract"))
        print(colored("  2. Setting"))
        print(colored("  3. About"))
        print(colored("  4. Open output folder"))
        print(colored("  5. Exit"))
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
                main.openOutputFolder()
                break
            elif ch == 53:
                print(colored("Thanks for using this program!", "green"))
                sleep(1)
                clearScreen()
                running = False
                break
            else:
                continue