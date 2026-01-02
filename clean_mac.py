#!/usr/bin/env python3
"""
Mac Cleaner - Clean temporary and unused files on macOS
"""

import os
import shutil
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict


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


def clean_directory(directory, description, stats_dict=None):
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
        
        # Track statistics
        if stats_dict is not None:
            stats_dict['items_removed'] += removed_count
            stats_dict['space_freed'] += size_before
        
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


def get_installed_apps():
    """Get list of installed applications"""
    apps = []
    app_paths = ["/Applications", os.path.expanduser("~/Applications")]
    
    for app_path in app_paths:
        if os.path.exists(app_path):
            try:
                for item in os.listdir(app_path):
                    if item.endswith('.app'):
                        apps.append(os.path.join(app_path, item))
            except Exception:
                pass
    
    return apps


def find_leftover_app_files():
    """Find leftover files from uninstalled applications"""
    print("\n🔍 Scanning for leftover files from uninstalled apps...")
    
    # Get list of installed apps
    installed_apps = get_installed_apps()
    installed_app_names = set()
    
    for app_path in installed_apps:
        app_name = os.path.basename(app_path).replace('.app', '')
        installed_app_names.add(app_name.lower())
    
    leftover_files = []
    total_size = 0
    
    # Directories to check for leftover files
    check_dirs = [
        (os.path.expanduser("~/Library/Application Support"), "Application Support"),
        (os.path.expanduser("~/Library/Preferences"), "Preferences"),
        (os.path.expanduser("~/Library/Caches"), "Caches"),
        (os.path.expanduser("~/Library/Saved Application State"), "Saved Application State"),
        (os.path.expanduser("~/Library/Logs"), "Logs"),
    ]
    
    for check_dir, dir_name in check_dirs:
        if not os.path.exists(check_dir):
            continue
        
        try:
            for item in os.listdir(check_dir):
                item_path = os.path.join(check_dir, item)
                
                # Check if this looks like an app-related directory
                # Skip if the app is still installed
                item_lower = item.lower()
                is_app_related = False
                
                # Check against installed apps
                for app_name in installed_app_names:
                    if app_name in item_lower or item_lower in app_name:
                        is_app_related = True
                        break
                
                # If not related to any installed app, consider it leftover
                if not is_app_related and os.path.isdir(item_path):
                    # Skip common system/generic directories
                    skip_items = ['apple', 'com.apple', 'google', 'microsoft', 'adobe']
                    should_skip = any(skip in item_lower for skip in skip_items)
                    
                    if not should_skip:
                        size = get_size_mb(item_path)
                        if size > 0.5:  # Only show items larger than 0.5 MB
                            leftover_files.append({
                                'path': item_path,
                                'name': item,
                                'location': dir_name,
                                'size': size
                            })
                            total_size += size
        except Exception as e:
            print(f"  ⚠ Could not scan {dir_name}: {str(e)}")
    
    return leftover_files, total_size


def clean_leftover_app_files():
    """Clean leftover files from uninstalled applications"""
    leftover_files, total_size = find_leftover_app_files()
    
    if not leftover_files:
        print("✓ No leftover files from uninstalled apps found")
        return 0
    
    print(f"\n📦 Found {len(leftover_files)} leftover items ({total_size:.2f} MB)")
    print("\nLeftover files from potentially uninstalled apps:")
    
    for i, file_info in enumerate(leftover_files[:10], 1):  # Show first 10
        print(f"  {i}. {file_info['name']} ({file_info['location']}) - {file_info['size']:.2f} MB")
    
    if len(leftover_files) > 10:
        print(f"  ... and {len(leftover_files) - 10} more")
    
    print("\nWould you like to remove these leftover files? [y/N]: ", end='')
    try:
        response = input().strip().lower()
        if response == 'y' or response == 'yes':
            removed_size = 0
            removed_count = 0
            
            for file_info in leftover_files:
                try:
                    shutil.rmtree(file_info['path'])
                    removed_size += file_info['size']
                    removed_count += 1
                    print(f"  ✓ Removed {file_info['name']}")
                except Exception as e:
                    print(f"  ⚠ Could not remove {file_info['name']}: {str(e)}")
            
            print(f"\n✓ Removed {removed_count} leftover items, freed {removed_size:.2f} MB")
            return removed_size
        else:
            print("✓ Skipped cleaning leftover files")
            return 0
    except Exception:
        print("\n✓ Skipped cleaning leftover files")
        return 0


