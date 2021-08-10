#!/usr/bin/env python
"""
"Wrote this since Win10 only allows two native clocks and the world clock app is too massive"
-Kaveh Tehrani
"""

from datetime import datetime
import pytz
# import tkinter as tk
import yaml

python_revision = 2
try:
    import Tkinter as tk
    import ttk
    print("* using Python 2 ttk")
except ImportError as ex2:
    python_revision = 3
    # python 3
    # Make this the exception since `import tkinter as tk` works in
    # recent versions of Python 2 but the other features do not.
    print("* using Python 3 ttk")
    try:
        import tkinter as tk
        # import tkinter.ttk as ttk
        from tkinter import ttk
        from ttkthemes import ThemedTk
    except ImportError as ex3:
        print()
        print("ERROR: Tk is not present."
              " Try installing python-tk or python3-tk")
        print()
        print()
        exit(1)
'''
from tkinter import ttk
try:
    from ttkthemes import ThemedTk
except ImportError:
    # python2
    pass
    # python3 -m pip install git+https://github.com/RedFantom/ttkthemes?
'''

# s=ttk.Style()
# print("theme names: {}".format(s.theme_names()))
# ^ theme names: ('clam', 'alt', 'default', 'classic')

from ttk_extensions import AutocompleteEntry, DropDown, matches
import platform
import os
try:
    from tkinter import messagebox
except ImportError:
    # Python 2
    import tkMessageBox as messagebox


autocompletions = {}


def append_completion(criteria, timezone):
    criteria = criteria.lower().strip()
    tmp = autocompletions.get(criteria)
    if tmp is None:
        autocompletions[criteria] = []
    autocompletions[criteria].append(timezone)


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
        self.master.title('Clock')

        # load last preset, otherwise load defaults
        self.loadConfig()
        if not self.config:
            if not zones:
                self.zones = [
                    {
                        'tz': 'US/Eastern',
                    },
                    {
                        'tz': 'US/Pacific',
                        'caption': 'California'
                    },
                ]
                self.showSeconds = tk.BooleanVar(value=True)

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
            self.tzEntries.append(AutocompleteEntry(pytz.all_timezones, self.frame, listboxLength=4, width=20, matchesFunction=matches))
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

        self.updateButton = ttk.Button(self.frame, text="Apply", command=self.redesignClocks)
        self.updateButton.grid(row=i + 1, column=0, columnspan=1)
        self.clockCountDropDown = DropDown(self.frame, range(1, self.maxClockCount + 1), self.clockCount)
        self.clockCountDropDown.grid(row=i + 1, column=1, columnspan=1)

        self.secondsCheckBox = ttk.Checkbutton(self.frame, text="Show Seconds", variable=self.showSeconds)
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
            self.config = yaml.safe_load(open(r'world_clock.yaml'))
            self.zones = self.config['zones']
            self.showSeconds = tk.BooleanVar(value=self.config['show_seconds'])
        except FileNotFoundError:
            self.config = {}

    def saveConfig(self):
        """
        Save current state
        """
        config = {'zones': self.zones, 'show_seconds': self.showSeconds.get()}

        with open(r'world_clock.yaml', 'w') as config_file:
            yaml.dump(config, config_file)


def change_text(app):
    """
    Takes our GUI and updates it for the time zones
    """
    show_seconds = app.showSeconds.get()
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
    app.saveConfig()

    # update clocks every second if showing seconds, every 10 seconds otherwise to reduce cpu load
    root.after(1000 if show_seconds else 10000, change_text, app)


if __name__ == '__main__':
    if python_revision == 3:
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
        # They all look the same, like RedHat circa 1998,
        # but are better than setting no
        # style which uses the old x11-style dent instead of an arrow
        # for drop-down boxes:
        # [0] clam
        # [1] alt
        # [2] default
        # [3] classic

    if platform.system() == "Windows":
        root.iconbitmap(r'clock_mini_icon.ico')
    else:
        iconPath = os.path.realpath('clock_mini_icon.png')
        img = tk.Image("photo", file=iconPath)
        try:
            root.tk.call('wm', 'iconphoto', root._w, img)
        except tk.TclError as ex:
            print(str(ex))

    change_text(app)
    root.mainloop()
