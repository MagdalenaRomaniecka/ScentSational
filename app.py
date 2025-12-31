import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. LUXURY STYLING & CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(page_title="ScentSational | Atelier", layout="wide")

st.markdown("""
    <style>
    /* FONTS IMPORT */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Lato:wght@300;400;700&display=swap');

    /* BACKGROUND: Deep Black/Charcoal Satin */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #1a1a1a 0%, #050505 70%);
        color: #E0E0E0;
        font-family: 'Lato', sans-serif;
    }

    /* --- TYPOGRAPHY HIERARCHY --- */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #D4AF37 !important; /* Classic Gold */
        text-align: center;
        font-weight: 500;
        letter-spacing: 1px;
    }
    
    h1 { font-size: 3rem !important; margin-bottom: 0px; text-transform: uppercase; letter-spacing: 4px; }
    .subtitle {
        font-family: 'Lato', sans-serif;
        text-align: center;
        color: #888;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 3rem;
    }

    /* --- CUSTOM METRIC FRAMES --- */
    div[data-testid="metric-container"] {
        background-color: transparent;
        border: 1px solid #333; /* Subtelna ramka */
        border-left: 1px solid #333;
        border-right: 1px solid #333;
        padding: 20px 10px;
        text-align: center;
        transition: 0.3s;
    }
    div[data-testid="metric-container"]:hover {
        border-color: #D4AF37; /* Złota poświata po najechaniu */
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.1);
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Playfair Display', serif;
        color: #F0E68C;
        font-size: 28px !important;
    }
    div[data-testid="stMetricLabel"] {
        font-family: 'Lato', sans-serif;
        text-transform: uppercase;
        font-size: 11px !important;
        letter-spacing: 2px;
        color: #aaa;
    }

    /* --- TABS STYLING (BIGGER & CENTERED) --- */
    button[data-baseweb="tab"] {
        font-size: 16px !important;
        font-family: 'Lato', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #888 !important;
        margin: 0 20px;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #D4AF37 !important;
        border-bottom: 2px solid #D4AF37 !important;
    }
    div[data-baseweb="tab-list"] {
        justify-content: center;
        margin-bottom: 30px;
    }

    /* --- PERFUME LIST ROW (The "Index Card" Look) --- */
    .perfume-row {
        border-bottom: 1px solid #222;
        padding: 25px 0;
        transition: 0.3s;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        margin-bottom: 10px;
        background: rgba(255,255,255,0.01);
    }
    .perfume-row:hover {
        background: rgba(255,255,255,0.02);
        border-bottom: 1px solid #D4AF37;
    }
    
    .row-brand {
        font-family: 'Lato', sans-serif;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        color: #D4AF37; /* Gold Brand */
        margin-bottom: 5px;
    }
    .row-name {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem; /* Większa nazwa, ale szeryfowa */
        color: #fff;
        font-weight: 500;
        margin-bottom: 10px;
        font-style: italic;
    }
    .row-rating {
        font-family: 'Lato', sans-serif;
        font-size: 0.8rem;
        color: #888;
        border: 1px solid #444;
        padding: 4px 12px;
        border-radius: 50px;
        margin-bottom: 15px;
        display: inline-block;
    }

    /* LINK BUTTON */
    .row-link {
        text-decoration: none;
        color: #000;
        background-color: #D4AF37;
        padding: 8px 20px;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: bold;
        transition: 0.3s;
        display: inline-block;
        margin-top: 15px;
    }
    .row-link:hover {
        background-color: #fff;
        color: #000;
    }

    /* --- SIDEBAR --- */
    section[data-testid="stSidebar"] {
        background-color: #080808;
        border-right: 1px solid #222;
    }
    .sidebar-text {
        color: #888;
        font-size: 0.85rem;
        margin-bottom: 20px;
        font-family: 'Lato', sans-serif;
    }
    .sidebar-header {
        color: #D4AF37;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.9rem;
        margin-top: 20px;
        margin-bottom: 10px;
        border-bottom: 1px solid #333;
        padding-bottom: 5px;
    }

    /* SEARCH INPUT */
    .stTextInput input {
        background-color: transparent !important;
        border: 1px solid #333;
        color: #D4AF37 !important;
        text-align: center;
        font-family: 'Playfair Display', serif;
        font-size: 1.2rem;
        padding: 10px;
    }
    .stTextInput input:focus {
        border-color: #D4AF37;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA ENGINE
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    file_path = 'scentsational_data.csv'
    df = None
    try:
        df = pd.read_csv(file_path, sep=';', encoding='latin1', on_bad_lines='skip', engine='python')
    except Exception:
        return None

    if 'Perfume' in df.columns: df = df.rename(columns={'Perfume': 'Name'})
    if 'url' not in df.columns and 'link' in df.columns: df = df.rename(columns={'link': 'url'})
    
    # Fix Ratings
    if 'Rating Value' in df.columns:
        df['Rating Value'] = df['Rating Value'].astype(str).str.replace(',', '.').apply(pd.to_numeric, errors='coerce')

    # Join Notes
    accord_cols = ['mainaccord1', 'mainaccord2', 'mainaccord3', 'mainaccord4', 'mainaccord5']
    existing_accord_cols = [c for c in accord_cols if c in df.columns]
    if existing_accord_cols:
        df['Main Accords'] = df[existing_accord_cols].apply(lambda x: ', '.join(x.dropna().astype(str)), axis=1)
        df['Main Accords'] = df['Main Accords'].replace('', 'Notes unavailable')
        # Extract Primary Accord for Chart
        df['Primary Accord'] = df[existing_accord_cols[0]].astype(str) if len(existing_accord_cols) > 0 else "Unknown"
    else:
        df['Main Accords'] = "Notes unavailable"
        df['Primary Accord'] = "Unknown"
        
    return df

def main():
    # --- SIDEBAR (English & Clean) ---
    with st.sidebar:
        st.markdown("<div class='sidebar-header'>ATELIER CONTROL</div>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-text'>Current Mode: <span style='color:#D4AF37'>Discovery (Lite)</span></div>", unsafe_allow_html=True)
        
        st.markdown("<div class='sidebar-header'>AI ENGINE</div>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-text'>Use our neural network to find your olfactory signature based on chemical similarity.</div>", unsafe_allow_html=True)
        
        st.markdown("""
            <a href="https://huggingface.co/spaces/MagdalenaRomaniecka/ScentSational-Fragrantica-LFS" target="_blank" style="
                display: block; text-align: center; border: 1px solid #D4AF37; color: #D4AF37; padding: 12px; text-decoration: none; 
                font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; transition: 0.3s;">
               LAUNCH AI CORE
            </a>
        """, unsafe_allow_html=True)

    # --- HEADER ---
    st.markdown("<h1>SCENTSATIONAL</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>The Fragrance Intelligence Platform</div>", unsafe_allow_html=True)

    df = load_data()
    if df is None: return

    # --- METRICS (ELEGANT FRAMES) ---
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculation
    top_note = "Woody" # Fallback
    if 'Main Accords' in df.columns:
        try:
            all_notes = df[df['Main Accords'] != 'Notes unavailable']['Main Accords'].astype(str).str.cat(sep=', ')
            from collections import Counter
            nl = [x.strip() for x in all_notes.split(',') if x.strip()]
            if nl: top_note = Counter(nl).most_common(1)[0][0].capitalize()
        except: pass
        
    avg_rating = "-"
    if 'Rating Value' in df.columns: avg_rating = f"{df['Rating Value'].mean():.2f}"

    col1.metric("Collection Size", f"{len(df):,}".replace(",", " "))
    col2.metric("Designers", f"{df['Brand'].nunique()}" if 'Brand' in df.columns else "-")
    col3.metric("Trending Note", top_note)
    col4.metric("Avg Score", avg_rating)

    st.write("") # Spacer

    # --- TABS ---
    tab_analytics, tab_explorer = st.tabs(["MARKET INSIGHTS", "CATALOGUE EXPLORER"])

    # === TAB 1: INSIGHTS ===
    with tab_analytics:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<h3>Top Designers by Volume</h3>", unsafe_allow_html=True)
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
                st.plotly_chart(fig, use_container_width=True)

        with c2:
            # ZMIANA WYKRESU: Zamiast Rating Distribution -> Olfactory Landscape
            st.markdown("<h3>Olfactory Landscape</h3>", unsafe_allow_html=True)
            if 'Primary Accord' in df.columns:
                # Count top 10 primary accords
                accord_counts = df['Primary Accord'].value_counts().head(10)
                
                fig2 = go.Figure(go.Bar(
                    x=accord_counts.values, y=accord_counts.index, orientation='h',
                    marker=dict(color='#D4AF37', opacity=0.8)
                ))
                fig2.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Lato", color="#bbb"), 
                    yaxis=dict(autorange="reversed"), xaxis_title="Number of Perfumes",
                    margin=dict(l=0, r=0, t=20, b=0), height=350,
                )
                st.plotly_chart(fig2, use_container_width=True)

    # === TAB 2: EXPLORER ===
    with tab_explorer:
        st.markdown("<div style='text-align: center; margin-bottom: 10px; color: #666; font-size: 0.8rem; letter-spacing: 2px;'>SEARCH THE ARCHIVES</div>", unsafe_allow_html=True)
        search_query = st.text_input("", placeholder="Type a brand or note...")

        # Centered Filters
        col_f_space, col_f1, col_f2, col_f3, col_f_space2 = st.columns([2, 1, 1, 1, 2])
        filter_type = None
        with col_f1: 
            if st.button("Top Rated"): filter_type = "high_rated"
        with col_f2:
            if st.button("Woody"): search_query = "woody"
        with col_f3:
            if st.button("Floral"): search_query = "floral"

        # Filtering
        filtered_df = df.copy()
        if filter_type == "high_rated" and 'Rating Value' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Rating Value'] >= 4.5]
        if search_query:
            mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
            filtered_df = filtered_df[mask]

        st.markdown(f"<div style='text-align: center; color: #444; margin: 30px 0; letter-spacing: 1px;'>{len(filtered_df)} SCENTS DISCOVERED</div>", unsafe_allow_html=True)
        
        # --- NEW ELEGANT LIST LAYOUT (Slim Rows) ---
        for index, row in filtered_df.head(40).iterrows():
            brand = row.get('Brand', 'Unknown Brand')
            name = row.get('Name', 'Unknown Name')
            notes = row.get('Main Accords', 'N/A')
            rating = row.get('Rating Value', 0)
            url = row.get('url', None)

            # Rating Display
            try: rating_val = float(rating)
            except: rating_val = 0
            
            link_html = ""
            if url and str(url).startswith('http'):
                link_html = f'<a href="{url}" target="_blank" class="row-link">Explore on Fragrantica</a>'

            # Kontener wiersza
            st.markdown(f"""
                <div class="perfume-row">
                    <div class="row-brand">{brand}</div>
                    <div class="row-name">{name}</div>
                    <div class="row-rating">Score: {rating_val:.2f} / 5.0</div>
                </div>
            """, unsafe_allow_html=True)
            
            # COLLAPSIBLE NOTES (Rozwijane, żeby nie śmiecić)
            with st.expander("View Olfactory Profile & Links"):
                st.markdown(f"<div style='text-align:center; color:#ccc; margin-bottom:10px;'><i>{notes}</i></div>", unsafe_allow_html=True)
                if link_html:
                    st.markdown(f"<div style='text-align:center;'>{link_html}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()