import streamlit as st
import pandas as pd
import numpy as np

# --- Page Configuration ---
st.set_page_config(
    page_title="Perfume Recommendation System",
    page_icon="🌸",
    layout="wide"
)

# --- Load Data ---
@st.cache_data
def load_data():
    try:
        # Load cleaned dataframe
        df = pd.read_csv("perfumes_cleaned.csv")
        # Load similarity matrix
        cosine_sim = np.load("hybrid_similarity.npy")
        return df, cosine_sim
    except FileNotFoundError:
        st.error("CRITICAL ERROR: Files 'perfumes_cleaned.csv' or 'hybrid_similarity.npy' not found.")
        st.error("Please ensure these files are in the same directory as app.py.")
        return None, None

# --- Recommendation Function ---
def get_recommendations(perfume_name, df, cosine_sim, indices):
    try:
        idx = indices[perfume_name]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]  # Top 10
        perfume_indices = [i[0] for i in sim_scores]
        return df.iloc[perfume_indices]
    except KeyError:
        return pd.DataFrame()

# --- User Interface (UI) ---
st.title("🌸 Perfume Recommendation System")
st.markdown("Select a perfume you like from the dropdown below to see 10 recommendations based on our hybrid model (analyzing both scent notes and descriptions).")

df, cosine_sim = load_data()

if df is not None and cosine_sim is not None:
    indices = pd.Series(df.index, index=df['Name']).drop_duplicates()
    sorted_perfume_names = sorted(df['Name'].unique())
    
    selected_perfume = st.selectbox(
        "Select a perfume you like:",
        options=sorted_perfume_names,
        index=None,
        placeholder="Start typing or select from list..."
    )
    
    st.divider()

    if selected_perfume:
        st.subheader(f"Recommendations for: {selected_perfume}")
        
        recommendations = get_recommendations(selected_perfume, df, cosine_sim, indices)
        
        if not recommendations.empty:
            cols = st.columns(3)
            for i, (idx, row) in enumerate(recommendations.iterrows()):
                with cols[i % 3]:
                    # Handle potential missing image URLs gracefully
                    if pd.notna(row['Image URL']):
                        st.image(row['Image URL'], width=150)
                    else:
                        st.text("No image available")
                        
                    st.markdown(f"**{row['Name']}**")
                    st.markdown(f"*{row['Brand']}*")
                    
                    # Truncate notes for cleaner display if they exist
                    notes = str(row['Notes'])
                    if len(notes) > 80:
                         st.caption(f"Notes: {notes[:80]}...")
                    else:
                         st.caption(f"Notes: {notes}")

        else:
            st.warning("Could not find recommendations.")