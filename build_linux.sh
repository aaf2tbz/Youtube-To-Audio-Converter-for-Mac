#!/bin/bash
# Build script for Linux - Run this on a Linux machine

echo "Installing dependencies..."
sudo apt update
sudo apt install -y python3 python3-pip ffmpeg yt-dlp

echo "Installing Python packages..."
pip3 install customtkinter pyinstaller

echo "Building executable..."
pyinstaller --onefile --name "YouTubeConverter" --console youtube_to_wav.py

echo "Done! Executable is in dist/YouTubeConverter"
