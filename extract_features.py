#Imports

import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple
from moviepy import VideoFileClip  # moviepy v2: import directly from moviepy (moviepy.editor was removed in v2)
import whisper
import pytesseract
from PIL import Image
import cv2
import numpy as np
import csv

VIDEO_DIR = "videos/" # folder where videos are stored
AUDIO_DIR = "audio/" # folder to save extracted audio
SLIDES_DIR = "slides/" # folder with slide images or screenshots per video
OUTPUT_CSV = "features_10_videos.csv"
PRESENTATION_MAX_SECONDS = 7 * 60 # 7 minutes
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
    basename = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = os.path.join(audio_dir, f"{basename}.wav")
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, logger=None)
    clip.close()
    return audio_path


def transcribe_audio_with_whisper(audio_path: str) -> Dict[str, Any]:
    try:
        result = whisper_model.transcribe(
            audio_path,
            verbose=False,
            word_timestamps=True,
        )
    except TypeError:
        result = whisper_model.transcribe(audio_path, verbose=False)
    return result
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
    wpm = total_words / (total_speaking_time / 60.0)
    pauses: List[float] = []
    if all_word_times:
        all_word_times.sort(key=lambda x: x[0])
        for i in range(len(all_word_times) - 1):
            cur_end = all_word_times[i][1]
            next_start = all_word_times[i + 1][0]
            gap = next_start - cur_end
            if 0.0 < gap <= 10.0:
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
        long_pauses = [p for p in pauses if p >= 1.0]
        long_pauses_per_min = len(long_pauses) / (total_speaking_time / 60.0)

    else:
        avg_pause_length = 0.0
        long_pauses_per_min = 0.0
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
    segments, analyzed_duration = join_segments_text_and_timing(transcript_result)
    if not segments:
        return {
            "has_intro": 0,
            "has_conclusion": 0,
            "has_recommendations": 0,
        }
    if analyzed_duration < 3 * 60:
        return {
            "has_intro": 0,
            "has_conclusion": 0,
            "has_recommendations": 0,
        }
    intro_end = 0.2 * analyzed_duration
    conclusion_start = 0.8 * analyzed_duration
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


def preprocess_for_ocr(pil_img: Image.Image) -> Image.Image:
    img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    kernel = np.ones((2, 2), np.uint8)
    binary = cv2.erode(binary, kernel, iterations=1)
    binary = cv2.dilate(binary, kernel, iterations=1)
    return Image.fromarray(binary)


def get_slide_images_for_video(video_basename: str) -> List[str]:
    """Original folder-based slide lookup — used by main.py batch pipeline."""
    slide_paths = []
    if not os.path.exists(SLIDES_DIR):
        return slide_paths
    for fname in sorted(os.listdir(SLIDES_DIR)):
        if fname.startswith(video_basename) and fname.lower().endswith((".png", ".jpg", ".jpeg")):
            slide_paths.append(os.path.join(SLIDES_DIR, fname))
    return slide_paths


def compute_avg_slide_words(video_basename: str) -> Tuple[float, int]:
    """Original folder-based OCR — used by main.py batch pipeline."""
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
        if len(words) < 3:
            continue
        total_words += len(words)
        counted_slides += 1
    if counted_slides == 0:
        return 0.0, 0
    return total_words / counted_slides, counted_slides


# Frame interval for slide sampling: one frame every N seconds.
# 5 s gives ~84 samples for a 7-min presentation — enough to catch every
# slide transition without being too slow.
FRAME_SAMPLE_INTERVAL = 5.0

# If two consecutive sampled frames differ by less than this fraction of
# pixels (after downscaling), treat them as the same slide and skip the
# duplicate.  0.02 = 2 % pixel difference threshold.
FRAME_DEDUP_THRESHOLD = 0.02


def _frames_are_duplicate(gray_a: np.ndarray, gray_b: np.ndarray) -> bool:
    """Return True if two greyscale frames are visually near-identical."""
    if gray_a.shape != gray_b.shape:
        return False
    diff = np.abs(gray_a.astype(np.int32) - gray_b.astype(np.int32))
    changed_pixels = np.sum(diff > 10)
    return (changed_pixels / gray_a.size) < FRAME_DEDUP_THRESHOLD


def compute_avg_slide_words_from_video(
    video_path: str,
    sample_interval: float = FRAME_SAMPLE_INTERVAL,
) -> Tuple[float, int]:
    """
    Extract slide content directly from a video file.

    Samples one frame every `sample_interval` seconds, deduplicates
    near-identical consecutive frames (repeated title cards, static
    backgrounds), then runs Tesseract OCR on each unique frame and
    computes the average word count per frame.

    Returns
    -------
    (avg_slide_words, unique_frames_used)
      avg_slide_words  – average word count per unique frame (0.0 if none)
      unique_frames_used – number of unique frames that passed dedup + had ≥3 words
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return 0.0, 0

    fps      = cap.get(cv2.CAP_PROP_FPS) or 25.0
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = n_frames / fps
    step     = int(fps * sample_interval)
    if step < 1:
        step = 1

    ocr_config   = r"--oem 3 --psm 6 -l eng"
    total_words  = 0
    counted      = 0
    prev_gray    = None
    frame_idx    = 0

    while True:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            break

        # Downscale for fast dedup comparison (keeps ~10 % of pixels)
        small = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)
        gray  = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

        if prev_gray is not None and _frames_are_duplicate(prev_gray, gray):
            frame_idx += step
            continue
        prev_gray = gray

        # Full-res OCR
        pil_img    = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        processed  = preprocess_for_ocr(pil_img)
        text       = pytesseract.image_to_string(processed, config=ocr_config)
        word_count = len(text.strip().split())

        if word_count >= 3:
            total_words += word_count
            counted     += 1

        frame_idx += step
        # Stop once we've passed the presentation window
        if frame_idx / fps > PRESENTATION_MAX_SECONDS:
            break

    cap.release()

    if counted == 0:
        return 0.0, 0
    return total_words / counted, counted


def process_single_video(video_path: str) -> Optional[PresentationFeatures]:
    basename = os.path.splitext(os.path.basename(video_path))[0]
    print(f"\n=== Processing {basename} ===")
    try:
        audio_path = extract_audio_from_video(video_path)
    except Exception as e:
        print(f"[WARN] Failed to extract audio for {basename}: {e}")
        return None
    try:
        transcript_result = transcribe_audio_with_whisper(audio_path)
    except Exception as e:
        print(f"[WARN] Failed to transcribe {basename}: {e}")
        return None
    delivery = compute_delivery_features(transcript_result)
    structure = compute_structure_features(transcript_result)
    # Try frame-based slide extraction first; fall back to folder-based
    avg_slide_words, slides_used = compute_avg_slide_words_from_video(video_path)
    if slides_used == 0:
        avg_slide_words, slides_used = compute_avg_slide_words(basename)
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
    feature_rows: List[Dict[str, Any]] = []
    for fname in sorted(os.listdir(video_dir)):
        if not fname.lower().endswith((".mp4", ".mov", ".mkv", ".avi")):
            continue
        video_path = os.path.join(video_dir, fname)
        feats = process_single_video(video_path)
        if feats is not None:
            feature_rows.append(asdict(feats))
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
