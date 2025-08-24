# 🛑 Torrent Auto Shutdown

A simple desktop application that monitors your torrent downloads and automatically shuts down your PC when the download is complete.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🚀 Features

- 🔍 **Smart Monitoring**: Monitors qBittorrent torrent client activity
- 🔄 **Multiple Detection Methods**: 
  - Process network activity
  - CPU usage monitoring
  - File modification detection in download folder
- ⚙️ **Configurable Settings**: Adjustable check intervals and shutdown delays
- ⏱️ **Countdown Timer**: Shutdown countdown with cancel option
- 💾 **Settings Persistence**: Automatically saves your preferences
- 🧪 **Test Mode**: Verify functionality without actually shutting down
- 🖥️ **GUI Interface**: User-friendly desktop application

## 📸 Screenshots

![Application Interface](https://via.placeholder.com/500x400/2196F3/ffffff?text=Torrent+Auto+Shutdown+GUI)

## 🛠️ Installation

### Option 1: Download Executable (Recommended)
1. Download the latest `TorrentAutoShutdown.exe` from [Releases](../../releases)
2. Run the executable - no installation required!

### Option 2: Build from Source
```bash
# Clone the repository
git clone https://github.com/yourusername/torrent-auto-shutdown.git
cd torrent-auto-shutdown

# Install dependencies
pip install -r requirements.txt

# Run the application
python torrent_shutdown.py

# Or build executable
.\build_exe.bat
```

## 📋 Requirements

- **Operating System**: Windows 10/11
- **Torrent Client**: qBittorrent (running)
- **Python**: 3.7+ (if running from source)

## 🎯 How to Use

1. **Launch the application**: Double-click `TorrentAutoShutdown.exe` or `run_app.bat`

2. **Select Download Folder**: Click "Browse" and select the folder where your torrents are being downloaded

3. **Configure Settings** (optional):
   - **Check Interval**: How often to check for activity (default: 30 seconds)
   - **Shutdown Delay**: How long to wait before shutdown after detecting completion (default: 60 seconds)

4. **Start Monitoring**: Click "Start Monitoring" button

5. **The app will automatically**:
   - Monitor qBittorrent process and network activity
   - Check for file modifications in your download folder
   - Show current status and activity
   - Initiate shutdown when no activity is detected for 2+ minutes across 3 consecutive checks

6. **Shutdown Process**:
   - A countdown window will appear
   - You can cancel the shutdown if needed
   - The PC will shutdown automatically when countdown reaches zero

## ⚠️ Safety Features

- **Test Mode**: Use "Test Shutdown" button to verify the countdown works without actually shutting down
- **Cancel Option**: You can always cancel the shutdown during the countdown
- **Multiple Checks**: Requires sustained inactivity before triggering shutdown
- **Minimum Time**: Waits at least 2 minutes of inactivity before considering download complete

## 🔧 Configuration

The application saves settings in `settings.json`:

```json
{
    "download_path": "C:\\Downloads\\Torrents",
    "check_interval": 30,
    "shutdown_delay": 60
}
```

## 🏗️ Building from Source

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Build Steps
```bash
# Install dependencies
pip install -r requirements.txt

# Build executable
pyinstaller --onefile --windowed --name "TorrentAutoShutdown" torrent_shutdown.py
```

Or use the provided batch file:
```cmd
.\build_exe.bat
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| App doesn't detect download completion | Ensure download folder path is correct and qBittorrent is running |
| Shutdown doesn't work | Run the application as administrator |
| False positives | Increase check interval or shutdown delay in settings |
| qBittorrent not detected | Make sure qBittorrent is running and actively downloading |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**Warning**: This application will actually shut down your computer! Always test with the "Test Shutdown" feature first to ensure it works as expected.

## 📧 Support

If you encounter any issues or have questions:
- Open an [Issue](../../issues)
- Check the [Wiki](../../wiki) for additional documentation

## 🌟 Acknowledgments

- Built with Python and Tkinter
- Uses [psutil](https://github.com/giampaolo/psutil) for process monitoring
- Packaged with [PyInstaller](https://www.pyinstaller.org/)

---

⭐ **Star this repository if you find it helpful!**
