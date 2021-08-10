"""
Wrote this since Win10 only allows two native clocks and the world clock app is too massive

Kaveh Tehrani
"""

import datetime
import pytz
import tkinter as tk
import yaml
from tkinter import ttk
from ttkthemes import ThemedTk
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
    show_tz_names = True

    def __init__(self, master, l_tz=None, num_max_clocks=20):
        self.master = master
        self.showing_hint = False
        self.hintLabel = None
        self.master.title('Clock')

        # load last preset, otherwise load defaults
        self.load_config()
        if not self.wc_config:
            if not l_tz:
                self.l_tz = [
                    {
                        'tz': 'US/Eastern',
                    },
                    {
                        'tz': 'US/Pacific',
                        'caption': 'California'
                    },
                ]
                self.b_show_seconds = tk.BooleanVar(value=True)

        self.num_max_clocks = num_max_clocks
        self.num_clocks = len(self.l_tz)

        self.frame = ttk.Frame()
        self.frame.pack()
        self.create_clocks()

    def showHint(self, hint):
        if self.hintLabel is None:
            self.hintLabel = ttk.Label(self.master, text=hint)
        if not self.showing_hint:
            self.hintLabel.pack()
        self.showing_hint = True

    def hideHint(self):
        if self.showing_hint:
            self.hintLabel.pack_forget()

    def getTzSafely(self, index):
        result = self.l_tz[index].get('tz')
        if result is None:
            result = ""
        return result

    def getCaptionSafely(self, index):
        result = self.l_tz[index].get('caption')
        if result is None:
            result = ""
        return result

    def create_clocks(self):
        """
        Create the GUI
        """
        self.l_entries = []
        self.captionEntries = []
        self.l_dd = []
        for i in range(self.num_clocks):
            self.l_dd.append(AutocompleteEntry(pytz.all_timezones, self.frame, listboxLength=4, width=20, matchesFunction=matches))
            self.l_dd[i].var.set(pytz.all_timezones[0])
            if i < len(self.l_tz):
                self.l_dd[i].delete(0, tk.END)
                self.l_dd[i].insert(0, self.getTzSafely(i))
            self.l_dd[i].listbox.destroy()
            self.l_dd[i].grid(row=i, column=0, columnspan=2)

            self.l_entries.append(ttk.Entry(self.frame))
            self.l_entries[i].grid(row=i, column=2, columnspan=1)
            self.l_entries[i].bind("<Key>", lambda e: "break")

            self.captionEntries.append(ttk.Entry(self.frame))
            if i < len(self.l_tz):
                self.captionEntries[i].delete(0, tk.END)
                self.captionEntries[i].insert(0, self.getCaptionSafely(i))
            self.captionEntries[i].grid(row=i, column=3, columnspan=1)

        self.bt_update = ttk.Button(self.frame, text="Apply", command=self.redesign_clocks)
        self.bt_update.grid(row=i + 1, column=0, columnspan=1)
        self.dd_num_clocks = DropDown(self.frame, range(1, self.num_max_clocks + 1), self.num_clocks)
        self.dd_num_clocks.grid(row=i + 1, column=1, columnspan=1)

        self.ck_seconds = ttk.Checkbutton(self.frame, text="Show Seconds", variable=self.b_show_seconds)
        self.ck_seconds.grid(row=i + 1, column=2, columnspan=1)
        change_text(self)

    def redesign_clocks(self):
        """
        Have to create a new GUI since the number of clocks changed
        """
        for w in self.frame.winfo_children():
            w.destroy()

        self.num_clocks = int(app.dd_num_clocks.get())
        self.create_clocks()

    def load_config(self):
        """
        Load previous known state if exists
        """
        try:
            self.wc_config = yaml.safe_load(open(r'world_clock.yaml'))
            self.l_tz = self.wc_config['zones']
            self.b_show_seconds = tk.BooleanVar(value=self.wc_config['show_seconds'])
        except FileNotFoundError:
            self.wc_config = {}

    def save_config(self):
        """
        Save current state
        """
        wc_config = {'zones': self.l_tz, 'show_seconds': self.b_show_seconds.get()}

        with open(r'world_clock.yaml', 'w') as config_file:
            yaml.dump(wc_config, config_file)


def change_text(app):
    """
    Takes our GUI and updates it for the time zones
    """
    b_seconds = app.b_show_seconds.get()
    app.l_tz = []
    for i in range(len(app.l_dd)):
        app.l_tz.append(
            {
                'tz': app.l_dd[i].var.get(),
                'caption': app.captionEntries[i].get(),
            },
        )
    any_hint = False
    for i, thisZone in enumerate(app.l_tz):
        str_tz = thisZone.get('tz')
        try:
            cur_zone = pytz.timezone(str_tz)
            cur_time = datetime.datetime.now(cur_zone).strftime(f"%I:%M{':%S' if b_seconds else ''} %p")
            app.l_entries[i].delete(0, tk.END)
            app.l_entries[i].insert(0, cur_time)
        except pytz.UnknownTimeZoneError:
            app.l_entries[i].delete(0, tk.END)
            app.l_entries[i].insert(0, "")
            matchingListStr = None
            if len(str_tz) > 2:
                matchingListStr = english_timezones_list(
                    str_tz,
                    sep="\n",
                    last_sep="\n",
                )
            if matchingListStr is not None:
                any_hint = True
                hint = ("for {} maybe you mean:\n{}"
                        "".format(str_tz, matchingListStr))
                app.showHint(hint)
            elif len(str_tz.strip()) > 0:
                print("There is no hint for {}".format(str_tz))
            if WorldClock.show_tz_names:
                WorldClock.show_tz_names = False
                print("Valid timezones: {}".format(pytz.all_timezones))
    if not any_hint:
        app.hideHint()
    app.save_config()

    # update clocks every second if showing seconds, every 10 seconds otherwise to reduce cpu load
    root.after(1000 if b_seconds else 10000, change_text, app)


if __name__ == '__main__':
    root = ThemedTk(themebg=True)
    app = WorldClock(master=root)
    root.set_theme('equilux')
    if platform.system() == "Windows":
        root.iconbitmap(r'clock_mini_icon.ico')
    else:
        iconPath = os.path.realpath('clock_mini_icon.png')
        img = tk.Image("photo", file=iconPath)
        root.tk.call('wm', 'iconphoto', root._w, img)

    change_text(app)
    root.mainloop()
