import streamlit as st
import pandas as pd
import numpy as np
import re

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="ScentSational AI",
    page_icon="💎",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. DATA LOADING ---
@st.cache_data
def load_data():
    try:
        # Loading the MERGED dataset (Images + Ratings)
        df = pd.read_csv("perfumes_dataset.csv")
        cosine_sim = np.load("hybrid_similarity.npy")
        return df, cosine_sim
    except FileNotFoundError:
        return None, None

# --- 3. HELPER FUNCTIONS ---
def get_initials(name):
    if not isinstance(name, str): return "SC"
    clean = re.sub(r"[^a-zA-Z0-9 ]", "", name)
    words = clean.split()
    if len(words) >= 2:
        return (words[0][0] + words[1][0]).upper()
    return clean[:2].upper()

def clean_text(text):
    if pd.isna(text): return "Classic Blend"
    text = str(text).replace("[", "").replace("]", "").replace("'", "").replace('"', "")
    return text

def generate_stars(score):
    try:
        val = float(score)
        full = int(val)
        # Cap at 5 stars
        full = min(full, 5)
        return "★" * full + "☆" * (5 - full)
    except:
        return "☆☆☆☆☆"

# --- 4. CSS STYLING (LUXURY THEME) ---
def load_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600&family=Playfair+Display:wght@400;600&display=swap');

        /* BACKGROUND */
        .stApp {
            background-color: #0E0E0E !important;
            background-image: radial-gradient(circle at 50% 0%, #1c1c1c 0%, #000000 100%) !important;
            background-attachment: fixed !important;
        }
        
        /* FONTS */
        * { font-family: 'Montserrat', sans-serif; color: #E0E0E0; }
        h1 { font-family: 'Playfair Display', serif; color: #D4AF37 !important; }

        /* HIDE DEFAULTS */
        header, [data-testid="stHeader"] { background: transparent !important; }
        section[data-testid="stSidebar"] { display: none; }

        /* TITLE FRAME */
        .title-box {
            border: 3px double #D4AF37;
            padding: 40px;
            text-align: center;
            margin-bottom: 50px;
            background: rgba(0,0,0,0.5);
            box-shadow: 0 0 25px rgba(212, 175, 55, 0.15);
        }

        /* DROPDOWN FIX */
        div[data-baseweb="select"] > div {
            background-color: #111 !important;
            border-color: #D4AF37 !important;
            color: #FFF !important;
            height: 50px;
        }
        div[data-baseweb="popover"], ul[role="listbox"], div[data-baseweb="menu"] {
            background-color: #0E0E0E !important;
            border: 1px solid #D4AF37 !important;
        }
        li[role="option"] {
            color: #CCC !important;
            background-color: #0E0E0E !important;
            font-size: 12px !important;
        }
        li[role="option"]:hover, li[role="option"][aria-selected="true"] {
            background-color: #D4AF37 !important;
            color: #000 !important;
            font-weight: bold;
        }
        div[data-baseweb="select"] span { color: #FFF !important; }

        /* METRICS & LINKS */
        div[data-testid="stMetricValue"] { color: #D4AF37 !important; font-size: 24px !important; }
        div[data-testid="stMetricLabel"] { color: #888 !important; font-size: 10px !important; }
        
        .footer-link { color: #888; text-decoration: none; border-bottom: 1px dotted #555; transition: 0.3s; }
        .footer-link:hover { color: #D4AF37; border-bottom: 1px solid #D4AF37; }
        
        hr { border-color: #333; margin: 2em 0; }
        </style>
    """, unsafe_allow_html=True)

# --- 5. RENDER CARD (IMAGE + RATING + NOTES) ---
def render_card(row, rank):
    # 1. Image Logic
    img_url = row['Image URL'] if 'Image URL' in row and pd.notna(row['Image URL']) else ""
    
    # 2. Rating Logic
    score = row['Score'] if 'Score' in row else 0
    stars = generate_stars(score)
    
    # 3. Text Logic
    brand = row['Brand'] if pd.notna(row['Brand']) else "Niche House"
    notes = clean_text(row['Notes'])
    if len(notes) > 100: notes = notes[:100] + "..."
    
    with st.container():
        # Layout: Image(1.5) | Details(4) | Rating(1.5)
        col1, col2, col3 = st.columns([1.5, 4, 1.5])
        
        with col1:
            if img_url:
                st.image(img_url, width=100)
            else:
                # Fallback: Elegant Monogram if no image
                initials = get_initials(row['Name'])
                st.markdown(f"""
                <div style='width:80px; height:80px; border:1px solid #D4AF37; border-radius:50%; 
                            display:flex; align-items:center; justify-content:center; 
                            color:#D4AF37; font-family: "Playfair Display"; font-size: 24px; margin:0 auto;'>
                    {initials}
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="margin-left: 10px;">
                <div style="font-size: 10px; color: #D4AF37; letter-spacing: 2px; text-transform: uppercase;">
                    MATCH NO. {rank}
                </div>
                <div style="font-family: 'Playfair Display'; font-size: 20px; color: #FFF; margin-top:5px; margin-bottom:5px;">
                    {row['Name']}
                </div>
                <div style="font-size: 12px; color: #AAA; font-style: italic; margin-bottom: 8px;">
                    {brand}
                </div>
                <div style="font-size: 10px; color: #888; line-height:1.4;">
                    <span style="color:#D4AF37;">NOTES:</span> {notes}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            # Star Rating
            st.metric(label="RATING", value=f"{score:.1f}", delta=stars)
        
        st.markdown("<div style='height:1px; background:#222; margin:20px 0;'></div>", unsafe_allow_html=True)

# --- 6. LOGIC ---
def get_recs(name, df, sim, indices):
    try:
        idx = indices[name]
        # Handle duplicates
        if isinstance(idx, pd.Series): idx = idx.iloc[0]
        
        scores = list(enumerate(sim[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        scores = scores[1:6] # Top 5
        return df.iloc[[i[0] for i in scores]]
    except KeyError:
        return pd.DataFrame()

# --- 7. APP EXECUTION ---
load_custom_css()

st.markdown("""
<div class="title-box">
    <h1 style='font-size: 42px; margin:0;'>SCENTSATIONAL</h1>
    <p style='font-size: 10px; color: #888; letter-spacing: 3px; margin-top: 5px;'>LUXURY AI CONCIERGE</p>
</div>
""", unsafe_allow_html=True)

df, cosine_sim = load_data()

if df is not None:
    indices = pd.Series(df.index, index=df['Name']).drop_duplicates()
    
    # HERO INPUT
    st.markdown("<div style='text-align:center; color:#D4AF37; font-size:12px; letter-spacing:1px; margin-bottom:10px;'>SELECT YOUR SIGNATURE SCENT</div>", unsafe_allow_html=True)
    
    target = st.selectbox(
        "hidden_label",
        options=sorted(df['Name'].unique()),
        index=None,
        placeholder="Type to search database...",
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

    if target:
        recs = get_recs(target, df, cosine_sim, indices)
        
        if not recs.empty:
            st.markdown(f"<center style='color:#666; font-size:11px; margin-bottom:40px;'>CURATED FOR LOVERS OF <b style='color:#D4AF37'>{target}</b></center>", unsafe_allow_html=True)
            st.markdown("<div style='height:1px; background:#333; margin-bottom:30px;'></div>", unsafe_allow_html=True)
            
            rank = 1
            for _, row in recs.iterrows():
                render_card(row, rank)
                rank += 1
            
            st.markdown("""
            <div style="text-align:center; margin-top:80px; padding-top:20px; border-top:1px solid #222; font-size:9px; color:#555; line-height:2.0;">
                <b>SCENTSATIONAL AI</b><br>
                Research: <a href="https://github.com/MagdalenaRomaniecka/ScentSational" target="_blank" class="footer-link">GitHub Repository</a><br>
                Data Source: Aggregated from Kaggle & Niche Perfumery<br>
                Created by <b>Magdalena Romaniecka</b>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("No matches found.")

else:
    st.error("CRITICAL: 'perfumes_dataset.csv' or 'hybrid_similarity.npy' not found. Please upload generated files.")