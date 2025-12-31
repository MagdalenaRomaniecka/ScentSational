import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. LUXURY STYLING
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

    /* --- GOLD FRAMES (RAMKI) --- */
    
    /* 1. Ramka Nagłówka */
    .header-frame {
        border: 1px solid #D4AF37;
        padding: 30px;
        margin-bottom: 40px;
        background: rgba(20, 20, 20, 0.4);
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.05);
    }

    /* 2. Ramki Metryk (Liczby) - WYMUSZONE STYLE */
    div[data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid #D4AF37 !important; /* Złota ramka */
        padding: 20px !important;
        border-radius: 2px !important; /* Lekko ścięte rogi */
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        text-align: center;
        transition: 0.3s;
        margin-bottom: 10px;
    }
    div[data-testid="metric-container"]:hover {
        border-color: #F0E68C !important; /* Jaśniejsze złoto po najechaniu */
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.2);
        transform: translateY(-2px);
    }
    
    /* Kolory wewnątrz metryk */
    div[data-testid="stMetricValue"] {
        font-family: 'Playfair Display', serif;
        color: #F0E68C !important; /* Jasne złoto */
        font-size: 32px !important;
    }
    div[data-testid="stMetricLabel"] {
        font-family: 'Lato', sans-serif;
        text-transform: uppercase;
        font-size: 12px !important;
        letter-spacing: 2px;
        color: #D4AF37 !important; /* Ciemniejsze złoto */
    }

    /* --- SEARCH BAR --- */
    div[data-baseweb="select"] > div {
        background-color: rgba(255,255,255,0.05);
        border-color: #333;
        color: #D4AF37;
    }
    
    /* --- PERFUME ROW (BALANCED TYPOGRAPHY) --- */
    .perfume-row {
        border-bottom: 1px solid #1a1a1a;
        padding: 50px 0;
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
    
    /* MARKA - WIĘKSZA I WYRAŹNIEJSZA */
    .row-brand {
        font-family: 'Lato', sans-serif;
        font-size: 1.1rem; /* Zwiększone z 0.75rem */
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 4px;
        color: #D4AF37;
        margin-bottom: 10px;
        opacity: 1; /* Pełna widoczność */
    }
    
    /* NAZWA - MNIEJSZA I BARDZIEJ ELEGANCKA */
    .row-name {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem; /* Zmniejszone z 3rem dla balansu */
        color: #fff;
        line-height: 1.2;
        margin-bottom: 20px;
        text-transform: capitalize; 
        font-weight: 400;
    }
    
    .row-rating {
        font-family: 'Lato', sans-serif;
        font-size: 0.9rem;
        color: #888;
        border: 1px solid #333;
        padding: 5px 15px;
        border-radius: 50px;
        margin-bottom: 25px;
        letter-spacing: 1px;
    }
    .row-notes {
        font-family: 'Playfair Display', serif;
        font-size: 1.1rem;
        color: #ccc;
        font-style: italic;
        margin-bottom: 30px;
        max-width: 600px;
        line-height: 1.6;
    }

    /* LINK BUTTON */
    .row-link {
        text-decoration: none;
        color: #000;
        background: linear-gradient(90deg, #C5A059, #D4AF37);
        padding: 12px 30px;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: bold;
        transition: 0.3s;
        display: inline-block;
        border: 1px solid #C5A059;
    }
    .row-link:hover {
        background: #000;
        color: #D4AF37;
        border: 1px solid #D4AF37;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.2);
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #050505;
        border-right: 1px solid #222;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA ENGINE (SMART CLEANER & FILTER)
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    file_path = 'scentsational_data.csv'
    df = None
    try:
        df = pd.read_csv(file_path, sep=';', encoding='latin1', on_bad_lines='skip', engine='python')
    except Exception:
        return None

    # Rename Columns
    if 'Perfume' in df.columns: df = df.rename(columns={'Perfume': 'Name'})
    if 'url' not in df.columns and 'link' in df.columns: df = df.rename(columns={'link': 'url'})
    
    # --- DATA CLEANING (Usuwanie śmieci typu "0", "09") ---
    if 'Name' in df.columns:
        # 1. Zamień na tekst
        df['Name'] = df['Name'].astype(str)
        # 2. Usuń nazwy krótsze niż 2 znaki (np "0")
        df = df[df['Name'].str.len() > 1]
        # 3. Usuń nazwy, które są samymi cyframi (np "09", "100")
        df = df[~df['Name'].str.match(r'^\d+$')]
        # 4. Formatowanie (usuwanie myślników)
        df['Name'] = df['Name'].str.replace('-', ' ').str.title()
    
    # Fix Ratings
    if 'Rating Value' in df.columns:
        df['Rating Value'] = df['Rating Value'].astype(str).str.replace(',', '.').apply(pd.to_numeric, errors='coerce')

    # Join Notes
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
    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("<div style='color:#D4AF37; font-size:0.8rem; letter-spacing:2px; margin-bottom:10px;'>ATELIER CONTROL</div>", unsafe_allow_html=True)
        st.info("Discovery Mode Active")
        
        st.markdown("<div style='color:#D4AF37; font-size:0.8rem; letter-spacing:2px; margin-top:30px; margin-bottom:10px;'>AI ENGINE</div>", unsafe_allow_html=True)
        st.write("Unlock the neural network to find scents based on chemical DNA.")
        
        st.markdown("""
            <a href="https://huggingface.co/spaces/MagdalenaRomaniecka/ScentSational-Fragrantica-LFS" target="_blank" style="
                display: block; text-align: center; border: 1px solid #D4AF37; color: #D4AF37; padding: 12px; text-decoration: none; 
                font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; margin-top:10px; transition: 0.3s;">
               LAUNCH AI CORE
            </a>
        """, unsafe_allow_html=True)

    # --- HEADER FRAME (GOLD BOX) ---
    st.markdown("""
        <div class="header-frame">
            <h1>SCENTSATIONAL</h1>
            <div class="subtitle">The Fragrance Intelligence Platform</div>
        </div>
    """, unsafe_allow_html=True)

    df = load_data()
    if df is None: return

    # --- METRICS (GOLD BOXES - FORCED STYLE) ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Collection Size", f"{len(df):,}".replace(",", " "))
    c2.metric("Designers", f"{df['Brand'].nunique()}" if 'Brand' in df.columns else "-")
    
    top_note = "Woody"
    if 'Primary Accord' in df.columns:
        top_note = df['Primary Accord'].mode()[0].capitalize() if not df['Primary Accord'].empty else "-"
    c3.metric("Trending Note", top_note)
    
    avg = df['Rating Value'].mean() if 'Rating Value' in df.columns else 0
    c4.metric("Avg Score", f"{avg:.2f}")

    st.write("")

    # --- TABS ---
    tab_insight, tab_explore = st.tabs(["MARKET INSIGHTS", "CATALOGUE"])

    # === TAB 1: INSIGHTS ===
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
                st.plotly_chart(fig, use_container_width=True)

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
                st.plotly_chart(fig2, use_container_width=True)

    # === TAB 2: EXPLORER ===
    with tab_explore:
        st.markdown("<div style='text-align:center; color:#666; font-size:0.8rem; margin-bottom:5px; letter-spacing:2px;'>SEARCH THE ARCHIVES</div>", unsafe_allow_html=True)
        
        # Search List - Cleaned
        search_options = sorted(list(set(df['Brand'].dropna().unique()) | set(df['Name'].dropna().unique())))
        selected_search = st.selectbox(
            "Type to search...", options=search_options, index=None, 
            placeholder="Start typing a brand (e.g. Chanel) or perfume name...", label_visibility="collapsed"
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
        
        # ROWS - BALANCED TYPOGRAPHY
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
                    <div class="row-rating">Score: {rating_val:.2f} / 5.0</div>
                    <div class="row-notes">{notes}</div>
                    {link_html}
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()