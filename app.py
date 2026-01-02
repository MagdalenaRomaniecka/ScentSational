import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
        h1 { font-size: 2.2rem !important; }
        div[data-testid="column"] { width: 100% !important; flex: 1 1 auto !important; }
        .stImage { max-width: 100% !important; }
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

# --- DATA LOADING & AI ENGINE ---
@st.cache_data
def load_and_process_data():
    """
    Loads CSV and computes the AI Similarity Matrix ON THE FLY.
    No external .npy file needed.
    """
    try:
        # 1. Load Data (Robust CSV handling)
        df = pd.read_csv('scentsational_data.csv', encoding='latin1', on_bad_lines='skip')
        df.columns = df.columns.str.strip()
        
        # 2. Create AI Features (The "Brain")
        # We combine important text columns to create a "profile" for each perfume
        # Adjust column names below based on what you actually have in CSV
        text_columns = ['Main Accords', 'Description', 'Brand', 'Notes']
        
        # Fill missing values with empty string
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].fillna('')
            else:
                df[col] = '' # Create empty col if missing to prevent error
                
        # Combine text for analysis
        df['combined_features'] = df['Main Accords'] + " " + df['Description'] + " " + df['Brand'] + " " + df['Notes']
        
        # 3. Calculate Cosine Similarity (Math)
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(df['combined_features'])
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
        return df, cosine_sim
        
    except Exception as e:
        st.error(f"Data Processing Error: {e}")
        return None, None

df, similarity_matrix = load_and_process_data()

# --- RECOMMENDATION LOGIC ---
def get_recommendations(perfume_name, df, matrix, top_n=4):
    try:
        # Map perfume names to index
        indices = pd.Series(df.index, index=df['Name']).drop_duplicates()
        
        if perfume_name not in indices:
            return None
            
        idx = indices[perfume_name]
        
        # Get pairwise similarity scores
        sim_scores = list(enumerate(matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n+1] # Skip self
        
        perfume_indices = [i[0] for i in sim_scores]
        return df.iloc[perfume_indices]
    except Exception as e:
        return None

# --- MAIN UI ---
st.title("ScentSational")
st.markdown("### *AI-Powered Fragrance Concierge*")

if df is not None and similarity_matrix is not None:
    
    # SEARCH INPUT
    perfume_list = sorted(df['Name'].astype(str).unique().tolist())
    
    selected_perfume = st.selectbox(
        "Select your signature scent:",
        options=[""] + perfume_list,
        index=0
    )

    if selected_perfume:
        st.markdown("---")
        
        # HERO SECTION
        # Safe logical indexing
        hero_row_list = df[df['Name'] == selected_perfume]
        if not hero_row_list.empty:
            hero_row = hero_row_list.iloc[0]
            
            c1, c2 = st.columns([1, 2])
            with c1:
                if 'Image URL' in df.columns and pd.notna(hero_row['Image URL']):
                    st.image(hero_row['Image URL'], use_container_width=True)
            with c2:
                st.markdown(f"## **{selected_perfume}**")
                if 'Brand' in df.columns:
                    st.markdown(f"**House:** {hero_row['Brand']}")
                st.info("Analyzing olfactory profile...")

            # RESULTS
            results = get_recommendations(selected_perfume, df, similarity_matrix)
            
            if results is not None and not results.empty:
                st.markdown("### ✨ Recommended for You")
                
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
                                st.write(f"**Notes:** {str(row['Main Accords'])[:100]}...")
                        st.markdown("---")
        else:
            st.error("Error finding perfume details.")

else:
    st.error("Critical Error: Could not load data from 'scentsational_data.csv'")

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("© 2026 Magdalena Romaniecka | Data & Web Analytics Portfolio")