def list_and_uninstall_apps():
    """Interactive mode to list and uninstall applications"""
    print("\n🗂️  Installed Applications Manager")
    print("=" * 60)
    
    installed_apps = get_installed_apps()
    
    if not installed_apps:
        print("No applications found")
        return
    
    # Sort by name
    installed_apps.sort(key=lambda x: os.path.basename(x).lower())
    
    print(f"\nFound {len(installed_apps)} installed applications:\n")
    
    for i, app_path in enumerate(installed_apps, 1):
        app_name = os.path.basename(app_path)
        size = get_size_mb(app_path)
        location = "System" if app_path.startswith("/Applications") else "User"
        print(f"  {i}. {app_name:<40} ({size:>8.2f} MB) [{location}]")
    
    print("\n" + "=" * 60)
    print("Enter app number to uninstall (or 'q' to skip): ", end='')
    
    try:
        response = input().strip()
        
        if response.lower() == 'q':
            print("✓ Skipped app uninstallation")
            return
        
        try:
            app_index = int(response) - 1
            if 0 <= app_index < len(installed_apps):
                app_path = installed_apps[app_index]
                app_name = os.path.basename(app_path)
                
                print(f"\n⚠️  Are you sure you want to uninstall '{app_name}'? [y/N]: ", end='')
                confirm = input().strip().lower()
                
                if confirm == 'y' or confirm == 'yes':
                    try:
                        size = get_size_mb(app_path)
                        shutil.rmtree(app_path)
                        print(f"✓ Uninstalled {app_name} (freed {size:.2f} MB)")
                        
                        # Also try to remove associated files
                        print("\n🔍 Checking for associated files...")
                        app_base_name = app_name.replace('.app', '').lower()
                        
                        check_dirs = [
                            os.path.expanduser("~/Library/Application Support"),
                            os.path.expanduser("~/Library/Preferences"),
                            os.path.expanduser("~/Library/Caches"),
                        ]
                        
                        total_cleaned = 0
                        for check_dir in check_dirs:
                            if os.path.exists(check_dir):
                                for item in os.listdir(check_dir):
                                    if app_base_name in item.lower():
                                        item_path = os.path.join(check_dir, item)
                                        try:
                                            if os.path.isdir(item_path):
                                                size = get_size_mb(item_path)
                                                shutil.rmtree(item_path)
                                                print(f"  ✓ Removed {item} ({size:.2f} MB)")
                                                total_cleaned += size
                                        except Exception:
                                            pass
                        
                        if total_cleaned > 0:
                            print(f"✓ Cleaned {total_cleaned:.2f} MB of associated files")
                        else:
                            print("✓ No additional associated files found")
                            
                    except Exception as e:
                        print(f"✗ Failed to uninstall: {str(e)}")
                else:
                    print("✓ Cancelled uninstallation")
            else:
                print("✗ Invalid app number")
        except ValueError:
            print("✗ Invalid input")
    except Exception:
        print("\n✓ Skipped app uninstallation")


def print_detailed_statistics(stats):
    """Print detailed cleaning statistics"""
    print("\n" + "=" * 60)
    print("📊 DETAILED CLEANING STATISTICS")
    print("=" * 60)
    
    print("\n📁 By Category:")
    for category, data in sorted(stats.items()):
        if data['space'] > 0:
            print(f"  • {category:<30} {data['space']:>10.2f} MB ({data['items']:>5} items)")
    
    total_space = sum(data['space'] for data in stats.values())
    total_items = sum(data['items'] for data in stats.values())
    
    print("\n" + "-" * 60)
    print(f"  {'TOTAL':<30} {total_space:>10.2f} MB ({total_items:>5} items)")
    print(f"\n  Space freed: {total_space:.2f} MB ({total_space/1024:.2f} GB)")
    print("=" * 60)


def main():
    """Main cleaning function"""
    print("=" * 60)
    print("Mac Cleaner - Starting cleanup process")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Initialize statistics tracking
    stats = defaultdict(lambda: {'space': 0, 'items': 0})
    
    total_freed = 0
    
    # Clean trash
    print("\n📁 Emptying Trash...")
    trash_stats = {'items_removed': 0, 'space_freed': 0}
    freed = empty_trash()
    stats['Trash']['space'] = freed
    stats['Trash']['items'] = trash_stats.get('items_removed', 0)
    total_freed += freed
    
    # Clean user caches
    print("\n🗄️  Cleaning User Caches...")
    cache_freed = 0
    cache_items = 0
    cache_path = os.path.expanduser("~/Library/Caches")
    
    if os.path.exists(cache_path):
        try:
            for item in os.listdir(cache_path):
                item_path = os.path.join(cache_path, item)
                if os.path.isdir(item_path):
                    size = get_size_mb(item_path)
                    if size > 0.1:
                        try:
                            shutil.rmtree(item_path)
                            print(f"  ✓ Removed {item}: {size:.2f} MB")
                            cache_freed += size
                            cache_items += 1
                        except Exception as e:
                            print(f"  ⚠ Could not remove {item}: {str(e)}")
        except Exception as e:
            print(f"✗ Error cleaning user caches: {str(e)}")
        
        print(f"✓ User Caches: Total freed {cache_freed:.2f} MB")
    else:
        print("✗ User Caches: Directory not found")
    
    stats['User Caches']['space'] = cache_freed
    stats['User Caches']['items'] = cache_items
    total_freed += cache_freed
    
    # Clean temporary files
    print("\n🗑️  Cleaning Temporary Files...")
    temp_freed = clean_old_tmp_files()
    stats['Temporary Files (/tmp)']['space'] = temp_freed
    total_freed += temp_freed
    
    # Clean user logs
    print("\n📝 Cleaning User Logs...")
    log_stats = {'items_removed': 0, 'space_freed': 0}
    log_freed = clean_directory(
        os.path.expanduser("~/Library/Logs"),
        "User Logs",
        log_stats
    )
    stats['User Logs']['space'] = log_freed
    stats['User Logs']['items'] = log_stats['items_removed']
    total_freed += log_freed
    
    # Clean leftover files from uninstalled apps
    print("\n🧹 Checking for leftover files from uninstalled apps...")
    leftover_freed = clean_leftover_app_files()
    if leftover_freed > 0:
        stats['Leftover App Files']['space'] = leftover_freed
    total_freed += leftover_freed
    
    # Print detailed statistics
    print_detailed_statistics(stats)
    
    # Ask if user wants to manage/uninstall apps
    print("\n" + "=" * 60)
    print("Would you like to manage installed applications? [y/N]: ", end='')
    try:
        response = input().strip().lower()
        if response == 'y' or response == 'yes':
            list_and_uninstall_apps()
    except Exception:
        pass
    
    # Final summary
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
