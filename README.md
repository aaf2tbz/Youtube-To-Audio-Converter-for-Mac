# YouTube Converter for Mac

A simple, native macOS application to download and convert YouTube videos to various audio and video formats.

## Features

- Convert to multiple formats: **MP3**, **M4A**, **WAV**, **MP4**
- Quality selection for each format:
  - MP3/M4A: 128, 192, 256, 320 kbps
  - WAV: Lossless (16-bit, 24-bit)
  - MP4: 360p, 480p, 720p, 1080p, 1440p, 4K
- Automatic dependency installation
- Native macOS look and feel
- No ads, no tracking

## Requirements

- macOS 10.13 (High Sierra) or later
- Python 3 (auto-detected)
- [Homebrew](https://brew.sh) (recommended for dependency installation)

## Installation

### Option 1: Download DMG (Recommended)

1. Download `YouTubeConverter.dmg` from the [releases](releases/) folder
2. Open the DMG file
3. Drag "YouTube Converter" to the Applications folder
4. Launch from Applications

### Option 2: Build from Source

```bash
# Clone the repository
git clone https://github.com/aaf2tbz/Youtube-To-Audio-Converter-for-Mac.git
cd Youtube-To-Audio-Converter-for-Mac

# Install dependencies
brew install python3 yt-dlp ffmpeg

# Run the app
python3 "YouTube Converter.app/Contents/Resources/youtube_to_wav.py"
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

These are automatically installed via Homebrew when you click "Install Dependencies" in the app.

## Technical Details

- Built with Python 3 and Tkinter
- Uses `yt-dlp` for downloading
- Uses `ffmpeg` for conversion
- Packaged as a native macOS .app bundle

## License

This project is for personal and educational use only. Please respect YouTube's Terms of Service and copyright laws when using this software.

## Disclaimer

This software is provided as-is. Users are responsible for ensuring they have the right to download and convert any content. The developers are not responsible for any misuse of this software.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

Made with care for the macOS community.
