@echo off
setlocal enabledelayedexpansion

set private_dir_name=.changeWall
set private_dir_path=%userprofile%\%private_dir_name%
set main_path=%private_dir_path%\Main.py

for /f "delims=" %%i in ('where python3') do set python3_path=%%i
if not %python3_path%=="" (
	echo "you have installed python3 in %python3_path%"

	echo "Info: create app directory in path: %private_dir_path%"

	mkdir %private_dir_path%

	echo "Info: coping files..."
	xcopy /r /d /i /s /y /exclude:excludelist.txt .\* %private_dir_path%

	echo "amin %main_path%"
    echo "Info: run app..."
    cmd /c %python3_path% %main_path%

    echo "Info: create crontab job to change wallpaper hourly(see crontab file)"
    echo "Info: download Bing and Nasa wallpaper"
    echo "Info: Finished"

	) else (
	echo "Error: you have not installed python3. This app work with python3 only."
	)