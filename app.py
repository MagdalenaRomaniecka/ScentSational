import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re

# -----------------------------------------------------------------------------
# 1. LUXURY STYLING & CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(page_title="ScentSational | Atelier", layout="wide")

st.markdown("""
    <style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Lato:wght@300;400;700&display=swap');

    /* BACKGROUND */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #151515 0%, #000000 80%);
        color: #E0E0E0;
        font-family: 'Lato', sans-serif;
    }

    /* TYPOGRAPHY - HEADER */
    h1 {
        font-family: 'Playfair Display', serif !important;
        color: #D4AF37 !important;
        text-align: center;
        font-size: 3.5rem !important;
        text-transform: uppercase;
        letter-spacing: 5px;
        margin-bottom: 5px;
        margin-top: 0;
    }
    .subtitle {
        text-align: center;
        color: #888;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 4px;
        margin-bottom: 0;
    }

    /* --- MOBILE OPTIMIZATION --- */
    @media only screen and (max-width: 600px) {
        h1 { font-size: 2.0rem !important; }
        .subtitle { font-size: 0.6rem !important; }
        
        /* Force columns to stack vertically */
        div[data-testid="column"] { 
            width: 100% !important; 
            flex: 1 1 auto !important; 
            min-width: 100% !important;
        }
        
        /* Adjust padding for mobile */
        .perfume-row { padding: 30px 0 !important; }
        .row-brand { font-size: 1.4rem !important; }
        .row-name { font-size: 1.1rem !important; }
    }

    /* --- GOLD FRAME FOR HEADER --- */
    .header-frame {
        border: 1px solid #D4AF37;
        padding: 30px;
        margin-bottom: 40px;
        background: rgba(20, 20, 20, 0.4);
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.05);
    }

    /* --- CUSTOM GOLD METRIC BOX --- */
    .gold-metric {
        border: 1px solid #D4AF37;
        background-color: rgba(255, 255, 255, 0.02);
        padding: 20px;
        text-align: center;
        border-radius: 2px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    .metric-label {
        font-family: 'Lato', sans-serif;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #D4AF37;
        margin-bottom: 10px;
        font-weight: 700;
    }
    .metric-value {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        color: #F0E68C;
        margin: 0;
        line-height: 1;
    }

    /* --- SIDEBAR STATUS --- */
    .status-box {
        border: 1px solid #D4AF37;
        background-color: rgba(212, 175, 55, 0.05);
        color: #D4AF37;
        padding: 15px;
        text-align: center;
        font-size: 0.8rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 20px;
    }

    /* --- SEARCH BAR --- */
    div[data-baseweb="select"] > div {
        background-color: rgba(255,255,255,0.05);
        border-color: #333;
        color: #D4AF37;
    }
    
    /* --- PERFUME ROW (BRAND DOMINANCE) --- */
    .perfume-row {
        border-bottom: 1px solid #1a1a1a;
        padding: 60px 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        transition: 0.4s ease;
    }
    .perfume-row:hover {
        background: radial-gradient(circle, rgba(212,175,55,0.03) 0%, transparent 70%);
        border-bottom: 1px solid #D4AF37;
    }
    
    /* BRAND - HUGE */
    .row-brand {
        font-family: 'Lato', sans-serif;
        font-size: 1.8rem; 
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 5px;
        color: #D4AF37;
        margin-bottom: 15px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.8);
    }
    
    /* NAME - SMALLER */
    .row-name {
        font-family: 'Playfair Display', serif;
        font-size: 1.3rem;
        color: #fff;
        line-height: 1.4;
        margin-bottom: 20px;
        text-transform: capitalize; 
        font-weight: 400;
        opacity: 0.9;
    }
    
    .row-notes {
        font-family: 'Playfair Display', serif;
        font-size: 1rem;
        color: #888;
        font-style: italic;
        margin-bottom: 30px;
        max-width: 600px;
        line-height: 1.6;
    }
    
    /* LINK BUTTON */
    .row-link {
        text-decoration: none !important;
        color: #000 !important;
        background: linear-gradient(90deg, #C5A059, #D4AF37);
        padding: 14px 35px;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-weight: 800;
        transition: 0.3s;
        display: inline-block;
        border: 1px solid #C5A059;
    }
    .row-link:hover {
        background: #000;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
    }
    a.row-link:visited {
        color: #000 !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #050505;
        border-right: 1px solid #222;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA ENGINE
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    # NAZWA PLIKU MUSI BYĆ TAKA JAK PONIŻEJ:
    file_path = 'scentsational_data.csv'
    df = None
    try:
        # Automatyczne wykrywanie separatora i naprawa błędów
        df = pd.read_csv(file_path, sep=None, encoding='latin1', on_bad_lines='skip', engine='python')
    except Exception:
        return None

    # Normalization
    if 'Perfume' in df.columns: df = df.rename(columns={'Perfume': 'Name'})
    if 'url' not in df.columns and 'link' in df.columns: df = df.rename(columns={'link': 'url'})
    
    # Clean Column Names
    df.columns = df.columns.str.strip()

    # --- DEEP CLEANING (REGEX) ---
    if 'Name' in df.columns:
        df['Name'] = df['Name'].astype(str).str.strip()
        df['Name'] = df['Name'].str.replace(r'^\d+\s*', '', regex=True)
        df['Name'] = df['Name'].str.replace('-', ' ').str.title()
        df = df[df['Name'].str.len() > 1]
        df = df[~df['Name'].str.match(r'^[\d\s]+$')]
    
    if 'Brand' in df.columns:
        df['Brand'] = df['Brand'].astype(str).str.replace(r'^\d+\s*', '', regex=True)

    if 'Rating Value' in df.columns:
        df['Rating Value'] = df['Rating Value'].astype(str).str.replace(',', '.').apply(pd.to_numeric, errors='coerce')

    accord_cols = ['mainaccord1', 'mainaccord2', 'mainaccord3', 'mainaccord4', 'mainaccord5']
    existing_accord_cols = [c for c in accord_cols if c in df.columns]
    
    if existing_accord_cols:
        df['Main Accords'] = df[existing_accord_cols].apply(lambda x: ', '.join(x.dropna().astype(str)), axis=1)
        df['Main Accords'] = df['Main Accords'].replace('', 'N/A')
        df['Primary Accord'] = df[existing_accord_cols[0]].astype(str) if len(existing_accord_cols) > 0 else "Unknown"
    else:
        df['Main Accords'] = "N/A"
        df['Primary Accord'] = "Unknown"
        
    return df

def main():
    with st.sidebar:
        st.markdown("<div style='color:#D4AF37; font-size:0.8rem; letter-spacing:2px; margin-bottom:10px;'>ATELIER CONTROL</div>", unsafe_allow_html=True)
        st.markdown("""<div class="status-box">DISCOVERY MODE ACTIVE</div>""", unsafe_allow_html=True)
        
        st.markdown("<div style='color:#D4AF37; font-size:0.8rem; letter-spacing:2px; margin-top:30px; margin-bottom:10px;'>AI ENGINE</div>", unsafe_allow_html=True)
        st.write("Unlock the neural network to find scents based on chemical DNA.")
        st.markdown("""
            <a href="https://huggingface.co/spaces/MagdalenaRomaniecka/ScentSational-Fragrantica-LFS" target="_blank" style="
                display: block; text-align: center; border: 1px solid #D4AF37; color: #D4AF37; padding: 12px; text-decoration: none; 
                font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; margin-top:10px; transition: 0.3s;">
               LAUNCH AI CORE
            </a>
        """, unsafe_allow_html=True)

    # --- HEADER ---
    st.markdown("""
        <div class="header-frame">
            <h1>SCENTSATIONAL</h1>
            <div class="subtitle">The Fragrance Intelligence Platform</div>
        </div>
    """, unsafe_allow_html=True)

    df = load_data()
    if df is None: return

    # --- METRICS ---
    c1, c2, c3, c4 = st.columns(4)
    val1 = f"{len(df):,}".replace(",", " ")
    val2 = f"{df['Brand'].nunique()}" if 'Brand' in df.columns else "-"
    val3 = df['Primary Accord'].mode()[0].capitalize() if 'Primary Accord' in df.columns and not df['Primary Accord'].empty else "-"
    val4 = f"{df['Rating Value'].mean():.2f}" if 'Rating Value' in df.columns else "-"

    def gold_box(label, value):
        return f"""<div class="gold-metric"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>"""

    c1.markdown(gold_box("Collection Size", val1), unsafe_allow_html=True)
    c2.markdown(gold_box("Designers", val2), unsafe_allow_html=True)
    c3.markdown(gold_box("Trending Note", val3), unsafe_allow_html=True)
    c4.markdown(gold_box("Avg Score", val4), unsafe_allow_html=True)

    st.write("")

    # --- TABS ---
    tab_insight, tab_explore = st.tabs(["MARKET INSIGHTS", "CATALOGUE"])

    with tab_insight:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3 style='color:#D4AF37; text-align:center;'>Top Designers</h3>", unsafe_allow_html=True)
            if 'Brand' in df.columns:
                top_brands = df['Brand'].value_counts().head(10).reset_index()
                top_brands.columns = ['Brand', 'Count']
                fig = go.Figure(go.Bar(
                    x=top_brands['Count'], y=top_brands['Brand'], orientation='h',
                    marker=dict(color='#D4AF37', line=dict(color='#F0E68C', width=0.5))
                ))
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Lato", color="#bbb"), yaxis=dict(autorange="reversed"),
                    margin=dict(l=0, r=0, t=20, b=0), height=350
                )
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        with col2:
            st.markdown("<h3 style='color:#D4AF37; text-align:center;'>Olfactory Landscape</h3>", unsafe_allow_html=True)
            if 'Primary Accord' in df.columns:
                accord_counts = df['Primary Accord'].value_counts().head(10)
                fig2 = go.Figure(go.Bar(
                    x=accord_counts.values, y=accord_counts.index, orientation='h',
                    marker=dict(color='#D4AF37', opacity=0.7)
                ))
                fig2.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Lato", color="#bbb"), yaxis=dict(autorange="reversed"),
                    margin=dict(l=0, r=0, t=20, b=0), height=350
                )
                st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    with tab_explore:
        st.markdown("<div style='text-align:center; color:#666; font-size:0.8rem; margin-bottom:5px; letter-spacing:2px;'>SEARCH THE ARCHIVES</div>", unsafe_allow_html=True)
        
        # --- SEARCH LIST GENERATION ---
        unique_brands = set(df['Brand'].dropna().unique())
        unique_names = set(df['Name'].dropna().unique())
        search_options = sorted(list(unique_brands | unique_names))
        
        selected_search = st.selectbox(
            "Type to search...", options=search_options, index=None, 
            placeholder="Type a brand (e.g. Xerjoff) or perfume name (e.g. Accento)...", label_visibility="collapsed"
        )
        
        col_f_space, col_f1, col_f2, col_f3, col_f_space2 = st.columns([2, 1, 1, 1, 2])
        filter_type = None
        with col_f1: 
            if st.button("Top Rated"): filter_type = "high_rated"
        with col_f2: pass
        with col_f3: pass

        filtered_df = df.copy()
        if selected_search:
            mask = (filtered_df['Brand'].astype(str) == selected_search) | (filtered_df['Name'].astype(str) == selected_search)
            if not mask.any(): mask = filtered_df.astype(str).apply(lambda x: x.str.contains(selected_search, case=False)).any(axis=1)
            filtered_df = filtered_df[mask]
        if filter_type == "high_rated": filtered_df = filtered_df[filtered_df['Rating Value'] >= 4.5]

        st.markdown(f"<div style='text-align: center; color: #444; margin: 30px 0; letter-spacing: 1px;'>{len(filtered_df)} SCENTS DISCOVERED</div>", unsafe_allow_html=True)
        
        # --- ROWS ---
        for index, row in filtered_df.head(40).iterrows():
            brand = row.get('Brand', 'Unknown Brand')
            name = row.get('Name', 'Unknown Name')
            notes = row.get('Main Accords', 'N/A')
            rating = row.get('Rating Value', 0)
            url = row.get('url', None)

            try: rating_val = float(rating)
            except: rating_val = 0
            
            link_html = ""
            if url and str(url).startswith('http'):
                link_html = f'<a href="{url}" target="_blank" class="row-link">Explore on Fragrantica</a>'

            st.markdown(f"""
                <div class="perfume-row">
                    <div class="row-brand">{brand}</div>
                    <div class="row-name">{name}</div>
                    <div style="color:#666; font-size:0.8rem; margin-bottom:10px;">Score: {rating_val:.2f} / 5.0</div>
                    <div class="row-notes">{notes}</div>
                    {link_html}
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()