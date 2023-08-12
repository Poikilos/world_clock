- yaml pip install error:
ERROR: Could not find a version that satisfies the requirement yaml (from world-clock) (from versions: none)
ERROR: No matching distribution found for yaml

- Missing tkinter error:
```
ModuleNotFoundError: No module named 'tkinter'
```
  - fix on Debian-like distros (Debian requires a separate package :( ):
    `sudo apt install python3-tk`
