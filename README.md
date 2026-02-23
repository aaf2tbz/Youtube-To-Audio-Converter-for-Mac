# YouTube Converter For All Platforms

A simple, native application to download and convert YouTube videos to various audio and video formats.

## Features

- **Multi-format conversion**: MP3, M4A, WAV, MP4
- **Quality options**:
  - Audio: 128, 192, 256, 320 kbps (MP3/M4A)
  - Lossless: 16-bit, 24-bit (WAV)
  - Video: 360p, 480p, 720p, 1080p, 1440p, 4K (MP4)
- **Automatic dependency installation** - yt-dlp, ffmpeg, customtkinter
- **In-app updates** - Check for app updates and dependency updates
- **Native dark theme UI** - Clean, modern interface
- **Cross-platform** - Windows, macOS, Linux
- **No ads, no tracking**

## Installation

### Windows

1. Download `YouTubeConverter.exe` from the [releases](releases/) folder
2. Run the executable
3. The app will automatically install required dependencies on first run

### macOS

#### Option 1: Download DMG (Recommended)

1. Download `YouTubeConverter.dmg` from the [releases](releases/) folder
2. Open the DMG file
3. Drag "YouTube Converter" to the Applications folder
4. Launch from Applications
5. **If you see a security warning**, see [Bypassing Security Checks](#bypassing-security-checks-macos) below

#### Option 2: Run .app Bundle

1. Download `YouTube Converter.app` from the [releases](releases/) folder
2. Move to Applications folder
3. Launch the app
4. **If you see a security warning**, see [Bypassing Security Checks](#bypassing-security-checks-macos) below

### Linux

#### Option 1: Build from Source

```bash
# Clone the repository
git clone https://github.com/aaf2tbz/Youtube-Converter-Application.git
cd Youtube-Converter-Application

# Make build script executable
chmod +x build_linux.sh

# Run the build script
./build_linux.sh

# Run the app
./dist/YouTubeConverter
```

#### Option 2: Manual Install

```bash
# Install system dependencies
sudo apt update
sudo apt install -y python3 python3-pip ffmpeg yt-dlp

# Install Python dependencies
pip3 install -r requirements.txt

# Run the app
python3 src/youtube_to_wav.py
```

## Usage

1. **Enter YouTube URL** - Paste any YouTube video link
2. **Enter Filename** - Choose a name for your output file
3. **Select Format** - Choose from MP3, M4A, WAV, or MP4
4. **Select Quality** - Pick your preferred quality level
5. **Click Download & Convert** - Choose where to save the file
6. **Check for Updates** - Use the built-in update checker to get the latest version
7. **Update Dependencies** - Keep yt-dlp, ffmpeg, and customtkinter up to date

## Bypassing Security Checks (macOS)

If macOS shows a security warning when opening the app ("Apple couldn't verify this app is free of malware"):

**Method 1: Right-click to open**
1. Right-click on the app in Applications
2. Select "Open"
3. Click "Open" in the dialog box

**Method 2: Allow in System Settings**
1. Try to open the app - you'll see a warning dialog
2. Go to **System Settings** > **Privacy & Security**
3. Scroll down to the "Security" section
4. Click "Open Anyway" next to the warning about the app

This is a one-time step. After bypassing, the app will launch normally.

## Building from Source

### Prerequisites

- Python 3.8+
- Homebrew (macOS) or equivalent package manager

### Build Steps

```bash
# Clone the repository
git clone https://github.com/aaf2tbz/Youtube-Converter-Application.git
cd Youtube-Converter-Application

# Install dependencies
pip3 install customtkinter pyinstaller

# Build for current platform
pyinstaller --onefile --name "YouTubeConverter" --console src/youtube_to_wav.py

# Output will be in dist/ folder
```

### Building for Other Platforms

- **Windows**: Use Wine + PyInstaller (see build scripts in repo)
- **macOS**: Use PyInstaller on macOS
- **Linux**: Use PyInstaller on Linux

## Dependencies

The app requires:
- **yt-dlp** - For downloading YouTube content
- **ffmpeg** - For audio/video conversion
- **customtkinter** - For the GUI

These are automatically installed when you click "Install Dependencies" or "Update Dependencies" in the app.

## Project Structure

```
Youtube-Converter-Application/
├── src/
│   └── youtube_to_wav.py      # Main application source
├── releases/
│   ├── YouTubeConverter.exe  # Windows executable
│   └── YouTubeConverter.dmg # macOS installer
├── build_linux.sh            # Linux build script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Troubleshooting

### "Python not found" error
- Install Python from python.org or via Homebrew: `brew install python3`

### "yt-dlp not found" error
- Click "Install Dependencies" in the app, or manually install:
  - macOS: `brew install yt-dlp ffmpeg`
  - Linux: `sudo apt install yt-dlp ffmpeg`

### App won't open (macOS)
- See [Bypassing Security Checks](#bypassing-security-checks-macos) above

### Download fails
- Make sure yt-dlp is installed and up to date
- Try clicking "Update Dependencies" to get the latest version

## Technical Details

- Built with Python 3 and customtkinter
- Uses yt-dlp for downloading
- Uses ffmpeg for conversion
- Packaged as native executables for each platform

## License

This project is for personal and educational use only. Please respect YouTube's Terms of Service and copyright laws when using this software.

## Disclaimer

This software is provided as-is. Users are responsible for ensuring they have the right to download and convert any content. The developers are not responsible for any misuse of this software.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

Made with care.
