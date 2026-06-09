#Imports
import os
import sys
import tempfile
import importlib.util
import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FBLA AI Judge",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #0d0f14; color: #e8eaf0; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 4rem; }

.hero { text-align: center; padding: 3rem 1rem 2rem; }
.hero-eyebrow { font-family: 'Space Grotesk', sans-serif; font-size: 0.72rem; font-weight: 600;
    letter-spacing: 0.18em; text-transform: uppercase; color: #5b8cf5; margin-bottom: 0.75rem; }
.hero-title { font-family: 'Space Grotesk', sans-serif; font-size: clamp(2rem,5vw,3.2rem);
    font-weight: 700; color: #f0f2f8; line-height: 1.1; margin: 0 0 0.6rem; }
.hero-title span { color: #5b8cf5; }
.hero-sub { font-size: 1rem; color: #8a8fa8; max-width: 540px; margin: 0 auto; line-height: 1.6; }

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
.badge-high   { background: #1a3a2a; color: #4ade80; border: 1px solid #166534; }
.badge-medium { background: #2d2a14; color: #facc15; border: 1px solid #713f12; }
.badge-low    { background: #2a1a1a; color: #f87171; border: 1px solid #7f1d1d; }

.crit-row { margin-bottom: 0.85rem; }
.crit-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.25rem; }
.crit-label { font-size: 0.82rem; color: #c8cad8; }
.crit-pts { font-size: 0.78rem; font-weight: 600; color: #8a8fa8; white-space: nowrap; }
.bar-track { height: 7px; background: #1e2230; border-radius: 999px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 999px; }
.bar-high   { background: linear-gradient(90deg,#3b82f6,#6366f1); }
.bar-medium { background: linear-gradient(90deg,#f59e0b,#fb923c); }
.bar-low    { background: linear-gradient(90deg,#ef4444,#f97316); }

.improve-item { background: #13161f; border-left: 3px solid #5b8cf5; border-radius: 0 8px 8px 0;
    padding: 0.75rem 1rem; margin-bottom: 0.6rem; font-size: 0.85rem; color: #c8cad8; line-height: 1.5; }
.improve-item strong { display: block; color: #f0f2f8; font-weight: 600;
    margin-bottom: 0.2rem; font-size: 0.82rem; }

.feat-grid { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem; }
.feat-chip { background: #1a1d28; border: 1px solid #1e2230; border-radius: 8px;
    padding: 0.35rem 0.7rem; font-size: 0.78rem; color: #8a8fa8; }
.feat-chip span { color: #c8cad8; font-weight: 600; margin-left: 0.3rem; }

.divider { height: 1px; background: #1e2230; margin: 1.5rem 0; }

.stSelectbox label, .stRadio label, .stFileUploader label {
    color: #8a8fa8 !important; font-size: 0.8rem !important; font-weight: 500 !important;
    letter-spacing: 0.08em !important; text-transform: uppercase !important; }
div[data-baseweb="select"] > div { background: #13161f !important;
    border-color: #1e2230 !important; border-radius: 8px !important; color: #e8eaf0 !important; }
div[data-testid="stFileUploader"] { background: #13161f;
    border: 1.5px dashed #1e2230; border-radius: 12px; padding: 0.5rem; }
.stButton > button { background: #5b8cf5 !important; color: #fff !important;
    border: none !important; border-radius: 8px !important; font-weight: 600 !important;
    font-size: 0.9rem !important; padding: 0.6rem 2rem !important;
    letter-spacing: 0.03em !important; width: 100%; }
.stButton > button:hover { opacity: 0.88 !important; }
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

# ── Load rubric_heuristics once ───────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_rubric_module():
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "rubric_heuristics.py")
    spec = importlib.util.spec_from_file_location("rubric_heuristics", path)
    mod  = importlib.util.module_from_spec(spec)
    sys.modules["rubric_heuristics"] = mod
    spec.loader.exec_module(mod)
    return mod

# ── Load Whisper once ─────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_whisper_model():
    import whisper
    return whisper.load_model("base")

# ── Pipeline helpers (called directly, not via process_single_video) ──────────
def run_pipeline(video_bytes: bytes, filename: str, event_key: str, level: str):
    """
    Full pipeline:
      1. Write bytes to temp file
      2. Extract audio with MoviePy
      3. Transcribe with Whisper
      4. Compute features
      5. Score with rubric_heuristics
    Returns (features_dict, score_result) or raises.
    """
    import whisper
    from moviepy import VideoFileClip
    import importlib.util as ilu, sys as _sys

    # Load extract_features module
    base = os.path.dirname(os.path.abspath(__file__))
    ef_path = os.path.join(base, "extract_features.py")
    spec = ilu.spec_from_file_location("extract_features_app", ef_path)
    ef = ilu.module_from_spec(spec)
    # Inject cached whisper model before exec so module-level load_model is skipped
    import types
    mock_whisper = types.ModuleType("whisper")
    mock_whisper.load_model = lambda *a, **kw: get_whisper_model()
    _sys.modules["whisper"] = mock_whisper
    spec.loader.exec_module(ef)
    # Patch the module-level whisper_model to use our cached one
    ef.whisper_model = get_whisper_model()

    suffix = os.path.splitext(filename)[-1] or ".mp4"
    audio_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
    os.makedirs(audio_dir, exist_ok=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(video_bytes)
        video_path = tmp.name

    try:
        # Extract audio
        audio_path = ef.extract_audio_from_video(video_path, audio_dir)

        # Transcribe
        transcript = ef.transcribe_audio_with_whisper(audio_path)

        # Compute features
        delivery  = ef.compute_delivery_features(transcript)
        structure = ef.compute_structure_features(transcript)
        avg_slide_words, slides_used = ef.compute_avg_slide_words(
            os.path.splitext(os.path.basename(video_path))[0]
        )

        features = {
            "wpm":                    delivery["wpm"],
            "avg_pause_length":       delivery["avg_pause_length"],
            "long_pauses_per_min":    delivery["long_pauses_per_min"],
            "has_intro":              structure["has_intro"],
            "has_conclusion":         structure["has_conclusion"],
            "has_recommendations":    structure["has_recommendations"],
            "avg_slide_words":        avg_slide_words,
            "analyzed_duration":      delivery["analyzed_duration"],
            "used_word_timestamps":   delivery["used_word_timestamps"],
        }

        # Score
        rh = get_rubric_module()
        feature_dict = {
            "wpm":                    features["wpm"],
            "avg_pause_length":       features["avg_pause_length"],
            "long_pauses_per_minute": features["long_pauses_per_min"],
            "has_intro":              features["has_intro"],
            "has_conclusion":         features["has_conclusion"],
            "has_recommendations":    features["has_recommendations"],
            "avg_slide_words":        features["avg_slide_words"] if features["avg_slide_words"] > 0 else None,
            "slides_per_minute":      None,
        }
        score_result = rh.score_presentation(event_key, feature_dict, competition_level=level)
        return features, score_result

    finally:
        try:
            os.unlink(video_path)
        except OSError:
            pass

# ── HTML helpers ──────────────────────────────────────────────────────────────
def badge_html(likelihood):
    cls = f"badge-{likelihood}"
    label = {"high": "HIGH", "medium": "MEDIUM", "low": "LOW"}.get(likelihood, likelihood.upper())
    return f'<span class="badge {cls}">{label}</span>'

def bar_class(fraction):
    if fraction >= 0.80: return "high"
    if fraction >= 0.60: return "medium"
    return "low"

def criterion_bar(label, pts, max_pts, fraction):
    pct = f"{fraction*100:.1f}%"
    cls = bar_class(fraction)
    return f"""
<div class="crit-row">
  <div class="crit-header">
    <span class="crit-label">{label}</span>
    <span class="crit-pts">{pts:.1f} / {max_pts}</span>
  </div>
  <div class="bar-track"><div class="bar-fill bar-{cls}" style="width:{pct}"></div></div>
</div>"""

def chip(label, value):
    return f'<div class="feat-chip">{label}<span>{value}</span></div>'

# ── Session state init ────────────────────────────────────────────────────────
for key in ("result", "features", "error"):
    if key not in st.session_state:
        st.session_state[key] = None

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">ISEF Research Project · FBLA AI Judge</div>
  <h1 class="hero-title">Rubric-Aware <span>Virtual Judge</span></h1>
  <p class="hero-sub">Upload your FBLA presentation video and get rubric-aligned scores,
     per-criterion feedback, and a placement estimate — instantly.</p>
</div>
""", unsafe_allow_html=True)

# ── Input form ────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="card-label">FBLA Event</div>', unsafe_allow_html=True)
    event_display = st.selectbox(
        "FBLA Event",
        options=sorted(EVENT_DISPLAY.values()),
        index=sorted(EVENT_DISPLAY.values()).index("Introduction to Business Presentation"),
        label_visibility="collapsed",
    )
    event_key = DISPLAY_TO_KEY[event_display]
    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card-label">Competition Level</div>', unsafe_allow_html=True)
    level = st.radio(
        "Competition Level",
        options=["State", "National"],
        horizontal=True,
        label_visibility="collapsed",
    ).lower()

with col_right:
    st.markdown('<div class="card-label">Presentation Video</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Upload video",
        type=["mp4", "mov", "mkv", "avi", "webm"],
        label_visibility="collapsed",
    )

st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)
_, btn_col, _ = st.columns([1, 1, 1])
with btn_col:
    run_pressed = st.button("Analyze Presentation →", use_container_width=True)

# ── Run pipeline on button press ──────────────────────────────────────────────
if run_pressed:
    if uploaded is None:
        st.error("Please upload a video file first.")
    else:
        st.session_state.result   = None
        st.session_state.features = None
        st.session_state.error    = None

        with st.spinner("Extracting audio and transcribing… (1–3 min)"):
            try:
                video_bytes = uploaded.read()
                features, score_result = run_pipeline(video_bytes, uploaded.name, event_key, level)
                st.session_state.features = features
                st.session_state.result   = score_result
            except Exception as e:
                st.session_state.error = str(e)

# ── Show error if any ─────────────────────────────────────────────────────────
if st.session_state.error:
    st.error(f"**Processing failed:** {st.session_state.error}")
    st.info("Make sure `ffmpeg` is installed: `brew install ffmpeg`")

# ── Results dashboard ─────────────────────────────────────────────────────────
if st.session_state.result is not None:
    r        = st.session_state.result
    features = st.session_state.features
    rh       = get_rubric_module()

    placement = r["placement_estimate"]
    criteria  = r["criterion_scores"]

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### Results")

    # ── Top 3 cards ───────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3, gap="medium")

    color_map = {"high": "#4ade80", "medium": "#facc15", "low": "#f87171"}
    score_col = color_map.get(placement["top3_likelihood"], "#5b8cf5")

    with c1:
        st.markdown(f"""
<div class="card" style="text-align:center">
  <div class="card-label">Overall Score</div>
  <div class="score-ring">
    <span class="big" style="color:{score_col}">{r['normalized_score']:.1f}</span>
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
    {badge_html(placement['top3_likelihood'])}
  </div>
  <div>
    <div style="font-size:0.78rem;color:#8a8fa8;margin-bottom:0.3rem">Top-10 likelihood</div>
    {badge_html(placement['top10_likelihood'])}
  </div>
  <div style="font-size:0.75rem;color:#4a4f68;margin-top:0.6rem">
    {r['competition_level'].upper()} · {EVENT_DISPLAY.get(r['event'], r['event'])}
  </div>
</div>""", unsafe_allow_html=True)

    with c3:
        flag = lambda v: f'<span style="color:{"#4ade80" if v else "#f87171"}">{"✓" if v else "✗"}</span>'
        dur  = features.get("analyzed_duration", 0)
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

    # ── Interpretation ────────────────────────────────────────────────────────
    st.markdown(f"""
<div class="card" style="border-color:#1e3050">
  <div class="card-label">Interpretation</div>
  <div style="font-size:0.9rem;color:#c8cad8;line-height:1.6;margin-top:0.3rem">
    {placement['interpretation']}
  </div>
</div>""", unsafe_allow_html=True)

    # ── Rubric breakdown + improvements ───────────────────────────────────────
    col_rubric, col_improve = st.columns([1.1, 0.9], gap="large")

    with col_rubric:
        st.markdown('<div class="card-label" style="margin-bottom:0.8rem">Rubric Criterion Breakdown</div>', unsafe_allow_html=True)
        bars = ""
        for key, crit in criteria.items():
            bars += criterion_bar(crit["label"], crit["points_earned"], crit["max_points"], crit["fraction"])
        st.markdown(bars, unsafe_allow_html=True)

    with col_improve:
        st.markdown('<div class="card-label" style="margin-bottom:0.8rem">Priority Improvements</div>', unsafe_allow_html=True)

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

        from rubric_heuristics import EVENTS  # noqa
        sorted_crits = sorted(criteria.items(), key=lambda x: x[1]["fraction"])
        html = ""
        shown = 0
        for key, crit in sorted_crits:
            if shown >= 4:
                break
            if crit["fraction"] >= 0.92:
                continue
            group = EVENTS[r["event"]]["criteria"][key]["feature_group"]
            tip   = FEEDBACK.get(group, "Review this criterion against the official rubric language.")
            html += f"""
<div class="improve-item">
  <strong>{crit['label']} — {crit['points_earned']:.1f}/{crit['max_points']}</strong>
  {tip}
</div>"""
            shown += 1

        if not html:
            html = '<div class="improve-item"><strong>Excellent across all criteria.</strong> Keep refining content depth and citations.</div>'

        st.markdown(html, unsafe_allow_html=True)

    # ── Reset ─────────────────────────────────────────────────────────────────
    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
    _, reset_col, _ = st.columns([2, 1, 2])
    with reset_col:
        if st.button("Analyze another video", use_container_width=True):
            st.session_state.result   = None
            st.session_state.features = None
            st.session_state.error    = None
            st.rerun()
