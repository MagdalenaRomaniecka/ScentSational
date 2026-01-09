import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import re
from typing import Optional, List

# -----------------------------------------------------------------------------
# 1. APP CONFIGURATION & GLOBAL SETTINGS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ScentSational | Atelier", 
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Clear cache to ensure fresh data load on restart
st.cache_data.clear()

# -----------------------------------------------------------------------------
# 2. UI & STYLE DEFINITIONS (CSS)
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    /* --- TYPOGRAPHY & FONTS --- */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=Montserrat:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"], .stMarkdown, .stRadio, .stSelectbox, .stTextInput, .stMultiSelect, div, span, p {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 400 !important; 
        color: #E0E0E0 !important;
        font-size: 0.9rem !important;
    }

    /* --- MAIN CONTAINER BACKGROUND --- */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #1a1a1a 0%, #000000 100%);
    }

    /* --- HEADERS --- */
    h1 {
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 300 !important;
        background: linear-gradient(to bottom, #D4AF37 0%, #F0E68C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: clamp(2rem, 5vw, 3.5rem) !important; 
        text-transform: uppercase;
        letter-spacing: clamp(4px, 1vw, 8px);
        margin: 0;
        padding-top: 10px;
        padding-bottom: 5px;
    }
    
    .sub-header {
        font-family: 'Montserrat', sans-serif !important;
        color: #888;
        font-size: 0.7rem !important;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-top: 0px;
        margin-bottom: 20px;
        text-align: center;
    }

    .header-frame {
        border-bottom: 1px solid rgba(212, 175, 55, 0.15);
        padding-bottom: 10px;
        margin-bottom: 20px;
        background: rgba(10, 10, 10, 0.4);
        text-align: center;
    }

    /* --- INPUT WIDGETS --- */
    .stSelectbox, .stMultiSelect { width: 100%; }
    
    .stSelectbox div[data-baseweb="select"] > div,
    .stMultiSelect div[data-baseweb="select"] > div {
        border: 1px solid rgba(212, 175, 55, 0.4) !important;
        background-color: rgba(10, 10, 10, 0.6) !important;
    }
    .stSelectbox label, .stMultiSelect label { display: none; }

    /* Radio Button Styling */
    div[data-testid="stRadio"] {
        width: 100%;
        display: flex;
        justify-content: center;
        margin-bottom: 15px;
    }
    div[data-testid="stRadio"] > div {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 15px; 
    }
    div[data-testid="stRadio"] label p {
        font-size: 0.85rem !important;
        color: #D4AF37 !important;
        font-weight: 500 !important;
    }

    /* Toggle Switch */
    div[data-testid="stToggle"] {
        justify-content: center;
        margin-top: 20px;
        padding: 8px 25px;
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 50px;
        background: rgba(212, 175, 55, 0.05);
        width: fit-content;
        margin-left: auto;
        margin-right: auto;
    }
    div[data-testid="stToggle"] label p {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        color: #D4AF37 !important;
        letter-spacing: 1px;
    }

    /* --- KPI METRICS --- */
    .gold-metric {
        border: 1px solid rgba(212, 175, 55, 0.2);
        background-color: rgba(255, 255, 255, 0.01);
        padding: 10px;
        text-align: center;
        margin-bottom: 5px;
    }
    .metric-label { color: #D4AF37 !important; font-size: 0.6rem !important; text-transform: uppercase; letter-spacing: 2px; font-weight: 600 !important; }
    .metric-value { font-family: 'Cormorant Garamond', serif !important; font-size: clamp(1.5rem, 3vw, 2rem) !important; color: #F0E68C !important; font-weight: 300; margin-top: 0px; }

    /* --- PRODUCT CARDS --- */
    .perfume-card {
        border: 1px solid rgba(212, 175, 55, 0.15);
        background: rgba(12, 12, 12, 0.9);
        padding: 30px;
        margin: 20px auto;
        max-width: 850px;
        text-align: center;
        box-shadow: 0 15px 40px rgba(0,0,0,0.6);
        border-radius: 4px;
        backdrop-filter: blur(10px);
    }
    
    .brand-emblem {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        border: 1px solid #D4AF37;
        color: #D4AF37;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Montserrat', sans-serif;
        font-size: 1rem;
        font-weight: bold;
        margin: 0 auto 15px auto;
        background: rgba(212, 175, 55, 0.05);
        letter-spacing: 0;
        text-transform: uppercase;
    }

    .row-brand { 
        font-family: 'Montserrat', sans-serif !important;
        font-size: 1rem !important; 
        font-weight: 600 !important; 
        letter-spacing: 2px; 
        color: #D4AF37 !important; 
        margin-bottom: 5px; 
        text-transform: uppercase;
    }
    .row-name { 
        font-family: 'Cormorant Garamond', serif !important; 
        font-size: 1.8rem !important; 
        color: #fff !important; 
        margin-bottom: 5px; 
        font-style: italic; 
    }
    .row-meta {
        font-size: 0.7rem !important;
        color: #888 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 20px;
        border-bottom: 1px solid #333;
        padding-bottom: 10px;
        display: inline-block;
        min-width: 200px;
    }
    .row-rating {
        color: #D4AF37;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 10px;
    }
    .row-notes {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 1.1rem !important;
        color: #AAA !important;
        font-style: italic;
        margin-bottom: 25px;
        line-height: 1.4;
    }

    /* Call to Action Button */
    a.gold-btn {
        text-decoration: none; 
        color: #000 !important; 
        background: #D4AF37; 
        padding: 12px 35px; 
        font-size: 0.75rem !important; 
        font-weight: 600 !important; 
        letter-spacing: 1px; 
        border-radius: 2px; 
        display: inline-block;
        font-family: 'Montserrat', sans-serif !important;
        transition: 0.3s;
        text-transform: uppercase;
    }
    a.gold-btn:hover {
        background: #F0E68C;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
    }
    
    /* --- FOOTER --- */
    .custom-footer {
        text-align: center;
        color: #444;
        font-size: 0.6rem !important;
        margin-top: 80px;
        padding-top: 20px;
        border-top: 1px solid #111;
        font-family: 'Montserrat', sans-serif !important;
        letter-spacing: 0.5px;
        opacity: 0.7;
    }
    .custom-footer a { color: #555 !important; text-decoration: none; }
    .custom-footer a:hover { color: #777 !important; }

    /* --- SIDEBAR & NAVIGATION --- */
    [data-testid="stSidebar"] { background-color: #080808 !important; border-right: 1px solid rgba(212, 175, 55, 0.15); }
    .sidebar-gold-box { border: 1px solid #D4AF37; padding: 20px; background: rgba(212, 175, 55, 0.03); text-align: center; margin-bottom: 20px; }

    .stTabs [data-baseweb="tab-list"] { gap: 30px; justify-content: center; margin-bottom: 30px;}
    .stTabs [data-baseweb="tab"] { letter-spacing: 2px; text-transform: uppercase; font-size: 0.75rem !important;}
    .stTabs [aria-selected="true"] { color: #D4AF37 !important; border-bottom-color: #D4AF37 !important; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def get_initials(text: str) -> str:
    """Generates 2-letter initials for the brand emblem."""
    if not text: return "SC"
    words = str(text).split()
    if not words: return "SC"
    if len(words) == 1:
        return words[0][:2].upper()
    return (words[0][0] + words[-1][0]).upper()

@st.cache_data
def load_data() -> Optional[pd.DataFrame]:
    """
    Loads and preprocesses the fragrance dataset.
    Performs data cleaning, type conversion, and feature engineering.
    """
    try:
        # Load dataset with robust encoding handling
        df = pd.read_csv('scentsational_data.csv', sep=None, encoding='latin1', engine='python')
        df.columns = df.columns.str.strip()
        
        # Column standardization and mapping
        cols = df.columns.tolist()
        brand_col = next((c for c in cols if 'brand' in c.lower()), 'Brand')
        name_col = next((c for c in cols if 'perfume' in c.lower() or 'name' in c.lower()), 'Name')
        rating_col = next((c for c in cols if 'rating' in c.lower()), 'Rating Value')
        gender_col = next((c for c in cols if 'gender' in c.lower()), 'Gender')
        year_col = next((c for c in cols if 'year' in c.lower() or 'date' in c.lower() or 'launch' in c.lower()), 'Year')

        df = df.rename(columns={
            brand_col: 'Brand', name_col: 'Name',
            rating_col: 'Rating Value', gender_col: 'Gender', year_col: 'Year'
        })
        
        # Data Cleaning: Strings
        df['Name'] = df['Name'].astype(str).str.strip()
        df['Brand'] = df['Brand'].astype(str).str.strip()
        
        # Remove cleaning artifacts (e.g., numeric prefixes)
        df['Name'] = df['Name'].str.replace(r'^\d+\s*-\s*', '', regex=True)
        df['Brand'] = df['Brand'].str.replace(r'^\d+\s*-\s*', '', regex=True)
        df['Name'] = df['Name'].str.replace(r'^0+\s+', '', regex=True)
        df = df[~df['Name'].str.match(r'^\d+$')] # Filter out numeric-only names
        
        # Title Case formatting
        df['Name'] = df['Name'].str.replace('-', ' ').str.title()
        df['Brand'] = df['Brand'].str.replace('-', ' ').str.title()
        
        # Numeric conversions
        df['Rating Value'] = pd.to_numeric(df['Rating Value'].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)
        
        # Meta Fields (Gender & Year)
        if 'Gender' not in df.columns: 
            df['Gender'] = "Unisex"
        else: 
            df['Gender'] = df['Gender'].fillna("Unisex")
        
        if 'Year' in df.columns:
            df['Year'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0).astype(int)
            # Filter valid years only
            df['Year'] = df['Year'].apply(lambda x: str(x) if x > 1000 else "")
        else:
            df['Year'] = ""

        # Accord Aggregation for Search
        accord_cols = ['mainaccord1', 'mainaccord2', 'mainaccord3', 'mainaccord4', 'mainaccord5']
        existing_accords = [c for c in accord_cols if c in df.columns]
        df['Main Accords'] = df[existing_accords].apply(lambda x: ', '.join(x.dropna().astype(str)), axis=1)
        
        # Create Search Index for fuzzy filtering
        df['Search_Index'] = df['Name'].str.lower() + " " + df['Brand'].str.lower() + " " + df['Main Accords'].str.lower()
        df = df.sort_values(by=['Brand', 'Name'])
        
        return df
    except Exception as e:
        st.error(f"Critical Data Error: {e}")
        return None

def get_all_notes(df: pd.DataFrame) -> List[str]:
    """Extracts a unique list of all olfactory notes from the dataset."""
    notes_set = set()
    if 'Main Accords' in df.columns:
        for accords in df['Main Accords'].dropna():
            parts = [x.strip() for x in accords.split(',')]
            for p in parts:
                if p: notes_set.add(p.capitalize())
    return sorted(list(notes_set))

# -----------------------------------------------------------------------------
# 4. MAIN APPLICATION LOGIC
# -----------------------------------------------------------------------------
def main():
    # Initialize Data
    df = load_data()
    if df is None: return
    all_notes_list = get_all_notes(df)

    # --- Sidebar Configuration ---
    with st.sidebar:
        st.markdown('<div class="sidebar-gold-box">', unsafe_allow_html=True)
        st.markdown("<p style='color:#D4AF37; font-size:0.8rem; font-weight:bold; letter-spacing:2px;'>AI ENGINE</p>", unsafe_allow_html=True)
        st.write("Unlock chemical DNA search.")
        st.markdown(f'<a href="https://baphomert-scentsational-fragrantica-lfs2.hf.space" target="_blank" style="display:inline-block; background:#D4AF37; color:black; padding:12px 25px; text-decoration:none; font-weight:bold; font-size:0.7rem; letter-spacing:2px; margin-top:10px;">LAUNCH AI CORE</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Header Section ---
    st.markdown('<div class="header-frame"><h1>SCENTSATIONAL</h1><div class="sub-header">The Atelier &bull; Intelligence Platform</div></div>', unsafe_allow_html=True)

    # --- Tab Layout ---
    tab_analytics, tab_catalog = st.tabs(["MARKET INSIGHTS", "DISCOVER SCENTS"])

    # -------------------------------------------------------------------------
    # TAB 1: ANALYTICS DASHBOARD
    # -------------------------------------------------------------------------
    with tab_analytics:
        # Key Performance Indicators (KPIs)
        col_kpi_1, col_kpi_2, col_kpi_3, col_kpi_4 = st.columns([1,1,1,1])
        
        col_kpi_1.markdown(f'<div class="gold-metric"><div class="metric-label">Collection Size</div><div class="metric-value">{len(df):,}</div></div>', unsafe_allow_html=True)
        col_kpi_2.markdown(f'<div class="gold-metric"><div class="metric-label">Designers</div><div class="metric-value">{df["Brand"].nunique()}</div></div>', unsafe_allow_html=True)
        
        trend_note = df["mainaccord1"].mode()[0].capitalize() if "mainaccord1" in df.columns else "N/A"
        col_kpi_3.markdown(f'<div class="gold-metric"><div class="metric-label">Trending Note</div><div class="metric-value">{trend_note}</div></div>', unsafe_allow_html=True)
        
        avg_rating = df[df["Rating Value"] > 0]["Rating Value"].mean()
        col_kpi_4.markdown(f'<div class="gold-metric"><div class="metric-label">Avg Rating</div><div class="metric-value">{avg_rating:.2f}</div></div>', unsafe_allow_html=True)
        
        st.write("") 

        # Visualizations
        col_chart_1, col_chart_2, col_chart_3 = st.columns(3)
        
        with col_chart_1:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.75rem; letter-spacing:2px; font-weight:bold;'>TOP DESIGNERS</p>", unsafe_allow_html=True)
            top_brands = df['Brand'].value_counts().head(10)
            fig_brands = px.bar(x=top_brands.values, y=top_brands.index, orientation='h', color_discrete_sequence=['#D4AF37'])
            fig_brands.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#888", height=300, yaxis={'autorange':'reversed', 'title': ''}, xaxis={'title': ''}, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig_brands, use_container_width=True, config={'staticPlot': True})
            
        with col_chart_2:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.75rem; letter-spacing:2px; font-weight:bold;'>OLFACTORY LANDSCAPE</p>", unsafe_allow_html=True)
            if "mainaccord1" in df.columns:
                top_accords = df['mainaccord1'].value_counts().head(10)
                fig_accords = px.bar(x=top_accords.values, y=top_accords.index, orientation='h', color_discrete_sequence=['#C5A059'])
                fig_accords.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#888", height=300, yaxis={'autorange':'reversed', 'title': ''}, xaxis={'title': ''}, margin=dict(l=0,r=0,t=0,b=0))
                st.plotly_chart(fig_accords, use_container_width=True, config={'staticPlot': True})
                
        with col_chart_3:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.75rem; letter-spacing:2px; font-weight:bold;'>SCORE DISTRIBUTION</p>", unsafe_allow_html=True)
            # Binning ratings for analysis
            score_data = pd.cut(df[df['Rating Value'] > 0]['Rating Value'], bins=[0, 3.5, 4.2, 5], labels=['Standard', 'Premium', 'Masterpiece'])
            fig_pie = px.pie(score_data.value_counts().reset_index(), values='count', names='Rating Value', hole=0.6, color_discrete_sequence=['#2C2C2C', '#96792e', '#F0E68C'])
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#888", height=300, margin=dict(l=0,r=0,t=20,b=0), showlegend=True)
            st.plotly_chart(fig_pie, use_container_width=True)

    # -------------------------------------------------------------------------
    # TAB 2: DISCOVERY ENGINE
    # -------------------------------------------------------------------------
    with tab_catalog:
        st.write("") 
        col_spacer_l, col_center, col_spacer_r = st.columns([1, 4, 1])

        with col_center:
            # 1. Tier Selector
            st.markdown("<p style='text-align:center; color:#666; font-size:0.7rem; letter-spacing:2px; margin-bottom: 5px; text-transform:uppercase;'>Select Quality Grade</p>", unsafe_allow_html=True)
            tier_choice = st.radio(
                "TIER_SELECTOR", 
                ["All Artifacts", "Masterpieces (4.5+)", "Premium (4.0+)", "Classics"],
                horizontal=True,
                label_visibility="collapsed"
            )
            
            st.write("") 
            
            # 2. Search & Filter Bar
            col_search, col_filter = st.columns([1.5, 1], gap="medium")
            
            with col_search:
                search_query = st.selectbox(
                    "SEARCH_HIDDEN",
                    options=sorted(list(df['Name'].unique()) + list(df['Brand'].unique())),
                    index=None,
                    placeholder="🔍 Search Brand or Name...",
                    label_visibility="collapsed"
                )
                
            with col_filter:
                selected_notes = st.multiselect(
                    "NOTES_HIDDEN",
                    options=all_notes_list,
                    placeholder="🧪 Filter by Notes...",
                    label_visibility="collapsed"
                )

            # 3. Advanced Toggle
            strict_mode = st.toggle("Strict Mode (4.5+ Only)")

        # --- Filtering Logic ---
        filtered_df = df.copy()
        
        # Apply Search
        if search_query: 
            filtered_df = filtered_df[(filtered_df['Name'] == search_query) | (filtered_df['Brand'] == search_query)]
        
        # Apply Strict Mode
        if strict_mode: 
            filtered_df = filtered_df[filtered_df['Rating Value'] >= 4.5]
        
        # Apply Tier Logic
        if tier_choice == "Masterpieces (4.5+)": 
            filtered_df = filtered_df[filtered_df['Rating Value'] >= 4.5]
        elif tier_choice == "Premium (4.0+)": 
            filtered_df = filtered_df[(filtered_df['Rating Value'] >= 4.0) & (filtered_df['Rating Value'] < 4.5)]
        elif tier_choice == "Classics": 
            filtered_df = filtered_df[(filtered_df['Rating Value'] > 0) & (filtered_df['Rating Value'] < 4.0)]
        
        # Apply Note Filtering
        if selected_notes:
            for note in selected_notes:
                filtered_df = filtered_df[filtered_df['Search_Index'].str.contains(note.lower())]

        # Results Counter
        st.markdown(f"""
            <div style='text-align:center; margin-top:30px; margin-bottom:20px; border-top:1px solid #333; padding-top:20px;'>
                <span style='color:#666; font-size:0.8rem; letter-spacing:2px; text-transform:uppercase;'>
                    {len(filtered_df)} Olfactory Signatures Found
                </span>
            </div>
        """, unsafe_allow_html=True)

        # --- Render Cards ---
        for _, row in filtered_df.head(20).iterrows():
            # Extract Attributes
            brand = str(row['Brand']).replace('"', '').replace("'", "")
            name = str(row['Name']).replace('"', '').replace("'", "")
            rating = float(row['Rating Value'])
            notes = str(row['Main Accords'])
            link = row.get('url', '#')
            
            initials = get_initials(brand)
            
            # Formatting Metadata
            gender = str(row.get('Gender', 'Unisex')).capitalize()
            year = str(row.get('Year', ''))
            meta_info = f"{gender}"
            if year: meta_info += f" &bull; {year}"

            # Display HTML Card
            st.markdown(f"""
                <div class="perfume-card">
                    <div class="brand-emblem">{initials}</div>
                    <div style="width:100%">
                        <div class="row-brand">{brand}</div>
                        <div class="row-name">{name}</div>
                        <div class="row-meta">{meta_info}</div>
                        <div class="row-rating">★ {rating:.2f}</div>
                        <div class="row-notes">{notes}</div>
                    </div>
                    <a href="{link}" target="_blank" class="gold-btn">FRAGRANTICA</a>
                </div>
            """, unsafe_allow_html=True)

    # --- Footer ---
    st.markdown("""
    <div class="custom-footer">
        ScentSational Atelier v3.0 &bull; Developed by Magdalena Romaniecka &bull; 2026<br>
        Data Source: <a href="https://www.kaggle.com/datasets/olgagmiufana1/fragrantica-com-fragrance-dataset" target="_blank">Fragrantica Dataset (Kaggle)</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
# FORCED UPDATE
