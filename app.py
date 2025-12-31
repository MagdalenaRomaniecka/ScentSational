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
    .perfume-title { color: #D4AF37; font-size: 1.3em; font-weight: bold; margin: 0; text-transform: uppercase; }
    .perfume-brand { color: #BBB; font-weight: bold; font-size: 0.9em; margin-bottom: 5px; }
    .perfume-sub { color: #888; font-size: 0.85em; margin-bottom: 10px; }
    .perfume-notes { color: #E0E0E0; font-size: 0.9em; font-style: italic; border-top: 1px solid #333; padding-top: 10px; }
    .highlight { color: #D4AF37; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA LOADING (CUSTOMIZED FOR YOUR CSV)
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    file_path = 'scentsational_data.csv'
    df = None
    
    # 1. Load with Semicolon Separator (Crucial for your file)
    try:
        df = pd.read_csv(file_path, sep=';', on_bad_lines='skip', engine='python')
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None

    # 2. Rename Columns to Standard Names
    # Your file has 'Perfume' -> We want 'Name'
    if 'Perfume' in df.columns:
        df = df.rename(columns={'Perfume': 'Name'})

    # 3. Fix Ratings (Convert "1,42" to 1.42 float)
    if 'Rating Value' in df.columns:
        # Replace comma with dot and convert to float
        df['Rating Value'] = df['Rating Value'].astype(str).str.replace(',', '.').astype(float)

    # 4. Create "Main Accords" by joining mainaccord1-5
    accord_cols = ['mainaccord1', 'mainaccord2', 'mainaccord3', 'mainaccord4', 'mainaccord5']
    # Check which of these actually exist in dataframe
    existing_accord_cols = [c for c in accord_cols if c in df.columns]
    
    if existing_accord_cols:
        # Join them with a comma, ignoring empty values
        df['Main Accords'] = df[existing_accord_cols].apply(
            lambda x: ', '.join(x.dropna().astype(str)), axis=1
        )
    else:
        df['Main Accords'] = "Notes unavailable"

    return df

def main():
    # --- SIDEBAR ---
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
        return

    # --- TOP METRICS ---
    st.markdown("### 📈 Database Overview")
    m1, m2, m3, m4 = st.columns(4)
    
    m1.metric("Total Perfumes", f"{len(df)}")
    m2.metric("Unique Brands", f"{df['Brand'].nunique()}" if 'Brand' in df.columns else "N/A")
    
    # Calculate trending accord from the new combined column
    top_note = "N/A"
    if 'Main Accords' in df.columns:
        try:
            all_notes = df['Main Accords'].astype(str).str.cat(sep=', ')
            from collections import Counter
            # Split by comma and strip whitespace
            note_list = [x.strip() for x in all_notes.split(',') if x.strip() != '']
            most_common = Counter(note_list).most_common(1)
            if most_common:
                top_note = most_common[0][0]
        except:
            pass
    
    m3.metric("Trending Accord", top_note)
    
    avg_rating = "N/A"
    if 'Rating Value' in df.columns:
        avg = df['Rating Value'].mean()
        avg_rating = f"{avg:.2f}"
    m4.metric("Avg Rating", avg_rating)

    st.write("")
    
    # --- TABS ---
    tab_analytics, tab_explorer = st.tabs(["📊 LIVE ANALYTICS", "🔍 CATALOG EXPLORER"])

    # === TAB 1: ANALYTICS ===
    with tab_analytics:
        st.markdown("### Market Trends")
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("#### 🏆 Top Brands by Volume")
            if 'Brand' in df.columns:
                top_brands = df['Brand'].value_counts().head(10).reset_index()
                top_brands.columns = ['Brand', 'Count']
                
                fig = px.bar(top_brands, x='Count', y='Brand', orientation='h',
                             color='Count', color_continuous_scale=['#806000', '#D4AF37'])
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#E0E0E0', yaxis=dict(autorange="reversed"),
                    margin=dict(l=0, r=0, t=0, b=0), height=350
                )
                st.plotly_chart(fig, use_container_width=True)

        with col_chart2:
            st.markdown("#### ⭐ Rating Distribution")
            if 'Rating Value' in df.columns:
                fig2 = px.histogram(df, x='Rating Value', nbins=20,
                                    color_discrete_sequence=['#D4AF37'])
                fig2.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#E0E0E0', margin=dict(l=0, r=0, t=0, b=0),
                    height=350, xaxis_title="Rating (1-5)", yaxis_title="Count", bargap=0.1
                )
                st.plotly_chart(fig2, use_container_width=True)

    # === TAB 2: EXPLORER ===
    with tab_explorer:
        st.markdown("### 🔎 Browse Collection")
        
        search_query = st.text_input("Search Collection:", placeholder="Type a brand (e.g. 'Xerjoff') or note (e.g. 'Rose')...")
        
        st.write("Quick Filters:")
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        filter_type = None
        
        if col_f1.button("🔥 High Rated (>4.5)"):
            filter_type = "high_rated"
        if col_f2.button("🌿 Woody Scents"):
            search_query = "woody"
        if col_f3.button("🪵 Fruity Scents"):
            search_query = "fruity"
            
        st.divider()

        filtered_df = df.copy()
        
        if filter_type == "high_rated" and 'Rating Value' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Rating Value'] >= 4.5]
        
        if search_query:
            mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
            filtered_df = filtered_df[mask]

        st.write(f"Found **{len(filtered_df)}** perfumes:")
        
        # Display Cards
        for index, row in filtered_df.head(50).iterrows():
            brand = row.get('Brand', 'Unknown Brand')
            name = row.get('Name', 'Unknown Name')
            notes = row.get('Main Accords', '')
            rating = row.get('Rating Value', 'N/A')
            gender = row.get('Gender', 'Unisex')
            
            st.markdown(f"""
                <div class="perfume-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <p class="perfume-title">{name}</p>
                        <span style="color: #D4AF37; font-weight: bold; font-size: 1.1em;">⭐ {rating}</span>
                    </div>
                    <p class="perfume-brand">{brand}</p>
                    <p class="perfume-sub">{gender}</p>
                    <p class="perfume-notes">🎶 {notes}</p>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()