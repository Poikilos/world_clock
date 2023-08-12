- yaml pip install error:
ERROR: Could not find a version that satisfies the requirement yaml (from world-clock) (from versions: none)
ERROR: No matching distribution found for yaml
- ttkthemes pip install error:
```
      Traceback (most recent call last):
        File "<string>", line 2, in <module>
        File "<pip-setuptools-caller>", line 34, in <module>
        File "/tmp/pip-install-9c4m31s5/ttkthemes_062f250b1faa4402bb5e2b9bf6d683e7/setup.py", line 7, in <module>
          from tkinter import TkVersion
      ModuleNotFoundError: No module named 'tkinter'
```
  - fix on Debian-like distros (Debian requires a separate package :( ):
    `sudo apt install python3-tk`
