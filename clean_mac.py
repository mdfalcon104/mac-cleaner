#!/usr/bin/env python3
"""
Mac Cleaner - Clean temporary and unused files on macOS
"""

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime


def get_size_mb(path):
    """Get size of a file or directory in MB"""
    try:
        if os.path.isfile(path):
            return os.path.getsize(path) / (1024 * 1024)
        elif os.path.isdir(path):
            total = 0
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total += os.path.getsize(filepath)
                    except (OSError, FileNotFoundError):
                        pass
            return total / (1024 * 1024)
    except (OSError, FileNotFoundError):
        return 0
    return 0


def clean_directory(directory, description):
    """Clean a directory and report space freed"""
    try:
        if not os.path.exists(directory):
            print(f"✗ {description}: Directory not found")
            return 0
        
        size_before = get_size_mb(directory)
        
        if size_before == 0:
            print(f"✓ {description}: Already clean (0 MB)")
            return 0
        
        # Remove contents but keep the directory
        removed_count = 0
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                    removed_count += 1
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    removed_count += 1
            except Exception as e:
                print(f"  ⚠ Could not remove {item}: {str(e)}")
        
        print(f"✓ {description}: Cleaned {size_before:.2f} MB ({removed_count} items)")
        return size_before
    except Exception as e:
        print(f"✗ {description}: Error - {str(e)}")
        return 0


def empty_trash():
    """Empty the macOS Trash"""
    trash_path = os.path.expanduser("~/.Trash")
    return clean_directory(trash_path, "Trash")


def clean_user_caches():
    """Clean user cache directories"""
    cache_path = os.path.expanduser("~/Library/Caches")
    total_freed = 0
    
    if not os.path.exists(cache_path):
        print("✗ User Caches: Directory not found")
        return 0
    
    print("\nCleaning User Caches...")
    try:
        for item in os.listdir(cache_path):
            item_path = os.path.join(cache_path, item)
            if os.path.isdir(item_path):
                size = get_size_mb(item_path)
                if size > 0.1:  # Only report items > 0.1 MB
                    try:
                        shutil.rmtree(item_path)
                        print(f"  ✓ Removed {item}: {size:.2f} MB")
                        total_freed += size
                    except Exception as e:
                        print(f"  ⚠ Could not remove {item}: {str(e)}")
    except Exception as e:
        print(f"✗ Error cleaning user caches: {str(e)}")
    
    print(f"✓ User Caches: Total freed {total_freed:.2f} MB")
    return total_freed


def clean_temp_files():
    """Clean temporary files"""
    temp_dirs = [
        "/tmp",
        os.path.expanduser("~/Library/Application Support/CrashReporter"),
        os.path.expanduser("~/Library/Logs"),
    ]
    
    total_freed = 0
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            # For /tmp, be cautious and only clean old files
            if temp_dir == "/tmp":
                freed = clean_old_tmp_files()
                total_freed += freed
            else:
                freed = clean_directory(temp_dir, f"Temp: {temp_dir}")
                total_freed += freed
    
    return total_freed


def clean_old_tmp_files():
    """Clean old temporary files from /tmp"""
    try:
        tmp_path = "/tmp"
        if not os.path.exists(tmp_path):
            return 0
        
        total_freed = 0
        removed_count = 0
        
        for item in os.listdir(tmp_path):
            item_path = os.path.join(tmp_path, item)
            try:
                # Skip system files and recently modified files
                if item.startswith('.'):
                    continue
                
                # Get modification time
                mtime = os.path.getmtime(item_path)
                age_days = (datetime.now() - datetime.fromtimestamp(mtime)).days
                
                # Remove files older than 7 days
                if age_days > 7:
                    size = get_size_mb(item_path)
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    removed_count += 1
                    total_freed += size
            except Exception:
                pass  # Skip files we can't access
        
        if removed_count > 0:
            print(f"✓ /tmp: Cleaned {total_freed:.2f} MB ({removed_count} old items)")
        else:
            print(f"✓ /tmp: No old files to clean")
        
        return total_freed
    except Exception as e:
        print(f"✗ /tmp: Error - {str(e)}")
        return 0


def main():
    """Main cleaning function"""
    print("=" * 60)
    print("Mac Cleaner - Starting cleanup process")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    total_freed = 0
    
    # Clean trash
    print("\n📁 Emptying Trash...")
    total_freed += empty_trash()
    
    # Clean user caches
    print("\n🗄️  Cleaning User Caches...")
    total_freed += clean_user_caches()
    
    # Clean temporary files
    print("\n🗑️  Cleaning Temporary Files...")
    total_freed += clean_temp_files()
    
    # Clean system logs (user accessible)
    print("\n📝 Cleaning User Logs...")
    total_freed += clean_directory(
        os.path.expanduser("~/Library/Logs"),
        "User Logs"
    )
    
    # Summary
    print("\n" + "=" * 60)
    print(f"✨ Cleanup Complete!")
    print(f"Total space freed: {total_freed:.2f} MB ({total_freed/1024:.2f} GB)")
    print("=" * 60)
    
    # Keep window open for a few seconds
    print("\nPress Enter to close...")
    try:
        input()
    except:
        pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCleaning interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {str(e)}")
        sys.exit(1)
