#!/usr/bin/env python
"""
Add and label world clocks, including duplicates with different names.
The labels can help you with remote collaboration if you put a name of
a person or organization in the label field.

"Wrote this since Win10 only allows two native clocks and the world
clock app is too massive"
-Kaveh Tehrani
"""

from __future__ import print_function

import os
import platform
import shutil
import copy
import sys
from datetime import datetime
import pytz  # provided by pytz on PyPI
import yaml  # provided by PyYAML on PyPI
# import tkinter as tk

verbosity = 0

for i in range(1, len(sys.argv)):
    arg = sys.argv[i]
    if arg == "--verbose":
        verbosity = 1
    elif arg == "--debug":
        verbosity = 2


def echo0(*args, **kwargs):  # formerly error
    print(*args, file=sys.stderr, **kwargs)


def echo1(*args, **kwargs):  # formerly debug, but verbosity was True (1)
    if verbosity >= 1:
        print(*args, file=sys.stderr, **kwargs)


def echo2(*args, **kwargs):
    if verbosity >= 2:
        print(*args, file=sys.stderr, **kwargs)


if sys.version_info.major >= 3:
    from tkinter import messagebox
else:
    # Python 2
    FileNotFoundError = IOError
    ModuleNotFoundError = ImportError
    NotADirectoryError = OSError
    import tkMessageBox as messagebox

ttkError = '''
ERROR: Tk is not present.
 Try installing python-tk or python3-tk
'''

if sys.version_info.major >= 3:
    # python 3
    # `import tkinter as tk` works in
    # recent versions of Python 2 but the other features do not.
    print("* using Python 3 ttk")
    try:
        import tkinter as tk
        # import tkinter.ttk as ttk
        from tkinter import ttk
    except ImportError as ex3:
        print()
        ttkError = str(ex3) + "\n" + ttkError
        try:
            messagebox.showerror("Error", ttkError)
        except:
            pass
        print(ttkError)
        # raise ex3
        exit(1)
else:
    import Tkinter as tk
    import ttk
    print("* using Python 2 ttk")


# s=ttk.Style()
# print("theme names: {}".format(s.theme_names()))
# ^ theme names: ('clam', 'alt', 'default', 'classic')
ttkExtError = "ttk_extensions.py should be in the worldclocktk module."
try:
    from worldclocktk.ttk_extensions import (
        AutocompleteEntry,
        DropDown,
        matches,
    )
except ModuleNotFoundError as ex:
    print(str(ex))
    messagebox.showerror("Error", ttkExtError)
    # print(ttkExtError)
    sys.exit(1)

myDir = os.path.dirname(os.path.abspath(__file__))
repoDir = os.path.dirname(myDir)
assetsDir = os.path.join(myDir, "assets")
iconPngPath = os.path.join(assetsDir, "clock_mini_icon.png")
iconIcoPath = os.path.join(assetsDir, "clock_mini_icon.ico")
THEMES_DIR = os.path.join(assetsDir, "Forest-ttk-theme")
THEME_DATA_DIR = os.path.join(THEMES_DIR, "forest-light")
autocompletions = {}


def append_completion(criteria, timezone):
    criteria = criteria.lower().strip()
    tmp = autocompletions.get(criteria)
    if tmp is None:
        autocompletions[criteria] = []
    autocompletions[criteria].append(timezone)

# region copied from hierosoft (has same author as this file)
HOME = None  # formerly profile
APPDATA = None  # formerly APPDATA
LOCALAPPDATA = None  # formerly local
SHORTCUTS_DIR = None  # formerly SHORTCUTS_DIR
SHARE = None  # formerly share
if platform.system() == "Windows":
    HOME = os.environ.get("USERPROFILE")
    _data_parent_ = os.path.join(HOME, "AppData")
    APPDATA = os.path.join(_data_parent_, "Roaming")
    LOCALAPPDATA = os.path.join(_data_parent_, "Local")
    del _data_parent_
    SHARE = LOCALAPPDATA  # It is synonymous
    SHORTCUTS_DIR = os.path.join(HOME, "Desktop")
