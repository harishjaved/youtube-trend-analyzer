# youtube_trend_analyzer.py
# Run: streamlit run youtube_trend_analyzer.py

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="YT Trend Analyzer",
    page_icon="https://www.youtube.com/favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_KEY = os.getenv("YOUTUBE_API_KEY")  # <-- Replace this

# ─────────────────────────────────────────────
#  GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

/* Reset & Base */
html, body, .stApp {
    font-family: 'DM Sans', sans-serif !important;
    background: #080b10 !important;
    color: #f0f4ff !important;
}

/* Container */
.block-container { padding: 2rem 3rem !important; max-width: 1400px; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0e1219 !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
section[data-testid="stSidebar"] * { color: #8892b0 !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stTextInput label { color: #5a6480 !important; font-family: 'DM Mono', monospace !important; font-size: 0.65rem !important; letter-spacing: 2px !important; text-transform: uppercase !important; }
section[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background: #141922 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #f0f4ff !important;
    border-radius: 10px !important;
}

/* Headings */
h1, h2, h3 { font-family: 'Syne', sans-serif !important; letter-spacing: -0.5px !important; }
h1 { font-size: 2.2rem !important; font-weight: 800 !important; }

/* Inputs */
.stTextInput > div > div > input {
    background: #0e1219 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #f0f4ff !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(255,60,60,0.5) !important;
    box-shadow: 0 0 0 3px rgba(255,60,60,0.08) !important;
}
.stTextInput > div > div > input::placeholder { color: #5a6480 !important; }

/* Buttons */
.stButton > button {
    background: #ff3c3c !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #e02020 !important;
    transform: translateY(-1px) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #0e1219 !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #5a6480 !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 1px !important;
    padding: 8px 16px !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(255,60,60,0.15) !important;
    color: #ff3c3c !important;
}

/* Dataframe */
.stDataFrame { background: #0e1219 !important; border-radius: 14px !important; }

/* Plotly chart backgrounds */
.js-plotly-plot .plotly { background: transparent !important; }

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.viewerBadge_container__1QSob { display: none !important; }

/* Custom cards */
.hero-banner {
    background: linear-gradient(135deg, rgba(255,60,60,0.08) 0%, rgba(0,229,255,0.05) 100%);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 24px;
    padding: 2.5rem 3rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute; top: 0; right: 0;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(255,60,60,0.1) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: -2px;
    background: linear-gradient(to right, #ffffff, #8892b0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}
.hero-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 3px;
    color: #5a6480;
    text-transform: uppercase;
    margin-top: 0.5rem;
}
.hero-accent { color: #ff3c3c; -webkit-text-fill-color: #ff3c3c; }

.kpi-card {
    background: #0e1219;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
}
.kpi-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    border-radius: 3px 0 0 3px;
}
.kpi-red::after   { background: #ff3c3c; }
.kpi-cyan::after  { background: #00e5ff; }
.kpi-gold::after  { background: #ffc847; }
.kpi-green::after { background: #00e676; }
.kpi-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 2px;
    color: #5a6480;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.kpi-value-red  { font-family:'Syne',sans-serif; font-size:1.7rem; font-weight:800; color:#ff3c3c; }
.kpi-value-cyan { font-family:'Syne',sans-serif; font-size:1.7rem; font-weight:800; color:#00e5ff; }
.kpi-value-gold { font-family:'Syne',sans-serif; font-size:1.7rem; font-weight:800; color:#ffc847; }
.kpi-value-green{ font-family:'Syne',sans-serif; font-size:1.7rem; font-weight:800; color:#00e676; }
.kpi-sub { font-size:0.75rem; color:#5a6480; margin-top:3px; }

.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #f0f4ff;
    margin-bottom: 1rem;
}
.mono-tag {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 1.5px;
    padding: 3px 10px;
    border-radius: 20px;
    text-transform: uppercase;
    display: inline-block;
    margin-left: 8px;
    vertical-align: middle;
}
.tag-red  { background:rgba(255,60,60,0.15);  color:#ff3c3c;  border:1px solid rgba(255,60,60,0.2);  }
.tag-cyan { background:rgba(0,229,255,0.1);   color:#00e5ff;  border:1px solid rgba(0,229,255,0.15); }

.video-glass-card {
    background: #0e1219;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    overflow: hidden;
    transition: all 0.3s;
    margin-bottom: 0.5rem;
}
.video-glass-card:hover { border-color: rgba(255,60,60,0.35); }

.top-card {
    background: #0e1219;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 1.5rem;
}
.metric-pill {
    background: #141922;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 0.65rem 0.9rem;
    text-align: center;
}
.pill-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 2px;
    color: #5a6480;
    text-transform: uppercase;
}
.pill-value {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    margin-top: 2px;
}

.results-banner {
    background: rgba(0,229,255,0.05);
    border: 1px solid rgba(0,229,255,0.15);
    border-radius: 10px;
    padding: 0.65rem 1rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: #00e5ff;
    margin-bottom: 1rem;
}

.tier-s { background:rgba(255,200,71,0.15); color:#ffc847; border:1px solid rgba(255,200,71,0.25); border-radius:20px; padding:3px 10px; font-family:'DM Mono',monospace; font-size:0.62rem; }
.tier-a { background:rgba(0,229,255,0.1);   color:#00e5ff; border:1px solid rgba(0,229,255,0.2);  border-radius:20px; padding:3px 10px; font-family:'DM Mono',monospace; font-size:0.62rem; }
.tier-b { background:rgba(255,60,60,0.1);   color:#ff3c3c; border:1px solid rgba(255,60,60,0.2);  border-radius:20px; padding:3px 10px; font-family:'DM Mono',monospace; font-size:0.62rem; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PLOTLY CHART THEME
# ─────────────────────────────────────────────
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Mono", color="#8892b0", size=11),
    margin=dict(t=20, b=20, l=10, r=10),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8892b0", size=10),
    ),
)
ACCENT_COLORS = ["#ff3c3c","#00e5ff","#ffc847","#00e676","#a78bfa","#f472b6","#34d399","#fb923c"]


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def fmt_num(n: int) -> str:
    if n >= 1_000_000_000:
        return f"{n/1e9:.1f}B"
    if n >= 1_000_000:
        return f"{n/1e6:.1f}M"
    if n >= 1_000:
        return f"{n/1e3:.0f}K"
    return str(n)


def engagement_rate(likes: int, views: int) -> float:
    return round((likes / max(1, views)) * 100, 2)


def tier(rate: float) -> str:
    if rate > 4:   return "S-TIER"
    if rate > 2.5: return "A-TIER"
    return "B-TIER"


def tier_html(rate: float) -> str:
    t = tier(rate)
    cls = {"S-TIER": "tier-s", "A-TIER": "tier-a", "B-TIER": "tier-b"}[t]
    return f'<span class="{cls}">{t}</span>'


# ─────────────────────────────────────────────
#  API — CATEGORY FETCH
# ─────────────────────────────────────────────
CLUTTER_WORDS = ["bhojpuri","arkestra","nirahua","maithili","shadi","khesari","pawan"]

CATEGORY_MAP = {
    "Trending":   {"id": "0",  "label": "TRENDING"},
    "Travel":     {"id": "19", "label": "TRAVEL"},
    "Education":  {"id": "27", "label": "EDUCATION"},
    "Technology": {"id": "28", "label": "TECHNOLOGY"},
    "Gaming":     {"id": "20", "label": "GAMING"},
}

SEARCH_QUERY_MAP = {
    "27": "educational documentary science explained full course",
    "19": "travel guide 4k best places to visit world tour",
}


@st.cache_data(ttl=600, show_spinner=False)
def fetch_category(cat_id: str) -> pd.DataFrame:
    """Fetch trending videos for a given category ID."""
    if cat_id in SEARCH_QUERY_MAP:
        q = SEARCH_QUERY_MAP[cat_id]
        url = (
            f"https://www.googleapis.com/youtube/v3/search"
            f"?part=snippet&q={requests.utils.quote(q)}&type=video"
            f"&maxResults=25&regionCode=IN&relevanceLanguage=en&key={API_KEY}"
        )
    else:
        url = (
            f"https://www.googleapis.com/youtube/v3/videos"
            f"?part=snippet,statistics,contentDetails"
            f"&chart=mostPopular&regionCode=IN&maxResults=25"
            f"&videoCategoryId={cat_id}&key={API_KEY}"
        )
    try:
        res = requests.get(url, timeout=8).json()
    except Exception:
        return pd.DataFrame()

    items = res.get("items", [])
    rows = []
    for item in items:
        snippet = item.get("snippet", {})
        v_id = item["id"] if isinstance(item["id"], str) else item["id"].get("videoId", "")
        stats = item.get("statistics", {})
        title = snippet.get("title", "")

        if any(w in title.lower() for w in CLUTTER_WORDS):
            continue

        rows.append({
            "id":       v_id,
            "title":    title,
            "channel":  snippet.get("channelTitle", ""),
            "views":    int(stats.get("viewCount",   0)),
            "likes":    int(stats.get("likeCount",   0)),
            "comments": int(stats.get("commentCount",0)),
            "thumb":    snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
        })
    df = pd.DataFrame(rows)
    if not df.empty:
        df["engagement"] = df.apply(lambda r: engagement_rate(r["likes"], r["views"]), axis=1)
        df["tier"]       = df["engagement"].apply(tier)
    return df


# ─────────────────────────────────────────────
#  API — SEARCH FETCH
# ─────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def fetch_search(query: str, sort_by: str = "relevance") -> pd.DataFrame:
    """Search YouTube for a keyword and return enriched results."""
    order_map = {
        "Relevance":   "relevance",
        "View Count":  "viewCount",
        "Rating":      "rating",
        "Date":        "date",
    }
    order = order_map.get(sort_by, "relevance")

    search_url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?part=snippet&q={requests.utils.quote(query)}&type=video"
        f"&maxResults=25&order={order}&regionCode=IN&relevanceLanguage=en"
        f"&key={API_KEY}"
    )
    try:
        search_res = requests.get(search_url, timeout=8).json()
    except Exception:
        return pd.DataFrame()

    items = search_res.get("items", [])
    if not items:
        return pd.DataFrame()

    # Batch-fetch statistics for all video IDs
    video_ids = ",".join(
        item["id"].get("videoId", "") for item in items
        if isinstance(item["id"], dict)
    )
    stats_map = {}
    if video_ids:
        try:
            stats_res = requests.get(
                f"https://www.googleapis.com/youtube/v3/videos"
                f"?part=statistics&id={video_ids}&key={API_KEY}",
                timeout=8,
            ).json()
            for v in stats_res.get("items", []):
                stats_map[v["id"]] = v.get("statistics", {})
        except Exception:
            pass

    rows = []
    for item in items:
        snippet = item.get("snippet", {})
        v_id = item["id"].get("videoId", "") if isinstance(item["id"], dict) else ""
        if not v_id:
            continue
        title = snippet.get("title", "")
        if any(w in title.lower() for w in CLUTTER_WORDS):
            continue
        s = stats_map.get(v_id, {})
        rows.append({
            "id":       v_id,
            "title":    title,
            "channel":  snippet.get("channelTitle", ""),
            "views":    int(s.get("viewCount",    0)),
            "likes":    int(s.get("likeCount",    0)),
            "comments": int(s.get("commentCount", 0)),
            "thumb":    snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
        })

    df = pd.DataFrame(rows)
    if not df.empty:
        df["engagement"] = df.apply(lambda r: engagement_rate(r["likes"], r["views"]), axis=1)
        df["tier"]       = df["engagement"].apply(tier)
    return df


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:1.5rem;">
        <div style="width:36px;height:36px;background:#ff3c3c;border-radius:9px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="white">
                <path d="M23 7s-.3-2-1.2-2.8c-1.1-1.2-2.4-1.2-3-1.3C16.1 2.8 12 2.8 12 2.8s-4.1 0-6.8.2c-.6.1-1.9.1-3 1.3C1.3 5 1 7 1 7S.7 9.1.7 11.3v2c0 2.1.3 4.2.3 4.2s.3 2 1.2 2.8c1.1 1.2 2.6 1.1 3.3 1.2C7.3 21.7 12 21.7 12 21.7s4.1 0 6.8-.3c.6-.1 1.9-.1 3-1.3.9-.8 1.2-2.8 1.2-2.8s.3-2.1.3-4.2v-2C23.3 9.1 23 7 23 7zm-13.5 8.5v-7l6.5 3.5-6.5 3.5z"/>
            </svg>
        </div>
        <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:0.95rem;line-height:1.15;color:#f0f4ff;">
            YT Trend<br><span style="color:#ff3c3c;">Analyzer</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-family:DM Mono,monospace;font-size:0.62rem;letter-spacing:2px;color:#5a6480;text-transform:uppercase;margin-bottom:0.4rem;">Category</div>', unsafe_allow_html=True)
    selected_cat = st.selectbox(
        "Category", list(CATEGORY_MAP.keys()), label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:DM Mono,monospace;font-size:0.62rem;letter-spacing:2px;color:#5a6480;text-transform:uppercase;margin-bottom:0.4rem;">Search Sort</div>', unsafe_allow_html=True)
    sort_order = st.selectbox(
        "Sort", ["Relevance","View Count","Rating","Date"], label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    max_results_show = st.slider("Videos in grid", min_value=4, max_value=25, value=8, step=4)

    st.markdown("""
    <br>
    <div style="background:#141922;border:1px solid rgba(255,255,255,0.05);border-radius:12px;padding:1rem;">
        <div style="font-family:'DM Mono',monospace;font-size:0.62rem;letter-spacing:2px;color:#5a6480;text-transform:uppercase;margin-bottom:0.5rem;">Data Source</div>
        <div style="font-size:0.78rem;color:#5a6480;line-height:1.7;">
            YouTube Data API v3<br>
            Region: IN<br>
            Auto-refresh: 10 min
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:1.5rem;background:rgba(0,230,118,0.05);border:1px solid rgba(0,230,118,0.15);border-radius:10px;padding:0.75rem 1rem;font-size:0.78rem;color:#00e676;font-family:'DM Mono',monospace;">
        <span style="display:inline-block;width:7px;height:7px;background:#00e676;border-radius:50%;margin-right:6px;animation:pulse 1.5s infinite;"></span>
        API Connected
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HERO BANNER
# ─────────────────────────────────────────────
cat_meta = CATEGORY_MAP[selected_cat]
st.markdown(f"""
<div class="hero-banner">
    <p class="hero-sub">YouTube Data Intelligence</p>
    <h1 class="hero-title">YT <span class="hero-accent">Trend</span> Analyzer</h1>
    <p style="font-family:'DM Mono',monospace;font-size:0.72rem;letter-spacing:2px;color:#5a6480;margin-top:0.75rem;">
        DECODING {cat_meta['label']} PERFORMANCE &bull; {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC
    </p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SEARCH BAR (TOP)
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">Search <span class="mono-tag tag-cyan">Custom Query</span></div>', unsafe_allow_html=True)

search_col1, search_col2, search_col3 = st.columns([4, 1, 1])
with search_col1:
    search_query = st.text_input(
        "Search", placeholder="Search videos, channels, topics...",
        label_visibility="collapsed", key="search_input"
    )
with search_col2:
    search_btn = st.button("Analyze", use_container_width=True)
with search_col3:
    clear_btn = st.button("Clear", use_container_width=True)

# State management for search
if "active_query" not in st.session_state:
    st.session_state.active_query = ""

if search_btn and search_query.strip():
    st.session_state.active_query = search_query.strip()
if clear_btn:
    st.session_state.active_query = ""

# Decide which dataset to use
is_search_mode = bool(st.session_state.active_query)

if is_search_mode:
    with st.spinner(f"Searching for '{st.session_state.active_query}'..."):
        df = fetch_search(st.session_state.active_query, sort_order)
    if df.empty:
        st.warning("No results found. Check your API key or try a different query.")
        st.stop()
    st.markdown(f"""
    <div class="results-banner">
        Showing {len(df)} results for &quot;{st.session_state.active_query}&quot;
        &bull; Sorted by: {sort_order}
    </div>
    """, unsafe_allow_html=True)
else:
    with st.spinner("Loading trending data..."):
        df = fetch_category(cat_meta["id"])
    if df.empty:
        st.warning("Could not fetch data. Check your YouTube API key.")
        st.stop()

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  KPI STRIP
# ─────────────────────────────────────────────
top = df.iloc[0]
total_views = df["views"].sum()
avg_engagement = df["engagement"].mean()
top_channel = df.groupby("channel")["views"].sum().idxmax()
s_tier_count = (df["tier"] == "S-TIER").sum()

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""
    <div class="kpi-card kpi-red">
        <div class="kpi-label">Total Views</div>
        <div class="kpi-value-red">{fmt_num(total_views)}</div>
        <div class="kpi-sub">Across {len(df)} videos</div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card kpi-cyan">
        <div class="kpi-label">Avg Engagement</div>
        <div class="kpi-value-cyan">{avg_engagement:.2f}%</div>
        <div class="kpi-sub">Likes-to-views ratio</div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card kpi-gold">
        <div class="kpi-label">Top Channel</div>
        <div class="kpi-value-gold" style="font-size:1.1rem;">{top_channel[:18]}</div>
        <div class="kpi-sub">By total views</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card kpi-green">
        <div class="kpi-label">S-Tier Videos</div>
        <div class="kpi-value-green">{s_tier_count}</div>
        <div class="kpi-sub">Engagement rate &gt; 4%</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["TOP PERFORMER", "ANALYTICS", "CONTENT FEED", "LEADERBOARD"])


# ── TAB 1: TOP PERFORMER ─────────────────────
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    vid_col, info_col = st.columns([1.5, 1], gap="large")

    with vid_col:
        st.video(f"https://www.youtube.com/watch?v={top['id']}")

    with info_col:
        er = engagement_rate(top["likes"], top["views"])
        st.markdown(f"""
        <div class="top-card">
            <div style="font-family:'DM Mono',monospace;font-size:0.62rem;letter-spacing:2px;color:#ff3c3c;text-transform:uppercase;margin-bottom:8px;">
                No.1 Performer
            </div>
            <div style="font-family:'Syne',sans-serif;font-size:1.15rem;font-weight:700;line-height:1.3;margin-bottom:6px;">
                {top["title"][:80]}{"..." if len(top["title"])>80 else ""}
            </div>
            <div style="font-size:0.8rem;color:#5a6480;margin-bottom:1.25rem;">
                {top["channel"]}
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:1rem;">
                <div class="metric-pill">
                    <div class="pill-label">Views</div>
                    <div class="pill-value" style="color:#ff3c3c;">{fmt_num(top["views"])}</div>
                </div>
                <div class="metric-pill">
                    <div class="pill-label">Likes</div>
                    <div class="pill-value" style="color:#00e5ff;">{fmt_num(top["likes"])}</div>
                </div>
                <div class="metric-pill">
                    <div class="pill-label">Comments</div>
                    <div class="pill-value" style="color:#ffc847;">{fmt_num(top["comments"])}</div>
                </div>
                <div class="metric-pill">
                    <div class="pill-label">Engagement</div>
                    <div class="pill-value" style="color:#00e676;">{er}%</div>
                </div>
            </div>
            <div style="margin-bottom:1rem;">
                <div style="display:flex;justify-content:space-between;font-size:0.72rem;color:#5a6480;margin-bottom:4px;">
                    <span>Engagement Rate</span><span>{er}%</span>
                </div>
                <div style="height:4px;background:rgba(255,255,255,0.06);border-radius:2px;">
                    <div style="height:100%;width:{min(100,er*10)}%;background:#00e5ff;border-radius:2px;"></div>
                </div>
            </div>
            <div style="text-align:center;margin-top:0.5rem;">
                {tier_html(er)}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.link_button(
            "Open on YouTube",
            f"https://www.youtube.com/watch?v={top['id']}",
            use_container_width=True,
        )


# ── TAB 2: ANALYTICS ─────────────────────────
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    chart_col1, chart_col2 = st.columns([1.4, 1], gap="large")

    with chart_col1:
        st.markdown('<div class="section-title">Views Distribution <span class="mono-tag tag-cyan">Bar</span></div>', unsafe_allow_html=True)
        top_n = df.nlargest(10, "views")
        fig_bar = px.bar(
            top_n,
            x="views", y="title",
            orientation="h",
            color="engagement",
            color_continuous_scale=["#ff3c3c","#ffc847","#00e5ff"],
            labels={"views":"Views","title":"","engagement":"Eng %"},
        )
        fig_bar.update_traces(
            hovertemplate="<b>%{y}</b><br>Views: %{x:,.0f}<extra></extra>",
        )
        fig_bar.update_layout(
            **CHART_LAYOUT,
            height=380,
            coloraxis_showscale=False,
            yaxis=dict(categoryorder="total ascending", tickfont=dict(size=10, color="#8892b0")),
            xaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(size=10, color="#8892b0")),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with chart_col2:
        st.markdown('<div class="section-title">Engagement Mix <span class="mono-tag tag-red">Donut</span></div>', unsafe_allow_html=True)
        top5 = df.nlargest(5, "views")
        fig_pie = px.pie(
            top5, values="views", names="channel",
            hole=0.62,
            color_discrete_sequence=ACCENT_COLORS,
        )
        fig_pie.update_traces(
            textfont=dict(color="#8892b0", size=10),
            hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>",
        )
        fig_pie.update_layout(**CHART_LAYOUT, height=380)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Scatter — Views vs Engagement
    st.markdown('<div class="section-title">Views vs Engagement <span class="mono-tag tag-cyan">Scatter</span></div>', unsafe_allow_html=True)
    fig_scatter = px.scatter(
        df, x="views", y="engagement",
        size="comments", color="tier",
        hover_name="title",
        color_discrete_map={"S-TIER":"#ffc847","A-TIER":"#00e5ff","B-TIER":"#ff3c3c"},
        labels={"views":"Views","engagement":"Engagement Rate (%)","tier":"Tier"},
    )
    fig_scatter.update_layout(
        **CHART_LAYOUT,
        height=320,
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(size=10)),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(size=10)),
    )
    st.plotly_chart(fig_scatter, use_container_width=True)


# ── TAB 3: CONTENT FEED ──────────────────────
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    grid_df = df.iloc[1:max_results_show + 1]   # skip top performer shown in tab 1

    for row_start in range(0, len(grid_df), 4):
        cols = st.columns(4, gap="small")
        batch = grid_df.iloc[row_start:row_start + 4]
        for col, (_, vid) in zip(cols, batch.iterrows()):
            with col:
                er = engagement_rate(vid["likes"], vid["views"])
                accent = ACCENT_COLORS[int(vid.name) % len(ACCENT_COLORS)]
                st.markdown(f"""
                <div class="video-glass-card">
                    <img src="{vid['thumb']}" style="width:100%;display:block;aspect-ratio:16/9;object-fit:cover;" />
                    <div style="padding:0.85rem;">
                        <div style="font-size:0.82rem;font-weight:600;line-height:1.4;height:2.3em;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;">
                            {vid["title"]}
                        </div>
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:0.55rem;">
                            <span style="font-family:'DM Mono',monospace;font-size:0.68rem;color:#ff3c3c;font-weight:500;">{fmt_num(vid["views"])} views</span>
                            <span style="font-size:0.68rem;color:#5a6480;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:80px;">{vid["channel"][:15]}</span>
                        </div>
                        <div style="height:2px;border-radius:1px;margin-top:0.45rem;background:linear-gradient(90deg,{accent} {min(100,er*15)}%,rgba(255,255,255,0.04) 0%);"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)


# ── TAB 4: LEADERBOARD ───────────────────────
with tab4:
    st.markdown("<br>", unsafe_allow_html=True)

    # Channel aggregation
    channel_agg = (
        df.groupby("channel")
        .agg(videos=("id","count"), total_views=("views","sum"),
             total_likes=("likes","sum"), avg_engagement=("engagement","mean"))
        .reset_index()
        .sort_values("total_views", ascending=False)
        .reset_index(drop=True)
    )
    channel_agg["tier"] = channel_agg["avg_engagement"].apply(tier)
    channel_agg["rank"] = channel_agg.index + 1

    # Header
    hcols = st.columns([0.5, 3, 1.5, 1.5, 1.5, 1])
    for col, txt in zip(hcols, ["#","Channel","Total Views","Total Likes","Avg Eng.","Tier"]):
        col.markdown(f'<div style="font-family:DM Mono,monospace;font-size:0.62rem;letter-spacing:2px;color:#5a6480;text-transform:uppercase;padding:0.5rem 0;">{txt}</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.06);margin-bottom:0.5rem;"></div>', unsafe_allow_html=True)

    for _, row in channel_agg.head(10).iterrows():
        rank_color = "#ffc847" if row["rank"] <= 3 else "#5a6480"
        rc = st.columns([0.5, 3, 1.5, 1.5, 1.5, 1])
        rc[0].markdown(f'<div style="font-family:DM Mono,monospace;font-size:0.78rem;color:{rank_color};font-weight:700;padding:0.6rem 0;">#{int(row["rank"])}</div>', unsafe_allow_html=True)
        rc[1].markdown(f'<div style="font-size:0.88rem;font-weight:500;padding:0.6rem 0;">{row["channel"]}</div>', unsafe_allow_html=True)
        rc[2].markdown(f'<div style="font-family:DM Mono,monospace;font-size:0.78rem;color:#8892b0;padding:0.6rem 0;">{fmt_num(int(row["total_views"]))}</div>', unsafe_allow_html=True)
        rc[3].markdown(f'<div style="font-family:DM Mono,monospace;font-size:0.78rem;color:#8892b0;padding:0.6rem 0;">{fmt_num(int(row["total_likes"]))}</div>', unsafe_allow_html=True)
        rc[4].markdown(f'<div style="font-family:DM Mono,monospace;font-size:0.78rem;color:#8892b0;padding:0.6rem 0;">{row["avg_engagement"]:.2f}%</div>', unsafe_allow_html=True)
        rc[5].markdown(f'<div style="padding:0.6rem 0;">{tier_html(row["avg_engagement"])}</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:1px;background:rgba(255,255,255,0.04);"></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Raw data expander
    with st.expander("Raw Data Table"):
        display_df = df[["title","channel","views","likes","comments","engagement","tier"]].copy()
        display_df.columns = ["Title","Channel","Views","Likes","Comments","Eng. %","Tier"]
        st.dataframe(
            display_df.style.background_gradient(subset=["Views","Eng. %"], cmap="Reds"),
            use_container_width=True,
            height=400,
        )
