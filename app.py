import streamlit as st
import pandas as pd
import numpy as np
import re
import streamlit.components.v1 as components

# CONFIGURATION
st.set_page_config(
    page_title="ScentSational AI",
    page_icon="💎",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ANALYTICS
def inject_ga4():
    GA_ID = "G-28PVV48GN5"
    components.html(f"""<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer = window.dataLayer || [];function gtag(){{dataLayer.push(arguments);}}gtag('js', new Date());gtag('config', '{GA_ID}');</script>""", height=0, width=0)
inject_ga4()

# LOAD DATA
@st.cache_data
def load_data():
    try:
        # TUTAJ JEST ZMIANA NA TWOJĄ NAZWĘ PLIKU:
        df = pd.read_csv("finale_perfume.csv")
        cosine_sim = np.load("hybrid_similarity.npy")
        
        # Usuwamy numery z nazw
        df['Name'] = df['Name'].astype(str).str.replace(r'^\d+[\.\s]*', '', regex=True)
        return df, cosine_sim
    except FileNotFoundError:
        return None, None

# HELPERS
def get_initials(name):
    clean = re.sub(r"[^a-zA-Z0-9 ]", "", str(name)).split()
    if len(clean) >= 2: return (clean[0][0] + clean[1][0]).upper()
    return clean[0][:2].upper() if clean else "SC"

def clean_text(text):
    if pd.isna(text): return "Classic Blend"
    return str(text).replace("[", "").replace("]", "").replace("'", "").replace('"', "")

def generate_stars(score):
    try:
        full = int(float(score))
        return "★" * min(full, 5) + "☆" * (5 - min(full, 5))
    except: return "☆☆☆☆☆"

# STYLE
def load_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600&family=Playfair+Display:wght@400;600&display=swap');
        .stApp { background-color: #0E0E0E !important; background-image: radial-gradient(circle at 50% 0%, #1c1c1c 0%, #000000 100%) !important; }
        * { font-family: 'Montserrat', sans-serif; color: #E0E0E0; }
        h1 { font-family: 'Playfair Display', serif; color: #D4AF37 !important; }
        header, [data-testid="stHeader"], section[data-testid="stSidebar"] { display: none; }
        
        .title-box { border: 3px double #D4AF37; padding: 30px; text-align: center; margin-bottom: 40px; background: rgba(0,0,0,0.5); box-shadow: 0 0 20px rgba(212, 175, 55, 0.15); }
        div[data-baseweb="select"] > div { background-color: #111 !important; border-color: #D4AF37 !important; color: #FFF !important; height: 50px; }
        div[data-baseweb="popover"], ul[role="listbox"] { background-color: #0E0E0E !important; border: 1px solid #D4AF37 !important; }
        li[role="option"] { color: #CCC !important; background-color: #0E0E0E !important; }
        li[role="option"]:hover { background-color: #D4AF37 !important; color: #000 !important; font-weight: bold; }
        div[data-baseweb="select"] span { color: #FFF !important; }
        .footer-link { color: #888; text-decoration: none; border-bottom: 1px dotted #555; }
        .footer-link:hover { color: #D4AF37; }
        div[data-testid="stMetricValue"] { color: #D4AF37 !important; }
        hr { border-color: #333; margin: 2em 0; }
        </style>
    """, unsafe_allow_html=True)

# RENDER CARD
def render_card(row, rank):
    img_url = row['Image URL'] if 'Image URL' in row and pd.notna(row['Image URL']) else ""
    score = row['Score'] if 'Score' in row else 0
    brand = row['Brand'] if pd.notna(row['Brand']) else "Niche House"
    notes = clean_text(row['Notes'])[:100] + "..."
    
    with st.container():
        c1, c2, c3 = st.columns([1.5, 4, 1.5])
        with c1:
            if img_url: st.image(img_url, width=100)
            else: st.markdown(f"<div style='width:80px; height:80px; border:1px solid #D4AF37; border-radius:50%; display:flex; align-items:center; justify-content:center; color:#D4AF37; margin:0 auto;'>{get_initials(row['Name'])}</div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div style='margin-left:0px;'><div style='font-size:10px; color:#D4AF37; letter-spacing:2px;'>MATCH NO. {rank}</div><div style='font-family:Playfair Display; font-size:20px; color:#FFF; margin-top:5px;'>{row['Name']}</div><div style='font-size:12px; color:#AAA; font-style:italic; margin-bottom:8px;'>{brand}</div><div style='font-size:10px; color:#888;'>{notes}</div></div>", unsafe_allow_html=True)
        with c3:
            st.metric(label="RATING", value=f"{score:.1f}", delta=generate_stars(score))
        st.markdown("<div style='height:1px; background:#222; margin:15px 0;'></div>", unsafe_allow_html=True)

# LOGIC
def get_recs(name, df, sim, indices):
    try:
        idx = indices[name]
        if isinstance(idx, pd.Series): idx = idx.iloc[0]
        scores = sorted(list(enumerate(sim[idx])), key=lambda x: x[1], reverse=True)[1:6]
        return df.iloc[[i[0] for i in scores]]
    except: return pd.DataFrame()

# APP
load_custom_css()
st.markdown("""<div class="title-box"><h1 style='font-size:42px; margin:0;'>SCENTSATIONAL</h1><p style='font-size:10px; color:#888; letter-spacing:3px; margin-top:5px;'>LUXURY AI CONCIERGE</p></div>""", unsafe_allow_html=True)
df, cosine_sim = load_data()

if df is not None:
    indices = pd.Series(df.index, index=df['Name']).drop_duplicates()
    st.markdown("<div style='text-align:center; color:#D4AF37; font-size:12px; letter-spacing:1px; margin-bottom:10px;'>SELECT YOUR SIGNATURE SCENT</div>", unsafe_allow_html=True)
    # Sortowanie czystych nazw dla listy
    clean_names = sorted(df['Name'].unique().tolist())
    target = st.selectbox("hidden", options=clean_names, index=None, placeholder="Type to search...", label_visibility="collapsed")
    st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)

    if target:
        recs = get_recs(target, df, cosine_sim, indices)
        if not recs.empty:
            st.markdown(f"<center style='color:#666; font-size:11px; margin-bottom:40px;'>CURATED FOR LOVERS OF <b style='color:#D4AF37'>{target}</b></center>", unsafe_allow_html=True)
            rank = 1
            for _, row in recs.iterrows(): render_card(row, rank); rank+=1
            st.markdown("""<div style="text-align:center; margin-top:80px; padding-top:20px; border-top:1px solid #222; font-size:9px; color:#555; line-height:2.0;"><b>SCENTSATIONAL AI</b><br>Research: <a href="https://github.com/MagdalenaRomaniecka/ScentSational" target="_blank" class="footer-link">GitHub</a><br>Created by <b>Magdalena Romaniecka</b></div>""", unsafe_allow_html=True)
        else: st.error("No matches found.")
else: st.error("CRITICAL: 'finale_perfume.csv' or 'hybrid_similarity.npy' missing.")