# ChangeWallpaper

## Table of content
* [General info](#General-info)

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
  
## Technologies

project is created with:
* python version: 3.6
* bash version: 4.4
* BeautifulSoup version: 4.8
* urllib3 version:1.25
* requests version:2.23

## Features

* Test on linux ubuntu 18.4 with Gnome 3.28
* download wallpaper once a day
* Change wallpaper periodically with crontab setup
* If the total downloaded images size is more than 2G(you can change this limit in`Utils/SpaceManager.py` file), remove the oldest image files from the application directory daily
* If there is not image in project's download directory use system default wallpaper in `/usr/share/backgrounds` directory 
also if there is not any wallpaper in this path use a default image there is in project `./image/def_wall.png` path

 ## Setup
 
 If you want to change your wallpaper periodically for example hourly, set crontab job for this script like this:
 
 `0 */1  * * * /usr/bin/python3  /your_local_path/ChangeWallpaper/Main.py`
 
 Also if you want to download wallpaper and change your wallpaper at boot time add this to crontab:
 
 `@reboot sleep 40 &&   /usr/bin/python3   /your_local_path/ChangeWallpaper/Main.py`
 
## To Do

* This project for linux os, change it to work on windows os
* add some another wallpaper site 
