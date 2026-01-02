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
    
    /* MOBILE OPTIMIZATION */
    @media only screen and (max-width: 600px) {
        h1 { font-size: 2.0rem !important; }
        h2 { font-size: 1.5rem !important; }
        .stButton button { width: 100%; }
        /* Stack columns vertically on mobile */
        div[data-testid="column"] { width: 100% !important; flex: 1 1 auto !important; }
        /* Adjust images on mobile */
        img { max-width: 100% !important; height: auto !important; }
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
        # 1. Smart Load: Engine python + sep=None pozwala automatycznie wykryć separator (; lub ,)
        df = pd.read_csv('scentsational_data.csv', encoding='latin1', sep=None, engine='python', on_bad_lines='skip')
        
        # 2. Safety Fix: Usuwamy spacje z nazw kolumn (np. "Name " -> "Name") - to naprawia KeyError
        df.columns = df.columns.str.strip()
        
        # 3. Rename columns if necessary (failsafe)
        # Jeśli z jakiegoś powodu kolumna nazywa się z małej litery, naprawiamy to
        df.rename(columns={'name': 'Name', 'brand': 'Brand', 'image_url': 'Image URL'}, inplace=True)
        
        return df
    except Exception as e:
        return None

df = load_data()

# --- LOGIC ENGINE ---
def get_recommendations(selected_perfume, df):
    """
    Returns recommendations based on Brand match or random discovery.
    """
    try:
        # Get target row
        target_row = df[df['Name'] == selected_perfume].iloc[0]
        recs = pd.DataFrame()
        
        # 1. Same Brand Strategy
        if 'Brand' in df.columns:
            brand = target_row['Brand']
            recs = df[(df['Brand'] == brand) & (df['Name'] != selected_perfume)]
        
        # 2. Fill with random if strictly filtered
        if len(recs) < 4:
            remaining = 4 - len(recs)
            pool = df[df['Name'] != selected_perfume]
            # Avoid error if pool is smaller than sample size
            n_sample = min(remaining, len(pool))
            if n_sample > 0:
                random_picks = pool.sample(n=n_sample)
                recs = pd.concat([recs, random_picks])
            
        return recs.head(4)
    except Exception:
        return pd.DataFrame()

# --- MAIN UI ---
st.title("ScentSational")
st.markdown("### *AI-Powered Fragrance Concierge*")

if df is not None:
    # Ensure 'Name' column exists before proceeding
    if 'Name' in df.columns:
        perfume_list = sorted(df['Name'].astype(str).unique().tolist())
        
        selected_perfume = st.selectbox(
            "Select your signature scent:",
            options=[""] + perfume_list,
            index=0
        )

        if selected_perfume:
            st.markdown("---")
            
            # Find the row
            row_list = df[df['Name'] == selected_perfume]
            
            if not row_list.empty:
                hero_row = row_list.iloc[0]
                
                # Hero Section (Responsive)
                c1, c2 = st.columns([1, 2])
                with c1:
                    if 'Image URL' in df.columns and pd.notna(hero_row['Image URL']):
                        st.image(hero_row['Image URL'], use_container_width=True)
                with c2:
                    st.markdown(f"## **{selected_perfume}**")
                    if 'Brand' in df.columns:
                        st.markdown(f"**House:** {hero_row['Brand']}")
                    st.info("Curating recommendations...")

                # Recommendations
                results = get_recommendations(selected_perfume, df)
                
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
                                    # Safe string conversion
                                    notes = str(row['Main Accords'])
                                    st.write(f"**Notes:** {notes[:50]}...")
                            st.markdown("---")
            else:
                st.error("Perfume not found in database.")
    else:
        st.error("Error: Column 'Name' not found in CSV. Please check column headers.")
else:
    st.error("Critical Error: 'scentsational_data.csv' could not be loaded.")

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("© 2026 Magdalena Romaniecka | Data & Web Analytics Portfolio")