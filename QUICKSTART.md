# Quick Start Guide

## Installation

### Option 1: Automated Installation (Recommended)
```bash
git clone https://github.com/mdfalcon104/mac-cleaner.git
cd mac-cleaner
./install.sh
```

### Option 2: Manual Setup
```bash
git clone https://github.com/mdfalcon104/mac-cleaner.git
cd mac-cleaner
chmod +x clean_mac.py
chmod +x "Mac Cleaner.app/Contents/MacOS/mac_cleaner_launcher"
```

## Usage

### Method 1: Click the App Icon 🖱️
1. Navigate to the repository folder (or `/Applications/` if installed there)
2. Double-click **Mac Cleaner.app**
3. A Terminal window will open showing the cleaning progress
4. Press Enter when complete

### Method 2: Run from Terminal 💻
```bash
python3 clean_mac.py
```

## What Gets Cleaned

| Location | Description | Space Saved |
|----------|-------------|-------------|
| `~/.Trash` | Deleted files | Varies |
| `~/Library/Caches/` | App cache files | 100MB - 5GB+ |
| `~/Library/Logs/` | Application logs | 10MB - 500MB |
| `/tmp/` | Old temp files (>7 days) | 50MB - 2GB |
| **Leftover App Files** | Files from uninstalled apps | 50MB - 2GB+ |

## New Interactive Features

### 🧹 Leftover App Files Cleanup
The cleaner will automatically:
1. Scan for files from apps you've uninstalled
2. Show you what it found (name, location, size)
3. Ask if you want to remove them
4. Clean up the files if you confirm

### 📦 Application Manager
Optional app management:
1. After cleaning, you can choose to manage apps
2. View all installed applications with sizes
3. Select an app to uninstall
4. Automatically removes associated files

## Safety Features

✅ **Safe Operations**
- Only removes temporary/cache files
- Skips system-critical files
- Reports errors without stopping
- No root/sudo required

✅ **Smart Cleaning**
- Only removes files older than 7 days from `/tmp/`
- Preserves directory structure
- Handles permission errors gracefully

## Example Output

```
============================================================
Mac Cleaner - Starting cleanup process
============================================================
Time: 2026-01-02 14:30:00

📁 Emptying Trash...
✓ Trash: Cleaned 250.50 MB (15 items)

🗄️  Cleaning User Caches...
  ✓ Removed com.apple.Safari: 45.30 MB
  ✓ Removed com.google.Chrome: 120.75 MB
  ✓ Removed com.spotify.client: 85.20 MB
✓ User Caches: Total freed 251.25 MB

🗑️  Cleaning Temporary Files...
✓ /tmp: Cleaned 150.00 MB (8 old items)

📝 Cleaning User Logs...
✓ User Logs: Cleaned 35.50 MB (42 items)

🧹 Checking for leftover files from uninstalled apps...

🔍 Scanning for leftover files from uninstalled apps...

📦 Found 5 leftover items (127.30 MB)

Leftover files from potentially uninstalled apps:
  1. OldAppName (Application Support) - 85.20 MB
  2. AnotherApp (Preferences) - 12.50 MB
  3. RemovedApp (Caches) - 24.60 MB
  ... and 2 more

Would you like to remove these leftover files? [y/N]: y
  ✓ Removed OldAppName
  ✓ Removed AnotherApp
  ✓ Removed RemovedApp

✓ Removed 5 leftover items, freed 127.30 MB

============================================================
📊 DETAILED CLEANING STATISTICS
============================================================

📁 By Category:
  • Trash                          250.50 MB (   15 items)
  • User Caches                    251.25 MB (    3 items)
  • Temporary Files (/tmp)         150.00 MB (    8 items)
  • User Logs                       35.50 MB (   42 items)
  • Leftover App Files             127.30 MB (    5 items)

------------------------------------------------------------
  TOTAL                            814.55 MB (   73 items)

  Space freed: 814.55 MB (0.80 GB)
============================================================

Would you like to manage installed applications? [y/N]: n

============================================================
✨ Cleanup Complete!
Total space freed: 814.55 MB (0.80 GB)
============================================================

Press Enter to close...
```

## Troubleshooting

### "Permission denied" errors
Some directories may require elevated permissions. The script will skip these and continue.

### App won't open
Run this command to remove quarantine attributes:
```bash
xattr -cr "Mac Cleaner.app"
```

Then right-click → Open → Open in the security dialog.

### Python not found
macOS should have Python 3 pre-installed. If not:
```bash
# Install Homebrew (if needed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3
```

## Customization

To clean additional directories, edit `clean_mac.py` and add more paths to the `temp_dirs` list in the `clean_temp_files()` function.

## Support

For issues or questions, please open an issue on GitHub:
https://github.com/mdfalcon104/mac-cleaner/issues
