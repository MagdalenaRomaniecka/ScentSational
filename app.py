import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. LUXURY STYLING & CONFIGURATION (MOBILE PERFECTED)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="ScentSational | Atelier", layout="wide", initial_sidebar_state="collapsed")

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

    /* --- TYPOGRAPHY (DESKTOP) --- */
    h1 {
        font-family: 'Playfair Display', serif !important;
        color: #D4AF37 !important;
        text-align: center;
        font-size: 3.5rem !important;
        text-transform: uppercase;
        letter-spacing: 5px;
        margin-bottom: 5px;
        margin-top: 0;
        line-height: 1.2;
        word-wrap: break-word; /* Safety */
    }
    .subtitle {
        text-align: center;
        color: #888;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 4px;
        margin-bottom: 0;
    }

    /* --- HEADER FRAME --- */
    .header-frame {
        border: 1px solid #D4AF37;
        padding: 30px;
        margin-bottom: 40px;
        background: rgba(20, 20, 20, 0.4);
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.05);
    }

    /* --- METRIC BOXES --- */
    .gold-metric {
        border: 1px solid #D4AF37;
        background-color: rgba(255, 255, 255, 0.02);
        padding: 15px;
        text-align: center;
        border-radius: 2px;
        margin-bottom: 10px;
        height: 100%;
    }
    .metric-label {
        font-family: 'Lato', sans-serif;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #D4AF37;
        margin-bottom: 5px;
        font-weight: 700;
    }
    .metric-value {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        color: #F0E68C;
        margin: 0;
        line-height: 1;
    }

    /* --- PERFUME ROW --- */
    .perfume-row {
        border-bottom: 1px solid #1a1a1a;
        padding: 40px 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        transition: 0.4s ease;
    }
    .row-brand {
        font-family: 'Lato', sans-serif;
        font-size: 1.8rem; 
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 4px;
        color: #D4AF37;
        margin-bottom: 10px;
        word-break: break-word; /* Prevents overflow */
    }
    .row-name {
        font-family: 'Playfair Display', serif;
        font-size: 1.3rem;
        color: #fff;
        margin-bottom: 15px;
        text-transform: capitalize; 
    }
    .row-notes {
        font-family: 'Playfair Display', serif;
        font-size: 0.95rem;
        color: #888;
        font-style: italic;
        margin-bottom: 25px;
        line-height: 1.5;
    }
    
    /* LINK BUTTON */
    .row-link {
        text-decoration: none !important;
        color: #000 !important;
        background: linear-gradient(90deg, #C5A059, #D4AF37);
        padding: 12px 30px;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 800;
        border: 1px solid #C5A059;
        display: inline-block;
    }

    /* --- MOBILE OPTIMIZATION (CRITICAL FIXES) --- */
    @media only screen and (max-width: 600px) {
        /* Force Title to fit screen width using VW units */
        h1 { 
            font-size: 8vw !important; /* Dynamic sizing based on screen width */
            letter-spacing: 0px !important; /* Remove spacing to save space */
            line-height: 1.1 !important;
        }
        .subtitle { 
            font-size: 0.65rem !important; 
            letter-spacing: 1px !important; 
        }
        .header-frame { 
            padding: 15px 5px !important; /* Minimal padding */
            margin-bottom: 20px; 
        }
        
        /* Adjust Rows */
        .perfume-row { padding: 25px 0; }
        .row-brand { font-size: 1.4rem; letter-spacing: 1px; }
        .row-name { font-size: 1.1rem; }
        
        /* Ensure charts have space */
        .js-plotly-plot { margin-bottom: 10px; }
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
    file_path = 'scentsational_data.csv'
    try:
        df = pd.read_csv(file_path, sep=';', encoding='latin1', on_bad_lines='skip', engine='python')
    except Exception:
        return None

    if 'Perfume' in df.columns: df = df.rename(columns={'Perfume': 'Name'})
    if 'url' not in df.columns and 'link' in df.columns: df = df.rename(columns={'link': 'url'})
    
    # Cleaning
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
        st.info("Discovery Mode Active")
        st.markdown("<div style='color:#D4AF37; font-size:0.8rem; letter-spacing:2px; margin-top:30px; margin-bottom:10px;'>AI ENGINE</div>", unsafe_allow_html=True)
        st.write("Unlock the neural network to find scents based on chemical DNA.")
        st.link_button("🧪 LAUNCH AI CORE", "https://huggingface.co/spaces/MagdalenaRomaniecka/ScentSational-Fragrantica-LFS", use_container_width=True)

    # HEADER
    st.markdown("""
        <div class="header-frame">
            <h1>SCENTSATIONAL</h1>
            <div class="subtitle">The Fragrance Intelligence Platform</div>
        </div>
    """, unsafe_allow_html=True)

    df = load_data()
    if df is None: return

    # METRICS
    c1, c2, c3, c4 = st.columns(4)
    val1 = f"{len(df):,}".replace(",", " ")
    val2 = f"{df['Brand'].nunique()}" if 'Brand' in df.columns else "-"
    val3 = df['Primary Accord'].mode()[0].capitalize() if 'Primary Accord' in df.columns and not df['Primary Accord'].empty else "-"
    val4 = f"{df['Rating Value'].mean():.2f}" if 'Rating Value' in df.columns else "-"

    def gold_box(label, value):
        return f"""<div class="gold-metric"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>"""

    with c1: st.markdown(gold_box("Collection", val1), unsafe_allow_html=True)
    with c2: st.markdown(gold_box("Designers", val2), unsafe_allow_html=True)
    with c3: st.markdown(gold_box("Trending", val3), unsafe_allow_html=True)
    with c4: st.markdown(gold_box("Avg Score", val4), unsafe_allow_html=True)

    st.write("")

    # TABS
    tab_insight, tab_explore = st.tabs(["MARKET INSIGHTS", "CATALOGUE"])

    # --- NUCLEAR CHART CONFIG ---
    # staticPlot: True sprawia, że wykres jest jak obrazek (zero interakcji).
    # To gwarantuje, że przewijanie strony na telefonie zawsze zadziała.
    chart_config = {
        'staticPlot': True, 
        'displayModeBar': False
    }

    with tab_insight:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h3 style='color:#D4AF37; text-align:center; font-size:1.2rem;'>Top Designers</h3>", unsafe_allow_html=True)
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
                    margin=dict(l=0, r=0, t=10, b=0), height=350,
                    dragmode=False
                )
                st.plotly_chart(fig, use_container_width=True, config=chart_config)

        with col2:
            st.markdown("<h3 style='color:#D4AF37; text-align:center; font-size:1.2rem;'>Olfactory Landscape</h3>", unsafe_allow_html=True)
            if 'Primary Accord' in df.columns:
                accord_counts = df['Primary Accord'].value_counts().head(10)
                fig2 = go.Figure(go.Bar(
                    x=accord_counts.values, y=accord_counts.index, orientation='h',
                    marker=dict(color='#D4AF37', opacity=0.7)
                ))
                fig2.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Lato", color="#bbb"), yaxis=dict(autorange="reversed"),
                    margin=dict(l=0, r=0, t=10, b=0), height=350,
                    dragmode=False
                )
                st.plotly_chart(fig2, use_container_width=True, config=chart_config)

    with tab_explore:
        st.markdown("<div style='text-align:center; color:#666; font-size:0.7rem; margin-bottom:5px; letter-spacing:2px;'>SEARCH THE ARCHIVES</div>", unsafe_allow_html=True)
        
        unique_brands = set(df['Brand'].dropna().unique())
        unique_names = set(df['Name'].dropna().unique())
        search_options = sorted(list(unique_brands | unique_names))
        
        selected_search = st.selectbox(
            "Search", options=search_options, index=None, 
            placeholder="Type a brand or perfume name...", label_visibility="collapsed"
        )
        
        col_t1, col_t2 = st.columns([1, 3])
        with col_t1:
            show_top_rated = st.toggle("Show Top Rated Only (4.5+)")
        
        filtered_df = df.copy()
        if selected_search:
            mask = (filtered_df['Brand'].astype(str) == selected_search) | (filtered_df['Name'].astype(str) == selected_search)
            if not mask.any(): mask = filtered_df.astype(str).apply(lambda x: x.str.contains(selected_search, case=False)).any(axis=1)
            filtered_df = filtered_df[mask]
            
        if show_top_rated:
            filtered_df = filtered_df[filtered_df['Rating Value'] >= 4.5]

        st.markdown(f"<div style='text-align: center; color: #444; margin: 20px 0; letter-spacing: 1px; font-size:0.8rem;'>{len(filtered_df)} SCENTS DISCOVERED</div>", unsafe_allow_html=True)
        
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
                link_html = f'<a href="{url}" target="_blank" class="row-link">Check Details</a>'

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