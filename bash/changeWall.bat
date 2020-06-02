@echo off
setlocal enabledelayedexpansion

set "wait_time=!time:~0.2!"
set image_address=%1

reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v WallpaperStyle /t REG_SZ /d 10 /f
reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v TileWallpaper /t REG_SZ /d 0 /f
rem WallpaperStyle = 10 and TileWallpaper = 0 make walpaper filled
rem WallpaperStyle = 6 and TileWallpaper = 0 make walpaper fited
rem WallpaperStyle = 2 and TileWallpaper = 0 make walpaper stretched
rem WallpaperStyle = 0 and TileWallpaper = 0 make walpaper centered
rem WallpaperStyle = 0 and TileWallpaper = 1 make walpaper tiled


if "!wait_time!" leq "20" reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d %image_address% /f & goto done
if "!wait_time!" geq "20" reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d %image_address% /f & goto done

:done

timeout /t 2 >nul
start "" /b RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters ,1 ,True
start "" /b RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters ,1 ,True
start "" /b RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters ,1 ,True
start "" /b RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters ,1 ,True
start "" /b RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters ,1 ,True

endlocal