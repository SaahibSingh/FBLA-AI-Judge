#Imports
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple
from moviepy.editor import VideoFileClip  
import whisper  
import pytesseract  
from PIL import Image
import cv2  
import numpy as np
import csv

VIDEO_DIR = "videos/"          # folder where  videos are stored
AUDIO_DIR = "audio/"           # folder to save extracted audio
SLIDES_DIR = "slides/"         # folder with slide images or screenshots per video
OUTPUT_CSV = "features_10_videos.csv"
PRESENTATION_MAX_SECONDS = 7 * 60  # 7 minutes
MIN_WPM = 60.0
MAX_WPM = 250.0
MAX_AVG_PAUSE = 5.0   

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(SLIDES_DIR, exist_ok=True)

whisper_model = whisper.load_model("base")

@dataclass
class PresentationFeatures:
    """
    Container for all extracted features for one presentation.

    Extra fields:
    - analyzed_duration: duration (seconds) of transcript window used (after clipping to 7 minutes).
    - slides_used: how many slides contributed to avg_slide_words (excluding very low-text slides).
    - used_word_timestamps: 1 if word-level timestamps were used for pauses, 0 if fallback.
    """
    video_id: str
    wpm: float
    avg_pause_length: float
    long_pauses_per_min: float
    has_intro: int
    has_conclusion: int
    has_recommendations: int
    avg_slide_words: float
    analyzed_duration: float
    slides_used: int
    used_word_timestamps: int

# 2. Audio extraction & transcription
def extract_audio_from_video(video_path: str, audio_dir: str = AUDIO_DIR) -> str:
    """
    Extract audio from a video file and save as WAV.

    Args:
        video_path: path to the video file (e.g., .mp4).
        audio_dir: directory where the .wav file will be stored.

    Returns:
        Path to the extracted audio file (.wav).
    """
    basename = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = os.path.join(audio_dir, f"{basename}.wav")

    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)
    clip.close()
    return audio_path

def transcribe_audio_with_whisper(audio_path: str) -> Dict[str, Any]:
    """
    Run Whisper transcription on an audio file.

    Tries to request word-level timestamps (word_timestamps=True) when supported, which allows finer-grained pause estimates between individual words. 

    Returns:
        Raw Whisper result dict, which includes "segments" and optionally "words".
    """
    try:
        result = whisper_model.transcribe(
            audio_path,
            verbose=False,
            word_timestamps=True
        )
    except TypeError:
        result = whisper_model.transcribe(audio_path, verbose = False)
    return result

# 3. Transcript-based features: delivery & structure
# Expanded cue phrase lists for detecting intro, conclusion, and recommendations.
INTRO_CUES = [
    "today we will",
    "in this presentation",
    "our topic is",
    "we will be discussing",
    "hello judges",
    "good morning",
    "good afternoon",
    "thank you for being here",
]

CONCLUSION_CUES = [
    "in conclusion",
    "to summarize",
    "in summary",
    "overall",
    "that concludes our presentation",
    "this concludes our presentation",
    "thank you for listening",
    "thank you for your time",
]

RECOMMENDATION_CUES = [
    "we recommend",
    "our recommendation",
    "businesses should",
    "we propose",
    "should consider",
    "we suggest",
    "our solution is",
]

def clip_to_presentation_window(
    segments: List[Dict[str, Any]],
    max_seconds: float = PRESENTATION_MAX_SECONDS,
) -> Tuple[List[Dict[str, Any]], float]:
    """
    Restrict analysis to the first max_seconds of the talk (e.g., 7 minutes).
    This approximates focusing on the main presentation and excluding Q&A.

    Args:
        segments: Whisper segments from the transcript.
        max_seconds: maximum number of seconds to keep.

    Returns:
        (clipped_segments, analyzed_duration)
        - clipped_segments: segments truncated to max_seconds.
        - analyzed_duration: end time of the last clipped segment (<= max_seconds).
    """
    if not segments:
        return [], 0.0
    clipped = []
    last_end = 0.0
    for seg in segments:
        start = seg.get("start", 0.0)
        end = seg.get("end", 0.0)
        if start >= max_seconds:
            break
        seg_copy = dict(seg)
        seg_copy["start"] = start
        seg_copy["end"] = min(end, max_seconds)
        clipped.append(seg_copy)
        last_end = seg_copy["end"]
    return clipped, last_end

