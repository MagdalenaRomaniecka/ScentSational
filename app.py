import streamlit as st
import pandas as pd
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ScentSational",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- DARK LUXURY DESIGN SYSTEM (CSS) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0E0E0E;
        color: #E0E0E0;
    }
    
    /* Typography */
    h1, h2, h3, h4 {
        color: #D4AF37 !important; /* Gold */
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* MOBILE OPTIMIZATION (Twoja prośba) */
    @media only screen and (max-width: 600px) {
        h1 { font-size: 2.0rem !important; }
        h2 { font-size: 1.5rem !important; }
        .stButton button { width: 100%; }
        /* To sprawia, że kolumny na telefonie układają się jedna pod drugą */
        div[data-testid="column"] { width: 100% !important; flex: 1 1 auto !important; }
    }
    
    /* Inputs */
    .stSelectbox > div > div > div {
        background-color: #1E1E1E !important;
        color: #E0E0E0 !important;
        border: 1px solid #D4AF37;
    }
    
    /* Images */
    img {
        border-radius: 8px;
        border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    try:
        # Ładowanie tylko CSV z naprawą kodowania
        df = pd.read_csv('scentsational_data.csv', encoding='latin1', on_bad_lines='skip')
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        return None

df = load_data()

# --- LOGIC (PROSTA, BEZ AI) ---
def get_simple_recommendations(selected_perfume, df):
    """
    Zwraca perfumy tej samej marki lub losowe, jeśli brak marki.
    Działa bez plików .npy.
    """
    try:
        # Znajdź wiersz wybranego perfumu
        target_row = df[df['Name'] == selected_perfume].iloc[0]
        recs = pd.DataFrame()
        
        # 1. Szukaj tej samej marki
        if 'Brand' in df.columns:
            brand = target_row['Brand']
            recs = df[(df['Brand'] == brand) & (df['Name'] != selected_perfume)]
        
        # 2. Uzupełnij losowymi, jeśli mało wyników
        if len(recs) < 4:
            remaining = 4 - len(recs)
            pool = df[df['Name'] != selected_perfume]
            random_picks = pool.sample(n=min(remaining, len(pool)))
            recs = pd.concat([recs, random_picks])
            
        return recs.head(4)
    except Exception:
        return pd.DataFrame()

# --- MAIN UI ---
st.title("ScentSational")
st.markdown("### *AI-Powered Fragrance Concierge*")

if df is not None:
    
    # Lista do wyboru
    perfume_list = sorted(df['Name'].astype(str).unique().tolist())
    
    selected_perfume = st.selectbox(
        "Select your signature scent:",
        options=[""] + perfume_list,
        index=0
    )

    if selected_perfume:
        st.markdown("---")
        
        # Sekcja Hero
        row_list = df[df['Name'] == selected_perfume]
        if not row_list.empty:
            hero_row = row_list.iloc[0]
            
            # Kolumny (responsywne dzięki CSS wyżej)
            c1, c2 = st.columns([1, 2])
            with c1:
                if 'Image URL' in df.columns and pd.notna(hero_row['Image URL']):
                    st.image(hero_row['Image URL'], use_container_width=True)
            with c2:
                st.markdown(f"## **{selected_perfume}**")
                if 'Brand' in df.columns:
                    st.markdown(f"**House:** {hero_row['Brand']}")
                st.info("Curating recommendations...")

            # Wyniki
            results = get_simple_recommendations(selected_perfume, df)
            
            if not results.empty:
                st.markdown("### ✨ You might also like")
                
                for _, row in results.iterrows():
                    with st.container():
                        rc1, rc2 = st.columns([1, 3])
                        with rc1:
                            if 'Image URL' in df.columns and pd.notna(row['Image URL']):
                                st.image(row['Image URL'], use_container_width=True)
                        with rc2:
                            st.subheader(row['Name'])
                            if 'Brand' in df.columns:
                                st.caption(f"By {row['Brand']}")
                            if 'Main Accords' in df.columns:
                                st.write(f"**Notes:** {str(row['Main Accords'])[:50]}...")
                        st.markdown("---")
        else:
            st.error("Perfume details not found.")

else:
    st.error("Critical Error: 'scentsational_data.csv' not found.")

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("© 2026 Magdalena Romaniecka | Data & Web Analytics Portfolio")