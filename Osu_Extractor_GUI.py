# Internal
import os
import subprocess
from sys import exit
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter.ttk as ttk
import webbrowser

# User lib
from osu_extractor.GetData import getSubFolder, getAllItemsInFolder, getFolderName, extractFiles, createPathIfNotExist, keepCertainListByKeyword
from osu_extractor.Public import jsonHandler, version

# Local
dir_path = os.path.dirname(os.path.realpath(__file__))


def OpenUrl(url):
    webbrowser.open_new(url)


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
            subprocess.Popen(["xdg-open", filename])
        except FileNotFoundError:
            print("Cannot open the file specified.")
        except Exception as e:
            print("Error: " + str(e))


class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """

    def __init__(self, widget, text="widget info", delay=250, wraplength=180, opacity=1.0, always_on_top=True):
        self.waittime = delay  # miliseconds
        self.wraplength = wraplength  # pixels
        self.widget = widget
        self.text = text
        self.opacity = opacity
        self.always_on_top = always_on_top
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = Toplevel(self.widget)
        # Make it stay on top
        self.tw.wm_attributes("-topmost", self.always_on_top)
        # Make it a little transparent
        self.tw.wm_attributes("-alpha", self.opacity)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify="left", background="#ffffff", relief="solid", borderwidth=1, wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


class Main:
    def __init__(self):
        # First read the config file
        status, data = jsonHandler.loadSetting()
        if status == False:  # No config file
            statusDefault, dataDefault = jsonHandler.setDefault()
            if statusDefault == False:
                messagebox.showerror("Error", "Fail to create default setting file! Please check the folder permission. Error details " + str(data))
                exit(1)
            else:
                messagebox.showinfo("Info", "Settings file not found! Default setting file has been created and aplied!")
                self.config = jsonHandler.default_Setting
        else:
            self.config = data

        # Create the main window
        self.root = Tk()
        self.root.title("Osu! Extractor V" + version)
        self.root.geometry("900x600")
        self.root.protocol("WM_DELETE_WINDOW", self.on_Closing)

        # Create the menu
        self.menubar = Menu(self.root)
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_checkbutton(label="Always on Top", command=self.always_On_Top)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit Application", command=self.on_Closing)
        self.menubar.add_cascade(label="Options", menu=self.file_menu)

        self.file_menu2 = Menu(self.menubar, tearoff=0)
        self.file_menu2.add_command(label="Osu!.exe", command=lambda: self.openOsu())
        self.file_menu2.add_command(label="Osu! folder", command=lambda: startfile(self.config["osu_path"]))
        # add output menu for each output type, nested
        self.output_menu = Menu(self.file_menu2, tearoff=0)
        self.output_menu.add_command(label="Song", command=lambda: startfile(self.getOutputPath(self.config["output_path"]["song"], "song")))
        self.output_menu.add_command(label="Image", command=lambda: startfile(self.getOutputPath(self.config["output_path"]["img"], "img")))
        self.output_menu.add_command(label="Video", command=lambda: startfile(self.getOutputPath(self.config["output_path"]["video"], "video")))
        self.output_menu.add_command(label="Custom", command=lambda: startfile(self.getOutputPath(self.config["output_path"]["custom"], "custom")))
        self.file_menu2.add_cascade(label="Output", menu=self.output_menu)
        self.menubar.add_cascade(label="Open", menu=self.file_menu2)

        self.file_menu3 = Menu(self.menubar, tearoff=0)
        self.file_menu3.add_command(label="Tutorial", command=self.tutorial)
        self.file_menu3.add_command(label="About", command=self.about)
        self.file_menu3.add_separator()
        self.file_menu3.add_command(label="Open Repository", command=lambda aurl="https://github.com/Dadangdut33/Osu-Extractor": OpenUrl(aurl))
        self.menubar.add_cascade(label="Help", menu=self.file_menu3)

        self.root.config(menu=self.menubar)

        self.root.bind("<F1>", self.about)

        # Frames
        # 1
        self.frame_1 = LabelFrame(self.root, text="Settings", padx=5, pady=5, font="TkDefaultFont 10 bold")
        self.frame_1.pack(side=TOP, fill=X, expand=False, padx=5, pady=5)

        self.frame_1_row_1 = Frame(self.frame_1)
        self.frame_1_row_1.pack(side=TOP, fill=X, expand=False)

        self.frame_1_row_2 = Frame(self.frame_1)
        self.frame_1_row_2.pack(side=TOP, fill=X, expand=False)

        self.frame_1_row_3 = Frame(self.frame_1)
        self.frame_1_row_3.pack(side=TOP, fill=X, expand=False)

        self.frame_1_row_4 = Frame(self.frame_1)
        self.frame_1_row_4.pack(side=TOP, fill=X, expand=False)

        self.frame_1_row_5 = Frame(self.frame_1)
        self.frame_1_row_5.pack(side=TOP, fill=X, expand=False)

        # 2
        self.frame_2 = LabelFrame(self.root, text="Output", padx=5, pady=5, font="TkDefaultFont 10 bold")
        self.frame_2.pack(side=TOP, fill=X, expand=False, padx=5, pady=5)

        self.frame_2_row_1 = Frame(self.frame_2)
        self.frame_2_row_1.pack(side=TOP, fill=X, expand=False)

        self.frame_2_row_2 = Frame(self.frame_2)
        self.frame_2_row_2.pack(side=TOP, fill=X, expand=False)

        # 3
        self.frame_3 = Frame(self.root)
        self.frame_3.pack(side=TOP, fill=X, expand=False, padx=5, pady=5)

        self.frame_3_row_1 = Frame(self.frame_3)
        self.frame_3_row_1.pack(side=TOP, fill=X, expand=False)

        # Content
        # 1
        self.label_OsuPath = Label(self.frame_1_row_1, text="Osu! Path")
        self.label_OsuPath.pack(side=LEFT, padx=5, pady=5)

        self.entry_OsuPath = ttk.Entry(self.frame_1_row_1, width=50)
        self.entry_OsuPath.pack(side=LEFT, padx=5, pady=5, expand=True, fill=X)
        self.entry_OsuPath.bind("<Key>", lambda event: self.allowedKey(event))  # Disable input

        self.browse_OsuPath = ttk.Button(self.frame_1_row_1, text="Browse", command=lambda: self.browseOsu())
        self.browse_OsuPath.pack(side=LEFT, padx=5, pady=5)

        self.varExtractSong = BooleanVar()
        self.varExtractSong.set(self.config["default_extract"]["song"])
        self.checkExtractSong = ttk.Checkbutton(self.frame_1_row_2, text="Extract Song (.mp3)", variable=self.varExtractSong)
        self.checkExtractSong.pack(side=LEFT, padx=5, pady=5)

        self.entryExtractSong = ttk.Entry(self.frame_1_row_2, width=16)
        self.entryExtractSong.pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)
        CreateToolTip(self.entryExtractSong, "Right Click to change output path of extracted song")
        self.entryExtractSong.bind("<Key>", lambda event: self.allowedKey(event))  # Disable input
        self.entryExtractSong.bind("<Button-3>", lambda event: self.browseOutputPath("song", self.entryExtractSong))

        self.varExtractImage = BooleanVar()
        self.varExtractImage.set(self.config["default_extract"]["img"])
        self.checkExtractImage = ttk.Checkbutton(self.frame_1_row_2, text="Extract Image (.jpg)", variable=self.varExtractImage)
        self.checkExtractImage.pack(side=LEFT, padx=5, pady=5)

        self.entryExtractImage = ttk.Entry(self.frame_1_row_2, width=15)
        self.entryExtractImage.pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)
        CreateToolTip(self.entryExtractImage, "Right Click to change output path of extracted image")
        self.entryExtractImage.bind("<Key>", lambda event: self.allowedKey(event))  # Disable input
        self.entryExtractImage.bind("<Button-3>", lambda event: self.browseOutputPath("img", self.entryExtractImage))

        self.varExtractVideo = BooleanVar()
        self.varExtractVideo.set(self.config["default_extract"]["video"])
        self.checkExtractVideo = ttk.Checkbutton(self.frame_1_row_3, text="Extract Video (.avi)", variable=self.varExtractVideo)
        self.checkExtractVideo.pack(side=LEFT, padx=(5, 11), pady=5)

        self.entryExtractVideo = ttk.Entry(self.frame_1_row_3, width=12)
        self.entryExtractVideo.pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)
        self.entryExtractVideo.bind("<Key>", lambda event: self.allowedKey(event))  # Disable input
        CreateToolTip(self.entryExtractVideo, "Right Click to change output path of extracted video")
        self.entryExtractVideo.bind("<Button-3>", lambda event: self.browseOutputPath("video", self.entryExtractVideo))

        self.varExtractCustom = BooleanVar()
        self.varExtractCustom.set(self.config["default_extract"]["custom"])
        self.checkExtractCustom = ttk.Checkbutton(self.frame_1_row_3, text="Extract Custom", variable=self.varExtractCustom, command=lambda: self.toggleExtractCustom())
        self.checkExtractCustom.pack(side=LEFT, padx=5, pady=5)

        self.entryExtractCustom = ttk.Entry(self.frame_1_row_3, width=15)
        self.entryExtractCustom.pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)
        self.entryExtractCustom.bind("<Key>", lambda event: self.allowedKey(event))  # Disable input
        CreateToolTip(self.entryExtractCustom, "Right Click to change output path of extracted custom list")

        # Custom list entry
        self.label_CustomList = Label(self.frame_1_row_4, text="Custom List")
        self.label_CustomList.pack(side=LEFT, padx=(5, 3), pady=5)

        self.entry_CustomList = ttk.Entry(self.frame_1_row_4, width=30)
        self.entry_CustomList.pack(side=LEFT, padx=(0, 5), pady=5, fill=X, expand=True)

        # Save, cancel, set default btn
        self.btn_Save = ttk.Button(self.frame_1_row_5, text="Save", command=lambda: self.saveConfig())
        self.btn_Save.pack(side=RIGHT, padx=5, pady=5)

        self.btn_Cancel = ttk.Button(self.frame_1_row_5, text="Cancel", command=lambda: self.cancelConfig())
        self.btn_Cancel.pack(side=RIGHT, padx=5, pady=5)

        self.btn_SetDefault = ttk.Button(self.frame_1_row_5, text="Set Default", command=lambda: self.setDefaultConfig())
        self.btn_SetDefault.pack(side=RIGHT, padx=5, pady=5)

        self.initConfig()

    def toggleExtractCustom(self):
        print(self.varExtractSong.get())
        print(self.varExtractImage.get())
        print(self.varExtractVideo.get())
        print(self.varExtractCustom.get())
        if self.varExtractCustom.get():
            self.entry_CustomList.config(state=NORMAL)
        else:
            self.entry_CustomList.config(state=DISABLED)

    def initConfig(self):
        self.entry_OsuPath.delete(0, END)
        self.entry_OsuPath.insert(0, self.config["osu_path"])

        self.varExtractSong.set(self.config["default_extract"]["song"])
        self.varExtractImage.set(self.config["default_extract"]["img"])
        self.varExtractVideo.set(self.config["default_extract"]["video"])
        self.varExtractCustom.set(self.config["default_extract"]["custom"])

        self.entryExtractSong.delete(0, END)
        self.entryExtractSong.insert(0, self.getOutputPath(self.config["output_path"]["song"], "song"))

        self.entryExtractImage.delete(0, END)
        self.entryExtractImage.insert(0, self.getOutputPath(self.config["output_path"]["img"], "img"))

        self.entryExtractVideo.delete(0, END)
        self.entryExtractVideo.insert(0, self.getOutputPath(self.config["output_path"]["video"], "video"))

        self.entryExtractCustom.delete(0, END)
        self.entryExtractCustom.insert(0, self.getOutputPath(self.config["output_path"]["custom"], "custom"))

        self.entry_CustomList.delete(0, END)
        self.entry_CustomList.insert(0, ", ".join(self.config["default_extract"]["custom_list"]))

        if self.varExtractCustom.get():
            # Enable custom list entry
            self.entry_CustomList.config(state=NORMAL)
        else:
            # Disable custom list entry
            self.entry_CustomList.config(state=DISABLED)

    def saveConfig(self):
        # ask confirmation
        if messagebox.askokcancel("Save", "Are you sure you want to save current configuration?"):
            self.config["osu_path"] = self.entry_OsuPath.get()
            self.config["default_extract"]["song"] = self.varExtractSong.get()
            self.config["default_extract"]["img"] = self.varExtractImage.get()
            self.config["default_extract"]["video"] = self.varExtractVideo.get()
            self.config["default_extract"]["custom"] = self.varExtractCustom.get()

            self.config["output_path"]["song"] = "default" if dir_path in self.entryExtractSong.get() else self.entryExtractSong.get()
            self.config["output_path"]["img"] = "default" if dir_path in self.entryExtractImage.get() else self.entryExtractImage.get()
            self.config["output_path"]["video"] = "default" if dir_path in self.entryExtractVideo.get() else self.entryExtractVideo.get()
            self.config["output_path"]["custom"] = "default" if dir_path in self.entryExtractCustom.get() else self.entryExtractCustom.get()

            self.config["default_extract"]["custom_list"] = self.entry_CustomList.get().split(", ")

            status, res = jsonHandler.writeSetting(self.config)
            if status:
                messagebox.showinfo("Success", "Settings saved successfully!", parent=self.root)
            else:
                messagebox.showerror("Error", res, parent=self.root)

    def cancelConfig(self):
        # ask confirmation
        if messagebox.askokcancel("Cancel", "Are you sure you want to cancel changes made in current configuration?"):
            self.initConfig()

    def setDefaultConfig(self):
        # ask confirmation
        if messagebox.askokcancel("Set Default", "Are you sure you want to set default configuration?"):
            jsonHandler.setDefault()
            self.config = jsonHandler.default_Setting
            self.initConfig()

    def openOsu(self):
        try:
            subprocess.Popen(self.config["osu_path"] + "\\osu!.exe")
        except Exception as e:
            messagebox.showerror("Error", "Cannot open osu!\n" + str(e), parent=self.root)

    def browseOsu(self):
        pathGet = filedialog.askdirectory(initialdir=self.config["osu_path"])
        if pathGet:
            self.entry_OsuPath.delete(0, END)
            self.entry_OsuPath.insert(0, pathGet.replace("/", "\\"))

    def browseOutputPath(self, type, ref):
        pathGet = filedialog.askdirectory(initialdir=self.getOutputPath(self.config["output_path"][type], type))
        if pathGet:
            ref.delete(0, END)
            ref.insert(0, pathGet.replace("/", "\\"))

    def on_Closing(self):
        if messagebox.askyesno("Confirmation", "Are you sure you want to exit?", parent=self.root):
            self.root.destroy()
            exit()

    def getOutputPath(self, path, fileFormat):
        if path.lower() == "default":
            return f"{dir_path}\\output\\{fileFormat}\\"
        else:
            return path

    # Allowed keys
    def allowedKey(self, event):
        key = event.keysym

        # Allow
        if key.lower() in ["left", "right"]:  # Arrow left right
            return
        if 12 == event.state and key == "a":  # Ctrl + a
            return
        if 12 == event.state and key == "c":  # Ctrl + c
            return

        # If not allowed
        return "break"

    # Menubar
    def always_On_Top(self):
        if self.alwaysOnTop:
            self.alwaysOnTop = False
            self.root.wm_attributes("-topmost", False)
        else:
            self.alwaysOnTop = True
            self.root.wm_attributes("-topmost", True)

    def tutorial(self):
        # open mbox tutorial
        messagebox.showinfo(
            "Tutorial",
            """1. Configure settings (The osu! folder, output folder, and output type)\n2. Load maps\n3. Choose certain beatmaps to extract or click extract all button\n4. Done""",
        )

    def about(self, event=None):
        messagebox.showinfo(
            "About",
            """A simple Osu! Beatmap extractor. Can be use to extract songs, images, and videos from locally installed beatmaps. Made by Dadangdut33
        \r\nVersion: """
            + version
            + """
        \r\nDisclaimer: 
        \rI do not gain any money from this tool. I do not intend to support piracy of any kind. This tool is only made to help extracting (copying) song/img/videos from a beatmap. You should support the creators of each song/img/videos you extract. I recommend tools such as saucenao and tineye to find the original image and author. You should also support the original music artist by buying their songs/albums or by listening their song on official platform.
        """,
        )


# Run
if __name__ == "__main__":
    main = Main()
    main.root.mainloop()