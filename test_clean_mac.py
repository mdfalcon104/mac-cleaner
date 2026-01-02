#!/usr/bin/env python3
"""
Basic tests for Mac Cleaner script
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clean_mac


class TestMacCleaner(unittest.TestCase):
    """Test cases for Mac Cleaner functions"""
    
    def test_get_size_mb_nonexistent(self):
        """Test get_size_mb with non-existent path"""
        size = clean_mac.get_size_mb("/nonexistent/path")
        self.assertEqual(size, 0)
    
    def test_get_size_mb_file(self):
        """Test get_size_mb with a real file"""
        # Use the script itself as a test file
        script_path = os.path.join(os.path.dirname(__file__), "clean_mac.py")
        size = clean_mac.get_size_mb(script_path)
        self.assertGreater(size, 0)
        self.assertLess(size, 1)  # Script should be less than 1 MB
    
    def test_clean_directory_nonexistent(self):
        """Test clean_directory with non-existent directory"""
        freed = clean_mac.clean_directory("/nonexistent/dir", "Test Dir")
        self.assertEqual(freed, 0)
    
    def test_clean_directory_empty(self):
        """Test clean_directory with empty directory"""
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            freed = clean_mac.clean_directory(tmpdir, "Empty Test Dir")
            self.assertEqual(freed, 0)
    
    def test_get_installed_apps(self):
        """Test get_installed_apps function"""
        apps = clean_mac.get_installed_apps()
        self.assertIsInstance(apps, list)
    
    def test_find_leftover_app_files(self):
        """Test find_leftover_app_files function"""
        leftover_files, total_size = clean_mac.find_leftover_app_files()
        self.assertIsInstance(leftover_files, list)
        self.assertIsInstance(total_size, (int, float))
        self.assertGreaterEqual(total_size, 0)


if __name__ == "__main__":
    print("Running Mac Cleaner tests...")
    print("=" * 60)
    unittest.main(verbosity=2)
