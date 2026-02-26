# Media Cleaner

A simple Python script designed to strip all metadata (EXIF data) from your media files (images and videos). It uses `exiftool` to safely copy and clean your files without modifying the originals.

## Prerequisites

This script uses built-in Python standard libraries, so there are no Python dependencies to install via `pip`. 

However, you **must** have `exiftool` installed on your system.

### Installing ExifTool

**macOS:**
```bash
brew install exiftool
```

**Ubuntu / Debian:**
```bash
sudo apt-get install libimage-exiftool-perl
```

**Windows:**
Download the standalone executable from the [ExifTool website](https://exiftool.org/) and ensure it is available in your system's PATH.

## How to Use

1. Clone this repository or download the script.
2. Run the script for the first time to generate the input and output directories:
   ```bash
   python clean_media.py
   ```
   *This will create two folders: `mediain` and `mediaout`.*
3. Place the images or videos you want to clean into the `mediain` folder.
4. Run the script again:
   ```bash
   python clean_media.py
   ```
5. Your cleaned files will be saved in the `mediaout` folder, with all their metadata stripped. The original files in `mediain` will remain untouched.

## How it Works
The script works by first copying each file from `mediain` into `mediaout`. Then, it runs the `exiftool -all= -overwrite_original` command on the copied files to remove all metadata while ensuring no backup files are left behind.
