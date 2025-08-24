@echo off
echo Building Torrent Auto Shutdown executable...
echo.

REM Activate virtual environment and build executable
D:\Development\AutoShut\.venv\Scripts\pyinstaller.exe ^
    --onefile ^
    --windowed ^
    --name "TorrentAutoShutdown" ^
    torrent_shutdown.py

echo.
echo Build complete! Executable created in 'dist' folder.
echo.
pause
