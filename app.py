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
    
    /* Headings */
    h1, h2, h3 {
        color: #D4AF37 !important; /* Gold */
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Text Input Styling */
    .stTextInput > div > div > input {
        background-color: #1E1E1E;
        color: #E0E0E0;
        border: 1px solid #D4AF37;
    }
    
    /* Metrics/Cards */
    div[data-testid="metric-container"] {
        background-color: #1A1A1A;
        border: 1px solid #333;
        padding: 10px;
        border-radius: 5px;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #D4AF37;
        color: #0E0E0E;
        border: none;
    }
    .stButton > button:hover {
        background-color: #B5952F;
        color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    """Loads the main dataset and pre-computed similarity matrix."""
    # Ensure these files exist in your folder
    try:
        df = pd.read_csv('perfumes_dataset.csv')
        # similarity_matrix = np.load('hybrid_similarity.npy') # Uncomment when file is ready
        return df
    except FileNotFoundError:
        return None

data = load_data()

# --- MAIN UI LAYOUT ---
st.title("ScentSational")
st.markdown("### *AI-Powered Fragrance Concierge*")

# Check if data loaded correctly
if data is not None:
    # Hero Input Section
    user_input = st.text_input("Enter a perfume you love (e.g., 'Black Opium')", "")

    if user_input:
        st.markdown("---")
        st.write(f"🔍 Analyzing olfactory signature for: **{user_input}**...")
        
        # Placeholder for AI Logic (This simulates the backend processing)
        st.info("Recommendation Engine is processing signatures...")
        
        # UI Structure for Results (Example)
        st.markdown("### Recommended Signature Scents")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 1. Velvet Orchid")
            st.caption("Similarity Score: 98%")
            st.markdown("*Vibe: Dark, Floral, Mystical*")
            
        with col2:
            st.markdown("#### 2. Black Orchid")
            st.caption("Similarity Score: 95%")
            st.markdown("*Vibe: Spicy, Earthy, Intense*")

else:
    st.error("Critical Error: 'perfumes_dataset.csv' not found. Please upload data.")

# --- FOOTER ---
st.markdown("---")
st.caption("© 2026 Magdalena Romaniecka | Data & Web Analytics Portfolio")