else:
    HOME = os.environ.get("HOME")
    LOCALAPPDATA = os.path.join(HOME, ".local", "share")
    SHARE = LOCALAPPDATA  # synonymous; generally written on install
    if platform.system() == "Darwin":
        SHORTCUTS_DIR = os.path.join(HOME, "Desktop")
        Library = os.path.join(HOME, "Library")
        APPDATA = os.path.join(Library, "Application Support")
    else:
        SHORTCUTS_DIR = os.path.join(SHARE, "applications")
        APPDATA = os.path.join(HOME, ".config")

MY_LUID = "world_clock"
myShare = os.path.join(SHARE, MY_LUID)

if platform.system() == "Windows":
    dtPath = os.path.join(SHORTCUTS_DIR, MY_LUID+".blnk")
elif platform.system() == "Darwin":
    dtPath = os.path.join(SHORTCUTS_DIR, MY_LUID+".desktop")
    # TODO: ^ Use ".command", applescript, or something else.
else:
    dtPath = os.path.join(SHORTCUTS_DIR, MY_LUID+".desktop")

CONFS_DIR = APPDATA
tryConfDirs = [
    os.path.join(HOME, "Nextcloud", "profile"),
    os.path.join(HOME, "ownCloud", "profile"),
]
for tryConfDir in tryConfDirs:
    if os.path.isdir(tryConfDir):
        CONFS_DIR = tryConfDir
        break  # prefer earliest in list
if CONFS_DIR == APPDATA:
    echo0("To save a cloud profile, install Nextcloud or ownCloud"
          " and create a profile dir like one of: %s")
del tryConfDirs

myConfDir = os.path.join(CONFS_DIR, MY_LUID)
# endregion

echo0("myShare={}".format(myShare))
echo0("dtPath={}".format(dtPath))
echo0("myConfDir={}".format(myConfDir))

if not os.path.isdir(myConfDir):
    # os.makedirs
    print('  * creating "{}"...')
    os.makedirs(myConfDir)

yamlName = "world_clock.yaml"
oldYamlPath = os.path.join(APPDATA, MY_LUID)
yamlPath = os.path.join(myConfDir, yamlName)
if yamlPath != oldYamlPath:
    # ^ If there is a cloud folder
    # Check for a duplicate local folder:
    if os.path.isfile(oldYamlPath):
        if not os.path.isfile(yamlPath):
            echo0('* mv "{}" "{}"'
                  ''.format(oldYamlPath, yamlPath))
            shutil.move(oldYamlPath, yamlPath)
        # else get_unique_path already shows a warning both folders exist
if not os.path.isfile(yamlPath):
    print('  * a new "{}" will be created.'.format(yamlPath))

append_completion("India", "Asia/Kolkata")
append_completion("Kolkata", "Asia/Kolkata")
append_completion("Mumbai", "Asia/Kolkata")
append_completion("New Delhi", "Asia/Kolkata")
append_completion("Delhi", "Asia/Kolkata")
append_completion("Yemen", "Asia/Aden")
append_completion("New York", "US/Eastern")
append_completion("Honolulu", "US/Hawaii")
append_completion("Knox", "US/Indiana-Starke")
append_completion("Indiana", "US/Indiana-Starke")
append_completion("Chicago", "US/Central")
append_completion("Detroit", "US/Eastern")
append_completion("Mountain", "US/Mountain")
append_completion("Pacific", "US/Pacific")
append_completion("Samoa", "US/Samoa")
append_completion("GMT", "Etc/Greenwich")  # or "UTC" or "Etc/GMT0"
append_completion("Oahu", "US/Hawaii")
append_completion("Waikiki", "US/Hawaii")
append_completion("Finland", "Europe/Helsinki")


# "Etc/GMT+0" to "Etc/GMT+12" are valid:
for i in range(13):
    append_completion("GMT+{}".format(i), "Etc/GMT+{}".format(i))


# "Etc/GMT-0" to "Etc/GMT-14" are valid:
for i in range(15):
    append_completion("GMT-{}".format(i), "Etc/GMT-{}".format(i))


def get_timezones(criteria):
    '''
    Sequential arguments:
    criteria -- Provide a search term such as a country or city (case
                insensitive).
    '''
    got = autocompletions.get(criteria.lower())
    if got is None:
        got = []
    for name in pytz.all_timezones:
        # Also find similar ones not in autocompletions:
        if criteria.lower() in name.lower():
            if name not in got:
                got.append(name)
    if len(got) == 0:
        got = None
    return got


