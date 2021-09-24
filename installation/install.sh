#!/usr/bin/env bash

is_installed=$(type -P python3  >/dev/null 2>&1 && echo 1 )

if [ "$is_installed" = 1 ]; then
    echo "Info: You have installed python3"
    private_dir_name=".changeWall"
    private_dir_path="$HOME/${private_dir_name}"
    echo "Info: creating app directory in path:'$private_dir_path'"
    mkdir -p "${private_dir_path}"

    echo "Info: Coping files..."
    rsync -a ../* "$private_dir_path" --exclude install.sh

    python3_path=$(type -P python3)
    main_path="$HOME/${private_dir_name}/Main.py"
    echo "Info: Run app..."
    $python3_path "$main_path"
    echo "Info: Create crontab job to change wallpaper hourly and when reboot"
    echo "Info: See crontab file by \"crontab -l\" command"
    echo "Info: Downloading Bing and Nasa wallpaper if the internet was reachable"
    echo "Info: Finished"

else echo "Error: you have not installed python3. This app works only with python3."
fi