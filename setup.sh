#!/bin/bash
echo
myPath="`realpath "$0"`"
echo "$myPath"
basePath="`dirname "$myPath"`"
echo "basePath: $basePath"
programs_path="$HOME/.local/lib"
this_module="worldclocktk"
this_package="world_clock"
dst_path="$programs_path/world_clock"
mkdir -p "$dst_path"
if [ $? -ne 0 ]; then exit 1; fi
icon_name="clock_mini_icon.png"
src_icon_path="worldclocktk/assets/$icon_name"
dst_icon_path="$dst_path/$icon_name"
# good_flag_file="worldclocktk/__init__.py"
good_flag_file="$src_icon_path"
shortcuts_dir="$HOME/.local/share/applications"
if [ ! -f "$good_flag_file" ]; then
    echo "Error: This script must run from the directory containing $good_flag_file."
    exit 1
fi
REPO_DIR="`pwd`"
# ^ Only set REPO_DIR if good (confirmed above, else exits).
main_script_path="`command -v world_clock`"
if [ ! -f "$main_script_path" ]; then
    cat <<END

Error: The world_clock command is not installed yet.
You must first run:
  python3 -m pip install $REPO_DIR
  # ^ installs the $this_package package which provides the $this_module module.

END
    exit 1
fi
cd /tmp
if [ $? -ne 0 ]; then exit 1; fi
if [ -d "$this_module" ]; then
    rm -Rf "$this_module"
fi
# ^ Change the directory & delete any present so the check below works.

THIS_PYTHON_NAME=python3
THIS_PYTHON="`command -v python3`"
if [ ! -f "$THIS_PYTHON" ]; then
    echo "Warning: this program requires python3."
    if [ -f "`command -v python`" ]; then
        THIS_PYTHON_NAME=python
        THIS_PYTHON="`command -v $THIS_PYTHON_NAME`"
        echo "* The Python binary for the icon was set to \"$THIS_PYTHON\"."
    fi
else
    THIS_PYTHON="`command -v $THIS_PYTHON_NAME`"
fi
THIS_PYTHON_NAME="`basename $THIS_PYTHON`"

$THIS_PYTHON -c "import $this_module" >& /dev/null
if [ $? -ne 0 ]; then
    cat <<END

Error: The $this_package package is not installed yet.
You must first run something like:
  $THIS_PYTHON -m pip install $REPO_DIR

END
    exit 1
fi
cd "$REPO_DIR"
if [ $? -ne 0 ]; then exit 1; fi
# printf "* chmod +x \"$dst_path/$main_script\"..."
# chmod +x "$dst_path/$main_script"
#if [ $? -eq 0 ]; then
#    echo "OK"
#else
#    echo "FAILED"
#fi
printf "* installing $dst_icon_path..."
cp -f "$src_icon_path" "$dst_icon_path"
if [ $? -ne 0 ]; then exit 1; fi
echo "OK"

cat > /dev/null <<END
for srcName in license.txt readme.md
do
    this_dst_file_path="$dst_path/$srcName"
    printf "* installing $this_dst_file_path..."
    if [ ! -f "$srcName" ]; then
        echo "Error: $srcName is missing from `pwd`"
        exit 1
    fi
    cp -f "$srcName" "$this_dst_file_path"
    if [ $? -ne 0 ]; then exit 1; fi
    echo "OK"
done
END

echo "* generating shortcut..."

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
Exec=$main_script_path
Path=$dst_path
Icon=$dst_icon_path
Terminal=false
Type=Application
END
# ^ formerly Exec=$THIS_PYTHON $main_script_path
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
echo
