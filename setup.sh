#!/bin/bash
myPath="`realpath "$0"`"
echo "$myPath"
basePath="`dirname "$myPath"`"
echo "$basePath"
programs_path="$HOME/.local/lib"
dst_path="$programs_path/world_clock"
mkdir -p "$programs_path"
main_script="world_clock.py"
good_flag_file="$main_script"
shortcuts_dir="$HOME/.local/share/applications"
if [ ! -f "$good_flag_file" ]; then
    echo "Error: This script must run from the directory containing $good_flag_file."
    exit 1
fi
if [ "@$basePath" = "@$dst_path" ]; then
    echo "The program is already installed."
else
    if [ ! -d "$dst_path" ]; then
        if [ ! -d "$programs_path" ]; then
            echo "This setup script requires $programs_path to exist."
            exit 1
        fi
        echo "* installing \"$dst_path\"..."
        cp -R "$basePath" $programs_path/
        if [ $? -eq 0 ]; then
            echo "  * installing...OK"
        else
            echo "  * installing...FAILED"
        fi
    else
        if [ ! -f "`command -v rsync`" ]; then
            echo "Error: upgrading is only available if you first install rsync."
            exit 1
        fi
        echo "* upgrading \"$dst_path\"..."
        rsync -rt "$basePath/" "$dst_path"
        if [ $? -eq 0 ]; then
            echo "  * upgrading...OK"
        else
            echo "  * upgrading...FAILED"
        fi
    fi
fi
printf "* chmod +x \"$dst_path/$main_script\"..."
chmod +x "$dst_path/$main_script"
if [ $? -eq 0 ]; then
    echo "OK"
else
    echo "FAILED"
fi
THIS_PYTHON_NAME=python3
THIS_PYTHON=/usr/bin/python3
if [ ! -f "`command -v python3`" ]; then
    echo "Warning: this program requires python3."
    if [ -f "`command -v python`" ]; then
        THIS_PYTHON_NAME=python
        THIS_PYTHON="`command -v $THIS_PYTHON_NAME`"
        echo "* The Python binary for the icon was set to \"$THIS_PYTHON\"."
    fi
else
    THIS_PYTHON="`command -v $THIS_PYTHON_NAME`"
fi
#if [ ! -d "$shortcuts_dir" ]; then
mkdir -p "$shortcuts_dir"
#fi
sc_path="$shortcuts_dir/world_clock.desktop"
# NOTE: If the program becomes a module, maybe do what sunflower does
# and prepend a line such as:
# #!/usr/bin/env python3 -m world_clock
# and change Exec to world_clock %U
cat > "$sc_path" <<END
[Desktop Entry]
Name=World Clock
Exec=$THIS_PYTHON $dst_path/$main_script
Path=$dst_path
Icon=$dst_path/clock_mini_icon.png
Terminal=false
Type=Application
END
printf "* chmod +x \"$sc_path\"..."
chmod +x "$sc_path"
if [ $? -eq 0 ]; then
    echo "OK"
else
    echo "FAILED"
fi
if [ -f "`command -v xdg-desktop-icon`" ]; then
    printf "* installing desktop icon..."
    xdg-desktop-icon install --novendor "$sc_path"
    if [ $? -eq 0 ]; then
        echo "OK"
    else
        echo "FAILED"
    fi
else
    echo "* The icon is in $sc_path."
    echo "  * The xdg-desktop-icon command was not present so the icon install was skipped: xdg-desktop-icon install --novendor \"$sc_path\""
fi
$THIS_PYTHON -m pip install --user ttkthemes
if [ $? -ne 0 ]; then
    echo "Error: '$THIS_PYTHON -m pip install --user ttkthemes' Failed. You will have to install ttkthemes."
else
    echo "* Setup is complete."
fi
echo
