import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. CONFIGURATION & DESIGN SYSTEM
# -----------------------------------------------------------------------------
st.set_page_config(page_title="ScentSational Discovery", layout="wide")

st.markdown("""
    <style>
    /* Global Styling */
    .stApp { background-color: #0E0E0E; color: #E0E0E0; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Helvetica Neue', sans-serif; }
    
    /* Custom Metric Styling */
    div[data-testid="stMetricValue"] { color: #D4AF37; font-size: 24px; }
    div[data-testid="stMetricLabel"] { color: #888; }
    div[data-testid="metric-container"] {
        background-color: #161616;
        border: 1px solid #333;
        padding: 10px;
        border-radius: 5px;
        border-left: 3px solid #D4AF37;
    }

    /* Bridge Button */
    .bridge-button {
        display: block;
        background: linear-gradient(45deg, #B59024, #D4AF37);
        color: #000;
        padding: 15px;
        text-align: center;
        text-decoration: none;
        font-weight: bold;
        border-radius: 8px;
        margin-top: 20px;
        transition: transform 0.2s;
    }
    .bridge-button:hover {
        transform: scale(1.02);
        color: #000;
        text-decoration: none;
    }

    /* Luxury Card for Results */
    .perfume-card {
        background-color: #161616;
        border: 1px solid #333;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        transition: 0.3s;
    }
    .perfume-card:hover {
        border-color: #D4AF37;
        background-color: #1A1A1A;
    }
    .perfume-title { color: #D4AF37; font-size: 1.2em; font-weight: bold; margin: 0; }
    .perfume-brand { color: #888; text-transform: uppercase; font-size: 0.8em; margin-bottom: 10px; }
    .perfume-notes { color: #CCC; font-size: 0.9em; font-style: italic; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA LOADING & PROCESSING (ROBUST VERSION)
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    file_path = 'scentsational_data.csv'
    df = None
    
    # Attempt 1: Standard load with bad lines skipping
    try:
        df = pd.read_csv(file_path, on_bad_lines='skip', engine='python')
    except Exception:
        pass 
        
    # Attempt 2: Latin-1 encoding with bad lines skipping
    if df is None:
        try:
            df = pd.read_csv(file_path, encoding='latin1', on_bad_lines='skip')
        except:
            pass 

    # Attempt 3: Last resort - ignore encoding errors and skip bad lines
    if df is None:
        try:
            df = pd.read_csv(file_path, encoding='utf-8', encoding_errors='ignore', on_bad_lines='skip')
        except Exception as e:
            st.error(f"Critical data loading error: {e}")
            return None

    # Column name standardization
    if 'Brand' not in df.columns and 'Brand_Clean' in df.columns:
        df['Brand'] = df['Brand_Clean'] 
            
    return df

def main():
    # --- SIDEBAR (THE BRIDGE) ---
    with st.sidebar:
        st.markdown("## ⚜️ MENU")
        st.info("Currently viewing: **Discovery Mode** (Lite)")
        
        st.markdown("---")
        st.markdown("### 🤖 Need AI Recommendations?")
        st.write("Switch to our advanced AI engine to find perfumes based on deep similarity.")
        st.markdown("""
            <a href="https://huggingface.co/spaces/MagdalenaRomaniecka/ScentSational-Fragrantica-LFS" target="_blank" class="bridge-button">
               🚀 LAUNCH AI CORE
            </a>
        """, unsafe_allow_html=True)

    # --- HEADER ---
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("SCENTSATIONAL | INSIGHTS")
        st.markdown("Interactive Market Analysis & Catalog Explorer")

    df = load_data()
    
    if df is None:
        st.error("Data missing or corrupted. Please ensure 'scentsational_data.csv' is valid.")
        return

    # --- TOP METRICS ROW ---
    st.markdown("### 📈 Database Overview")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Perfumes", f"{len(df)}")
    m2.metric("Unique Brands", f"{df['Brand'].nunique()}" if 'Brand' in df.columns else "N/A")
    
    # Logic for trending note
    top_note = "Oud" 
    if 'Main Accords' in df.columns:
        try:
            all_notes = df['Main Accords'].astype(str).str.cat(sep=', ')
            from collections import Counter
            most_common = Counter(x.strip() for x in all_notes.split(',')).most_common(1)
            if most_common:
                top_note = most_common[0][0]
        except:
            pass
            
    m3.metric("Trending Note", top_note)
    
    # Safe rating calculation
    avg_rating = "N/A"
    if 'Rating Value' in df.columns:
        try:
            # Convert to numeric, forcing errors to NaN, then calculate mean
            avg_rating = f"{pd.to_numeric(df['Rating Value'], errors='coerce').mean():.2f}"
        except:
            pass
    m4.metric("Avg Rating", avg_rating)

    st.write("")
    
    # --- TABS ---
    tab_analytics, tab_explorer = st.tabs(["📊 LIVE ANALYTICS", "🔍 CATALOG EXPLORER"])

    # === TAB 1: MODERN ANALYTICS (PLOTLY) ===
    with tab_analytics:
        st.markdown("### Market Trends")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("#### 🏆 Top Niche Brands")
            if 'Brand' in df.columns:
                top_brands = df['Brand'].value_counts().head(10).reset_index()
                top_brands.columns = ['Brand', 'Count']
                
                fig = px.bar(top_brands, x='Count', y='Brand', orientation='h',
                             color='Count', color_continuous_scale=['#806000', '#D4AF37'])
                
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#E0E0E0',
                    yaxis=dict(autorange="reversed"),
                    margin=dict(l=0, r=0, t=0, b=0),
                    height=350,
                    xaxis_title="", yaxis_title=""
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Brand data not available.")

        with col_chart2:
            st.markdown("#### ⭐ Rating Distribution")
            if 'Rating Value' in df.columns:
                # Ensure numeric for histogram
                df_chart = df.copy()
                df_chart['Rating Value'] = pd.to_numeric(df_chart['Rating Value'], errors='coerce')
                
                fig2 = px.histogram(df_chart, x='Rating Value', nbins=20,
                                    color_discrete_sequence=['#D4AF37'])
                
                fig2.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#E0E0E0',
                    margin=dict(l=0, r=0, t=0, b=0),
                    height=350,
                    xaxis_title="Rating (1-5)", yaxis_title="Count",
                    bargap=0.1
                )
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.warning("Rating data not available.")

    # === TAB 2: EXPLORER (BETTER UI) ===
    with tab_explorer:
        st.markdown("### 🔎 Browse Collection")
        
        search_query = st.text_input("Search Collection:", placeholder="Type a brand (e.g. 'Creed') or note (e.g. 'Vanilla')...")
        
        st.write("Quick Filters:")
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        filter_type = None
        
        if col_f1.button("🔥 High Rated (>4.5)"):
            filter_type = "high_rated"
        if col_f2.button("🌿 Vetiver Scents"):
            search_query = "vetiver"
        if col_f3.button("🪵 Oud Scents"):
            search_query = "oud"
        
        st.divider()

        filtered_df = df.copy()
        
        # Safe filtering for high rated
        if filter_type == "high_rated":
             if 'Rating Value' in filtered_df.columns:
                filtered_df['Rating Value'] = pd.to_numeric(filtered_df['Rating Value'], errors='coerce')
                filtered_df = filtered_df[filtered_df['Rating Value'] >= 4.5]
        
        if search_query:
            mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
            filtered_df = filtered_df[mask]

        st.write(f"Found **{len(filtered_df)}** perfumes:")
        
        for index, row in filtered_df.head(50).iterrows():
            brand = row.get('Brand', 'Unknown Brand')
            name = row.get('Name', 'Unknown Name')
            notes = row.get('Main Accords', 'Notes unavailable')
            rating = row.get('Rating Value', 'N/A')
            
            st.markdown(f"""
                <div class="perfume-card">
                    <div style="display: flex; justify-content: space-between;">
                        <p class="perfume-title">{name}</p>
                        <span style="color: #D4AF37;">⭐ {rating}</span>
                    </div>
                    <p class="perfume-brand">{brand}</p>
                    <p class="perfume-notes">🎶 {notes}</p>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()