import streamlit as st
import pandas as pd
import numpy as np
import os

# -----------------------------------------------------------------------------
# CONFIGURATION & DESIGN SYSTEM (Dark Luxury)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="ScentSational AI", layout="centered")

st.markdown("""
    <style>
    /* Global Theme */
    .stApp { background-color: #0E0E0E; color: #E0E0E0; }
    
    /* Typography */
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Helvetica Neue', sans-serif; text-align: center; }
    
    /* Widgets */
    .stSelectbox > div > div { background-color: #1A1A1A; color: #D4AF37; border: 1px solid #D4AF37; }
    
    /* Buttons */
    .stButton > button { background-color: #D4AF37; color: #0E0E0E; border: none; width: 100%; font-weight: bold; }
    .stButton > button:hover { background-color: #B59024; color: #FFFFFF; }
    
    /* Cards */
    .perfume-card {
        background-color: #161616; border: 1px solid #333; border-left: 3px solid #D4AF37;
        padding: 20px; margin-bottom: 15px; border-radius: 5px;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        color: #D4AF37 !important;
        font-weight: bold;
        border: 1px solid #333;
        background-color: #161616;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA ENGINE
# -----------------------------------------------------------------------------
@st.cache_data
def load_resources():
    try:
        # 1. Load Data
        df = pd.read_csv('scentsational_data.csv')
        similarity_matrix = np.load('hybrid_similarity.npy')
        
        # 2. Integrity Check
        n_perfumes = len(df)
        n_matrix_rows = similarity_matrix.shape[0]
        
        if n_perfumes != n_matrix_rows:
            st.error(f"❌ CRITICAL DATA MISMATCH: CSV ({n_perfumes}) vs Matrix ({n_matrix_rows})")
            return None, None

        if 'Name' not in df.columns:
            st.error("❌ MISSING COLUMN: 'Name'")
            return None, None
            
        return df, similarity_matrix

    except Exception as e:
        st.error(f"❌ SYSTEM ERROR: {e}")
        return None, None

def get_recommendations(perfume_name, df, matrix, top_k=5):
    try:
        idx = df[df['Name'] == perfume_name].index[0]
        sim_scores = list(enumerate(matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_k+1]
        return df.iloc[[i[0] for i in sim_scores]]
    except:
        return None

# -----------------------------------------------------------------------------
# MAIN INTERFACE
# -----------------------------------------------------------------------------
def main():
    st.title("⚜️ SCENTSATIONAL")
    st.markdown("<p style='text-align: center; color: #888; letter-spacing: 2px; margin-bottom: 30px;'>AI-POWERED FRAGRANCE CONCIERGE</p>", unsafe_allow_html=True)
    
    df, similarity_matrix = load_resources()

    if df is not None:
        available_perfumes = sorted(df['Name'].unique())
        
        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            selected_perfume = st.selectbox("SELECT YOUR SIGNATURE SCENT:", options=available_perfumes)
            st.write("")
            search_btn = st.button("CURATE MY COLLECTION")

        # --- RESULTS SECTION ---
        if search_btn:
            st.divider()
            results = get_recommendations(selected_perfume, df, similarity_matrix)
            
            if results is not None:
                for _, row in results.iterrows():
                    brand = row.get('Brand', "Niche House")
                    accords = row.get('Main Accords', "Exclusive Notes")
                    st.markdown(f"""
                        <div class="perfume-card">
                            <h3 style="margin:0; color:#E0E0E0;">{row['Name']}</h3>
                            <p style="color:#D4AF37; text-transform:uppercase; font-size:0.8em;">{brand}</p>
                            <p style="color:#BBB; font-style:italic; font-size:0.9em;">{accords}</p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No recommendations found.")

        # --- ANALYTICS SECTION (HIDDEN GEM) ---
        st.write("")
        st.write("")
        st.write("")
        with st.expander("📊 VIEW DATA ANALYTICS & INSIGHTS"):
            st.markdown("### 🧬 The DNA of Niche Perfumery")
            st.write("An analysis of over 5,000 niche fragrances to determine the most dominant olfactory profiles.")
            
            # Check if images exist before displaying
            col_a, col_b = st.columns(2)
            
            with col_a:
                if os.path.exists("brands.png"):
                    st.image("brands.png", caption="Top 20 Niche Brands by Volume")
                else:
                    st.info("Brand analysis chart loading...")
            
            with col_b:
                if os.path.exists("wordcloud.jpg"):
                    st.image("wordcloud.jpg", caption="Most Common Notes (Olfactory Cloud)")
                else:
                    st.info("Wordcloud chart loading...")
                    
            st.caption("Data Source: Fragrantica Niche Collection | Analysis: Python (Pandas, Matplotlib, WordCloud)")

if __name__ == "__main__":
    main()