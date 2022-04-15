#!/bin/bash
myPath="`realpath "$0"`"
echo "$myPath"
basePath="`dirname "$myPath"`"
echo "basePath: $basePath"
programs_path="$HOME/.local/lib"
this_module="worldclocktk"
this_package="world_clock"
dst_path="$programs_path/world_clock"
mkdir -p "$programs_path"
main_script="world_clock.py"
good_flag_file="worldclocktk/__init__.py"
shortcuts_dir="$HOME/.local/share/applications"

THIS_PYTHON_NAME=python3
THIS_PYTHON="`command -v python3`"
if [ ! -f "$THIS_PYTHON" ]; then
    echo "Warning: The program requires python3."
    if [ -f "`command -v python`" ]; then
        THIS_PYTHON_NAME=python
        THIS_PYTHON="`command -v $THIS_PYTHON_NAME`"
        echo "* The Python binary for the icon was set to \"$THIS_PYTHON\"."
    fi
else
    THIS_PYTHON="`command -v $THIS_PYTHON_NAME`"
fi
THIS_PYTHON_NAME="`basename $THIS_PYTHON`"


if [ ! -f "$good_flag_file" ]; then
    echo "Error: This script must run from the directory containing $good_flag_file."
    exit 1
fi
REPO_DIR="`pwd`"

cat <<END
Warning: This script is only for cleaning up files from setup.sh
(including ones from old versions of setup.sh)
END


cd /tmp
if [ $? -ne 0 ]; then exit 1; fi
if [ -d "$this_module" ]; then
    rm -Rf "$this_module"
fi
# ^ Change the directory & delete any present so the check below works.

$THIS_PYTHON -c "import $this_module" >& /dev/null
if [ $? -ne 0 ]; then
    cat <<END

The $this_module module is already uninstalled.
END
else
    cat <<END
The $this_package package is installed. You must first run something like:
  $THIS_PYTHON_NAME -m pip uninstall $this_package

END
    exit 1
fi
readlink $dst_path
if [ $? -eq 0 ]; then
    rm $dst_path
    if [ $? -ne 0 ]; then
        echo "Error: refusing to uninstall since $dst_path seems to be a symlink but it can't be removed!"
        exit 1
    else
        echo "Warning: removed symlink \"$dst_path\""
    fi
    exit 1
fi

if [ -d "$dst_path/__pycache__" ]; then
    echo "* attempting to remove *.pyc from $dst_path/__pycache__"
    rm $dst_path/__pycache__/*.pyc
    code=$?
    if [ $code -ne 0 ]; then
        echo "  FAILED (code $code)"
    else
        echo "  OK"
    fi
    echo "* attempting to remove *.pyc from $dst_path/__pycache__"
    rmdir --ignore-fail-on-non-empty "$dst_path/__pycache__"
    if [ $code -ne 0 ]; then
        echo "  FAILED (code $code)"
    else
        echo "  OK"
    fi
fi

cd "$REPO_DIR"
echo "dst_path: $dst_path"
for dstName in clock_mini_icon.ico clock_mini_icon.png clock_scr.png environment.yml license.txt __pycache__ readme.md setup.sh ttk_extensions.py ttk_extensions.pyc world_clock.py
do
    dstFilePath="$dst_path/$dstName"
    if [ -f "$dstFilePath" ]; then
        echo "rm \"$dstFilePath\""
        rm "$dstFilePath"
    fi
done

if [ -d "$dst_path" ]; then
    rmdir --ignore-fail-on-non-empty "$dst_path"
fi
dstFilePath="$dst_path/world_clock.yaml"

if [ -d "$dst_path" ]; then
    echo "WARNING: You must remove your files manualy if desired:"
else
    echo "* removed $dst_path"
    exit 0
fi

if [ -f $dst_path/.gitignore ]; then
    cat <<END
# rm "$dst_path/.gitignore"  # may dangerous if unsure why present (This only makes sense if you installed it manually or used the old setup.sh from before setup.py)!
END
fi

if [ -d $dst_path/.git ]; then
    cat <<END
# rm -rf "$dst_path/.git"  # may dangerous if unsure why present (This only makes sense if you installed it manually or used the old setup.sh from before setup.py)!
END
fi

if [ -f "$dstFilePath" ]; then
    cat <<END
rm "$dstFilePath"
END
fi

cat <<END
rmdir "$dst_path"
END

