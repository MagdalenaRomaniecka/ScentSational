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
        df = pd.read_csv("perfumes_dataset.csv")
        cosine_sim = np.load("hybrid_similarity.npy")
        
        # --- FIX: CLEAN NAMES (REMOVE NUMBERS) ---
        # This removes any leading numbers (e.g., "0. Chanel" -> "Chanel")
        df['Name'] = df['Name'].astype(str).apply(lambda x: re.sub(r'^\d+\s+', '', x))
        
        return df, cosine_sim
    except FileNotFoundError:
        return None, None

# --- 3. HELPER FUNCTIONS ---
def get_initials(name):
    if not isinstance(name, str): return "SC"
    # Clean non-alphanumeric characters but keep spaces
    clean = re.sub(r"[^a-zA-Z0-9 ]", "", name).split()
    if len(clean) >= 2: 
        return (clean[0][0] + clean[1][0]).upper()
    return clean[0][:2].upper() if clean else "SC"

def clean_text(text):
    if pd.isna(text): return "Classic Blend"
    # Remove JSON artifacts
    return str(text).replace("[", "").replace("]", "").replace("'", "").replace('"', "")

def generate_stars(score):
    try:
        val = float(score)
        full = int(val)
        full = min(full, 5)
        return "★" * full + "☆" * (5 - full)
    except:
        return "☆☆☆☆☆"

# --- 4. CSS STYLING ---
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
        
        /* TEXT & FONTS */
        * { font-family: 'Montserrat', sans-serif; color: #E0E0E0; }
        h1 { font-family: 'Playfair Display', serif; color: #D4AF37 !important; }

        /* HIDE DEFAULTS */
        header, [data-testid="stHeader"] { background: transparent !important; }
        section[data-testid="stSidebar"] { display: none; }

        /* TITLE FRAME */
        .title-box {
            border: 3px double #D4AF37;
            padding: 30px;
            text-align: center;
            margin-bottom: 40px;
            background: rgba(0,0,0,0.5);
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.15);
        }

        /* DROPDOWN & INPUTS */
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
            font-weight: bold !important;
        }
        div[data-baseweb="select"] span {
            color: #FFF !important;
        }

        /* LINKS & METRICS */
        .footer-link { color: #888; text-decoration: none; border-bottom: 1px dotted #555; }
        .footer-link:hover { color: #D4AF37; }
        div[data-testid="stMetricValue"] { color: #D4AF37 !important; }
        div[data-testid="stMetricLabel"] { color: #888 !important; }
        
        hr { border-color: #333; margin: 2em 0; }
        </style>
    """, unsafe_allow_html=True)

# --- 5. RENDER CARD ---
def render_card(row, rank):
    img_url = row['Image URL'] if 'Image URL' in row and pd.notna(row['Image URL']) else ""
    score = row['Score'] if 'Score' in row else 0
    stars = generate_stars(score)
    brand = row['Brand'] if pd.notna(row['Brand']) else "Niche House"
    notes = clean_text(row['Notes'])
    if len(notes) > 100: notes = notes[:100] + "..."
    
    with st.container():
        col1, col2, col3 = st.columns([1.5, 4, 1.5])
        
        with col1:
            if img_url:
                st.image(img_url, width=100)
            else:
                initials = get_initials(row['Name'])
                st.markdown(f"<div style='width:80px; height:80px; border