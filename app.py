import streamlit as st
import pandas as pd
import numpy as np

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
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA ENGINE WITH INTEGRITY CHECK
# -----------------------------------------------------------------------------
@st.cache_data
def load_resources():
    try:
        # 1. Load Data (Expected filename: scentsational_data.csv)
        df = pd.read_csv('scentsational_data.csv')
        similarity_matrix = np.load('hybrid_similarity.npy')
        
        # 2. INTEGRITY CHECK (Prevents crashing if files mismatch)
        n_perfumes = len(df)
        n_matrix_rows = similarity_matrix.shape[0]
        
        if n_perfumes != n_matrix_rows:
            st.error(f"""
                ❌ CRITICAL DATA MISMATCH:
                - CSV File has {n_perfumes} perfumes.
                - Similarity Matrix has {n_matrix_rows} rows.
                ACTION REQUIRED: Please regenerate the .npy file using the current .csv file.
            """)
            return None, None

        # 3. Column Check
        if 'Name' not in df.columns:
            st.error("❌ MISSING COLUMN: The dataset must contain a 'Name' column.")
            return None, None
            
        return df, similarity_matrix

    except FileNotFoundError as e:
        st.error(f"❌ MISSING FILES: {e}")
        return None, None
    except Exception as e:
        st.error(f"❌ UNEXPECTED ERROR: {e}")
        return None, None

def get_recommendations(perfume_name, df, matrix, top_k=5):
    try:
        idx = df[df['Name'] == perfume_name].index[0]
        sim_scores = list(enumerate(matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_k+1]
        perfume_indices = [i[0] for i in sim_scores]
        return df.iloc[perfume_indices]
    except Exception:
        return None

# -----------------------------------------------------------------------------
# MAIN INTERFACE
# -----------------------------------------------------------------------------
def main():
    st.title("⚜️ SCENTSATIONAL")
    st.markdown("<p style='text-align: center; color: #888; letter-spacing: 2px; margin-bottom: 30px;'>AI-POWERED FRAGRANCE CONCIERGE</p>", unsafe_allow_html=True)
    
    df, similarity_matrix = load_resources()

    if df is not None and similarity_matrix is not None:
        
        available_perfumes = sorted(df['Name'].unique())
        
        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            selected_perfume = st.selectbox("SELECT YOUR SIGNATURE SCENT:", options=available_perfumes)
            st.write("")
            search_btn = st.button("CURATE MY COLLECTION")

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

if __name__ == "__main__":
    main()