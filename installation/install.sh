#!/usr/bin/env bash

is_installed=$(type -P python3  >/dev/null 2>&1 && echo 1 )

if [ "$is_installed" = 1 ]; then
    echo "Info: you have install python3"
    private_dir_name=".changeWall"
    private_dir_path="$HOME/${private_dir_name}"
    echo "Info: create app directory in path:'$private_dir_path'"
    mkdir -p "${private_dir_path}"

    echo "Info: coping files..."
    rsync -a ../* "$private_dir_path" --exclude install.sh

    python3_path=$(type -P python3)
    main_path="$HOME/${private_dir_name}/Main.py"
    echo "Info: run app..."
    $python3_path "$main_path"
    echo "Info: create crontab job to change wallpaper hourly(see crontab file)"
    echo "Info: download Bing and Nasa wallpaper if net connection was ok"
    echo "Info: Finished"

else echo "Error: you have not installed python3. This app work with python3 only."
fi