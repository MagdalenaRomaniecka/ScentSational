import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. KONFIGURACJA I STYL "VOGUE" (CSS)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="ScentSational | Haute Couture", layout="wide")

st.markdown("""
    <style>
    /* IMPORT CZCIONEK: Playfair Display (Nagłówki) i Montserrat (Tekst) */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Montserrat:wght@300;400;600&display=swap');

    /* TŁO: SATYNOWA CZERŃ (Gradient) */
    .stApp {
        background: radial-gradient(circle at center, #1a1a1a 0%, #000000 100%);
        color: #E0E0E0;
        font-family: 'Montserrat', sans-serif;
    }

    /* NAGŁÓWKI - STYL VOGUE */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #C5A059 !important; /* Złoto */
        text-align: center;
        font-weight: 700;
        letter-spacing: 1px;
    }
    
    h1 { font-size: 3.5rem !important; margin-bottom: 0.5rem; text-transform: uppercase; }
    h3 { font-size: 1.8rem !important; margin-top: 2rem; border-bottom: 1px solid #333; padding-bottom: 10px; }

    /* ELEGANCKIE METRYKI (Metrics) */
    div[data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid #333;
        border-top: 3px solid #C5A059;
        padding: 15px;
        text-align: center;
        border-radius: 0px; /* Ostry, elegancki kąt */
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Playfair Display', serif;
        color: #F0E68C;
        font-size: 32px;
    }
    div[data-testid="stMetricLabel"] {
        font-family: 'Montserrat', sans-serif;
        text-transform: uppercase;
        font-size: 12px;
        letter-spacing: 2px;
        color: #888;
        justify-content: center;
    }

    /* KARTA PERFUM (LUKSUSOWA RAMKA) */
    .perfume-card {
        background-color: rgba(20, 20, 20, 0.6); /* Półprzezroczystość */
        border: 1px solid #444;
        border-radius: 2px;
        padding: 30px;
        margin-bottom: 25px;
        text-align: center;
        transition: all 0.4s ease;
    }
    .perfume-card:hover {
        border-color: #C5A059; /* Złota poświata po najechaniu */
        background-color: rgba(30, 30, 30, 0.9);
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(197, 160, 89, 0.1);
    }
    .perfume-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.8em;
        color: #fff;
        margin-bottom: 5px;
        letter-spacing: 1px;
    }
    .perfume-brand {
        font-family: 'Montserrat', sans-serif;
        text-transform: uppercase;
        color: #C5A059;
        font-size: 0.8em;
        letter-spacing: 3px;
        margin-bottom: 20px;
        font-weight: 600;
    }
    .perfume-notes {
        font-size: 0.9em;
        color: #ccc;
        font-style: italic;
        margin-bottom: 25px;
        line-height: 1.6;
        font-weight: 300;
    }
    
    /* LINK BUTTON (FRAGRANTICA) */
    .fragrantica-link {
        display: inline-block;
        text-decoration: none;
        color: #000;
        background: linear-gradient(45deg, #B59024, #F0E68C, #B59024);
        padding: 10px 25px;
        font-size: 0.75em;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: bold;
        transition: 0.5s;
        border-radius: 0px; /* Kwadratowe brzegi high-fashion */
    }
    .fragrantica-link:hover {
        color: #fff;
        background: #000;
        border: 1px solid #C5A059;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #080808;
        border-right: 1px solid #222;
    }
    
    /* Input Styling */
    .stTextInput input {
        background-color: transparent !important;
        border: none;
        border-bottom: 2px solid #333;
        color: #C5A059 !important;
        font-family: 'Playfair Display', serif;
        font-size: 1.2em;
        text-align: center;
    }
    .stTextInput input:focus {
        border-bottom: 2px solid #C5A059;
        box-shadow: none;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA LOADING (BEZ UTRATY DANYCH)
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    file_path = 'scentsational_data.csv'
    df = None
    
    try:
        # Wczytujemy z kodowaniem Latin-1 i separatorem ;
        df = pd.read_csv(
            file_path, 
            sep=';', 
            encoding='latin1',
            on_bad_lines='skip', 
            engine='python'
        )
    except Exception as e:
        st.error(f"Błąd wczytywania bazy: {e}")
        return None

    # Normalizacja nazw kolumn
    if 'Perfume' in df.columns:
        df = df.rename(columns={'Perfume': 'Name'})
    
    # Obsługa URL (jeśli kolumna nazywa się inaczej, np 'Link', kod spróbuje ją znaleźć)
    if 'url' not in df.columns and 'link' in df.columns:
         df = df.rename(columns={'link': 'url'})

    # Naprawa ocen (zamiana 1,42 na 1.42)
    if 'Rating Value' in df.columns:
        df['Rating Value'] = df['Rating Value'].astype(str).str.replace(',', '.').apply(pd.to_numeric, errors='coerce')

    # Łączenie nut w jedną kolumnę (zachowując te wiersze, które nie mają nut!)
    accord_cols = ['mainaccord1', 'mainaccord2', 'mainaccord3', 'mainaccord4', 'mainaccord5']
    existing_accord_cols = [c for c in accord_cols if c in df.columns]
    
    if existing_accord_cols:
        df['Main Accords'] = df[existing_accord_cols].apply(
            lambda x: ', '.join(x.dropna().astype(str)), axis=1
        )
        # Zamień puste stringi na "N/A"
        df['Main Accords'] = df['Main Accords'].replace('', 'Notes unavailable')
    else:
        df['Main Accords'] = "Notes unavailable"

    return df

def main():
    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("## ⚜️ ATELIER")
        st.info("Tryb: **Discovery Mode**")
        st.markdown("---")
        st.write("Skorzystaj z AI, aby odkryć swoją olfaktoryczną sygnaturę.")
        st.markdown("""
            <a href="https://huggingface.co/spaces/MagdalenaRomaniecka/ScentSational-Fragrantica-LFS" target="_blank" style="
                display: block; text-align: center; color: #000; background: #C5A059; padding: 10px; text-decoration: none; font-weight: bold; margin-top: 20px; text-transform: uppercase; letter-spacing: 1px;">
               ✨ LAUNCH AI CORE
            </a>
        """, unsafe_allow_html=True)

    # --- HEADER ---
    st.title("SCENTSATIONAL")
    st.markdown("<h3 style='border:none; margin-top:0;'>The Fragrance Intelligence Platform</h3>", unsafe_allow_html=True)
    st.write("")

    df = load_data()
    
    if df is None:
        return

    # --- METRICS (ELEGANT ROW) ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Collection Size", f"{len(df):,}".replace(",", " "))
    m2.metric("Designers", f"{df['Brand'].nunique()}" if 'Brand' in df.columns else "-")
    
    # Trending Accord Calculation
    top_note = "-"
    if 'Main Accords' in df.columns:
        try:
            all_notes = df[df['Main Accords'] != 'Notes unavailable']['Main Accords'].astype(str).str.cat(sep=', ')
            from collections import Counter
            note_list = [x.strip() for x in all_notes.split(',') if x.strip()]
            if note_list:
                top_note = Counter(note_list).most_common(1)[0][0].capitalize()
        except:
            pass
    m3.metric("Trending Note", top_note)
    
    avg_rating = "-"
    if 'Rating Value' in df.columns:
        avg = df['Rating Value'].mean()
        avg_rating = f"{avg:.2f}"
    m4.metric("Avg Score", avg_rating)

    st.markdown("---")
    
    # --- TABS ---
    tab_analytics, tab_explorer = st.tabs(["📊 MARKET INSIGHTS", "🔎 CATALOGUE"])

    # === TAB 1: ELEGANT ANALYTICS ===
    with tab_analytics:
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("### Top Designers by Volume")
            if 'Brand' in df.columns:
                top_brands = df['Brand'].value_counts().head(10).reset_index()
                top_brands.columns = ['Brand', 'Count']
                
                # Złoty wykres słupkowy
                fig = go.Figure(go.Bar(
                    x=top_brands['Count'],
                    y=top_brands['Brand'],
                    orientation='h',
                    marker=dict(color='#C5A059', line=dict(color='#F0E68C', width=1))
                ))
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Montserrat", color="#E0E0E0"),
                    yaxis=dict(autorange="reversed"),
                    margin=dict(l=0, r=0, t=30, b=0), height=400
                )
                st.plotly_chart(fig, use_container_width=True)

        with col_chart2:
            st.markdown("### Rating Distribution")
            if 'Rating Value' in df.columns:
                # Grupujemy oceny, żeby wykres był czytelniejszy (zaokrąglenie do 0.5)
                ratings = df['Rating Value'].dropna().apply(lambda x: round(x * 2) / 2)
                rating_counts = ratings.value_counts().sort_index()
                
                fig2 = go.Figure(go.Bar(
                    x=rating_counts.index,
                    y=rating_counts.values,
                    marker=dict(color='#C5A059', opacity=0.8)
                ))
                fig2.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Montserrat", color="#E0E0E0"),
                    xaxis_title="Score (1-5)",
                    margin=dict(l=0, r=0, t=30, b=0), height=400
                )
                st.plotly_chart(fig2, use_container_width=True)

    # === TAB 2: EXPLORER (VOGUE CARDS) ===
    with tab_explorer:
        st.markdown("<div style='text-align: center; margin-bottom: 20px;'>Search the Archives</div>", unsafe_allow_html=True)
        
        search_query = st.text_input("", placeholder="Type a brand (e.g. Chanel) or note (e.g. Jasmine)...")
        
        # Filtry w jednej linii, wycentrowane
        c1, c2, c3, c4, c5 = st.columns([1,2,2,2,1])
        filter_type = None
        with c2: 
            if st.button("✨ Top Rated (>4.5)"): filter_type = "high_rated"
        with c3:
            if st.button("🪵 Woody"): search_query = "woody"
        with c4:
            if st.button("🌸 Floral"): search_query = "floral"

        st.write("")

        # Logika filtrowania (zachowawcza - nie usuwamy N/A jeśli nie trzeba)
        filtered_df = df.copy()
        
        if filter_type == "high_rated" and 'Rating Value' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Rating Value'] >= 4.5]
        
        if search_query:
            # Szukamy wszędzie (case insensitive)
            mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
            filtered_df = filtered_df[mask]

        st.markdown(f"<div style='text-align: center; color: #888; margin-bottom: 30px;'>Found {len(filtered_df)} olfactory signatures</div>", unsafe_allow_html=True)
        
        # Wyświetlanie kart
        for index, row in filtered_df.head(40).iterrows(): # Limit 40 dla płynności
            brand = row.get('Brand', 'Unknown Brand')
            name = row.get('Name', 'Unknown Name')
            notes = row.get('Main Accords', 'Notes unavailable')
            rating = row.get('Rating Value', 'N/A')
            url = row.get('url', '#') # Pobieramy link
            
            # Jeśli brak linku, ukrywamy przycisk, lub dajemy pusty
            link_html = ""
            if url and str(url).startswith('http'):
                link_html = f'<a href="{url}" target="_blank" class="fragrantica-link">Odkryj na Fragrantica</a>'
            
            st.markdown(f"""
                <div class="perfume-card">
                    <div class="perfume-brand">{brand}</div>
                    <div class="perfume-title">{name}</div>
                    <div style="color: #C5A059; font-size: 1.2em; margin: 10px 0;">
                        {'★' * int(float(rating) if isinstance(rating, (int, float)) else 0)} 
                        <span style="font-size:0.8em; color:#666;">({rating})</span>
                    </div>
                    <div class="perfume-notes">{notes}</div>
                    {link_html}
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()