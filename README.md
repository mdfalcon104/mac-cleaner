# Mac Cleaner 🧹

A simple macOS application to clean temporary and unused files from your Mac.

## Features

- 🗑️ **Empty Trash** - Clear all files from your Trash
- 🗄️ **Clean User Caches** - Remove cached files from `~/Library/Caches/`
- 📝 **Clean User Logs** - Remove old log files from `~/Library/Logs/`
- ⏰ **Clean Old Temp Files** - Remove temporary files older than 7 days from `/tmp/`
- 📊 **Space Report** - See how much space you've freed

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/mdfalcon104/mac-cleaner.git
   cd mac-cleaner
   ```

2. **(Optional)** Convert the icon to `.icns` format (macOS only):
   ```bash
   mkdir AppIcon.iconset
   sips -z 16 16     "Mac Cleaner.app/Contents/Resources/AppIcon.png" --out AppIcon.iconset/icon_16x16.png
   sips -z 32 32     "Mac Cleaner.app/Contents/Resources/AppIcon.png" --out AppIcon.iconset/icon_16x16@2x.png
   sips -z 32 32     "Mac Cleaner.app/Contents/Resources/AppIcon.png" --out AppIcon.iconset/icon_32x32.png
   sips -z 64 64     "Mac Cleaner.app/Contents/Resources/AppIcon.png" --out AppIcon.iconset/icon_32x32@2x.png
   sips -z 128 128   "Mac Cleaner.app/Contents/Resources/AppIcon.png" --out AppIcon.iconset/icon_128x128.png
   sips -z 256 256   "Mac Cleaner.app/Contents/Resources/AppIcon.png" --out AppIcon.iconset/icon_128x128@2x.png
   sips -z 256 256   "Mac Cleaner.app/Contents/Resources/AppIcon.png" --out AppIcon.iconset/icon_256x256.png
   sips -z 512 512   "Mac Cleaner.app/Contents/Resources/AppIcon.png" --out AppIcon.iconset/icon_256x256@2x.png
   sips -z 512 512   "Mac Cleaner.app/Contents/Resources/AppIcon.png" --out AppIcon.iconset/icon_512x512.png
   sips -z 1024 1024 "Mac Cleaner.app/Contents/Resources/AppIcon.png" --out AppIcon.iconset/icon_512x512@2x.png
   iconutil -c icns AppIcon.iconset
   mv AppIcon.icns "Mac Cleaner.app/Contents/Resources/"
   rm -rf AppIcon.iconset
   ```

3. Copy the app to your Applications folder (optional):
   ```bash
   cp -r "Mac Cleaner.app" /Applications/
   ```

## Usage

### Option 1: Double-click the App (Recommended)

1. Open Finder and navigate to the repository folder (or `/Applications/` if you copied it there)
2. Double-click on **Mac Cleaner.app**
3. The app will open a Terminal window and run the cleaning script
4. Review the output to see what was cleaned and how much space was freed
5. Press Enter to close the Terminal window

### Option 2: Run the Python Script Directly

```bash
python3 clean_mac.py
```

## What Gets Cleaned

| Location | Description | Safety |
|----------|-------------|--------|
| `~/.Trash` | User trash/bin | ✅ Safe - empties trash |
| `~/Library/Caches/` | Application caches | ✅ Safe - apps will regenerate |
| `~/Library/Logs/` | User log files | ✅ Safe - old logs |
| `/tmp/` | Temporary files (>7 days old) | ✅ Safe - only old files |

## Safety

- ✅ Only cleans user-accessible directories (no system files)
- ✅ Only removes temporary and cache files that can be regenerated
- ✅ For `/tmp/`, only removes files older than 7 days
- ✅ Skips files/directories it doesn't have permission to delete
- ✅ Reports errors without stopping the entire process

## Requirements

- macOS 10.13 or later
- Python 3.x (usually pre-installed on macOS)

## Troubleshooting

### App won't open

If you see a security warning when trying to open the app:
1. Right-click (or Ctrl+click) on "Mac Cleaner.app"
2. Select "Open" from the menu
3. Click "Open" in the security dialog

Alternatively, you can run:
```bash
xattr -cr "Mac Cleaner.app"
```

### Permission errors

Some cache directories may require elevated permissions. The script will skip these and continue cleaning what it can access.

## Development

### Project Structure

```
mac-cleaner/
├── clean_mac.py                    # Main Python cleaning script
├── generate_icon.py                # Icon generator script
├── Mac Cleaner.app/               # macOS application bundle
│   └── Contents/
│       ├── Info.plist             # App metadata
│       ├── MacOS/
│       │   └── mac_cleaner_launcher  # Launch script
│       └── Resources/
│           └── AppIcon.png        # App icon (convert to .icns)
└── README.md                      # This file
```

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.