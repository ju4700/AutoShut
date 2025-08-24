@echo off
echo Starting Torrent Auto Shutdown...
echo.
echo IMPORTANT: Make sure qBittorrent is running and downloading torrents!
echo.
echo Instructions:
echo 1. Select your download folder
echo 2. Configure check intervals if needed
echo 3. Click "Start Monitoring"
echo 4. The app will automatically shutdown your PC when downloads complete
echo.
pause
echo.
cd /d "%~dp0"
.\dist\TorrentAutoShutdown.exe
