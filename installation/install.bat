@echo off
setlocal enabledelayedexpansion

set private_dir_name=.changeWall
set private_dir_path=%userprofile%\%private_dir_name%
set run_path=%private_dir_path%\run.vbs

for /f "delims=" %%i in ('where python3') do set python3_path=%%i
if not %python3_path%=="" (
	echo "You have installed python3 in %python3_path%"

	echo "Info: Creating app directory in path: %private_dir_path%"

	mkdir %private_dir_path%

	echo "Info: Coping files..."
	xcopy /r /d /i /s /y /exclude:excludelist.txt ..\* %private_dir_path%

	echo "Run path is:  %run_path%"
    echo "Info: Run app..."
    cmd /c %run_path%

    echo "Info: Create schtasks job to change wallpaper hourly(see \"schtasks /query /fo list\" command)"
    echo "Info: See \"schtasks /query /fo list\" command"
    echo "Info: Downloading Bing and Nasa wallpaper if the internet was reachable"
    echo "Info: Finished"

	) else (
	echo "Error: you have not installed python3. This app works only with python3."
	)