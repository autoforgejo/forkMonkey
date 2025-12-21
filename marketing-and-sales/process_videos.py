
import os
import subprocess
from PIL import Image
import sys

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEOS_DIR = os.path.join(BASE_DIR, "screenshots", "videos")
OUTPUT_DIR = os.path.join(BASE_DIR, "promo_videos")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Input files (WebP)
inputs = {
    "dashboard": "02_dashboard_view.webp",
    "evolution": "03_evolution_view.webp",
    "tree": "05_family_tree_view.webp",
    "community": "04_community_view.webp",
    "leaderboard": "01_leaderboard_view.webp"
}

# 1. Conversion Function using PIL -> ffmpeg stdin
def convert_webp_to_mp4(input_path, output_path):
    print(f"Processing {os.path.basename(input_path)}...")
    try:
        img = Image.open(input_path)
        width, height = img.size
        # FFMpeg rawvideo requires exact dimensions
        
        # Start ffmpeg process
        # Input: raw rgb24 data from pipe
        # Output: mp4 h264
        cmd = [
            'ffmpeg', '-y', '-v', 'error',
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-s', f'{width}x{height}', # Match input frame size
            '-pix_fmt', 'rgb24',
            '-r', '10', # Use 10 FPS to make the scroll slower/smoother
            '-i', '-',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-preset', 'medium',
            '-crf', '23',
            # Force output to 1400x900 padding/scaling
            '-vf', 'scale=1400:900:force_original_aspect_ratio=decrease,pad=1400:900:(ow-iw)/2:(oh-ih)/2', 
            output_path
        ]
        
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        
        n_frames = getattr(img, 'n_frames', 1)
        for i in range(n_frames):
            img.seek(i)
            frame = img.convert('RGB')
            try:
                process.stdin.write(frame.tobytes())
            except BrokenPipeError:
                break
            
        process.stdin.close()
        process.wait()
        
        if process.returncode != 0:
            print(f"  Error: ffmpeg exited with code {process.returncode}")
        else:
            print(f"  Success -> {os.path.basename(output_path)}")

    except Exception as e:
        print(f"  Exception: {e}")

# 2. Convert all files
mp4_files = {}

print("Step 1: Converting WebP to MP4 via generic frame pipe...")
for key, filename in inputs.items():
    input_path = os.path.join(VIDEOS_DIR, filename)
    if not os.path.exists(input_path):
        print(f"Warning: {filename} not found, skipping.")
        continue
    
    output_path = os.path.join(OUTPUT_DIR, f"{key}.mp4")
    mp4_files[key] = output_path
    
    convert_webp_to_mp4(input_path, output_path)


# 3. Concatenation
def concat_videos_filter(video_keys, output_filename):
    print(f"Concatenating to {output_filename}...")
    valid_inputs = [mp4_files[k] for k in video_keys if k in mp4_files]
    if not valid_inputs:
        print(f"  No valid inputs for {output_filename}")
        return

    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    # [0:v] [1:v] ... concat=n=... [v]
    input_args = []
    filter_parts = []
    for i, path in enumerate(valid_inputs):
        input_args.extend(["-i", path])
        filter_parts.append(f"[{i}:v]")
    
    filter_complex = f"{''.join(filter_parts)}concat=n={len(valid_inputs)}:v=1:a=0[v]"
    
    cmd = [
        "ffmpeg", "-y", "-v", "error"
    ] + input_args + [
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_path
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"  Created {output_filename}")
    except subprocess.CalledProcessError as e:
        print(f"  Error creating {output_filename}: {e}")

print("\nStep 2: Creating Promo Videos...")

# 1. Main Features
concat_videos_filter(["dashboard", "evolution", "tree"], "promo_main_features.mp4")

# 2. Social Features
concat_videos_filter(["community", "leaderboard"], "promo_social_features.mp4")

# 3. Full Walkthrough
concat_videos_filter(["dashboard", "evolution", "tree", "community", "leaderboard"], "promo_full_walkthrough.mp4")

print("\nDone! Videos are ready in marketing-and-sales/promo_videos/")
