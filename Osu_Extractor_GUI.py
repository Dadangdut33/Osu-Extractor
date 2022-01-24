# Internal
import os
import subprocess
from sys import exit
import threading
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter.ttk as ttk
import webbrowser

# User lib
from osu_extractor.GetData import getSubFolder, getAllItemsInFolder, getFolderName, extractFiles, createPathIfNotExist, keepCertainListByKeyword, getFileTypeListInFolder
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
        messagebox.showerror("Error", "Cannot find the file specified.")
    except Exception:
        try:
            subprocess.Popen(["xdg-open", filename])
        except FileNotFoundError:
            messagebox.showerror("Error", "Cannot find the file specified.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


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
        self.frame_2.pack(side=TOP, fill=BOTH, expand=TRUE, padx=5, pady=5)

        self.frame_2_row_1 = Frame(self.frame_2)
        self.frame_2_row_1.pack(side=TOP, fill=X, expand=False)

        self.frame_2_row_2 = Frame(self.frame_2)
        self.frame_2_row_2.pack(side=TOP, fill=X, expand=False)

        self.frame_2_row_3 = Frame(self.frame_2)  # TABLE
        self.frame_2_row_3.pack(side=TOP, fill=BOTH, expand=TRUE)

        # 3
        self.frame_3 = Frame(self.root)
        self.frame_3.pack(side=BOTTOM, fill=X, expand=False, padx=5, pady=5)

        self.frame_3_row_1 = Frame(self.frame_3)
        self.frame_3_row_1.pack(side=TOP, fill=X, expand=False)

        # Content
        # 1
        self.label_OsuPath = Label(self.frame_1_row_1, text="Osu! Path")
        self.label_OsuPath.pack(side=LEFT, padx=5, pady=5)
        CreateToolTip(self.label_OsuPath, "Osu game directory")

        self.entry_OsuPath = ttk.Entry(self.frame_1_row_1, width=50)
        self.entry_OsuPath.pack(side=LEFT, padx=5, pady=5, expand=True, fill=X)
        self.entry_OsuPath.bind("<Key>", lambda event: self.allowedKey(event))  # Disable input
        CreateToolTip(self.entry_OsuPath, "Osu game directory")

        self.browse_OsuPath = ttk.Button(self.frame_1_row_1, text="Browse", command=lambda: self.browseOsu())
        self.browse_OsuPath.pack(side=LEFT, padx=5, pady=5)

        self.varExtractSong = BooleanVar()
        self.varExtractSong.set(self.config["default_extract"]["song"])
        self.checkExtractSong = ttk.Checkbutton(self.frame_1_row_2, text="Extract Song (.mp3)", variable=self.varExtractSong)
        self.checkExtractSong.pack(side=LEFT, padx=5, pady=5)
        CreateToolTip(self.checkExtractSong, "Extract song to output folder")

        self.entryExtractSong = ttk.Entry(self.frame_1_row_2, width=16)
        self.entryExtractSong.pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)
        CreateToolTip(self.entryExtractSong, "Right Click to change output path of extracted song")
        self.entryExtractSong.bind("<Key>", lambda event: self.allowedKey(event))  # Disable input
        self.entryExtractSong.bind("<Button-3>", lambda event: self.browseOutputPath("song", self.entryExtractSong))

        self.varExtractImage = BooleanVar()
        self.varExtractImage.set(self.config["default_extract"]["img"])
        self.checkExtractImage = ttk.Checkbutton(self.frame_1_row_2, text="Extract Image (.jpg)", variable=self.varExtractImage)
        self.checkExtractImage.pack(side=LEFT, padx=5, pady=5)
        CreateToolTip(self.checkExtractImage, "Extract image to output folder")

        self.entryExtractImage = ttk.Entry(self.frame_1_row_2, width=15)
        self.entryExtractImage.pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)
        CreateToolTip(self.entryExtractImage, "Right Click to change output path of extracted image")
        self.entryExtractImage.bind("<Key>", lambda event: self.allowedKey(event))  # Disable input
        self.entryExtractImage.bind("<Button-3>", lambda event: self.browseOutputPath("img", self.entryExtractImage))

        self.varExtractVideo = BooleanVar()
        self.varExtractVideo.set(self.config["default_extract"]["video"])
        self.checkExtractVideo = ttk.Checkbutton(self.frame_1_row_3, text="Extract Video (.avi)", variable=self.varExtractVideo)
        self.checkExtractVideo.pack(side=LEFT, padx=(5, 11), pady=5)
        CreateToolTip(self.checkExtractVideo, "Extract video to output folder")

        self.entryExtractVideo = ttk.Entry(self.frame_1_row_3, width=12)
        self.entryExtractVideo.pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)
        self.entryExtractVideo.bind("<Key>", lambda event: self.allowedKey(event))  # Disable input
        CreateToolTip(self.entryExtractVideo, "Right Click to change output path of extracted video")
        self.entryExtractVideo.bind("<Button-3>", lambda event: self.browseOutputPath("video", self.entryExtractVideo))

        self.varExtractCustom = BooleanVar()
        self.varExtractCustom.set(self.config["default_extract"]["custom"])
        self.checkExtractCustom = ttk.Checkbutton(self.frame_1_row_3, text="Extract Custom", variable=self.varExtractCustom, command=lambda: self.toggleExtractCustom())
        self.checkExtractCustom.pack(side=LEFT, padx=5, pady=5)
        CreateToolTip(self.checkExtractCustom, "Extract custom lists provided to output folder")

        self.entryExtractCustom = ttk.Entry(self.frame_1_row_3, width=15)
        self.entryExtractCustom.pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)
        self.entryExtractCustom.bind("<Key>", lambda event: self.allowedKey(event))  # Disable input
        CreateToolTip(self.entryExtractCustom, "Right Click to change output path of extracted custom list")

        # Custom list entry
        self.label_CustomList = Label(self.frame_1_row_4, text="Custom List")
        self.label_CustomList.pack(side=LEFT, padx=(5, 3), pady=5)
        CreateToolTip(self.label_CustomList, "Custom file type extract. Input the file format with dot and separated by space, ex: .png .wav")

        self.entry_CustomList = ttk.Entry(self.frame_1_row_4, width=30)
        self.entry_CustomList.pack(side=LEFT, padx=(0, 5), pady=5, fill=X, expand=True)
        CreateToolTip(self.entry_CustomList, "Custom file type extract. Input the file format with dot and separated by space, ex: .png .wav")

        # Save, cancel, set default btn
        self.btn_Save = ttk.Button(self.frame_1_row_5, text="Save", command=lambda: self.saveConfig())
        self.btn_Save.pack(side=RIGHT, padx=5, pady=5)
        CreateToolTip(self.btn_Save, "Save current settings so they can be loaded next time")

        self.btn_Cancel = ttk.Button(self.frame_1_row_5, text="Cancel", command=lambda: self.cancelConfig())
        self.btn_Cancel.pack(side=RIGHT, padx=5, pady=5)
        CreateToolTip(self.btn_Cancel, "Cancel any changes and reset to currently saved settings")

        self.btn_SetDefault = ttk.Button(self.frame_1_row_5, text="Set Default", command=lambda: self.setDefaultConfig())
        self.btn_SetDefault.pack(side=RIGHT, padx=5, pady=5)
        CreateToolTip(self.btn_SetDefault, "Reset to default settings")

        self.initConfig()

        # 2
        # Label for map count
        self.label_MapCount = Label(self.frame_2_row_1, text="Beatmaps loaded: 0")
        self.label_MapCount.pack(side=LEFT, padx=5, pady=5)

        # label processed
        self.label_Processed = Label(self.frame_2_row_1, text="Processed: 0/0")
        self.label_Processed.pack(side=LEFT, padx=5, pady=5)

        # entry for filter
        # filter label
        self.label_Filter = Label(self.frame_2_row_2, text="Filter:")
        self.label_Filter.pack(side=LEFT, padx=5, pady=5)
        CreateToolTip(self.label_Filter, "Filter beatmaps by folder/beatmap name")

        self.varEntryFilter = StringVar()
        self.entry_Filter = ttk.Entry(self.frame_2_row_2, textvariable=self.varEntryFilter, width=30)
        self.entry_Filter.pack(side=LEFT, padx=(0, 5), pady=5, fill=X, expand=False)
        CreateToolTip(self.entry_Filter, "Filter beatmaps by folder/beatmap name")

        # Btn
        # Load, extract all, extract selected, clear all, clear selected
        self.btn_Load = ttk.Button(self.frame_2_row_2, text="Load Maps", command=lambda: self.loadMaps())
        self.btn_Load.pack(side=LEFT, padx=5, pady=5)
        CreateToolTip(self.btn_Load, "Load beatmaps data into table")

        self.btn_ExtractAll = ttk.Button(self.frame_2_row_2, text="Extract All", command=lambda: self.extractAll())
        self.btn_ExtractAll.pack(side=LEFT, padx=5, pady=5)
        CreateToolTip(self.btn_ExtractAll, "Extract all loaded beatmaps")

        self.btn_ExtractSelected = ttk.Button(self.frame_2_row_2, text="Extract Selected", command=lambda: self.extractSelected())
        self.btn_ExtractSelected.pack(side=LEFT, padx=5, pady=5)
        CreateToolTip(self.btn_ExtractSelected, "Extract currently selected beatmaps")

        self.btn_ClearAll = ttk.Button(self.frame_2_row_2, text="Clear All", command=lambda: self.clearAll())
        self.btn_ClearAll.pack(side=LEFT, padx=5, pady=5)
        CreateToolTip(self.btn_ClearAll, "Clear table")

        self.btn_ClearSelected = ttk.Button(self.frame_2_row_2, text="Clear Selected", command=lambda: self.clearSelected())
        self.btn_ClearSelected.pack(side=LEFT, padx=5, pady=5)
        CreateToolTip(self.btn_ClearSelected, "Delete currently selected beatmaps from the table")

        # Table for map list
        self.scrollbarY = Scrollbar(self.frame_2_row_3, orient=VERTICAL)
        self.scrollbarY.pack(side=RIGHT, fill=Y)
        # self.scrollbarX = Scrollbar(self.frame_2_row_3, orient=HORIZONTAL)
        # self.scrollbarX.pack(side=BOTTOM, fill=X)

        self.table_MapList = ttk.Treeview(self.frame_2_row_3, height=10, selectmode="extended", columns=("#", "Name", "Path"))
        self.table_MapList.pack(side=LEFT, padx=5, pady=5, fill=BOTH, expand=True)

        self.table_MapList.heading("#0", text="", anchor=CENTER)
        self.table_MapList.heading("#1", text="#", anchor=CENTER)
        self.table_MapList.heading("#2", text="Name", anchor=CENTER)
        self.table_MapList.heading("#3", text="Available Extension", anchor=CENTER)

        self.table_MapList.column("#0", width=0, stretch=False)
        self.table_MapList.column("#1", width=50, stretch=False)
        self.table_MapList.column("#2", width=300, stretch=True)
        self.table_MapList.column("#3", width=200, stretch=False)

        # self.scrollbarX.config(command=self.table_MapList.xview)
        self.scrollbarY.config(command=self.table_MapList.yview)
        self.table_MapList.config(yscrollcommand=self.scrollbarY.set)
        self.table_MapList.bind("<Button-1>", self.handle_click)

        # 3
        # loadbar
        self.loadbar = ttk.Progressbar(self.frame_3_row_1, orient=HORIZONTAL, length=200, mode="determinate")
        self.loadbar.pack(side=TOP, fill=BOTH, expand=True)

        # For the label
        self.processed = 0
        self.total = 0
        self.cancel = False

        # Set logo
        try:
            self.root.iconbitmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), "logo.ico"))
        except Exception:
            pass

    def clearAll(self):
        # Ask confirmation first
        if len(self.table_MapList.get_children()) > 0:
            if messagebox.askokcancel("Clear All", "Are you sure you want to clear all loaded beatmaps?"):
                self.table_MapList.delete(*self.table_MapList.get_children())

                # Update label
                self.label_MapCount.config(text="Beatmaps loaded: 0")
                self.label_Processed.config(text="Processed: 0/0")

    def clearSelected(self):
        if len(self.table_MapList.selection()) > 0:
            for item in self.table_MapList.selection():
                self.table_MapList.delete(item)
                self.total -= 1
            # Update label
            self.label_MapCount.config(text="Beatmaps loaded: {}".format(len(self.table_MapList.get_children())))
            self.label_Processed.config(text="Processed: {}/{}".format(self.processed, self.total))

    def extractAll(self):
        # Check if osu exist in path or not
        if not os.path.exists(self.entry_OsuPath.get()) or "osu!.exe" not in os.listdir(self.entry_OsuPath.get()):
            messagebox.showwarning("Warning", "Couldn't find osu!.exe in path provided.", parent=self.root)
            # show warning and ask confirmation to procceed or not
            if not messagebox.askokcancel("Warning", "Seems like your Osu! path is incorrect, we couldn't find osu!.exe in the path.\nDo you still want to continue?", parent=self.root):
                return

        # Check if value > 0
        if len(self.table_MapList.get_children()) > 0:
            # Check if any of the setting is checked
            if not self.varExtractSong.get() and not self.varExtractImage.get() and not self.varExtractVideo.get() and not self.varExtractCustom.get():
                messagebox.showerror("Error", "No setting is checked. Please check at least one setting.")
                return

            # Check if custom only but there is no custom list
            customList = self.entry_CustomList.get().strip().split(" ")
            # remove any empty string in customList
            customList = list(filter(None, customList))
            # Check if custom list is empty
            if self.varExtractCustom.get() and len(customList) == 0:
                messagebox.showerror("Error", "Custom extract is checked but there is no custom list. Please set the custom list first.")
                return

            # Ask confirmation first
            if messagebox.askokcancel("Extract All", "Are you sure you want to extract all loaded beatmaps with the current configuration?"):
                # Loop through all loaded beatmaps
                counter = 0
                totals = len(self.table_MapList.get_children())
                self.loadbar.config(maximum=totals)
                # Update val
                updateVal = 50
                self.disableWidgets()

                for i, item in enumerate(self.table_MapList.get_children()):
                    theItem = self.table_MapList.item(item)["text"]
                    theFile = getAllItemsInFolder(theItem)
                    counter += 1
                    # Check extract type
                    if self.varExtractSong.get():
                        extractFiles(theItem, theFile, ".mp3", self.getOutputPath(self.config["output_path"]["song"], "song"), getFolderName(theItem))
                    if self.varExtractImage.get():
                        extractFiles(theItem, theFile, ".jpg", self.getOutputPath(self.config["output_path"]["img"], "img"), getFolderName(theItem))
                    if self.varExtractVideo.get():
                        extractFiles(theItem, theFile, ".avi", self.getOutputPath(self.config["output_path"]["video"], "video"), getFolderName(theItem))
                    if self.varExtractCustom.get():
                        for custom in customList:
                            extractFiles(theItem, theFile, custom, self.getOutputPath(self.config["output_path"]["custom"], "custom"), getFolderName(item))

                    # Delete item index 0
                    self.table_MapList.delete(item)

                    # Update label
                    self.processed += 1
                    # Update root
                    if i % updateVal == 0:
                        self.label_Processed.config(text="Processed: {}/{}".format(self.processed, self.total))
                        self.loadbar.config(value=counter)
                        self.root.update()

                # Update label and enable widgets again
                self.label_Processed.config(text="Processed: {}/{}".format(self.processed, self.total))
                self.enableWidgets()

                # Set loadbar back to 0
                self.loadbar.config(value=0)

                # Tell success
                messagebox.showinfo("Extract All Success", "Extraction completed successfully! Successfully extracted {} beatmaps.".format(self.processed))
        else:
            messagebox.showinfo("Extract All", "No beatmaps loaded.")

    def extractSelected(self):
        # Check if osu exist in path or not
        if not os.path.exists(self.entry_OsuPath.get()) or "osu!.exe" not in os.listdir(self.entry_OsuPath.get()):
            messagebox.showwarning("Warning", "Couldn't find osu!.exe in path provided.", parent=self.root)
            # show warning and ask confirmation to procceed or not
            if not messagebox.askokcancel("Warning", "Seems like your Osu! path is incorrect, we couldn't find osu!.exe in the path.\nDo you still want to continue?", parent=self.root):
                return

        # Check if custom only but there is no custom list
        customList = self.entry_CustomList.get().strip().split(" ")
        # remove any empty string in customList
        customList = list(filter(None, customList))
        # Check if custom list is empty
        if self.varExtractCustom.get() and len(customList) == 0:
            messagebox.showerror("Error", "Custom extract is checked but there is no custom list. Please set the custom list first.")
            return

        # Check if there is any selected
        if len(self.table_MapList.selection()) > 0:
            # Ask confirmation first
            if messagebox.askokcancel("Extract Selected", "Are you sure you want to extract currently selected beatmaps with the current configuration?"):
                # Get the data of selected in table
                selected_data = [self.table_MapList.item(item)["values"] for item in self.table_MapList.selection()]
                counter = 0
                for item in selected_data:
                    item = f"{self.entry_OsuPath.get()}\\songs\\{item[1]}"
                    theFile = getAllItemsInFolder(item)

                    counter += 1
                    # Check extract type
                    if self.varExtractSong.get():
                        extractFiles(item, theFile, ".mp3", self.getOutputPath(self.config["output_path"]["song"], "song"), getFolderName(item))
                    if self.varExtractImage.get():
                        extractFiles(item, theFile, ".jpg", self.getOutputPath(self.config["output_path"]["img"], "img"), getFolderName(item))
                    if self.varExtractVideo.get():
                        extractFiles(item, theFile, ".avi", self.getOutputPath(self.config["output_path"]["video"], "video"), getFolderName(item))
                    if self.varExtractCustom.get():
                        for custom in customList:
                            extractFiles(item, theFile, custom, self.getOutputPath(self.config["output_path"]["custom"], "custom"), getFolderName(item))

                for item in self.table_MapList.selection():
                    self.table_MapList.delete(item)

                self.processed += counter
                # Update label
                self.label_Processed.config(text="Processed: {}/{}".format(self.processed, self.total))

                # Show mbox success
                messagebox.showinfo("Extract Selected Success", "Successfully extracted {} selected beatmaps".format(counter))

    def loadMaps(self):
        # load maps
        path = f"{self.config['osu_path']}\Songs"
        beatmapsPath = getSubFolder(path)

        # check filter
        filter = self.varEntryFilter.get().strip()
        if len(filter) > 0:
            beatmapsPath = keepCertainListByKeyword(beatmapsPath, filter)

        totals = len(beatmapsPath)
        self.loadbar.config(maximum=totals)

        self.label_MapCount.config(text=f"Beatmaps loaded: {totals}")
        self.label_Processed.config(text="Processed: 0/{}".format(totals))

        # clear table
        self.table_MapList.delete(*self.table_MapList.get_children())

        self.disableWidgets()

        # Update val
        updateVal = 100
        if totals > 100:
            updateVal = 100
        if totals > 300:
            updateVal = 300
        if totals > 1500:
            updateVal = 500

        # load table
        for i, beatmap in enumerate(beatmapsPath):
            self.table_MapList.insert("", "end", text=beatmap, values=(i + 1, getFolderName(beatmap), getFileTypeListInFolder(beatmap)))
            # update loadbar
            self.loadbar["value"] = i + 1

            # Update root
            if i % updateVal == 0:
                self.root.update()

        # Set loadbar value to 0
        self.loadbar.config(value=0)
        self.total = totals
        self.processed = 0

        self.enableWidgets()

    def disableWidgets(self):
        # Disable some widgets
        self.scrollbarY.pack_forget()
        self.menubar.entryconfig(1, state="disabled")
        self.menubar.entryconfig(2, state="disabled")
        self.menubar.entryconfig(3, state="disabled")
        for child in self.frame_1_row_1.winfo_children():
            child.configure(state=DISABLED)

        for child in self.frame_1_row_2.winfo_children():
            child.configure(state=DISABLED)

        for child in self.frame_1_row_3.winfo_children():
            child.configure(state=DISABLED)

        for child in self.frame_1_row_5.winfo_children():
            child.configure(state=DISABLED)

        for child in self.frame_2_row_2.winfo_children():
            child.configure(state=DISABLED)

        self.entryExtractSong.bind("<Button-3>", lambda event: None)
        self.entryExtractImage.bind("<Button-3>", lambda event: None)
        self.entryExtractVideo.bind("<Button-3>", lambda event: None)
        self.entryExtractCustom.bind("<Button-3>", lambda event: None)

    def enableWidgets(self):
        # Enable again
        self.scrollbarY.pack(side=RIGHT, fill=Y)
        self.menubar.entryconfig(1, state=NORMAL)
        self.menubar.entryconfig(2, state=NORMAL)
        self.menubar.entryconfig(3, state=NORMAL)
        for child in self.frame_1_row_1.winfo_children():
            child.configure(state=NORMAL)

        for child in self.frame_1_row_2.winfo_children():
            child.configure(state=NORMAL)

        for child in self.frame_1_row_3.winfo_children():
            child.configure(state=NORMAL)

        for child in self.frame_1_row_5.winfo_children():
            child.configure(state=NORMAL)

        for child in self.frame_2_row_2.winfo_children():
            child.configure(state=NORMAL)

        self.entryExtractSong.bind("<Button-3>", lambda event: self.browseOutputPath("song", self.entryExtractSong))
        self.entryExtractImage.bind("<Button-3>", lambda event: self.browseOutputPath("img", self.entryExtractImage))
        self.entryExtractVideo.bind("<Button-3>", lambda event: self.browseOutputPath("video", self.entryExtractVideo))
        self.entryExtractCustom.bind("<Button-3>", lambda event: self.browseOutputPath("custom", self.entryExtractCustom))

    def handle_click(self, event):
        if self.table_MapList.identify_region(event.x, event.y) == "separator":
            return "break"

    def toggleExtractCustom(self):
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
        self.entry_CustomList.insert(0, " ".join(self.config["default_extract"]["custom_list"]))

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

            self.config["default_extract"]["custom_list"] = self.entry_CustomList.get().split(" ")

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
            # check if osu!.exe is in the directory
            if not os.path.isfile(pathGet + "\\osu!.exe"):
                # Show warning
                messagebox.showwarning("Warning", "Could not found osu!.exe in the directory!", parent=self.root)

                # Ask confirmation to procceed
                if not messagebox.askokcancel("Warning", "Osu!.exe could not be found in the directory provided. Are you sure you want to use it as the Osu! path?", parent=self.root):
                    return

            self.entry_OsuPath.delete(0, END)
            self.entry_OsuPath.insert(0, pathGet.replace("/", "\\"))

            # Show success
            messagebox.showinfo("Success", "Osu! path set successfully!", parent=self.root)

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
