import streamlit as st
import pandas as pd
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ScentSational AI",
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
        /* Forces columns to stack nicely on mobile */
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
    
    /* Metrics/Cards */
    div[data-testid="metric-container"] {
        background-color: #1A1A1A;
        border: 1px solid #333;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    """
    Loads the original .npy matrix and the corrected CSV.
    """
    try:
        # 1. Load CSV (Fixing filename and encoding errors)
        # scentsational_data.csv is the correct file we agreed on
        df = pd.read_csv('scentsational_data.csv', encoding='latin1', on_bad_lines='skip')
        df.columns = df.columns.str.strip()
        
        # 2. Load the original AI Matrix
        similarity_matrix = np.load('hybrid_similarity.npy')
        
        return df, similarity_matrix
    except Exception as e:
        return None, None

df, similarity_matrix = load_data()

# --- ORIGINAL AI LOGIC ---
def get_recommendations(perfume_name, df, matrix, top_n=4):
    try:
        # Look up index
        indices = pd.Series(df.index, index=df['Name']).drop_duplicates()
        
        if perfume_name not in indices:
            return None
            
        idx = indices[perfume_name]
        
        # Get scores from pre-computed matrix
        sim_scores = list(enumerate(matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n+1]
        
        perfume_indices = [i[0] for i in sim_scores]
        return df.iloc[perfume_indices]
    except Exception:
        return None

# --- MAIN UI ---
st.title("ScentSational")
st.markdown("### *AI-Powered Fragrance Concierge*")

if df is not None and similarity_matrix is not None:
    
    # Search Input
    perfume_list = sorted(df['Name'].astype(str).unique().tolist())
    
    selected_perfume = st.selectbox(
        "Select your signature scent:",
        options=[""] + perfume_list,
        index=0
    )

    if selected_perfume:
        st.markdown("---")
        
        # Hero Section
        hero_row_list = df[df['Name'] == selected_perfume]
        if not hero_row_list.empty:
            hero_row = hero_row_list.iloc[0]
            
            # Columns optimized for mobile via CSS
            c1, c2 = st.columns([1, 2])
            with c1:
                if 'Image URL' in df.columns and pd.notna(hero_row['Image URL']):
                    st.image(hero_row['Image URL'], use_container_width=True)
            with c2:
                st.markdown(f"## **{selected_perfume}**")
                if 'Brand' in df.columns:
                    st.markdown(f"**House:** {hero_row['Brand']}")
                st.info("Analyzing olfactory profile...")

            # Recommendations
            results = get_recommendations(selected_perfume, df, similarity_matrix)
            
            if results is not None:
                st.markdown("### ✨ Recommended for You")
                
                for _, row in results.iterrows():
                    with st.container():
                        # Mobile-friendly layout
                        rc1, rc2 = st.columns([1, 3])
                        with rc1:
                            if 'Image URL' in df.columns and pd.notna(row['Image URL']):
                                st.image(row['Image URL'], use_container_width=True)
                        with rc2:
                            st.subheader(row['Name'])
                            if 'Brand' in df.columns:
                                st.caption(f"By {row['Brand']}")
                        st.markdown("---")
        else:
            st.error("Perfume details not found in database.")

else:
    st.error("System Error: Could not load 'scentsational_data.csv' or 'hybrid_similarity.npy'. Check files in repo.")

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("© 2026 Magdalena Romaniecka | Data & Web Analytics Portfolio")