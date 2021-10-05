# ChangeWallpaper
Download The Bing and Nasa daily wallpapers and change Linux and Windows Wallpaper automatically

## Table of content

* [General info](#General-info)

* [Installation](#Installation)

* [Technologies](#Technologies)

* [Features](#Features)

* [Setup](#setup)

* [Issues](#Issues)

* [To Do](#To-Do)


## General info

This script downloads the Bing and Nasa daily wallpaper and saves the downloaded images in a directory with the `wallpaper` name created in the home directory.

Those site addresses are:
* https://www.bing.com
* https://apod.nasa.gov/apod/astropix.html

 Download those wallpaper once a day and set one of them as wallpaper randomly. This script will change the wallpaper once an hour by default, but you can change it.
 
## Installation

To install it, clone the repository in a path and run the install script based on your os type. Install process creates a file named `.changeWall` in your home directory and uses it as the project folder. 

* ##### linux
    Go to the installation directory and run `./install.sh` from the terminal. 
    
    - Make sure the install script has execution permission. By default it has that permission, but you can give that permission by `sudo chmod +x install.sh` if it does not have.

* ##### windows
    Go to the installation directory and run `install.bat` from cmd.

## Technologies

project is built with:
* python version: 3.6
* bash version: 4.4
* BeautifulSoup version: 4.8
* urllib3 version:1.25
* requests version:2.23
* python-crontab version:2.5.1 for schedule task on linux
* Use schtasks for schedule task on windows

## Features

* Tested on Ubuntu 20 LTS and Windows 10
* Tested on Linux ubuntu 18.4 with Gnome 3.28
* Check and remove duplicate images with the hash algorithm(use hash table)
* Use vbs file to run python file on Windows
* Download wallpaper once a day
* Change wallpaper periodically(hourly and reboot) with `crontab` setup for Linux and `schtasks` for windows
* If the total downloaded images' size is more than 2GB(you can change this limit in the `Utils/SpaceManager.py` file), it will remove the oldest image files from the application directory, which is named `wallpaper directory in your home directory
* If there is no image in the project's download directory, use system default's wallpaper in `/usr/share/backgrounds` directory on the Linux. Also, if there is no image in this path, use a default image which is in project `./image/def_wall.png` path

 ## Setup
 
 Schedule change wallpaper hourly, and at the time of os reboot, it's done automatically. But if you want to change it, use the below commands. 

   * ##### linux
      If you want to change your wallpaper periodically, for example change it every two hours, set crontab job for this script like this:

       `0 */2  * * * /usr/bin/python3  /your_home_path/.chagneWall/Main.py`

   * ##### windows
      Can not change wallpaper at reboot time because you need administrator privilege.
       if you want to change your wallpaper daily run follow command:

      `schtasks /create /sc daily  /tr " +   /your_home_path/.chagneWall/run.vbs`

 ## Issues

If you install the script without any errors, but your background is not changed, open an issue and tell your os and GUI version to fix it. because the background in desktop environments is sometimes different.  
## To Do
* Add some another wallpaper site 
* Use Apod API to download Nasa daily images
* Add The Uninstall script
* Remove previously cron job with the sabe comment
* Decrease the wallpaper folder default size
