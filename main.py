# Imports
import os
import sys
import csv
import argparse
from dataclasses import asdict
from typing import Optional

# ── Pipeline modules ──────────────────────────────────────────────────────────
from extract_features import (
    process_single_video,
    PresentationFeatures,
    VIDEO_DIR,
    OUTPUT_CSV,
)
from rubric_heuristics import score_presentation, generate_feedback

# ──────────────────────────────────────────────────────────────────────────────
# VIDEO REGISTRY
# Maps each video slot (1-10) to:
#   filename  – file that must exist inside VIDEO_DIR
#   label     – human-readable name (from meeting notes p.21)
#   event     – FBLA rubric event key from rubric_heuristics.EVENTS
#
# Filename convention: video_<slot>_<short_description>.<ext>
# Use whatever extension the actual file has (.mp4 / .mov / .mkv / .avi).
# If you rename your files differently, update the "filename" field below.
# ──────────────────────────────────────────────────────────────────────────────
VIDEOS = [
    {
        "slot": 1,
        "filename": "video_01_fbla_intro_business_2026_1.mp4",
        "label": "FBLA Introduction to Business Presentation 2026 #1",
        "event": "IntroductiontoBusinessPresentation",
    },
    {
        "slot": 2,
        "filename": "video_02_fbla_intro_business_2026_2_3rd_slc.mp4",
        "label": "FBLA Introduction to Business Presentation #2 (3rd Place SLC 2026)",
        "event": "IntroductiontoBusinessPresentation",
    },
    {
        "slot": 3,
        "filename": "video_03_fbla_intro_business_3.mp4",
        "label": "FBLA Introduction to Business Presentation #3",
        "event": "IntroductiontoBusinessPresentation",
    },
    {
        "slot": 4,
        "filename": "video_04_fbla_intro_business_4.mp4",
        "label": "FBLA Introduction to Business Presentation #4",
        "event": "IntroductiontoBusinessPresentation",
    },
    {
        "slot": 5,
        "filename": "video_05_fbla_sales_presentation_1st_slc_2021.mp4",
        "label": "FBLA Sales Presentation (1st Place SLC 2021)",
        "event": "SalesPresentation",
    },
    {
        "slot": 6,
        "filename": "video_06_fbla_digital_video_production_2023.mp4",
        "label": "FBLA 2023 Digital Video Production Contest Presentation",
        "event": "DigitalVideoProduction",
    },
    {
        "slot": 7,
        "filename": "video_07_spelpreneur_pitch_2025.mp4",
        "label": "Spelpreneur Pitch Competition 2025 – Student Business Pitch",
        "event": "BusinessPlan",
    },
    {
        "slot": 8,
        "filename": "video_08_warrior_startup_challenge_2025.mp4",
        "label": "2025 Warrior Startup Challenge – Student Business Plan Competition",
        "event": "BusinessPlan",
    },
    {
        "slot": 9,
        "filename": "video_09_high_school_business_pitch.mp4",
        "label": "High School Business Pitch Competition",
        "event": "BusinessPlan",
    },
    {
        "slot": 10,
        "filename": "video_10_high_school_entrepreneurship_pitch.mp4",
        "label": "High School Entrepreneurship Pitch",
        "event": "BusinessPlan",
    },
]

# HELPERS
def resolve_video_path(filename: str) -> Optional[str]:
    """
    Find a video file by its registered filename, trying all common extensions
    so you don't have to rename files just to change the container format.
    Returns the full path if found, None otherwise.
    """
    base, _ = os.path.splitext(filename)
    for ext in (".mp4", ".mov", ".mkv", ".avi", ".webm"):
        candidate = os.path.join(VIDEO_DIR, base + ext)
        if os.path.isfile(candidate):
            return candidate
    # Also try exact filename as-is
    exact = os.path.join(VIDEO_DIR, filename)
    if os.path.isfile(exact):
        return exact
    return None

def print_separator(char: str = "─", width: int = 68) -> None:
    print(char * width)

def print_feature_table(feats: PresentationFeatures) -> None:
    """Pretty-print extracted features in a compact table."""
    rows = [
        ("WPM",                    f"{feats.wpm:.1f}"),
        ("Avg pause length (s)",   f"{feats.avg_pause_length:.2f}"),
        ("Long pauses / min",      f"{feats.long_pauses_per_min:.2f}"),
        ("Has intro",              str(feats.has_intro)),
        ("Has conclusion",         str(feats.has_conclusion)),
        ("Has recommendations",    str(feats.has_recommendations)),
        ("Avg slide words",        f"{feats.avg_slide_words:.1f}"),
        ("Analyzed duration (s)",  f"{feats.analyzed_duration:.1f}"),
        ("Slides used",            str(feats.slides_used)),
        ("Word-level timestamps",  str(feats.used_word_timestamps)),
    ]
    col = max(len(r[0]) for r in rows)
    for label, value in rows:
        print(f"  {label:<{col}}  {value}")
 
