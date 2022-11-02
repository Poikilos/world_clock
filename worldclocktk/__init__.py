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
import pytz
import yaml
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


python_mr = sys.version_info.major
if python_mr >= 3:  # try:
    from tkinter import messagebox
else:  # except ImportError:
    # Python 2
    import tkMessageBox as messagebox

ttkError = '''
ERROR: Tk is not present.
 Try installing python-tk or python3-tk

# If you still get an error, try:
python3 -m pip install ttkthemes
# See also:
# <https://stackoverflow.com/questions/66233714/installation-of-ttk-themes-for-tkinter>

'''

'''
from tkinter import ttk
try:
    from ttkthemes import ThemedTk
except ImportError:
    # python2
    pass
    # python3 -m pip install git+https://github.com/RedFantom/ttkthemes?
'''

if python_mr >= 3:  # except ImportError as ex2:
    # python 3
    # `import tkinter as tk` works in
    # recent versions of Python 2 but the other features do not.
    print("* using Python 3 ttk")
    try:
        import tkinter as tk
        # import tkinter.ttk as ttk
        from tkinter import ttk
        from ttkthemes import ThemedTk
        # ^ ImportError: No module named ttkthemes (Python2 or 3)
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
else:  # try:
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
    exit(1)

myDir = os.path.dirname(os.path.abspath(__file__))
repoDir = os.path.dirname(myDir)
assetsDir = os.path.join(myDir, "assets")
iconPngPath = os.path.join(assetsDir, "clock_mini_icon.png")
iconIcoPath = os.path.join(assetsDir, "clock_mini_icon.ico")

autocompletions = {}


def append_completion(criteria, timezone):
    criteria = criteria.lower().strip()
    tmp = autocompletions.get(criteria)
    if tmp is None:
        autocompletions[criteria] = []
    autocompletions[criteria].append(timezone)

from .find_moreplatform import moreplatform

from moreplatform import (
    # profile,
    AppData,
    # local,
    # myLocal,
    # shortcutsDir,
    # replacements,
    # username,
    # logsDir,
    # share,
    profiles,
    # temporaryFiles,
    # myCloudName,
    myCloudPath,
    getUnique,
)

MY_LUID = "world_clock"  # formerly myDirName
# ^ TODO: set to "worldclocktk"?
myShare = getUnique(MY_LUID, key="Share:Unique")
dtPath = getUnique(MY_LUID, key="Desktop:Unique")
myConfDir = getUnique(MY_LUID, key="Configs:Unique", allow_cloud=True)

if not os.path.isdir(myConfDir):
    # os.makedirs
    print('  * creating "{}"...')
    os.mkdir(myConfDir)

yamlName = "world_clock.yaml"
oldYamlPath = getUnique(MY_LUID, key="Configs:Unique")
yamlPath = os.path.join(myConfDir, yamlName)
if yamlPath != oldYamlPath:
    # ^ If there is a cloud folder
    # Check for a duplicate local folder:
    if os.path.isfile(oldYamlPath):
        if not os.path.isfile(yamlPath):
            echo0('* mv "{}" "{}"'
                  ''.format(yamlPath, newYamlPath))
            shutil.move(yamlPath, newYamlPath)
        # else getUnique already shows a warning both folders exist
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

    def __init__(self, master, zones=None, maxClockCount=20):
        self.master = master
        self.isShowingHint = False
        self.hintLabel = None
        self.savedConfig = None
        self.master.title('World Clock')

        # load last preset, otherwise load defaults
        self.loadConfig()
        if not self.config:
            if not self.zones:
                self.zones = [
                    {
                        'tz': 'US/Eastern',
                    },
                    {
                        'tz': 'US/Pacific',
                        'caption': 'California'
                    },
                ]
            self.showSecondsVar = tk.BooleanVar(value=True)

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
    if python_mr >= 3:
        root = ThemedTk(themebg=True)
        app = WorldClock(master=root)
        root.set_theme('equilux')
    else:
        # Python 2
        root = tk.Tk()
        app = WorldClock(master=root)
        app.style = ttk.Style(root)
        names = app.style.theme_names()
        styleI = 1
        print("* theme names: {}".format(names))
        app.style.theme_use(names[1])
        print("  * using style: {}".format(names[styleI]))
        '''
        See <https://www.pythontutorial.net/tkinter/tkinter-theme/> but
        they all look the same, like RedHat circa 1998, but are better
        than setting no style which uses the old x11-style dent instead
        of an arrow for drop-down boxes:
        [0] clam
        [1] alt
        [2] default
        [3] classic
        '''

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
