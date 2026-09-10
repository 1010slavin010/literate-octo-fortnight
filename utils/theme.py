import streamlit as st

PAGES = [
    ("home", "Home", "🌾"),
    ("ai", "AI Assistant", "🤖"),
    ("sensor", "Sensors", "🌡️"),
    ("alerts", "Alerts", "🚨"),
    ("camera", "Camera", "📷"),
    ("disease", "Disease Scan", "🔬"),
]


def inject_theme():
    st.markdown("""
    <style>
    :root { --bg-0:#0a0812; --bg-1:#120f1e; --panel:#161328; --panel-2:#1c1832; --accent:#8b5cf6; --cyan:#22d3ee; --pink:#f43f8d; --amber:#f5b942; --green:#34d399; }
    .stApp { background: radial-gradient(circle at top right, #20183a 0%, var(--bg-0) 42%, #07060b 100%); color:#f8fafc; }
    [data-testid="stHeader"] { background:transparent; }
    [data-testid="stSidebar"] { background:var(--bg-1); border-right:1px solid rgba(255,255,255,.08); }
    [data-testid="stMetric"] { background:var(--panel); border:1px solid rgba(255,255,255,.08); border-radius:16px; padding:16px; }
    [data-testid="stMetricValue"] { font-weight:700; }
    div[data-testid="stVerticalBlock"] > div:has(> div.stButton) .stButton > button { border-radius:12px; }
    .card-marker { height:3px; width:42px; background:linear-gradient(90deg,var(--accent),var(--cyan)); border-radius:10px; margin-bottom:10px; }
    .chip { display:inline-block; border:1px solid rgba(255,255,255,.12); border-radius:999px; padding:3px 9px; font-size:.75rem; margin-bottom:8px; }
    .chip-green { color:var(--green); border-color:rgba(52,211,153,.3); }
    .chip-cyan { color:var(--cyan); border-color:rgba(34,211,238,.3); }
    .chip-pink { color:var(--pink); border-color:rgba(244,63,141,.3); }
    .chip-amber { color:var(--amber); border-color:rgba(245,185,66,.3); }
    .nav-brand { font-size:1.25rem; font-weight:800; padding:8px 0 14px; }
    </style>
    """, unsafe_allow_html=True)


def topnav(active_key: str):
    st.markdown('<div class="nav-brand">🌾 KisanSense <span style="opacity:.55">· Smart Farm</span></div>', unsafe_allow_html=True)
    cols = st.columns(6)
    for col, (key, label, icon) in zip(cols, PAGES):
        with col:
            if st.button(f"{icon} {label}", key=f"nav_{key}", use_container_width=True, type="primary" if key == active_key else "secondary"):
                page_map = st.session_state.get("_pages", {})
                target = page_map.get(key)
                if target is not None:
                    if isinstance(target, str):
                        st.switch_page(target)
                    else:
                        st.switch_page(target)
