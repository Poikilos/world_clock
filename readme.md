# Small GUI for a compact world clock
<https://github.com/Poikilos/world_clock> (fork of <https://github.com/kavehtehrani/world_clock>)

With other multi-timezone clocks you can see where has what time, but
with world_clock you can see who! You can add a person's name or any
custom note to any clock, and even add more than one with the same
timezone.

Save to the cloud if you have a working Nextcloud/profile/ or
ownCloud/profile/ directory in your user folder! This program does not
use a web API. It simply uses one of those directories if it is there,
instead of the default which is AppData (or .config for GNU+Linux
systems, or Application Support for Darwin).


## Differences in Poikilos' fork
- It saves to a proper appdata folder for the OS, or to a cloud profile.
- You can add a note to any clock.
- Allow some colloquial timezones in the auto-complete (There are some manually-defined auto-complete strings not just technical ones from pytz.all_timezones).
  - The feedback for correct or incorrect strings is improved.
  - See [worldclocktk/__init__.py](worldclocktk/__init__.py) for the complete list.
- The installation has been standardized (There is a requirements.txt file and a setup.py file.
  - There is also a special setup.sh you can run afterward to get a visible icon if you have a GNU+Linux desktop.
- The custom icon appears on the taskbar on both Windows and GNU+Linux systems.
- The theme is now the Forest theme (included; Hierosoft python2-compatible fork; See [./worldclocktk/assets/Forest-ttk-theme/LICENSE](./worldclocktk/assets/Forest-ttk-theme/LICENSE))
  - Therefore, the ttkthemes package is no longer required.

upstream screenshot, before adding notes feature:
![alt text](screenshot.png)


## Install
- If you first create `$HOME/Nextcloud/profile` [or the same in ownCloud], that will be detected and used as the application data folder.
- Get Python
  - If you are using Windows, you must first install Python from python.org.
  - Other OS: install the `python` package using your "Software" application (You also need `python3-tk` or `python-tk` packages if you are using a Debian-based distro such as Ubuntu).
- `git clone https://github.com/Poikilos/world_clock`
- `cd world_clock`
- Install the module:
  - Windows: `python -m pip install setup.py`
  - Other OS: `python3 -m pip install setup.py`
- If you are using Python 2 (Run `python --version` to check), you must:
  - Download pyyaml from <https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyyaml> for your version of python (cp27 for Python 2.7 for example, and amd64 in most cases [64-bit Windows, AMD or Intel]).
  - Open a Command Prompt
  - `cd Downloads`
  - `pip install PyYAML‑5.3‑cp27‑cp27m‑win_amd64.whl` (replace `PyYAML‑5.3‑cp27‑cp27m‑win_amd64.whl` with the correct one you downloaded for your Python and OS)
- Install the shortcut (icon):
  - Windows: Right-click the Desktop then:
    - Create the Shortcut to `C:\Python27\Scripts\world_clock.exe`
      - Except: Replace `C:\Python27` with your Python installation such as `C:\Program Files\Python311`, or `%LOCALAPPDATA%\Programs\Python311` if you didn't install Python with the "All Users" option.
      - Choose the icon from `C:\Python27\lib\site-packages\world_clock\assets\`.
  - Other OS: Run via `bash setup.sh` (as a non-root user that you use for your desktop environment)
