# YouTube Converter For all Platforms

A simple, native application to download and convert YouTube videos to various audio and video formats.

## Features

- Convert to multiple formats: **MP3**, **M4A**, **WAV**, **MP4**
- Quality selection for each format:
  - MP3/M4A: 128, 192, 256, 320 kbps
  - WAV: Lossless (16-bit, 24-bit)
  - MP4: 360p, 480p, 720p, 1080p, 1440p, 4K
- Automatic dependency installation
- Native dark theme UI
- No ads, no tracking

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

#### Option 2: Run .app Bundle

1. Download `YouTube Converter.app` from the [releases](releases/) folder
2. Move to Applications folder
3. Launch the app

### Linux

#### Option 1: Build from Source

```bash
# Clone the repository
git clone https://github.com/aaf2tbz/Youtube-To-Audio-Converter-for-Mac.git
cd Youtube-To-Audio-Converter-for-Mac

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

The app will automatically install `yt-dlp` and `ffmpeg` if they're missing.

## Dependencies

The app requires:
- **yt-dlp** - For downloading YouTube content
- **ffmpeg** - For audio/video conversion

These are automatically installed when you click "Install Dependencies" in the app.

## Technical Details

- Built with Python 3 and customtkinter
- Uses `yt-dlp` for downloading
- Uses `ffmpeg` for conversion
- Packaged as native executables for each platform

## License

This project is for personal and educational use only. Please respect YouTube's Terms of Service and copyright laws when using this software.

## Disclaimer

This software is provided as-is. Users are responsible for ensuring they have the right to download and convert any content. The developers are not responsible for any misuse of this software.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

Made with care.
