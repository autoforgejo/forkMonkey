# Experiment 2: Video-Based Frame Extraction

## Approach

Generate videos of the monkey in various states using Gemini AI video generation, then extract frames and convert to animated GIFs.

## Method

1. **Video Generation:** Use Gemini Video Generation to create ~6 second videos with white background
2. **Frame Extraction:** Use ffmpeg to extract frames at 4 FPS from the video
3. **Processing:** Remove white background, resize to 111×101, and remove semi-transparency
4. **Assembly:** Select evenly-spaced frames to create smooth animation cycle GIFs

## Results

✅ **Pros:**
- **Single API call per animation** (vs 4-8 calls in Experiment 1)
- **8x faster** generation (~30 seconds vs 4 minutes per animation)
- **29-42% smaller files**
- **Lower cost** (1 video generation vs multiple image generations)
- **Smooth, natural motion** from video
- **Easy to extract different cycles** from same video
- **Works for both motion AND static animations**

❌ **Cons:**
- Less control over specific poses
- Limited to motion shown in video
- One animation type per video
- Requires video processing tools (ffmpeg)

## Animations Created

### 1. Idle Animation 😌
- **Video:** `idle_monkey.mp4` (5.9 sec, 141 frames)
- **GIF:** `brown_idle_8fps.gif` (9.8 KB, 4 frames)
- **Savings:** 29% smaller than Experiment 1 (13.8 KB)
- **Description:** Subtle breathing movement, calm standing pose

### 2. Walking Animation 🚶
- **Video:** `walking_monkey.mp4` (5.9 sec, 141 frames)
- **GIF:** `brown_walk_8fps.gif` (12.0 KB, 6 frames)
- **Savings:** 42% smaller than Experiment 1 (20.8 KB)
- **Description:** Natural walking cycle with smooth motion

### 3. Running Animation 🏃
- **Video:** `running_monkey.mp4` (5.9 sec, 141 frames)
- **GIF:** `brown_run_8fps.gif` (20.1 KB, 8 frames)
- **Savings:** 28% smaller than Experiment 1 (28.0 KB)
- **Description:** Fast, energetic running with dynamic motion

## Technical Details

- **AI Model:** Gemini Video Generation
- **Video Specs:** 1920×1080, 24 FPS, ~6 seconds
- **Extraction:** 4 FPS = ~24 frames extracted per video
- **Generation Time:** ~30 seconds per video
- **Processing Time:** ~5 seconds per GIF
- **Total Size:** 41.9 KB (3 GIFs)

## Comparison with Experiment 1

| Animation | Experiment 1 | Experiment 2 | Savings |
|-----------|--------------|--------------|---------|
| Idle | 13.8 KB | 9.8 KB | **29%** |
| Walk | 20.8 KB | 12.0 KB | **42%** |
| Run | 28.0 KB | 20.1 KB | **28%** |
| **Total** | **62.6 KB** | **41.9 KB** | **33%** |

### Overall Metrics

| Metric | Experiment 1 | Experiment 2 | Winner |
|--------|--------------|--------------|--------|
| API Calls | 18 (3 animations) | 3 (3 animations) | ✅ Exp 2 (83% fewer) |
| Generation Time | ~12 min | ~1.5 min | ✅ Exp 2 (8x faster) |
| File Size | 62.6 KB | 41.9 KB | ✅ Exp 2 (33% smaller) |
| Control | High | Medium | ✅ Exp 1 |
| Motion Quality | Good | Excellent | ✅ Exp 2 |
| Versatility | High | High | ✅ Tie |

## File Structure

```
experiment2/
├── videos/
│   ├── idle_monkey.mp4        # Idle video
│   ├── walking_monkey.mp4     # Walking video
│   └── running_monkey.mp4     # Running video
├── frames/
│   └── frame_*.png            # Walking frames
├── frames_idle/
│   └── idle_frame_*.png       # Idle frames
├── frames_run/
│   └── run_frame_*.png        # Running frames
├── gifs/
│   ├── brown_idle_8fps.gif    # Idle GIF (9.8 KB)
│   ├── brown_walk_8fps.gif    # Walking GIF (12 KB)
│   └── brown_run_8fps.gif     # Running GIF (20 KB)
├── scripts/
│   ├── create_idle_gif.py     # Idle conversion
│   ├── video_to_gif.py        # Walking conversion
│   └── create_run_gif.py      # Running conversion
└── README.md                  # This file
```

## Usage

### Generate Videos

Use Gemini API to generate videos with prompts like:

```python
# Idle
"A cute brown monkey standing still with subtle breathing, 
holding a golden fork, pixel art style, white background"

# Walking
"A cute brown monkey walking with a golden fork, pixel art style, 
white background, side view, 2-3 walking cycles"

# Running
"A cute brown monkey running fast with a golden fork, pixel art style,
white background, side view, energetic motion, 2-3 running cycles"
```

### Extract and Convert

```bash
# Idle animation
python3 scripts/create_idle_gif.py

# Walking animation
python3 scripts/video_to_gif.py

# Running animation
python3 scripts/create_run_gif.py
```

## Conclusion

**Experiment 2 is the clear winner across the board!**

### Key Achievements:
- ✅ **83% fewer API calls** (3 vs 18)
- ✅ **8x faster generation** (1.5 min vs 12 min)
- ✅ **33% smaller files** (42 KB vs 63 KB)
- ✅ **Smoother, more natural motion**
- ✅ **Lower costs**
- ✅ **Works for ALL animation types** (motion + static)

### Surprising Discovery:

Video generation works **even for idle/static animations**! The AI can create subtle breathing movements that look natural and alive, proving that video generation is superior not just for motion-based animations, but for ALL animation types.

### Recommendation:

**Use Video Generation (Exp 2) for ALL animations:**
- ✅ Idle animation (subtle breathing)
- ✅ Walk animation (smooth motion)
- ✅ Run animation (dynamic motion)
- ✅ Any future animations

The only reason to use Image Generation (Exp 1) would be if you need very specific, precise poses that are difficult to describe in a video prompt.

## Next Steps

1. ✅ Idle animation complete
2. ✅ Walking animation complete
3. ✅ Running animation complete
4. ⏳ Generate swipe animation (eating with fork)
5. ⏳ Generate with_ball animation (holding ball)
6. ⏳ Create complete asset set for VS Code Pets integration

**Experiment 2 has proven to be the superior approach for Fork Monkey sprite generation!** 🎬🐵🍴
