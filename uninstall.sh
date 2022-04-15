#!/bin/bash
myPath="`realpath "$0"`"
echo "$myPath"
basePath="`dirname "$myPath"`"
echo "basePath: $basePath"
programs_path="$HOME/.local/lib"
dst_path="$programs_path/world_clock"
mkdir -p "$programs_path"
main_script="world_clock.py"
good_flag_file="worldclocktk/__init__.py"
shortcuts_dir="$HOME/.local/share/applications"
if [ ! -f "$good_flag_file" ]; then
    echo "Error: This script must run from the directory containing $good_flag_file."
    exit 1
fi
echo "dst_path: $dst_path"
for dstName in clock_mini_icon.ico clock_mini_icon.png clock_scr.png environment.yml license.txt __pycache__ readme.md setup.sh ttk_extensions.py ttk_extensions.pyc world_clock.py world_clock.yaml
do
    dstFilePath="$dst_path/$dstName"
    if [ -f "$dstFilePath" ]; then
        echo "rm \"$dstFilePath\""
        rm "$dstFilePath"
    fi
done
