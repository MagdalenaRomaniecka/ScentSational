import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.neighbors import NearestNeighbors

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="ScentSational | Perfume Recommender",
    page_icon="👃",
    layout="wide"
)

# --- STYLE ---
st.markdown("""
    <style>
    .main {
        background-color: #fafafa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_resource
def load_data():
    try:
        # Load CSV and Matrix
        df = pd.read_csv("final_fragrantica_data.csv")
        similarity_matrix = np.load("hybrid_similarity.npy")
        
        # Sync dimensions
        if len(df) > similarity_matrix.shape[0]:
            df = df.iloc[:similarity_matrix.shape[0]].copy()
            
        # Fit KNN model
        model = NearestNeighbors(metric='cosine', algorithm='brute')
        model.fit(similarity_matrix)
        
        return df, similarity_matrix, model
    except Exception as e:
        st.error(f"Error loading assets: {e}")
        return None, None, None

df, similarity_matrix, model_knn = load_data()

# --- HEADER ---
st.title("👃 ScentSational")
st.subheader("Hybrid Niche Fragrance Recommendation System")
st.markdown("---")

if df is not None:
    # Identify the Name column (assumed to be the first one)
    name_col = df.columns[0]
    perfume_list = sorted(df[name_col].unique())

    # --- SELECTION UI ---
    col_input, col_empty = st.columns([1, 1])
    with col_input:
        selected_perfume = st.selectbox("Select a perfume you currently enjoy:", perfume_list)
        n_recommendations = st.slider("Number of recommendations:", 5, 10, 5)

    if st.button("Generate Recommendations"):
        # Find index and neighbors
        idx = df[df[name_col] == selected_perfume].index[0]
        distances, indices = model_knn.kneighbors(
            similarity_matrix[idx].reshape(1, -1), 
            n_neighbors=n_recommendations + 1
        )
        
        # Prepare results
        results = []
        for i in range(1, len(distances.flatten())):
            res_idx = indices.flatten()[i]
            score = 1 - distances.flatten()[i]
            results.append({
                "Perfume Name": df.iloc[res_idx][name_col],
                "Match Score (%)": round(score * 100, 2)
            })
        
        res_df = pd.DataFrame(results)

        # --- RESULTS VISUALIZATION ---
        st.write(f"### Results for: **{selected_perfume}**")
        
        tab1, tab2 = st.tabs(["📊 Visualization", "📋 Data Table"])
        
        with tab1:
            # Match Score Chart (Plotly)
            fig = px.bar(
                res_df, 
                x='Match Score (%)', 
                y='Perfume Name', 
                orientation='h',
                title="Recommendation Confidence Levels",
                color='Match Score (%)',
                color_continuous_scale='RdBu',
                text='Match Score (%)'
            )
            fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=400)
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.table(res_df)

# --- SIDEBAR ---
st.sidebar.image("https://img.icons8.com/ios/100/000000/perfume-bottle.png", width=100)
st.sidebar.header("About ScentSational")
st.sidebar.info("""
This application uses a hybrid algorithm combining:
- **Feature Analysis:** Scents and notes profiles.
- **User Preference:** Fragrantica community ratings.

*Created for Niche Perfume Enthusiasts.*
""")