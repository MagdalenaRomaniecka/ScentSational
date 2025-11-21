import streamlit as st
import pandas as pd
import numpy as np
import re
import streamlit.components.v1 as components

# --- 1. KONFIGURACJA ---
st.set_page_config(
    page_title="ScentSational AI",
    page_icon="💎",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. ANALITYKA (GA4) ---
def inject_ga4():
    GA_ID = "G-28PVV48GN5"
    ga_code = f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{GA_ID}');
    </script>
    """
    components.html(ga_code, height=0, width=0)

inject_ga4()

# --- 3. ŁADOWANIE DANYCH (Te "sklejone") ---
@st.cache_data
def load_data():
    try:
        # Wczytujemy plik powstały z połączenia fra_perfumes i perfumes_cleaned
        df = pd.read_csv("perfumes_dataset.csv")
        cosine_sim = np.load("hybrid_similarity.npy")
        
        # Usuwamy numery z nazw (np. "86. Chanel" -> "Chanel")
        df['Name'] = df['Name'].astype(str).str.replace(r'^\d+[\.\s]*', '', regex=True)
        
        return df, cosine_sim
    except FileNotFoundError:
        return None, None

# --- 4. FUNKCJE POMOCNICZE ---
def get_initials(name):
    if not isinstance(name, str): return "SC"
    clean = re.sub(r"[^a-zA-Z0-9 ]", "", name).split()
    if len(clean) >= 2: 
        return (clean[0][0] + clean[1][0]).upper()
    return clean[0][:2].upper() if clean else "SC"

def clean_text(text):
    if pd.isna(text): return "Classic Blend"
    return str(text).replace("[", "").replace("]", "").replace("'", "").replace('"', "")

def generate_stars(score):
    try:
        val = float(score)
        return "★" * int(val) + "☆" * (5 - int(val))
    except:
        return "☆☆☆☆☆"

# --- 5. STYL (Dla wyglądu Luxury) ---
def load_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600&family=Playfair+Display:wght@400;600&display=swap');

        .stApp {
            background-color: #0E0E0E !important;
            background-image: radial-gradient(circle at 50% 0%, #1c1c1c 0%, #000000 100%) !important;
            background-attachment: fixed !important;
        }
        
        * { font-family: 'Montserrat', sans-serif; color: #E0E0E0; }
        h1 { font-family: 'Playfair Display', serif; color: #D4AF37 !important; }
        header, [data-testid="stHeader"], section[data-testid="stSidebar"] { display: none; }

        .title-box {
            border: 3px double #D4AF37;
            padding: 40px;
            text-align: center;
            margin-bottom: 30px;
            background: rgba(0,0,0,0.5);
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.15);
        }

        div[data-baseweb="select"] > div {
            background-color: #111 !important;
            border-color: #D4AF37 !important;
            color: #FFF !important;
            height: 50px;
        }
        div[data-baseweb="popover"], ul[role="listbox"] {
            background-color: #0E0E0E !important;
            border: 1px solid #D4AF37 !important;
        }
        li[role="option"] {
            color: #CCC !important;
            background-color: #0E0E0E !important;
            font-size: 12px !important;
        }
        li[role="option"]:hover {
            background-color: #D4AF37 !important;
            color: #000 !important;
            font-weight: bold !important;
        }
        div[data-baseweb="select"] span { color: #FFF !important; }

        .footer {
            margin-top: 80px;
            padding: 20px 0;
            border-top: 1px solid #222;
            text-align: center;
            font-size: 10px;
            color: #666;
            line-height: 2.0;
        }
        .footer a { color: #888; text-decoration: none; margin: 0 5px; border-bottom: 1px dotted #555; }
        .footer a:hover { color: #D4AF37; }
        
        div[data-testid="stMetricValue"] { color: #D4AF37 !important; }
        hr { border-color: #333; margin: 2em 0; }
        </style>
    """, unsafe_allow_html=True)

# --- 6. WYŚWIETLANIE KARTY (Zdjęcie + Ocena) ---
def render_card(row, rank):
    img_url = row['Image URL'] if 'Image URL' in row and pd.notna(row['Image URL']) else ""
    score = row['Score'] if 'Score' in row else 0
    stars = generate_stars(score)
    
    brand = row['Brand'] if 'Brand' in row and pd.notna(row['Brand']) else "Niche House"
    notes = clean_text(row['Notes'])
    if len(notes) > 100: notes = notes[:100] + "..."
    
    with st.container():
        col1, col2