def list_to_english(l, sep=", ", last_sep=" or "):
    '''
    Get a list as a series of quoted elements with commas and "or",
    otherwise None if the list is None.
    '''
    if l is None:
        return None
    result = ""
    for i in range(len(l)):
        if i == (len(l)-1):
            result += last_sep
        else:
            result += sep
        result += '"{}"'.format(l[i])
    return result


def english_timezones_list(criteria, sep=", ", last_sep=" or "):
    '''
    Get matching timezones as a series of quoted elements with commas
    and "or".
    '''
    return list_to_english(get_timezones(criteria), sep=sep,
                           last_sep=last_sep)


class WorldClock:
    showTZNames = True

    @classmethod
    def getDefaultZones(cls):
        return [
            {
                'tz': 'US/Eastern',
            },
            {
                'tz': 'US/Pacific',
                'caption': 'California'
            },
        ]

    def __init__(self, master, zones=None, maxClockCount=20):
        self.master = master
        self.isShowingHint = False
        self.hintLabel = None
        self.savedConfig = None
        self.master.title('World Clock')
        self.zones = None

        # load last preset, otherwise load defaults
        self.loadConfig()

        if not self.config:
            if not self.zones:
                self.zones = WorldClock.getDefaultZones()
            self.showSecondsVar = tk.BooleanVar(value=True)
        elif not self.zones:
            self.zones = WorldClock.getDefaultZones()

        self.maxClockCount = maxClockCount
        self.clockCount = len(self.zones)

        self.frame = ttk.Frame()
        self.frame.pack()
        self.createClocks()

    def showHint(self, hint):
        if self.hintLabel is None:
            self.hintLabel = ttk.Label(self.master, text=hint)
        if not self.isShowingHint:
            self.hintLabel.pack()
        self.isShowingHint = True

    def hideHint(self):
        if self.isShowingHint:
            self.hintLabel.pack_forget()

    def getTzSafely(self, index):
        result = self.zones[index].get('tz')
        if result is None:
            result = ""
        return result

    def getCaptionSafely(self, index):
        result = self.zones[index].get('caption')
        if result is None:
            result = ""
        return result

    def createClocks(self):
        """
        Create the GUI
        """
        self.timeLabels = []
        self.captionEntries = []
        self.tzEntries = []
        for i in range(self.clockCount):
            self.tzEntries.append(AutocompleteEntry(
                pytz.all_timezones,
                self.frame,
                listboxLength=4,
                width=20,
                matchesFunction=matches,
            ))
            self.tzEntries[i].var.set(pytz.all_timezones[0])
            if i < len(self.zones):
                self.tzEntries[i].delete(0, tk.END)
                self.tzEntries[i].insert(0, self.getTzSafely(i))
            self.tzEntries[i].listbox.destroy()
            self.tzEntries[i].grid(row=i, column=0, columnspan=2)

            self.timeLabels.append(ttk.Entry(self.frame))
            self.timeLabels[i].grid(row=i, column=2, columnspan=1)
            self.timeLabels[i].bind("<Key>", lambda e: "break")

            self.captionEntries.append(ttk.Entry(self.frame, width=50))
            if i < len(self.zones):
                self.captionEntries[i].delete(0, tk.END)
                self.captionEntries[i].insert(0, self.getCaptionSafely(i))
            self.captionEntries[i].grid(row=i, column=3, columnspan=1)

        self.updateButton = ttk.Button(
            self.frame,
            text="Apply",
            command=self.redesignClocks,
        )
        self.updateButton.grid(row=i + 1, column=0, columnspan=1)
        self.clockCountDropDown = DropDown(
            self.frame,
            range(1, self.maxClockCount + 1),
            self.clockCount,
        )
        self.clockCountDropDown.grid(row=i + 1, column=1, columnspan=1)

        self.secondsCheckBox = ttk.Checkbutton(
            self.frame,
            text="Show Seconds",
            variable=self.showSecondsVar,
        )
        self.secondsCheckBox.grid(row=i + 1, column=2, columnspan=1)
        change_text(self)

    def redesignClocks(self):
        """
        Have to create a new GUI since the number of clocks changed
        """
        for w in self.frame.winfo_children():
            w.destroy()

        self.clockCount = int(app.clockCountDropDown.get())
        self.createClocks()

    def loadConfig(self):
        """
        Load previous known state if exists
        """
        try:
            self.config = yaml.safe_load(open(yamlPath))
            self.zones = self.config['zones']
            self.showSecondsVar = tk.BooleanVar(
                value=self.config['show_seconds']
            )
        except FileNotFoundError as ex:
            self.config = {}
            echo1(str(ex))
        self.savedConfig = copy.deepcopy(self.config)

    def readGUI(self):
        self.config = {
            'zones': self.zones,
            'show_seconds': self.showSecondsVar.get(),
        }

    def saveConfig(self):
        """
        Save current state
        """
        self.readGUI()
        with open(yamlPath, 'w') as config_file:
            yaml.dump(self.config, config_file)
            echo0('* wrote "{}"'.format(yamlPath))
            self.savedConfig = copy.deepcopy(self.config)


