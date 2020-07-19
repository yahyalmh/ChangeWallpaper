# ChangeWallpaper
Download and change wallpaper automatically
## Table of content
* [General info](#General-info)

* [Installation](#Installation)

* [Technologies](#Technologies)

* [Features](#Features)

* [Setup](#setup)

* [To Do](#To-Do)


## General info

This scrip download bing and nasa daily wallpaper. save downloaded image in directory with  "wallpaper" name, it creates in home directory.
those site addresses are:
* https://www.bing.com
* https://apod.nasa.gov/apod/astropix.html

 Download those wallpaper once a day and set on of them as wallpaper randomly.
 also if you set a crontab job for this script can change wallpaper periodically without download those wallpaper again in same day.
## Installation
install process create file name `.changeWall` in you home and copy project file to that path and run it.
* ##### linux
Go to installation directory and run `install.sh` from command line.  
* ##### windows
Go to installation directory and run `install.bat` from cmd.
## Technologies

project is created with:
* python version: 3.6
* bash version: 4.4
* BeautifulSoup version: 4.8
* urllib3 version:1.25
* requests version:2.23
* python-crontab version:2.5.1 for schedule task on linux
* Use schtasks for schedule task on windows

## Features

* Test on linux ubuntu 18.4 with Gnome 3.28 and windows 10
* download wallpaper once a day
* Change wallpaper periodically(hourly and reboot) with crontab setup for linux and schtasks for windows
* If the total downloaded images size is more than 2G(you can change this limit in`Utils/SpaceManager.py` file), remove the oldest image files from the application directory daily
* If there is not image in project's download directory use system default wallpaper in `/usr/share/backgrounds` directory on linux.
also if there is not any wallpaper in this path use a default image there is in project `./image/def_wall.png` path

 ## Setup
 schedule change wallpaper hourly and at the time of os reboot it's done automatically. but if you want to change it use below way. 
* ##### linux
 If you want to change your wallpaper periodically for example change every two hours, set crontab job for this script like this:
 
 `0 */2  * * * /usr/bin/python3  /your_home_path/.chagneWall/Main.py`
* ##### windows
 if you want to download wallpaper and change your wallpaper daily run follow command:
 
 `"schtasks /create /sc daily  /tr " +   /your_home_path/.chagneWall/run.vbs`
 
## To Do
* add some another wallpaper site 
