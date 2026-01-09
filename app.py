import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. APP CONFIGURATION & GLOBAL SETTINGS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ScentSational | Atelier",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. VISUAL STYLING (DARK LUXURY THEME)
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    /* Headers - Gold Color */
    h1, h2, h3 {
        color: #D4AF37 !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 300;
    }
    /* Sidebar Background */
    [data-testid="stSidebar"] {
        background-color: #161a24;
        border-right: 1px solid #333;
    }
    /* Metrics Styling */
    div[data-testid="metric-container"] {
        background-color: #1e2530;
        border: 1px solid #333;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    div[data-testid="metric-container"] label {
        color: #D4AF37 !important; /* Gold Label */
    }
    /* Custom Links */
    a {
        color: #D4AF37 !important;
        text-decoration: none;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. DATA LOADING & PREPROCESSING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    try:
        # Load dataset
        df = pd.read_csv("scentsational_data.csv")
        
        # Normalize column names (strip spaces)
        df.columns = [c.strip() for c in df.columns]
        
        # Ensure numeric columns are actually numeric
        if 'Rating' in df.columns:
            df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
        
        if 'Votes' in df.columns:
            df['Votes'] = pd.to_numeric(df['Votes'], errors='coerce')

        return df
    
    except FileNotFoundError:
        st.error("⚠️ Database file 'scentsational_data.csv' not found. Please upload the dataset.")
        return pd.DataFrame()

df = load_data()

# ----------------