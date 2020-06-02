#!/usr/bin/env bash

is_installed=$(type -P python3  >/dev/null 2>&1 && echo 1 )

if [ "$is_installed" = 1 ]; then
    echo "you have install python3"
    private_dir_name=".changeWall"
    private_dir_path="$HOME/${private_dir_name}"
    mkdir -p "${private_dir_path}"
    rsync -a ./* "$private_dir_path" --exclude install.sh
else echo "you have not installed python3 and above"
fi