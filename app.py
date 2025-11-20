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
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&family=Playfair+Display:wght@600;700&display=swap');

        /* BACKGROUND */
        .stApp {
            background-color: #0E0E0E !important;
            background-image: radial-gradient(circle at 50% 0%, #1c1c1c 0%, #000000 100%) !important;
            background-attachment: fixed !important;
        }

        /* HIDE HEADER/SIDEBAR */
        header, [data-testid="stHeader"] { background-color: transparent !important; }
        section[data-testid="stSidebar"] { display: none; }

        /* TITLE FRAME */
        .title-frame {
            border: 3px double #D4AF37;
            padding: 40px;
            margin-bottom: 40px;
            text-align: center;
            background: rgba(0, 0, 0, 0.4);
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.15);
        }
        
        /* FONTS */
        * { font-family: 'Montserrat', sans-serif; color: #E0E0E0; }
        h1 { font-family: 'Playfair Display', serif; color: #D4AF37 !important; }

        /* DROPDOWN FIX */
        div[data-baseweb="select"] > div {
            background-color: #111 !important;
            border-color: #333 !important;
            color: #FFF !important;
        }
        div[data-baseweb="popover"], ul[role="listbox"], div[data-baseweb="menu"] {
            background-color: #0E0E0E !important;
            border: 1px solid #D4AF37 !important;
        }
        li[role="option"] {
            color: #CCC !important;
            background-color: #0E0E0E !important;
        }
        li[role="option"]:hover, li[role="option"][aria-selected="true"] {
            background-color: #D4AF37 !important;
            color: #000 !important;
            font-weight: bold !important;
        }
        div[data-baseweb="select"] span {
            color: #FFF !important;
        }

        /* LABELS STYLE */
        .soft-label {
            font-size: 10px;
            color: #888;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 5px;
            font-family: 'Montserrat', sans-serif;
        }
        
        hr { border-color: #333; margin: 2em 0; }
        </style>
    """, unsafe_allow_html=True)

# --- 5. RENDER CARD ---
def render_recommendation(row, rank):
    initials = get_initials(row['Name'])
    brand = row['Brand'] if 'Brand' in row else "Unknown Brand"
    notes = clean_text(row['Notes']) if 'Notes' in row else "N/A"
    if len(notes) > 120: notes = notes[:120] + "..."

    with st.container():
        col1, col2 = st.columns([1, 5])
        with col1:
            st.markdown(f"""
            <div style="
                width: 60px; height: 60px; 
                border: 2px solid #D4AF37; 
                border-radius: 50%; 
                background-color: #000;
                display: flex; align-items: center; justify-content: center;
                font-family: 'Playfair Display'; font-size: 22px; color: #D4AF37;
                box-shadow: 0 0 10px rgba(212, 175, 55, 0.2);
                margin: 0 auto;
            ">
                {initials}
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="margin-left: 10px;">
                <div style="font-size: 10px; color: #D4AF37; letter-spacing: 2px;">NO. {rank}</div>
                <div style="font-family: 'Playfair Display'; font-size: 20px; color: #FFF;">{row['Name']}</div>
                <div style="font-size: 12px; color: #888; font-style: italic; margin-bottom: 5px;">{brand}</div>
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

st.markdown("""
<div class="title-frame">
    <h1 style='margin-bottom: 5px; font-size: 42px; letter-spacing: 4px;'>SCENTSATIONAL</h1>
    <p style='color:#888; font-size:11px; letter-spacing:4px; margin:0; text-transform: uppercase;'>
        Personal Fragrance Curator
    </p>
</div>
""", unsafe_allow_html=True)

df, cosine_sim = load_data()

if df is not None and cosine_sim is not None:
    indices = pd.Series(df.index, index=df['Name']).drop_duplicates()
    
    # --- ELEGANT SELECTION FLOW ---
    
    all_brands = sorted(df['Brand'].unique()) if 'Brand' in df.columns else []
    
    # Row 1: Refine
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<p class="soft-label">NARROW DOWN BY HOUSE (OPTIONAL)</p>', unsafe_allow_html=True)
        selected_brand = st.selectbox("Brand", ["View All Houses"] + all_brands, label_visibility="collapsed")

    with col_b:
        st.markdown('<p class="soft-label">PREFERRED STYLE</p>', unsafe_allow_html=True)
        selected_gender = st.selectbox("Gender", ["All Collections", "Women", "Men", "Unisex"], label_visibility="collapsed")

    # Logic
    filtered_df = df.copy()
    if selected_brand != "View All Houses":
        filtered_df = filtered_df[filtered_df['Brand'] == selected_brand]
    
    if 'Gender' in filtered_df.columns and selected_gender != "All Collections":
        if selected_gender == "Women": filtered_df = filtered_df[filtered_df['Gender'].str.contains("women", case=False, na=False)]
        elif selected_gender == "Men": filtered_df = filtered_df[filtered_df['Gender'].str.contains("men", case=False, na=False)]
        elif selected_gender == "Unisex": filtered_df = filtered_df[filtered_df['Gender'].str.contains("women and men", case=False, na=False)]

    available_perfumes = sorted(filtered_df['Name'].unique())

    st.write("")
    st.write("")

    # Row 2: Main Input
    st.markdown('<p class="soft-label" style="text-align:center;">WHAT IS YOUR SIGNATURE SCENT?</p>', unsafe_allow_html=True)
    selected_perfume = st.selectbox(
        "Main Selection",
        options=available_perfumes,
        index=None,
        placeholder="Select a fragrance you love...",
        label_visibility="collapsed"
    )
    
    st.write("") 

    if selected_perfume:
        st.markdown(f"<center style='color:#666; font-size:12px; margin: 40px 0; letter-spacing:1px;'>CURATING A COLLECTION INSPIRED BY <b style='color:#D4AF37'>{selected_perfume}</b></center>", unsafe_allow_html=True)
        
        recommendations = get_recommendations(selected_perfume, df, cosine_sim, indices)
        
        if not recommendations.empty:
            rank = 1
            for idx, row in recommendations.iterrows():
                render_recommendation(row, rank)
                rank += 1
            
            st.markdown("""
            <div style='text-align:center; font-size:9px; color:#444; margin-top:50px; line-height:1.6;'>
                AI ENGINE: COSINE SIMILARITY<br>
                © 2025 MAGDALENA ROMANIECKA
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No recommendations found.")
else:
    st.error("Data files missing.")