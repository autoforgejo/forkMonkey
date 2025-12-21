
from PIL import Image
import os

path = "screenshots/videos/02_dashboard_view.webp"

try:
    img = Image.open(path)
    print(f"Opened: {path}")
    print(f"Format: {img.format}")
    print(f"Size: {img.size}")
    print(f"Frames: {getattr(img, 'n_frames', 1)}")
    
    # Try to access a frame
    img.seek(0)
    print("Frame 0 access successful")
except Exception as e:
    print(f"Failed to open with Pillow: {e}")
