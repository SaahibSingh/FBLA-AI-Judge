"""
app.py — FBLA AI Judge  |  Interactive Dashboard
Run with:  python3 -m streamlit run app.py
"""

import os
import sys
import tempfile
import traceback
import importlib.util
import subprocess
import re

import streamlit as st

st.set_page_config(
    page_title="FBLA AI Judge",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #0d0f14; color: #e8eaf0; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 4rem; }
.hero { text-align: center; padding: 3rem 1rem 2rem; }
.hero-eyebrow { font-family: 'Space Grotesk', sans-serif; font-size: 0.72rem;
    font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase;
    color: #5b8cf5; margin-bottom: 0.75rem; }
.hero-title { font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(2rem,5vw,3.2rem); font-weight: 700; color: #f0f2f8;
    line-height: 1.1; margin: 0 0 0.6rem; }
.hero-title span { color: #5b8cf5; }
.hero-sub { font-size: 1rem; color: #8a8fa8; max-width: 540px;
    margin: 0 auto; line-height: 1.6; }
.card { background: #13161f; border: 1px solid #1e2230; border-radius: 12px;
    padding: 1.5rem; margin-bottom: 1rem; }
.card-label { font-size: 0.72rem; font-weight: 600; letter-spacing: 0.12em;
    text-transform: uppercase; color: #5b8cf5; margin-bottom: 0.5rem; }
.score-ring { text-align: center; padding: 1.2rem 0; }
.score-ring .big { font-family: 'Space Grotesk', sans-serif; font-size: 4rem;
    font-weight: 700; line-height: 1; }
.score-ring .denom { font-size: 1.4rem; color: #8a8fa8; font-weight: 400; }
.badge { display: inline-block; padding: 0.3rem 0.9rem; border-radius: 999px;
    font-size: 0.78rem; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; }
.badge-high   { background:#1a3a2a; color:#4ade80; border:1px solid #166534; }
.badge-medium { background:#2d2a14; color:#facc15; border:1px solid #713f12; }
.badge-low    { background:#2a1a1a; color:#f87171; border:1px solid #7f1d1d; }
.crit-row { margin-bottom: 0.85rem; }
.crit-header { display:flex; justify-content:space-between; align-items:baseline; margin-bottom:0.25rem; }
.crit-label { font-size:0.82rem; color:#c8cad8; }
.crit-pts { font-size:0.78rem; font-weight:600; color:#8a8fa8; white-space:nowrap; }
.bar-track { height:7px; background:#1e2230; border-radius:999px; overflow:hidden; }
.bar-fill  { height:100%; border-radius:999px; }
.bar-high   { background:linear-gradient(90deg,#3b82f6,#6366f1); }
.bar-medium { background:linear-gradient(90deg,#f59e0b,#fb923c); }
.bar-low    { background:linear-gradient(90deg,#ef4444,#f97316); }
.improve-item { background:#13161f; border-left:3px solid #5b8cf5;
    border-radius:0 8px 8px 0; padding:0.75rem 1rem; margin-bottom:0.6rem;
    font-size:0.85rem; color:#c8cad8; line-height:1.5; }
.improve-item strong { display:block; color:#f0f2f8; font-weight:600;
    margin-bottom:0.2rem; font-size:0.82rem; }
.feat-grid { display:flex; flex-wrap:wrap; gap:0.5rem; margin-top:0.5rem; }
.feat-chip { background:#1a1d28; border:1px solid #1e2230; border-radius:8px;
    padding:0.35rem 0.7rem; font-size:0.78rem; color:#8a8fa8; }
.feat-chip span { color:#c8cad8; font-weight:600; margin-left:0.3rem; }
.divider { height:1px; background:#1e2230; margin:1.5rem 0; }
.stSelectbox label, .stRadio label, .stFileUploader label, .stTextInput label {
    color:#8a8fa8 !important; font-size:0.8rem !important; font-weight:500 !important;
    letter-spacing:0.08em !important; text-transform:uppercase !important; }
div[data-baseweb="select"] > div { background:#13161f !important;
    border-color:#1e2230 !important; border-radius:8px !important; color:#e8eaf0 !important; }
div[data-testid="stFileUploader"] { background:#13161f;
    border:1.5px dashed #1e2230; border-radius:12px; padding:0.5rem; }
div[data-baseweb="input"] > div { background:#13161f !important;
    border-color:#1e2230 !important; border-radius:8px !important; }
div[data-baseweb="input"] input { color:#e8eaf0 !important; background:#13161f !important; }
.stButton > button { background:#5b8cf5 !important; color:#fff !important;
    border:none !important; border-radius:8px !important; font-weight:600 !important;
    font-size:0.9rem !important; padding:0.6rem 2rem !important;
    letter-spacing:0.03em !important; width:100%; }
.stButton > button:hover { opacity:0.88 !important; }
.tab-note { font-size:0.78rem; color:#4a4f68; margin-top:0.4rem; }
</style>
""", unsafe_allow_html=True)

# ── Event names ───────────────────────────────────────────────────────────────
EVENT_DISPLAY = {
    "BroadcastJournalism":               "Broadcast Journalism",
    "BusinessEthics":                    "Business Ethics",
    "BusinessPlan":                      "Business Plan",
    "CareerPortfolio":                   "Career Portfolio",
    "CodingandProgramming":              "Coding and Programming",
    "ComputerGameSimulationProgramming": "Computer Game & Simulation Programming",
    "DataAnalysis":                      "Data Analysis",
    "DigitalAnimation":                  "Digital Animation",
    "DigitalVideoProduction":            "Digital Video Production",
    "EventPlanning":                     "Event Planning",
    "FinancialPlanning":                 "Financial Planning",
    "FinancialStatementAnalysis":        "Financial Statement Analysis",
    "FutureBusinessEducator":            "Future Business Educator",
    "FutureBusinessLeader":              "Future Business Leader",
    "GraphicDesign":                     "Graphic Design",
    "ImpromptuSpeaking":                 "Impromptu Speaking",
    "IntroductiontoBusinessPresentation":"Introduction to Business Presentation",
    "IntroductiontoProgramming":         "Introduction to Programming",
    "IntroductiontoPublicSpeaking":      "Introduction to Public Speaking",
    "IntroductiontoSocialMediaStrategy": "Introduction to Social Media Strategy",
    "JobInterview":                      "Job Interview",
    "MobileApplicationDevelopment":      "Mobile Application Development",
    "PublicServiceAnnouncement":         "Public Service Announcement",
    "PublicSpeaking":                    "Public Speaking",
    "SalesPresentation":                 "Sales Presentation",
    "SocialMediaStrategies":             "Social Media Strategies",
    "SupplyChainManagement":             "Supply Chain Management",
    "VisualDesign":                      "Visual Design",
    "WebsiteCodingandDevelopment":       "Website Coding and Development",
    "WebsiteDesign":                     "Website Design",
}
DISPLAY_TO_KEY = {v: k for k, v in EVENT_DISPLAY.items()}

FEEDBACK = {
    "delivery_org":            "Add clear signposting ('First…', 'In conclusion…') to guide judges.",
    "delivery_conf":           "Reduce filler words and practice maintaining steady eye contact.",
    "delivery_qa":             "Anticipate judge questions and rehearse concise, evidence-backed answers.",
    "delivery_pace":           "Target 120–160 wpm. Practice with a timer to find a natural cadence.",
    "delivery_voice":          "Vary pitch and volume deliberately — flat delivery signals nervousness.",
    "content_structure":       "Ensure an explicit intro, logically sequenced body, and clear conclusion.",
    "structure_intro":         "Open with a clear purpose statement in the first 20% of your talk.",
    "structure_conclusion":    "End with a phrase that echoes your opening purpose ('In summary…').",
    "content_recommendations": "Add specific recommendations ('We recommend…') — heavily weighted on most rubrics.",
    "content_topic":           "Use industry terminology throughout to demonstrate topic depth.",
    "content_accuracy":        "Explicitly cite at least 2–3 credible sources by name during the presentation.",
    "slide_design":            "Aim for fewer than 30 words per slide. Replace text blocks with visuals.",
    "protocol":                "Review the event checklist — time limit, materials, and technology restrictions.",
}

# ── Load rubric_heuristics once ───────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_rh():
    base = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        "rubric_heuristics",
        os.path.join(base, "rubric_heuristics.py")
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["rubric_heuristics"] = mod
    spec.loader.exec_module(mod)
    return mod

# ── YouTube helpers ───────────────────────────────────────────────────────────
def is_youtube_url(url: str) -> bool:
    """Return True if the string looks like a YouTube URL."""
    url = url.strip()
    patterns = [
        r"https?://(www\.)?youtube\.com/watch",
        r"https?://youtu\.be/",
        r"https?://(www\.)?youtube\.com/shorts/",
    ]
    return any(re.match(p, url) for p in patterns)

def yt_dlp_available() -> bool:
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def download_youtube_video(url: str, output_path: str) -> str:
    """
    Download a YouTube video to output_path using yt-dlp.
    Returns the actual file path written (yt-dlp may add an extension).
    Raises RuntimeError with a user-friendly message on failure.
    """
    cmd = [
        "yt-dlp",
        "--format", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--output", output_path,
        "--no-playlist",
        "--quiet",
        "--no-warnings",
        url.strip(),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"yt-dlp failed to download the video.\n\n"
            f"Error: {result.stderr.strip() or result.stdout.strip()}\n\n"
            f"Common causes:\n"
            f"• The video is private or age-restricted\n"
            f"• The URL is invalid\n"
            f"• yt-dlp needs updating: run `brew upgrade yt-dlp`"
        )
    # yt-dlp may write e.g. output_path.mp4 — find what was actually written
    if os.path.exists(output_path):
        return output_path
    for ext in [".mp4", ".mkv", ".webm", ".mov", ".avi"]:
        candidate = output_path + ext
        if os.path.exists(candidate):
            return candidate
    raise RuntimeError("yt-dlp reported success but no output file was found.")

# ── HTML helpers ──────────────────────────────────────────────────────────────
def badge(likelihood):
    label = {"high":"HIGH","medium":"MEDIUM","low":"LOW"}.get(likelihood, likelihood.upper())
    return f'<span class="badge badge-{likelihood}">{label}</span>'

def bar_cls(f):
    return "high" if f >= 0.80 else ("medium" if f >= 0.60 else "low")

def crit_bar(label, pts, max_pts, fraction):
    return f"""
<div class="crit-row">
  <div class="crit-header">
    <span class="crit-label">{label}</span>
    <span class="crit-pts">{pts:.1f} / {max_pts}</span>
  </div>
  <div class="bar-track">
    <div class="bar-fill bar-{bar_cls(fraction)}" style="width:{fraction*100:.1f}%"></div>
  </div>
</div>"""

def chip(label, value):
    return f'<div class="feat-chip">{label}<span>{value}</span></div>'

def flag(v):
    return f'<span style="color:{"#4ade80" if v else "#f87171"}">{"✓" if v else "✗"}</span>'

# ── Session state ─────────────────────────────────────────────────────────────
for k in ("result", "features"):
    if k not in st.session_state:
        st.session_state[k] = None

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">ISEF Research Project · FBLA AI Judge</div>
  <h1 class="hero-title">Rubric-Aware <span>Virtual Judge</span></h1>
  <p class="hero-sub">Upload your FBLA presentation video or paste a YouTube URL
  and get rubric-aligned scores, per-criterion feedback, and a placement estimate.</p>
</div>
""", unsafe_allow_html=True)

# ── Input controls ────────────────────────────────────────────────────────────
col_l, col_r = st.columns(2, gap="large")

with col_l:
    st.markdown('<div class="card-label">FBLA Event</div>', unsafe_allow_html=True)
    event_display = st.selectbox(
        "event", sorted(EVENT_DISPLAY.values()),
        index=sorted(EVENT_DISPLAY.values()).index("Introduction to Business Presentation"),
        label_visibility="collapsed",
    )
    event_key = DISPLAY_TO_KEY[event_display]
    st.markdown('<div style="height:0.8rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card-label">Competition Level</div>', unsafe_allow_html=True)
    level = st.radio("level", ["State", "National"],
                     horizontal=True, label_visibility="collapsed").lower()

with col_r:
    st.markdown('<div class="card-label">Presentation Video</div>', unsafe_allow_html=True)
    input_tab, url_tab = st.tabs(["📁  Upload file", "▶️  YouTube URL"])

    with input_tab:
        uploaded = st.file_uploader(
            "video", type=["mp4","mov","mkv","avi","webm"],
            label_visibility="collapsed",
        )
        st.markdown('<p class="tab-note">Your video is processed locally and never stored.</p>',
                    unsafe_allow_html=True)

    with url_tab:
        yt_url = st.text_input(
            "YouTube URL",
            placeholder="https://www.youtube.com/watch?v=...",
            label_visibility="collapsed",
        )
        if yt_url and not is_youtube_url(yt_url):
            st.warning("That doesn't look like a YouTube URL. Paste the full link from your browser.")
        if not yt_dlp_available():
            st.caption("⚠️  yt-dlp not found. Install with: `brew install yt-dlp`")
        else:
            st.markdown('<p class="tab-note">Downloads and processes locally. Video is deleted after analysis.</p>',
                        unsafe_allow_html=True)

st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)
_, btn_col, _ = st.columns([1, 1, 1])
with btn_col:
    analyze = st.button("Analyze Presentation →", use_container_width=True)

# ── Process ───────────────────────────────────────────────────────────────────
if analyze:
    # Determine input source
    using_youtube = yt_url.strip() != "" if yt_url else False
    using_upload  = uploaded is not None

    if not using_upload and not using_youtube:
        st.error("Please upload a video file or paste a YouTube URL.")
    elif using_youtube and not is_youtube_url(yt_url):
        st.error("Please enter a valid YouTube URL (youtube.com/watch or youtu.be/...).")
    elif using_youtube and not yt_dlp_available():
        st.error("yt-dlp is required to download YouTube videos. Install it with: `brew install yt-dlp`")
    else:
        st.session_state.result   = None
        st.session_state.features = None

        base      = os.path.dirname(os.path.abspath(__file__))
        audio_dir = os.path.join(base, "audio")
        os.makedirs(audio_dir, exist_ok=True)
        video_path = None

        p1 = st.empty()
        p2 = st.empty()
        p3 = st.empty()

        try:
            if using_youtube:
                p1.info("⏳  Step 1 / 3 — Downloading YouTube video…")
                tmp_base = tempfile.mktemp(suffix="")   # no extension yet
                video_path = download_youtube_video(yt_url.strip(), tmp_base)
                p1.success("✅  Step 1 / 3 — Video downloaded. Extracting audio…")
            else:
                p1.info("⏳  Step 1 / 3 — Saving video and extracting audio…")
                suffix = os.path.splitext(uploaded.name)[-1] or ".mp4"
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uploaded.read())
                    video_path = tmp.name

            # Import extract_features — loads Whisper on import; use importlib so
            # it picks up the copy in the repo folder on every button press.
            spec = importlib.util.spec_from_file_location(
                "extract_features",
                os.path.join(base, "extract_features.py")
            )
            ef = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(ef)

            audio_path = ef.extract_audio_from_video(video_path, audio_dir)
            p1.success("✅  Step 1 / 3 — Audio extracted.")

            p2.info("⏳  Step 2 / 3 — Transcribing speech (1–3 min)…")
            transcript = ef.transcribe_audio_with_whisper(audio_path)
            p2.success("✅  Step 2 / 3 — Transcription complete.")

            p3.info("⏳  Step 3 / 3 — Computing features and scoring…")
            delivery  = ef.compute_delivery_features(transcript)
            structure = ef.compute_structure_features(transcript)
            avg_words, _ = ef.compute_avg_slide_words_from_video(video_path)

            features = {
                "wpm":                  delivery["wpm"],
                "avg_pause_length":     delivery["avg_pause_length"],
                "long_pauses_per_min":  delivery["long_pauses_per_min"],
                "has_intro":            structure["has_intro"],
                "has_conclusion":       structure["has_conclusion"],
                "has_recommendations":  structure["has_recommendations"],
                "avg_slide_words":      avg_words,
                "analyzed_duration":    delivery["analyzed_duration"],
                "used_word_timestamps": delivery["used_word_timestamps"],
            }

            rh = load_rh()
            score_result = rh.score_presentation(
                event_key,
                {
                    "wpm":                    features["wpm"],
                    "avg_pause_length":       features["avg_pause_length"],
                    "long_pauses_per_minute": features["long_pauses_per_min"],
                    "has_intro":              features["has_intro"],
                    "has_conclusion":         features["has_conclusion"],
                    "has_recommendations":    features["has_recommendations"],
                    "avg_slide_words":        features["avg_slide_words"] if features["avg_slide_words"] > 0 else None,
                    "slides_per_minute":      None,
                },
                competition_level=level,
            )

            st.session_state.features = features
            st.session_state.result   = score_result
            p3.success("✅  Step 3 / 3 — Done! Results below.")

        except Exception as e:
            p1.empty()
            st.error(f"**Failed:** {e}")
            st.code(traceback.format_exc())
            if using_youtube:
                st.info("Make sure yt-dlp is installed and up to date: `brew install yt-dlp` or `brew upgrade yt-dlp`")
            else:
                st.info("Make sure ffmpeg is installed: `brew install ffmpeg`")
        finally:
            if video_path:
                try:
                    os.unlink(video_path)
                except OSError:
                    pass

# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.result is not None:
    r        = st.session_state.result
    features = st.session_state.features
    rh       = load_rh()
    pl       = r["placement_estimate"]
    criteria = r["criterion_scores"]

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="medium")
    score_color = {"high":"#4ade80","medium":"#facc15","low":"#f87171"}.get(
        pl["top3_likelihood"], "#5b8cf5")

    with c1:
        st.markdown(f"""
<div class="card" style="text-align:center">
  <div class="card-label">Overall Score</div>
  <div class="score-ring">
    <span class="big" style="color:{score_color}">{r['normalized_score']:.1f}</span>
    <span class="denom"> / 100</span>
  </div>
  <div style="font-size:0.82rem;color:#8a8fa8;margin-top:0.3rem">
    {r['total_score']:.1f} of {r['total_possible']} rubric points
  </div>
</div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
<div class="card">
  <div class="card-label">Placement Estimate</div>
  <div style="margin:0.6rem 0 0.4rem">
    <div style="font-size:0.78rem;color:#8a8fa8;margin-bottom:0.3rem">Top-3 likelihood</div>
    {badge(pl['top3_likelihood'])}
  </div>
  <div>
    <div style="font-size:0.78rem;color:#8a8fa8;margin-bottom:0.3rem">Top-10 likelihood</div>
    {badge(pl['top10_likelihood'])}
  </div>
  <div style="font-size:0.75rem;color:#4a4f68;margin-top:0.6rem">
    {r['competition_level'].upper()} · {EVENT_DISPLAY.get(r['event'], r['event'])}
  </div>
</div>""", unsafe_allow_html=True)

    with c3:
        dur = features.get("analyzed_duration", 0)
        st.markdown(f"""
<div class="card">
  <div class="card-label">Delivery Snapshot</div>
  <div class="feat-grid">
    {chip("WPM", f"{features['wpm']:.0f}")}
    {chip("Avg pause", f"{features['avg_pause_length']:.2f}s")}
    {chip("Long pauses/min", f"{features['long_pauses_per_min']:.1f}")}
    {chip("Intro", flag(features['has_intro']))}
    {chip("Conclusion", flag(features['has_conclusion']))}
    {chip("Recommendations", flag(features['has_recommendations']))}
    {chip("Duration", f"{dur/60:.1f} min")}
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown(f"""
<div class="card" style="border-color:#1e3050">
  <div class="card-label">Interpretation</div>
  <div style="font-size:0.9rem;color:#c8cad8;line-height:1.6;margin-top:0.3rem">
    {pl['interpretation']}
  </div>
</div>""", unsafe_allow_html=True)

    col_rb, col_imp = st.columns([1.1, 0.9], gap="large")

    with col_rb:
        st.markdown('<div class="card-label" style="margin-bottom:0.8rem">Rubric Criterion Breakdown</div>',
                    unsafe_allow_html=True)
        bars = "".join(
            crit_bar(c["label"], c["points_earned"], c["max_points"], c["fraction"])
            for c in criteria.values()
        )
        st.markdown(bars, unsafe_allow_html=True)

    with col_imp:
        st.markdown('<div class="card-label" style="margin-bottom:0.8rem">Priority Improvements</div>',
                    unsafe_allow_html=True)

        from rubric_heuristics import EVENTS
        html = ""
        shown = 0
        for key, c in sorted(criteria.items(), key=lambda x: x[1]["fraction"]):
            if shown >= 4:
                break
            if c["fraction"] >= 0.92:
                continue
            group = EVENTS[r["event"]]["criteria"][key]["feature_group"]
            tip   = FEEDBACK.get(group, "Review this criterion against the official rubric language.")
            html += f"""
<div class="improve-item">
  <strong>{c['label']} — {c['points_earned']:.1f}/{c['max_points']}</strong>
  {tip}
</div>"""
            shown += 1

        if not html:
            html = '<div class="improve-item"><strong>Excellent across all criteria.</strong> Focus on citation depth and industry terminology.</div>'
        st.markdown(html, unsafe_allow_html=True)

    with st.expander("📋  Key assumptions underlying this report", expanded=False):
        st.markdown("""
<div style="font-size:0.85rem;color:#c8cad8;line-height:1.7">
<b style="color:#f0f2f8">1. Protocol compliance</b><br>
The system assumes the competitor followed all event guidelines — time limit, allowed materials,
technology restrictions, and dress code. These cannot be verified from video alone.
<br><br>
<b style="color:#f0f2f8">2. Q&A effectiveness †</b><br>
Judge Q&A typically occurs after the filmed portion and is not captured in the video.
This criterion is estimated from overall delivery fluency, not directly measured.
<br><br>
<b style="color:#f0f2f8">3. Content accuracy and source citation †</b><br>
The system cannot verify factual claims or detect citations unless the speaker explicitly
names a source out loud. Structural completeness is used as a proxy.
<br><br>
<b style="color:#f0f2f8">4. Topic understanding and content depth †</b><br>
Speaking fluency and structural clarity are used as proxies for subject-matter knowledge.
<br><br>
<b style="color:#f0f2f8">5. Structural flag recall</b><br>
Intro, conclusion, and recommendations are detected from a fixed phrase list. Non-standard
phrasing may not trigger these flags even when the element is clearly present.
<br><br>
<b style="color:#f0f2f8">6. Slide design quality †</b><br>
Average word count per frame is used as a proxy for slide quality. Visual design elements
cannot be assessed from word count alone.
<br><br>
<span style="color:#4a4f68">Criteria marked † are estimated rather than directly measured.
Each assumption is a concrete direction for future work.</span>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
    _, rc, _ = st.columns([2, 1, 2])
    with rc:
        if st.button("Analyze another video", use_container_width=True):
            st.session_state.result   = None
            st.session_state.features = None
            st.rerun()
