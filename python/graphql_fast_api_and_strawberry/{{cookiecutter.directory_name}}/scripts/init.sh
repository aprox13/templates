#!/usr/bin/env bash

set -e
set -u

die() {
  echo "$*" 1>&2
  exit 1
}

# usage
# [prog] WORKING_DIR PYTHON_VERSION VENV_DIR
init_venv() {
  local root=$1
  local py="python$2"
  local venv_folder="$3"
  local venv_python="$venv_folder/bin/$py"
  test -d "$root" || die "$root is not a directory or doesn't exists"
  local installed;
  installed=$("$venv_python" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null) || echo "" 1>/dev/null;
  if test -d "$root/venv" && test "$installed" = "$2"; then
    echo "venv is installed"
  else
    echo "Installing venv"


    echo "Detecting installed $py" && "$py" -V || die "$py is not installed"

    echo "Install and/or upgrade pip..." && "$py" -m pip install --upgrade pip
    echo "Install virtualenv..." && "$py" -m pip install virtualenv

    virtualenv --python "$py" --clear "$venv_folder"
  fi
}

"$@"
