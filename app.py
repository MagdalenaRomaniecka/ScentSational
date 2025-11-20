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

        /* HEADER FRAME (Restored but compact) */
        .title-frame {
            border: 3px double #D4AF37;
            padding: 25px;
            margin-bottom: 30px;
            text-align: center;
            background: rgba(0, 0, 0, 0.6);
            box-shadow: 0 0 25px rgba(212, 175, 55, 0.1);
        }

        /* FONTS */
        * { font-family: 'Montserrat', sans-serif; color: #E0E0E0; }
        h1 { font-family: 'Playfair Display', serif; color: #D4AF37 !important; }

        /* --- ULTRA AGGRESSIVE DROPDOWN FIX --- */
        /* Input container */
        div[data-baseweb="select"] > div {
            background-color: #111 !important;
            border-color: #D4AF37 !important;
            color: #FFF !important;
        }
        /* The Pop-up Container */
        div[data-baseweb="popover"] {
            background-color: #0E0E0E !important;
            border: 1px solid #333 !important;
        }
        div[data-baseweb="menu"] {
            background-color: #0E0E0E !important;
        }
        /* List Items */
        ul[role="listbox"] {
            background-color: #0E0E0E !important;
        }
        li[role="option"] {
            background-color: #0E0E0E !important;
            color: #CCC !important;
            font-size: 12px !important;
        }
        /* Hover / Selected */
        li[role="option"]:hover, li[role="option"][aria-selected="true"] {
            background-color: #D4AF37 !important;
            color: #000 !important;
            font-weight: bold !important;
        }
        /* Selected item text in box */
        div[data-baseweb="select"] span {
            color: #FFF !important;
        }
        /* --- END FIX --- */

        /* GOLD CARD */
        hr { border-color: #333; margin: 2em 0; }
        </style>
    """, unsafe_allow_html=True)

# --- 5. RENDER CARD ---
def render_recommendation(row, rank):
    initials = get_initials(row['Name'])
    brand = row['Brand'] if 'Brand' in row else "Unknown Brand"
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
                box-shadow: 0 0 10px rgba(212, 175, 55, 0.1);
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

# TITLE
st.markdown("""
<div class="title-frame">
    <h1 style='margin-bottom: 5px; font-size: 38px; letter-spacing: 3px;'>SCENTSATIONAL</h1>
    <p style='color:#888; font-size:10px; letter-spacing:3px; margin:0; text-transform: uppercase;'>
        AI-Powered Perfume Concierge
    </p>
</div>
""", unsafe_allow_html=True)

df, cosine_sim = load_data()

if df is not None and cosine_sim is not None:
    indices = pd.Series(df.index, index=df['Name']).drop_duplicates()
    
    # --- HERO SECTION (MAIN INPUT FIRST) ---
    st.markdown("<div style='text-align:center; margin-bottom:10px; color:#D4AF37; font-size:12px; letter-spacing:1px; font-weight:bold;'>SELECT YOUR SIGNATURE SCENT</div>", unsafe_allow_html=True)
    
    # Initialize filtered dataframe
    filtered_df = df.copy()
    
    # To make it open downwards, it needs space below. 
    # Since it's the first element, browser logic usually forces it down unless page is tiny.
    
    # --- OPTIONAL FILTERS (COLLAPSIBLE OR BELOW) ---
    # Using columns for compact look underneath the main bar
    
    # We need placeholders for filters to affect the main list
    if 'brand_filter' not in st.session_state: st.session_state.brand_filter = "All Brands"
    
    # LOGIC: We show filters below, but they update the list above.
    # However, Streamlit runs top-down. To make filters affect the list above, we must declare them first but render them visually? 
    # No, easiest way in Streamlit: Render filters, then Render Main list.
    # BUT user wants Main List first visually.
    
    # SOLUTION: Filters ABOVE but subtle, OR Filters BELOW (but user has to unselect main to see full list?)
    # Let's stick to: Filters ABOVE (but very small/subtle) is best for logic.
    # User said "Signature scent mial byc pierwszy". 
    # So: Main Selectbox takes FULL list by default.
    # Filters below update the selectbox? Streamlit reruns script. Yes.
    
    # Let's put Filters in an Expander below to keep UI clean, but allow filtering.
    
    col_main = st.container() # Placeholder for main input
    
    with st.expander("cant find your perfume? filter list here ▾"):
        col_a, col_b = st.columns(2)
        with col_a:
            all_brands = sorted(df['Brand'].unique()) if 'Brand' in df.columns else []
            brand_val = st.selectbox("Filter by Brand", ["All Brands"] + all_brands)
        with col_b:
             gender_val = st.selectbox("Filter by Category", ["All Categories", "Women", "Men", "Unisex"])

    # Apply filters
    if brand_val != "All Brands":
        filtered_df = filtered_df[filtered_df['Brand'] == brand_val]
    
    if 'Gender' in filtered_df.columns and gender_val != "All Categories":
        if gender_val == "Women": filtered_df = filtered_df[filtered_df['Gender'].str.contains("women", case=False, na=False)]
        elif gender_val == "Men": filtered_df = filtered_df[filtered_df['Gender'].str.contains("men", case=False, na=False)]
        elif gender_val == "Unisex": filtered_df = filtered_df[filtered_df['Gender'].str.contains("women and men", case=False, na=False)]

    available_perfumes = sorted(filtered_df['Name'].unique())

    # NOW RENDER MAIN INPUT (At the top visually via container)
    with col_main:
        selected_perfume = st.selectbox(
            "Label Hidden",
            options=available_perfumes,
            index=None,
            placeholder="Type to search database...",
            label_visibility="collapsed"
        )

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
            
            # FOOTER (Credits & Links)
            st.markdown("""
            <div style="text-align:center; margin-top:80px; padding-top:20px; border-top:1px solid #222; font-size:9px; color:#555; line-height:1.8;">
                <b>SCENTSATIONAL AI</b><br>
                Research: <a href="https://github.com/MagdalenaRomaniecka/ScentSational" target="_blank" style="color:#888; text-decoration:none;">GitHub Repository</a><br>
                Data: <a href="https://www.kaggle.com/datasets/nandini1999/perfume-recommendation-dataset" target="_blank" style="color:#888; text-decoration:none;">Kaggle Dataset</a><br>
                Created by <b>Magdalena Romaniecka</b>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No recommendations found.")
else:
    st.error("System Error: Data files not found.")