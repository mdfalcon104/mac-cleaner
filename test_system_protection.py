#!/usr/bin/env python3
"""
Test system file protection in Mac Cleaner
"""

import sys
sys.path.insert(0, '/Users/mdlabs/Downloads/mac-cleaner')

from clean_mac import is_system_file, SYSTEM_SKIP_PATTERNS, SYSTEM_PREFIXES

def test_system_file_protection():
    """Test that system files are properly detected and protected"""
    
    print("Testing System File Protection")
    print("=" * 60)
    
    # Test cases: (filename, should_be_protected)
    test_cases = [
        # Apple system files
        ("com.apple.SwiftUI.filePromises-A7B79DDC-71E3-4A3D-86FF-95CEB1AFA475", True),
        ("com.apple.Safari", True),
        ("com.apple.security.checkfixpermissions", True),
        ("Apple.plist", True),
        ("apple-internal", True),
        
        # Other system vendors
        ("com.google.Chrome", True),
        ("com.microsoft.Office", True),
        ("com.adobe.Reader", True),
        
        # macOS system components
        ("WebKit.cache", True),
        ("Safari.history", True),
        ("Finder.cache", True),
        ("com.apple.Metal", True),
        ("com.apple.CloudKit", True),
        
        # User apps that should be cleaned
        ("com.spotify.client", False),
        ("Slack", False),
        ("VSCode", False),
        ("Discord", False),
        ("MyCustomApp", False),
        ("com.example.myapp", False),
        ("UserApplication", False),
    ]
    
    print("\n✅ Should be PROTECTED (system files):")
    print("-" * 60)
    for filename, should_protect in test_cases:
        if should_protect:
            is_protected = is_system_file(filename)
            status = "✓" if is_protected else "✗ FAILED"
            print(f"  {status} {filename:<60} {'Protected' if is_protected else 'NOT PROTECTED!'}")
            if not is_protected:
                print(f"      ⚠️  WARNING: This file should be protected but isn't!")
    
    print("\n🗑️  Should be CLEANABLE (user files):")
    print("-" * 60)
    for filename, should_protect in test_cases:
        if not should_protect:
            is_protected = is_system_file(filename)
            status = "✓" if not is_protected else "✗ FAILED"
            print(f"  {status} {filename:<60} {'Cleanable' if not is_protected else 'PROTECTED!'}")
            if is_protected:
                print(f"      ⚠️  WARNING: This user file is being protected!")
    
    # Count results
    print("\n" + "=" * 60)
    failures = []
    for filename, should_protect in test_cases:
        is_protected = is_system_file(filename)
        if should_protect != is_protected:
            failures.append((filename, should_protect, is_protected))
    
    if failures:
        print(f"❌ FAILED: {len(failures)} test(s) failed")
        for filename, should_protect, is_protected in failures:
            expected = "protected" if should_protect else "cleanable"
            actual = "protected" if is_protected else "cleanable"
            print(f"   - {filename}: expected {expected}, got {actual}")
    else:
        print(f"✅ SUCCESS: All {len(test_cases)} tests passed!")
    
    print("\n📋 Protection Configuration:")
    print(f"   - System patterns: {len(SYSTEM_SKIP_PATTERNS)}")
    print(f"   - System prefixes: {len(SYSTEM_PREFIXES)}")
    print("\n" + "=" * 60)
    
    return len(failures) == 0


if __name__ == "__main__":
    success = test_system_file_protection()
    sys.exit(0 if success else 1)