def change_text(app):
    """
    Takes our GUI and updates it for the time zones
    """
    show_seconds = app.showSecondsVar.get()
    app.zones = []
    for i in range(len(app.tzEntries)):
        app.zones.append(
            {
                'tz': app.tzEntries[i].var.get(),
                'caption': app.captionEntries[i].get(),
            },
        )
    any_hint = False
    for i, thisZone in enumerate(app.zones):
        tzStr = thisZone.get('tz')
        try:
            thisZone = pytz.timezone(tzStr)
            timeFmt = "%I:%M %p"
            if show_seconds:
                timeFmt = "%I:%M:%S %p"
            # timeFmt = f"%I:%M{':%S' if show_seconds else ''} %p"
            thisTimeStr = datetime.now(thisZone).strftime(timeFmt)
            app.timeLabels[i].delete(0, tk.END)
            app.timeLabels[i].insert(0, thisTimeStr)
        except pytz.UnknownTimeZoneError:
            app.timeLabels[i].delete(0, tk.END)
            app.timeLabels[i].insert(0, "")
            matchingListStr = None
            if len(tzStr) > 2:
                matchingListStr = english_timezones_list(
                    tzStr,
                    sep="\n",
                    last_sep="\n",
                )
            if matchingListStr is not None:
                any_hint = True
                hint = ("for {} maybe you mean:\n{}"
                        "".format(tzStr, matchingListStr))
                app.showHint(hint)
            elif len(tzStr.strip()) > 0:
                print("There is no hint for {}".format(tzStr))
            if WorldClock.showTZNames:
                WorldClock.showTZNames = False
                print("Valid timezones: {}".format(pytz.all_timezones))
    if not any_hint:
        app.hideHint()

    app.readGUI()
    if app.config != app.savedConfig:
        app.saveConfig()
    else:
        echo1("app.config: {}".format(app.config))

    # Update clocks every second if showing seconds,
    #   every 10 seconds otherwise to reduce CPU load:
    root.after(1000 if show_seconds else 10000, change_text, app)


root = None
app = None


def main():
    global root
    global app
    root = tk.Tk()
    app = WorldClock(master=root)
    app.style = ttk.Style(root)
    root.option_add("*tearOff", False) # This is always a good idea

    # Make the app responsive (from Forest ttk theme example)
    root.columnconfigure(index=0, weight=1)
    root.columnconfigure(index=1, weight=1)
    root.columnconfigure(index=2, weight=1)
    root.rowconfigure(index=0, weight=1)
    root.rowconfigure(index=1, weight=1)
    root.rowconfigure(index=2, weight=1)

    theme_name = "forest-dark"

    root.tk.call("source", os.path.join(THEMES_DIR, "%s.tcl" % theme_name))
    root.tk.call('lappend', 'auto_path', THEMES_DIR)  # necessary if not in CWD
    app.style.theme_use(theme_name)

    if platform.system() == "Windows":
        # root.iconbitmap(r'clock_mini_icon.ico')
        root.iconbitmap(iconIcoPath)
    else:
        # iconPath = os.path.realpath('clock_mini_icon.png')
        iconPath = iconPngPath
        img = tk.Image("photo", file=iconPath)
        try:
            root.tk.call('wm', 'iconphoto', root._w, img)
        except tk.TclError as ex:
            print(str(ex))

    change_text(app)
    root.mainloop()


if __name__ == '__main__':
    main()
