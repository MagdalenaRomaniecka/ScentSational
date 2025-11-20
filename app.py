import streamlit as st
import pandas as pd
import numpy as np
import re

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="ScentSational AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
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

        /* FONTS */
        * { font-family: 'Montserrat', sans-serif; color: #E0E0E0; }
        h1, h2, h3 { font-family: 'Playfair Display', serif; color: #D4AF37 !important; }
        
        /* HEADER & TITLE */
        header, [data-testid="stHeader"] { background-color: transparent !important; }
        
        .title-frame {
            border: 3px double #D4AF37;
            padding: 40px;
            margin-bottom: 30px;
            text-align: center;
            background: rgba(0, 0, 0, 0.4);
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.15);
        }

        /* SIDEBAR STYLING */
        section[data-testid="stSidebar"] {
            background-color: #050505 !important;
            border-right: 1px solid #222;
        }
        .stSidebar h2, .stSidebar h3 {
            font-size: 12px !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .stRadio, .stMultiSelect, .stSlider { margin-bottom: -15px !important; }

        /* DROPDOWN FIX */
        div[data-baseweb="select"] > div, div[data-baseweb="popover"], ul[role="listbox"] {
            background-color: #0E0E0E !important;
            border: 1px solid #333 !important;
            color: #FFF !important;
        }
        li[role="option"] { color: #EEE !important; }
        li[role="option"]:hover, li[role="option"][aria-selected="true"] {
            background-color: #D4AF37 !important;
            color: #000 !important;
            font-weight: bold;
        }

        /* GOLD CARD */
        .reco-card {
            background-color: #121212;
            border-left: 4px solid #D4AF37;
            padding: 20px;
            margin-bottom: 15px;
        }
        
        hr { border-color: #333; margin: 2em 0; }
        </style>
    """, unsafe_allow_html=True)

# --- 5. RENDER RECOMMENDATION ---
def render_recommendation(row, rank):
    initials = get_initials(row['Name'])
    brand = row['Brand'] if 'Brand' in row else "Unknown Brand"
    notes = clean_text(row['Notes']) if 'Notes' in row else "N/A"
    if len(notes) > 100: notes = notes[:100] + "..."

    with st.container():
        col1, col2 = st.columns([1, 5])
        with col1:
            # MONOGRAM
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
                <div style="font-size: 10px; color: #D4AF37; letter-spacing: 2px;">#{rank} RECOMMENDED</div>
                <div style="font-family: 'Playfair Display'; font-size: 20px; color: #FFF;">{row['Name']}</div>
                <div style="font-size: 12px; color: #888; font-style: italic; margin-bottom: 5px;">{brand}</div>
                <div style="font-size: 10px; color: #AAA;"><span style="color: #D4AF37;">NOTES:</span> {notes}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<div style='height: 1px; background: #222; margin: 15px 0;'></div>", unsafe_allow_html=True)

# --- 6. MAIN LOGIC ---
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

# SIDEBAR FILTERS (Przywrócone z oryginalnego projektu!)
with st.sidebar:
    st.markdown("### FILTER DATABASE")
    st.write("Help us find your perfume faster.")
    
    # 1. Filter by Gender
    gender_filter = st.radio("Category", ["All", "Women", "Men", "Unisex"], label_visibility="collapsed")
    
    # 2. Filter by Brand (New!)
    df, cosine_sim = load_data()
    if df is not None:
        all_brands = sorted(df['Brand'].unique()) if 'Brand' in df.columns else []
        brand_filter = st.selectbox("Brand (Optional)", ["All Brands"] + all_brands)
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; font-size:9px; color:#555;'>
        SCENTSATIONAL AI v2.0<br>© 2025 MAGDALENA ROMANIECKA
    </div>
    """, unsafe_allow_html=True)

# MAIN CONTENT
st.markdown("""
<div class="title-frame">
    <h1 style='margin-bottom: 5px; font-size: 42px; letter-spacing: 4px;'>SCENTSATIONAL</h1>
    <p style='color:#888; font-size:11px; letter-spacing:4px; margin:0; text-transform: uppercase;'>
        AI-Powered Perfume Concierge
    </p>
</div>
""", unsafe_allow_html=True)

if df is not None and cosine_sim is not None:
    # --- SMART FILTERING LOGIC ---
    # Najpierw filtrujemy listę wyboru na podstawie Sidebara
    filtered_df = df.copy()
    
    # Filter Gender (Jeśli dane mają kolumnę Gender/Gender_Clean)
    # (Zakładam, że w Twoim perfumes_cleaned.csv może nie być idealnej kolumny Gender, 
    # więc filtrowanie opieramy na tym co jest, lub pomijamy jeśli brak)
    
    # Filter Brand
    if brand_filter != "All Brands":
        filtered_df = filtered_df[filtered_df['Brand'] == brand_filter]
    
    # Tworzymy listę do Selectboxa tylko z przefiltrowanych perfum
    available_perfumes = sorted(filtered_df['Name'].unique())
    indices = pd.Series(df.index, index=df['Name']).drop_duplicates()

    st.markdown(f"<div style='text-align:center; margin-bottom:10px; color:#D4AF37; font-size:12px;'>SELECT A PERFUME FROM <b>{len(available_perfumes)}</b> AVAILABLE:</div>", unsafe_allow_html=True)
    
    selected_perfume = st.selectbox(
        "Label Hidden",
        options=available_perfumes,
        index=None,
        placeholder="Type to search...",
        label_visibility="collapsed"
    )
    
    st.write("")

    if selected_perfume:
        st.markdown(f"<center style='color:#666; font-size:12px; margin: 30px 0;'>BECAUSE YOU LIKED <b style='color:#D4AF37'>{selected_perfume}</b>, WE SUGGEST:</center>", unsafe_allow_html=True)
        
        # Uwaga: Rekomendacje biorą z PEŁNEJ bazy, nie tylko przefiltrowanej (AI szuka wszędzie)
        recommendations = get_recommendations(selected_perfume, df, cosine_sim, indices)
        
        if not recommendations.empty:
            rank = 1
            for idx, row in recommendations.iterrows():
                render_recommendation(row, rank)
                rank += 1
            st.markdown("<center style='font-size:10px; color:#444; margin-top:50px;'>POWERED BY COSINE SIMILARITY</center>", unsafe_allow_html=True)
        else:
            st.warning("No similar perfumes found.")
else:
    st.error("Data files missing.")