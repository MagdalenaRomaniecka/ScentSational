import streamlit as st
import pandas as pd
import numpy as np
import re

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="ScentSational AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. DATA LOADING ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("perfumes_cleaned.csv")
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

        /* HIDE HEADER & SIDEBAR */
        header, [data-testid="stHeader"] { background-color: transparent !important; }
        section[data-testid="stSidebar"] { display: none; }

        /* HEADER (Much smaller and elegant) */
        .header-text {
            font-family: 'Playfair Display', serif;
            font-size: 32px;
            color: #D4AF37;
            text-align: center;
            letter-spacing: 3px;
            margin-top: 20px;
            margin-bottom: 5px;
        }
        .sub-header-text {
            font-family: 'Montserrat', sans-serif;
            font-size: 10px;
            color: #888;
            text-align: center;
            letter-spacing: 4px;
            text-transform: uppercase;
            margin-bottom: 40px;
        }

        /* DROPDOWN FIX (Dark Theme) */
        div[data-baseweb="select"] > div {
            background-color: #111 !important;
            border-color: #333 !important;
            color: #FFF !important;
            text-align: center !important; /* Center text in box */
        }
        div[data-baseweb="popover"], ul[role="listbox"] {
            background-color: #0E0E0E !important;
            border: 1px solid #D4AF37 !important;
        }
        li[role="option"] {
            color: #CCC !important;
            font-family: 'Montserrat', sans-serif;
            font-size: 12px;
            justify-content: center; /* Center items in list */
        }
        li[role="option"]:hover, li[role="option"][aria-selected="true"] {
            background-color: #D4AF37 !important;
            color: #000 !important;
            font-weight: bold !important;
        }
        /* Fix white text in input */
        div[data-baseweb="select"] span {
            color: #E0E0E0 !important; 
        }

        /* LABELS STYLE (Centered & Gold) */
        .input-label {
            font-family: 'Montserrat', sans-serif;
            font-size: 10px;
            color: #D4AF37;
            letter-spacing: 1px;
            text-transform: uppercase;
            text-align: center;
            margin-bottom: 5px;
        }
        
        /* FOOTER STYLE */
        .footer-box {
            margin-top: 80px;
            padding-top: 20px;
            border-top: 1px solid #222;
            text-align: center;
            font-family: 'Montserrat', sans-serif;
            font-size: 9px;
            color: #555;
            line-height: 1.8;
        }
        .footer-link {
            color: #888;
            text-decoration: none;
            transition: color 0.3s;
        }
        .footer-link:hover {
            color: #D4AF37;
        }

        /* CARD STYLING */
        hr { border-color: #333; margin: 2em 0; }
        </style>
    """, unsafe_allow_html=True)

# --- 5. RENDER CARD ---
def render_recommendation(row, rank):
    initials = get_initials(row['Name'])
    brand = row['Brand'] if 'Brand' in row else "Unknown"
    notes = clean_text(row['Notes']) if 'Notes' in row else "N/A"
    if len(notes) > 110: notes = notes[:110] + "..."

    with st.container():
        col1, col2 = st.columns([1, 5])
        with col1:
            st.markdown(f"""
            <div style="
                width: 55px; height: 55px; 
                border: 1px solid #D4AF37; 
                border-radius: 50%; 
                background-color: #050505;
                display: flex; align-items: center; justify-content: center;
                font-family: 'Playfair Display'; font-size: 20px; color: #D4AF37;
                margin: 0 auto;
            ">
                {initials}
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="margin-left: 15px;">
                <div style="font-family: 'Playfair Display'; font-size: 18px; color: #FFF; letter-spacing: 0.5px;">{row['Name']}</div>
                <div style="font-size: 11px; color: #888; font-style: italic; margin-bottom: 4px;">{brand}</div>
                <div style="font-size: 10px; color: #AAA;"><span style="color: #D4AF37;">ACCORDS:</span> {notes}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<div style='height: 1px; background: #222; margin: 15px 0;'></div>", unsafe_allow_html=True)

# --- 6. LOGIC ---
def get_recommendations(perfume_name, df, cosine_sim, indices):
    try:
        idx = indices[perfume_name]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:6]
        perfume_indices = [i[0] for i in sim_scores]
        return df.iloc[perfume_indices]
    except KeyError:
        return pd.DataFrame()

# --- 7. APP EXECUTION ---
load_custom_css()

# --- ELEGANT HEADER ---
st.markdown('<div class="header-text">SCENTSATIONAL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header-text">AI PERFUME CONCIERGE</div>', unsafe_allow_html=True)

df, cosine_sim = load_data()

if df is not None and cosine_sim is not None:
    indices = pd.Series(df.index, index=df['Name']).drop_duplicates()
    
    # --- FILTERS (Small & Centered) ---
    # These help narrow the list but are visually secondary
    col_a, col_b, col_c = st.columns([1, 2, 1]) # Use columns to center width
    
    with col_b:
        # Brand Filter
        all_brands = sorted(df['Brand'].unique()) if 'Brand' in df.columns else []
        st.markdown('<div class="input-label">Filter by Brand (Optional)</div>', unsafe_allow_html=True)
        selected_brand = st.selectbox("Brand", ["All Brands"] + all_brands, label_visibility="collapsed")
        
        st.write("") # Tiny gap
        
        # --- MAIN HERO INPUT ---
        filtered_df = df.copy()
        if selected_brand != "All Brands":
            filtered_df = filtered_df[filtered_df['Brand'] == selected_brand]
        
        available_perfumes = sorted(filtered_df['Name'].unique())

        st.markdown('<div class="input-label" style="font-size:12px; margin-top:10px; font-weight:bold;">SELECT YOUR SIGNATURE SCENT</div>', unsafe_allow_html=True)
        selected_perfume = st.selectbox(
            "Main Selection",
            options=available_perfumes,
            index=None,
            placeholder="Start typing...",
            label_visibility="collapsed"
        )

    st.write("") 
    st.write("") 

    # --- RESULTS ---
    if selected_perfume:
        st.markdown(f"<center style='color:#666; font-size:11px; margin: 30px 0; letter-spacing:1px;'>CURATING COLLECTION BASED ON <b style='color:#D4AF37'>{selected_perfume}</b></center>", unsafe_allow_html=True)
        st.markdown("<div style='height: 1px; background: #333; margin-bottom: 30px;'></div>", unsafe_allow_html=True)
        
        recommendations = get_recommendations(selected_perfume, df, cosine_sim, indices)
        
        if not recommendations.empty:
            rank = 1
            for idx, row in recommendations.iterrows():
                render_recommendation(row, rank)
                rank += 1
        else:
            st.warning("No recommendations found.")
    
    # --- FOOTER (CREDITS & LINKS) ---
    st.markdown("""
    <div class="footer-box">
        <b>SCENTSATIONAL AI</b><br>
        Part of Research Project: <a href="https://github.com/MagdalenaRomaniecka/ScentSational" target="_blank" class="footer-link">GitHub Repository</a><br>
        Data Source: <a href="https://www.kaggle.com/datasets/nandini1999/perfume-recommendation-dataset" target="_blank" class="footer-link">Kaggle Dataset</a><br>
        <br>
        Created by <b>Magdalena Romaniecka</b>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("System Error: Data files (csv/npy) not found.")