def compute_delivery_features(
    transcript_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Compute speaking rate and pause statistics.

    - Uses word-level timestamps when available for more precise pauses.
    - Falls back to segment-level timing otherwise.
    - Restricts analysis to the first PRESENTATION_MAX_SECONDS seconds.
    - Clamps extreme WPM and average pause lengths for robustness.

    Returns:
        dict with keys:
            wpm,
            avg_pause_length,
            long_pauses_per_min,
            analyzed_duration,
            used_word_timestamps (0/1)
    """
    raw_segments = transcript_result.get("segments", [])
    segments, analyzed_duration = clip_to_presentation_window(
        raw_segments, PRESENTATION_MAX_SECONDS
    )
    
    total_words = 0.0
    total_speaking_time = 0.0
    all_word_times: List[tuple] = []
    used_word_timestamps = 0

    for seg in segments:
        text = seg.get("text", "")
        start = seg.get("start", 0.0)
        end = seg.get("end", 0.0)

        words_in_seg = len(text.strip().split())
        total_words += words_in_seg
        total_speaking_time += max(0.0, end - start)

        # Collect per-word times if available (Whisper word-level timestamps).
        if "words" in seg and isinstance(seg["words"], list):
            for w in seg["words"]:
                if "start" in w and "end" in w:
                    all_word_times.append((w["start"], w["end"]))
            used_word_timestamps = 1
    if total_speaking_time == 0 or total_words == 0:
        return {
            "wpm": 0.0,
            "avg_pause_length": 0.0,
            "long_pauses_per_min": 0.0,
            "analyzed_duration": analyzed_duration,
            "used_word_timestamps": 0,
        }
   
    wpm = total_words / (total_speaking_time / 60.0)  # Words per minute
    pauses: List[float] = []

    if all_word_times:
        all_word_times.sort(key=lambda x: x[0])
        for i in range(len(all_word_times) - 1):
            cur_end = all_word_times[i][1]
            next_start = all_word_times[i + 1][0]
            gap = next_start - cur_end
            if 0.0 < gap <= 10.0:  # ignore insane gaps
                pauses.append(gap)
    else:
        for i in range(len(segments) - 1):
            cur_end = segments[i]["end"]
            next_start = segments[i + 1]["start"]
            gap = next_start - cur_end
            if 0.0 < gap <= 10.0:
                pauses.append(gap)

    if pauses:
        avg_pause_length = sum(pauses) / len(pauses)
        long_pauses = [p for p in pauses if p >= 1.0]  # "long" pause threshold = 1s
        long_pauses_per_min = len(long_pauses) / (total_speaking_time / 60.0)
    else:
        avg_pause_length = 0.0
        long_pauses_per_min = 0.0

    # Clamp unrealistic values for robustness.
    if wpm < MIN_WPM or wpm > MAX_WPM:
        wpm = max(MIN_WPM, min(wpm, MAX_WPM))
    if avg_pause_length > MAX_AVG_PAUSE:
        avg_pause_length = MAX_AVG_PAUSE
    return {
        "wpm": wpm,
        "avg_pause_length": avg_pause_length,
        "long_pauses_per_min": long_pauses_per_min,
        "analyzed_duration": analyzed_duration,
        "used_word_timestamps": used_word_timestamps,
    }

def join_segments_text_and_timing(
    transcript_result: Dict[str, Any]
) -> Tuple[List[Dict[str, Any]], float]:
    """
    Flatten segments into a list with start, end, and lowercase text, for structure analysis.

    Also returns analyzed_duration (same clipping as in delivery features).
    """
    raw_segments = transcript_result.get("segments", [])
    segments, analyzed_duration = clip_to_presentation_window(
        raw_segments, PRESENTATION_MAX_SECONDS
    )

    flattened = []
    for seg in segments:
        flattened.append({
            "start": seg.get("start", 0.0),
            "end": seg.get("end", 0.0),
            "text": seg.get("text", "").lower(),
        })
    return flattened, analyzed_duration

def compute_structure_features(
    transcript_result: Dict[str, Any]
) -> Dict[str, int]:
    """
    Detect intro, conclusion, and recommendations using cue phrases and timing.

    - Uses proportion-of-time regions (first 20%, last 20%) within the clipped window.
    - If the analyzed duration is too short (< 3 minutes), structure flags are 0
      because a full intro/body/conclusion is less meaningful.
    """
    segments, analyzed_duration = join_segments_text_and_timing(transcript_result)
    if not segments:
        return {
            "has_intro": 0,
            "has_conclusion": 0,
            "has_recommendations": 0,
        }

    # Very short talks: treat structure as absent/undefined.
    if analyzed_duration < 3 * 60:  # < 3 minutes
        return {
            "has_intro": 0,
            "has_conclusion": 0,
            "has_recommendations": 0,
        }

    intro_end = 0.2 * analyzed_duration         # first 20% of time
    conclusion_start = 0.8 * analyzed_duration  # last 20% of time

    intro_text = " ".join(seg["text"] for seg in segments if seg["start"] <= intro_end)
    conclusion_text = " ".join(seg["text"] for seg in segments if seg["end"] >= conclusion_start)
    full_text = " ".join(seg["text"] for seg in segments)

    def contains_any(text: str, cues: List[str]) -> bool:
        return any(cue in text for cue in cues)

    has_intro = int(contains_any(intro_text, INTRO_CUES))
    has_conclusion = int(contains_any(conclusion_text, CONCLUSION_CUES))
    has_recommendations = int(contains_any(full_text, RECOMMENDATION_CUES))

    return {
        "has_intro": has_intro,
        "has_conclusion": has_conclusion,
        "has_recommendations": has_recommendations,
    }

# 4. Slide text density using OCR (with preprocessing and low-text filter)

def preprocess_for_ocr(pil_img: Image.Image) -> Image.Image:
    """
    Basic preprocessing to improve OCR on slide images. [web:152][web:155]

    Steps:
    - Convert to grayscale.
    - Binarize using OTSU thresholding.
    - Light morphology (erode + dilate) to reduce small noise.
    """
    img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    kernel = np.ones((2, 2), np.uint8)
    binary = cv2.erode(binary, kernel, iterations=1)
    binary = cv2.dilate(binary, kernel, iterations=1)

    return Image.fromarray(binary)

def get_slide_images_for_video(video_basename: str) -> List[str]:
    """
    Return a list of slide image paths for a given video ID.

    Expected naming convention:
        slides/{video_basename}_slide1.png,
        slides/{video_basename}_slide2.png, ...
    """
    slide_paths = []
    if not os.path.exists(SLIDES_DIR):
        return slide_paths
    for fname in sorted(os.listdir(SLIDES_DIR)):
        if fname.startswith(video_basename) and fname.lower().endswith((".png", ".jpg", ".jpeg")):
            slide_paths.append(os.path.join(SLIDES_DIR, fname))
    return slide_paths

def compute_avg_slide_words(video_basename: str) -> Tuple[float, int]:
    """
    Estimate average words per slide using pytesseract OCR. 

    - Preprocess slide images (grayscale + binarization + morphology).
    - Run Tesseract with config tuned for English blocks of text.
    - Ignore slides with very few words (< 3) to avoid title-only / mostly-image slides
      dominating the average.

    Returns:
        (avg_words, slides_used)
        - avg_words: average word count per slide (over slides that passed filter),
        - slides_used: number of slides included in the average.
    """
    slide_paths = get_slide_images_for_video(video_basename)
    if not slide_paths:
        return 0.0, 0

    total_words = 0
    counted_slides = 0

    custom_config = r"--oem 3 --psm 6 -l eng"

    for path in slide_paths:
        try:
            pil_img = Image.open(path)
        except Exception:
            continue

        preprocessed = preprocess_for_ocr(pil_img)
        text = pytesseract.image_to_string(preprocessed, config=custom_config)
        words = text.strip().split()
        word_count = len(words)

        # Ignore very low-text slides (likely title-only or mostly images)
        if word_count < 3:
            continue

        total_words += word_count
        counted_slides += 1

    if counted_slides == 0:
        return 0.0, 0

    avg_words = total_words / counted_slides
    return avg_words, counted_slides

# 5. Main pipeline for a list of videos

def process_single_video(video_path: str) -> Optional[PresentationFeatures]:
    """
    End-to-end feature extraction for one video file.

    Handles:
    - Audio extraction
    - ASR transcription
    - Delivery features
    - Structure features
    - Slide text density

    Returns:
        PresentationFeatures object, or None if something failed.
    """
    basename = os.path.splitext(os.path.basename(video_path))[0]
    print(f"\n=== Processing {basename} ===")

    # 1) Extract audio
    try:
        audio_path = extract_audio_from_video(video_path)
    except Exception as e:
        print(f"[WARN] Failed to extract audio for {basename}: {e}")
        return None

    # 2) Transcribe audio
    try:
        transcript_result = transcribe_audio_with_whisper(audio_path)
    except Exception as e:
        print(f"[WARN] Failed to transcribe {basename}: {e}")
        return None

    # 3) Delivery features
    delivery = compute_delivery_features(transcript_result)

    # 4) Structure features
    structure = compute_structure_features(transcript_result)

    # 5) Slide features
    avg_slide_words, slides_used = compute_avg_slide_words(basename)

    # Quick sanity log for this video
    print(
        f"  analyzed_duration={delivery['analyzed_duration']:.1f}s, "
        f"wpm={delivery['wpm']:.1f}, "
        f"avg_pause={delivery['avg_pause_length']:.2f}s, "
        f"long_pauses/min={delivery['long_pauses_per_min']:.2f}, "
        f"intro={structure['has_intro']}, "
        f"conclusion={structure['has_conclusion']}, "
        f"recs={structure['has_recommendations']}, "
        f"avg_slide_words={avg_slide_words:.1f} (slides_used={slides_used}), "
        f"used_word_ts={delivery['used_word_timestamps']}"
    )

    return PresentationFeatures(
        video_id=basename,
        wpm=delivery["wpm"],
        avg_pause_length=delivery["avg_pause_length"],
        long_pauses_per_min=delivery["long_pauses_per_min"],
        has_intro=structure["has_intro"],
        has_conclusion=structure["has_conclusion"],
        has_recommendations=structure["has_recommendations"],
        avg_slide_words=avg_slide_words,
        analyzed_duration=delivery["analyzed_duration"],
        slides_used=slides_used,
        used_word_timestamps=delivery["used_word_timestamps"],
    )

def process_all_videos(video_dir: str = VIDEO_DIR, output_csv: str = OUTPUT_CSV):
    """
    Loop over all video files in VIDEO_DIR and extract features to a CSV.

    Only video files with typical extensions (.mp4, .mov, .mkv, .avi) are processed.
    """
    feature_rows: List[Dict[str, Any]] = []

    for fname in sorted(os.listdir(video_dir)):
        if not fname.lower().endswith((".mp4", ".mov", ".mkv", ".avi")):
            continue
        video_path = os.path.join(video_dir, fname)
        feats = process_single_video(video_path)
        if feats is not None:
            feature_rows.append(asdict(feats))

    # Write to CSV
    if feature_rows:
        fieldnames = list(feature_rows[0].keys())
        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in feature_rows:
                writer.writerow(row)
        print(f"\nSaved features for {len(feature_rows)} videos to {output_csv}")
    else:
        print("No valid feature rows produced.")

if __name__ == "__main__":
    process_all_videos()