# PER-VIDEO TEST RUNNER
def run_video_test(entry: dict, dry_run: bool = False) -> Optional[dict]:
    """
    Process one video entry end-to-end:
      1. Resolve file path.
      2. Extract features (skip in dry-run mode).
      3. Score against the event rubric.
      4. Print results.
    Returns a flat dict suitable for CSV writing, or None on failure.
    """
    slot     = entry["slot"]
    filename = entry["filename"]
    label    = entry["label"]
    event    = entry["event"]
    print()
    print_separator("═")
    print(f"  VIDEO {slot:02d} / 10")
    print(f"  {label}")
    print(f"  Event rubric : {event}")
    print(f"  File         : {filename}")
    print_separator("═")
  
    # ── 1. File check ──────────────────────────────────────────────────────
    video_path = resolve_video_path(filename)
    if video_path is None:
        print(f"\n  [SKIP] File not found in '{VIDEO_DIR}'.")
        print( "         Expected name (any extension):")
        print(f"           {os.path.splitext(filename)[0]}.<mp4|mov|mkv|avi>")
        print( "         Rename your downloaded file to match and re-run.")
        return None
    print(f"  Found        : {video_path}")
    if dry_run:
        print("  [DRY-RUN] Skipping processing.")
        return None
      
    # ── 2. Feature extraction ─────────────────────────────────────────────
    print()
    feats: Optional[PresentationFeatures] = process_single_video(video_path)
    if feats is None:
        print(f"\n  [ERROR] Feature extraction failed for video {slot}.")
        return None
    print()
    print("  EXTRACTED FEATURES")
    print_separator()
    print_feature_table(feats)
    # ── 3. Rubric scoring ─────────────────────────────────────────────────
    feature_dict = {
        "wpm":                   feats.wpm,
        "avg_pause_length":      feats.avg_pause_length,
        "long_pauses_per_minute": feats.long_pauses_per_min,
        "has_intro":             feats.has_intro,
        "has_conclusion":        feats.has_conclusion,
        "has_recommendations":   feats.has_recommendations,
        "avg_slide_words":       feats.avg_slide_words if feats.avg_slide_words > 0 else None,
        "slides_per_minute":     None,
    }
    score_result = score_presentation(event, feature_dict)
    report = generate_feedback(score_result)
    print()
    print(report)
  
    # ── 4. Build CSV row ──────────────────────────────────────────────────
    row = asdict(feats)
    row["event"] = event
    row["normalized_score"] = score_result["normalized_score"]
    row["score_band"]       = score_result["placement_estimate"]["score_band"]
    row["top3_likelihood"]  = score_result["placement_estimate"]["top3_likelihood"]
    row["top10_likelihood"] = score_result["placement_estimate"]["top10_likelihood"]
    row["label"]            = label
    return row

# MAIN
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run feature extraction + rubric scoring on the 10 test videos."
    )
    parser.add_argument(
        "--video",
        nargs="+",
        type=int,
        metavar="N",
        help="Run only specific video slots (1-10). Omit to run all 10.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Check which video files exist without running extraction.",
    )
    args = parser.parse_args()
    # Filter video list
    if args.video:
        invalid = [n for n in args.video if n < 1 or n > 10]
        if invalid:
            print(f"[ERROR] Invalid slot numbers: {invalid}. Must be 1-10.")
            sys.exit(1)
        selected = [v for v in VIDEOS if v["slot"] in args.video]
    else:
        selected = VIDEOS
    mode = "DRY-RUN" if args.dry_run else "FULL PIPELINE"
    print()
    print("=" * 68)
    print(f"  FBLA-AI-Judge — Test Harness  [{mode}]")
    print(f"  Videos to process: {len(selected)} / 10")
    print(f"  Video directory  : {os.path.abspath(VIDEO_DIR)}")
    print(f"  Output CSV       : {OUTPUT_CSV}")
    print("=" * 68)
    results = []
    skipped = []
    failed  = []
    for entry in selected:
        row = run_video_test(entry, dry_run=args.dry_run)
        if row is not None:
            results.append(row)
        elif resolve_video_path(entry["filename"]) is None:
            skipped.append(entry["slot"])
        else:
            failed.append(entry["slot"])
    # ── Summary ───────────────────────────────────────────────────────────
    print()
    print_separator("═")
    print("  RUN SUMMARY")
    print_separator("═")
    print(f"  Processed : {len(results)}")
    print(f"  Skipped   : {len(skipped)}  (files not found — slots: {skipped or 'none'})")
    print(f"  Failed    : {len(failed)}   (extraction errors — slots: {failed or 'none'})")
    if results:
        print()
        print("  SCORE OVERVIEW")
        print_separator()
        header = f"  {'Slot':>4}  {'Score':>6}  {'Band':<22}  {'Top3':<6}  Label"
        print(header)
        print_separator()
        for row in results:
            slot_num = next(v["slot"] for v in VIDEOS if v["label"] == row["label"])
            print(
                f"  {slot_num:>4}  {row['normalized_score']:>5.1f}%"
                f"  {row['score_band']:<22}"
                f"  {row['top3_likelihood']:<6}"
                f"  {row['label'][:45]}"
            )
        # ── Write CSV ─────────────────────────────────────────────────────
        if not args.dry_run:
            fieldnames = list(results[0].keys())
            with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for row in results:
                    writer.writerow(row)
            print()
            print(f"  CSV written → {OUTPUT_CSV}")
    print_separator("═")
    print()
if __name__ == "__main__":
    main()
