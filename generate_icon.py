#!/usr/bin/env python3
"""
Generate a simple app icon for Mac Cleaner
This script creates a basic icon image that can be converted to .icns format
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    # Create a 1024x1024 image (required for icns)
    size = 1024
    img = Image.new('RGB', (size, size), color='#4A90E2')
    draw = ImageDraw.Draw(img)
    
    # Draw a broom/cleaner icon (simplified)
    # Draw a circle for the background
    circle_margin = 100
    draw.ellipse([circle_margin, circle_margin, size-circle_margin, size-circle_margin], 
                 fill='#2C5AA0', outline='#1E3A6B', width=10)
    
    # Draw a broom handle (rectangle)
    handle_width = 40
    handle_x = size // 2 - handle_width // 2
    handle_y_start = size // 3
    handle_y_end = size - 200
    draw.rectangle([handle_x, handle_y_start, handle_x + handle_width, handle_y_end], 
                   fill='#8B4513', outline='#654321', width=5)
    
    # Draw broom bristles (triangular shape)
    bristle_width = 200
    bristle_x_left = size // 2 - bristle_width // 2
    bristle_x_right = size // 2 + bristle_width // 2
    bristle_y_top = handle_y_end - 50
    bristle_y_bottom = size - 150
    
    # Draw bristles as a trapezoid
    draw.polygon([
        (bristle_x_left, bristle_y_top),
        (bristle_x_right, bristle_y_top),
        (bristle_x_right - 30, bristle_y_bottom),
        (bristle_x_left + 30, bristle_y_bottom)
    ], fill='#F4A460', outline='#CD853F', width=5)
    
    # Add some bristle lines
    num_lines = 8
    for i in range(num_lines):
        x = bristle_x_left + 30 + (bristle_width - 60) * i / (num_lines - 1)
        draw.line([x, bristle_y_top, x, bristle_y_bottom - 10], fill='#CD853F', width=3)
    
    # Add sparkle effect (stars)
    sparkle_size = 60
    sparkles = [
        (size // 4, size // 4),
        (3 * size // 4, size // 4),
        (size // 2, size // 2 - 100),
    ]
    
    for sx, sy in sparkles:
        # Draw a 4-pointed star
        points = []
        for i in range(8):
            angle = i * 45
            r = sparkle_size if i % 2 == 0 else sparkle_size // 3
            import math
            x = sx + r * math.cos(math.radians(angle))
            y = sy + r * math.sin(math.radians(angle))
            points.append((x, y))
        draw.polygon(points, fill='#FFFF00', outline='#FFD700', width=2)
    
    # Save the icon
    output_path = 'Mac Cleaner.app/Contents/Resources/AppIcon.png'
    img.save(output_path, 'PNG')
    print(f"✓ Icon created: {output_path}")
    print(f"  Size: {size}x{size} pixels")
    print("\nTo convert to .icns format on macOS, run:")
    print(f"  mkdir AppIcon.iconset")
    print(f"  sips -z 16 16     {output_path} --out AppIcon.iconset/icon_16x16.png")
    print(f"  sips -z 32 32     {output_path} --out AppIcon.iconset/icon_16x16@2x.png")
    print(f"  sips -z 32 32     {output_path} --out AppIcon.iconset/icon_32x32.png")
    print(f"  sips -z 64 64     {output_path} --out AppIcon.iconset/icon_32x32@2x.png")
    print(f"  sips -z 128 128   {output_path} --out AppIcon.iconset/icon_128x128.png")
    print(f"  sips -z 256 256   {output_path} --out AppIcon.iconset/icon_128x128@2x.png")
    print(f"  sips -z 256 256   {output_path} --out AppIcon.iconset/icon_256x256.png")
    print(f"  sips -z 512 512   {output_path} --out AppIcon.iconset/icon_256x256@2x.png")
    print(f"  sips -z 512 512   {output_path} --out AppIcon.iconset/icon_512x512.png")
    print(f"  sips -z 1024 1024 {output_path} --out AppIcon.iconset/icon_512x512@2x.png")
    print(f"  iconutil -c icns AppIcon.iconset")
    print(f"  mv AppIcon.icns 'Mac Cleaner.app/Contents/Resources/'")
    
except ImportError:
    print("PIL (Pillow) not found. Installing...")
    import subprocess
    subprocess.run(['pip3', 'install', 'Pillow'])
    print("Please run this script again.")
