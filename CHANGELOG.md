# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-08-25

### Added
- Initial release of Torrent Auto Shutdown
- Desktop GUI application with Tkinter
- qBittorrent process monitoring
- Network activity detection
- File modification monitoring in download directories
- Configurable check intervals and shutdown delays
- Countdown timer with cancel option
- Test mode for safe verification
- Settings persistence (JSON)
- Portable executable build with PyInstaller
- Comprehensive error handling and safety features

### Features
- **Smart Detection**: Multiple methods to detect download completion
- **User-Friendly GUI**: Simple and intuitive interface
- **Safety First**: Test mode and cancellation options
- **Configurable**: Adjustable timing and monitoring settings
- **Portable**: Single executable file, no installation required

### Technical Details
- Built with Python 3.13
- Uses psutil for process monitoring
- Tkinter for cross-platform GUI
- PyInstaller for executable packaging
- JSON for settings storage
