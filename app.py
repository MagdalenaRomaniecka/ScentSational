import streamlit as st
import pandas as pd
import os

# -----------------------------------------------------------------------------
# 1. CONFIGURATION & DESIGN SYSTEM (Dark Luxury)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="ScentSational Discovery", layout="wide")

st.markdown("""
    <style>
    /* Global Background */
    .stApp { background-color: #0E0E0E; color: #E0E0E0; }
    
    /* Typography */
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Helvetica Neue', sans-serif; }
    
    /* Metrics & Cards */
    [data-testid="stMetricValue"] { color: #D4AF37; }
    .css-1r6slb0 { background-color: #161616; border: 1px solid #333; }
    
    /* The Bridge Button (Golden Link) */
    .bridge-button {
        display: inline-block;
        background-color: #D4AF37;
        color: #000000;
        padding: 15px 30px;
        text-align: center;
        text-decoration: none;
        font-size: 18px;
        font-weight: bold;
        border-radius: 5px;
        border: 1px solid #B59024;
        width: 100%;
        margin-top: 20px;
        transition: 0.3s;
    }
    .bridge-button:hover {
        background-color: #F4CF57;
        color: #000000;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.5);
    }
    
    /* Image Captions */
    .caption { text-align: center; color: #888; font-style: italic; margin-top: 5px; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA LOADING (Lightweight - No AI Model)
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('scentsational_data.csv')
        return df
    except FileNotFoundError:
        return None

def main():
    # --- HEADER ---
    col_logo, col_title = st.columns([1, 4])
    with col_title:
        st.title("⚜️ SCENTSATIONAL | DISCOVERY")
        st.markdown("### Interactive Niche Perfume Analytics")

    df = load_data()
    
    if df is None:
        st.error("Data file not found. Please upload 'scentsational_data.csv'.")
        return

    # --- THE BRIDGE (Sidebar) ---
    with st.sidebar:
        st.header("🤖 AI CONCIERGE")
        st.info("Looking for personalized recommendations based on your favorite scent?")
        # LINK DO HUGGING FACE (Tu wstawimy Twój link do Space'a, jak już go postawimy)
        st.markdown("""
            <a href="https://huggingface.co/spaces/MagdalenaRomaniecka/ScentSational-Fragrantica-LFS" target="_blank" class="bridge-button">
               🚀 LAUNCH AI ENGINE
            </a>
        """, unsafe_allow_html=True)
        st.write("")
        st.markdown("---")
        st.write("**Database Stats:**")
        st.metric("Niche Perfumes", len(df))
        st.metric("Unique Brands", df['Brand'].nunique() if 'Brand' in df.columns else 0)

    # --- MAIN CONTENT TABS ---
    tab1, tab2 = st.tabs(["📊 MARKET INSIGHTS", "🔍 CATALOG EXPLORER"])

    # TAB 1: VISUAL ANALYTICS (Twoje Wykresy)
    with tab1:
        st.subheader("The DNA of Niche Perfumery")
        st.write("Visualizing the most dominant notes and exclusive brands in our collection.")
        
        # Row 1: Wordcloud & Brands
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ☁️ Olfactory Word Cloud")
            if os.path.exists("wordcloud.jpg"):
                st.image("wordcloud.jpg", use_container_width=True)
                st.markdown("<p class='caption'>Most frequent fragrance notes analyzed from 5,000+ descriptions.</p>", unsafe_allow_html=True)
            else:
                st.warning("Wordcloud image not found.")

        with col2:
            st.markdown("#### 🏆 Top Niche Brands")
            if os.path.exists("brands.png"):
                st.image("brands.png", use_container_width=True)
                st.markdown("<p class='caption'>Leading houses by number of releases in the dataset.</p>", unsafe_allow_html=True)
            else:
                st.warning("Brands chart image not found.")

        # Row 2: Notes Analysis (New Chart)
        st.divider()
        st.markdown("#### 🎵 Top 20 Olfactory Notes")
        if os.path.exists("notes.png"):
            st.image("notes.png", use_container_width=True)
            st.markdown("<p class='caption'>A breakdown of the most popular ingredients in niche perfumery.</p>", unsafe_allow_html=True)
        else:
             st.warning("Notes chart image not found.")


    # TAB 2: SIMPLE EXPLORER (Baza danych)
    with tab2:
        st.subheader("Browse the Collection")
        
        # Simple Search
        search_term = st.text_input("Search by Name, Brand, or Note:", placeholder="e.g. Oud, Creed, Rose...")
        
        if search_term:
            # Simple string matching
            mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
            results = df[mask].head(20) # Limit to 20 to keep it fast
            
            st.write(f"Found {len(results)} matches (showing top 20):")
            st.dataframe(
                results[['Name', 'Brand', 'Main Accords', 'Rating Value']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Enter a keyword above to explore the database.")

if __name__ == "__main__":
    main()