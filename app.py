import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import re

# -----------------------------------------------------------------------------
# 1. LUXURY CONFIGURATION & VISUAL ENGINE
# -----------------------------------------------------------------------------
st.set_page_config(page_title="ScentSational | Atelier", layout="wide")

st.markdown("""
    <style>
    /* IMPORT FONTS: Cormorant (Titles) & Montserrat (Body/UI) */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=Montserrat:wght@200;300;400;500;600&display=swap');

    /* --- GLOBAL TYPOGRAPHY ENFORCEMENT --- */
    html, body, [class*="css"], .stMarkdown, .stRadio, .stCheckbox, .stSelectbox {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 300 !important;
        color: #E0E0E0 !important;
    }

    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #1a1a1a 0%, #000000 100%);
    }

    /* HEADER */
    h1 {
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 300 !important;
        background: linear-gradient(to bottom, #D4AF37 0%, #F0E68C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: clamp(2.5rem, 8vw, 4.5rem) !important;
        text-transform: uppercase;
        letter-spacing: clamp(6px, 1.8vw, 14px);
        margin: 0;
        padding-bottom: 10px;
    }

    .header-frame {
        border-bottom: 1px solid rgba(212, 175, 55, 0.2);
        padding: 30px 0;
        margin-bottom: 30px;
        background: rgba(10, 10, 10, 0.4);
        text-align: center;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] { background-color: #080808 !important; border-right: 1px solid rgba(212, 175, 55, 0.15); }
    .sidebar-gold-box { border: 1px solid #D4AF37; padding: 25px; background: rgba(212, 175, 55, 0.03); text-align: center; margin-bottom: 20px; }

    /* METRICS */
    .gold-metric {
        border: 1px solid rgba(212, 175, 55, 0.3);
        background-color: rgba(255, 255, 255, 0.01);
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-label { 
        color: #D4AF37 !important; 
        font-size: 0.65rem; 
        text-transform: uppercase; 
        letter-spacing: 3px; 
        font-weight: 600 !important; 
    }
    .metric-value { 
        font-family: 'Cormorant Garamond', serif !important; 
        font-size: clamp(1.8rem, 4vw, 2.4rem); 
        color: #F0E68C !important; 
        font-weight: 300; 
        margin-top: 5px;
    }

    /* PERFUME CARD */
    .perfume-card {
        border: 1px solid rgba(212, 175, 55, 0.15);
        background: rgba(12, 12, 12, 0.9);
        padding: clamp(30px, 5vw, 55px);
        margin: 30px auto;
        max-width: 850px;
        text-align: center;
        box-shadow: 0 20px 50px rgba(0,0,0,0.8);
    }
    .row-brand { 
        font-family: 'Montserrat', sans-serif !important;
        font-size: clamp(1.4rem, 5vw, 1.8rem); 
        font-weight: 600 !important; 
        letter-spacing: 5px; 
        color: #D4AF37 !important; 
        margin-bottom: 10px; 
        text-transform: uppercase; 
    }
    .row-name { 
        font-family: 'Cormorant Garamond', serif !important; 
        font-size: clamp(1.3rem, 4vw, 1.8rem); 
        color: #fff !important; 
        margin-bottom: 20px; 
        font-style: italic; 
        font-weight: 400;
    }
    
    /* --- ADVANCED CENTERING & UI FIXES --- */
    
    /* 1. Radio Buttons Centering */
    div[data-testid="stRadio"] > div { 
        justify-content: center; 
        flex-wrap: wrap; 
        gap: 25px; 
    }
    div[data-testid="stRadio"] label { 
        font-size: 0.9rem !important; 
        letter-spacing: 1px; 
    }

    /* 2. Checkbox Absolute Centering */
    div[data-testid="stCheckbox"] {
        display: flex;
        justify-content: center;
        width: 100%;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    div[data-testid="stCheckbox"] label span {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.9rem !important;
    }

    /* 3. Input Fields Centering */
    .stSelectbox, .stTextInput { max-width: 650px; margin: 0 auto !important; }
    .stSelectbox div[data-baseweb="select"] > div { text-align: center; }
    .stTextInput input { text-align: center; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 40px; justify-content: center; margin-bottom: 40px;}
    .stTabs [data-baseweb="tab"] { letter-spacing: 3px; text-transform: uppercase; font-size: 0.8rem;}
    .stTabs [aria-selected="true"] { color: #D4AF37 !important; border-bottom-color: #D4AF37 !important; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('scentsational_data.csv', sep=None, encoding='latin1', engine='python')
        df.columns = df.columns.str.strip()
        if 'Perfume' in df.columns: df = df.rename(columns={'Perfume': 'Name'})
        
        # --- DATA CLEANING V3 (SMART) ---
        df['Name'] = df['Name'].astype(str).str.strip()
        df['Brand'] = df['Brand'].astype(str).str.strip().str.upper()

        # 1. Usuń indeksy typu "001-", "01-" (cyfry + myślnik na początku)
        # To naprawi "001-Orange", ale zostawi "212 VIP" (bo w 212 nie ma myślnika po liczbie)
        df['Name'] = df['Name'].str.replace(r'^\d+-', '', regex=True)
        df['Brand'] = df['Brand'].str.replace(r'^\d+-', '', regex=True)

        # 2. Usuń same zera na początku (np. "0 Absolute")
        df['Name'] = df['Name'].str.replace(r'^0+\s*', '', regex=True)

        # 3. Zamień pozostałe myślniki w środku na spacje i sformatuj
        df['Name'] = df['Name'].str.replace('-', ' ').str.title()
        df['Brand'] = df['Brand'].str.replace('-', ' ')

        # 4. Usuń puste lub błędne rekordy (krótsze niż 2 znaki)
        df = df[df['Name'].str.len() > 1]
        
        # Metryki
        df['Rating Value'] = pd.to_numeric(df['Rating Value'].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)
        accord_cols = ['mainaccord1', 'mainaccord2', 'mainaccord3', 'mainaccord4', 'mainaccord5']
        existing = [c for c in accord_cols if c in df.columns]
        df['Main Accords'] = df[existing].apply(lambda x: ', '.join(x.dropna().astype(str)), axis=1)
        
        df['Search_Index'] = df['Name'].str.lower() + " " + df['Brand'].str.lower() + " " + df['Main Accords'].str.lower()
        
        return df
    except Exception as e:
        return None

def main():
    df = load_data()
    if df is None: return

    # SIDEBAR
    with st.sidebar:
        st.markdown('<div class="sidebar-gold-box">', unsafe_allow_html=True)
        st.markdown("<p style='color:#D4AF37; font-size:0.8rem; font-weight:bold; letter-spacing:2px;'>AI ENGINE</p>", unsafe_allow_html=True)
        st.write("Unlock chemical DNA search.")
        st.markdown(f'<a href="https://huggingface.co/spaces/MagdalenaRomaniecka/ScentSational-Fragrantica-LFS" target="_blank" style="display:inline-block; background:#D4AF37; color:black; padding:12px 25px; text-decoration:none; font-weight:bold; font-size:0.7rem; letter-spacing:2px; margin-top:10px;">LAUNCH AI CORE</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # HEADER
    st.markdown('<div class="header-frame"><h1>SCENTSATIONAL</h1><div style="color:#888; font-size:0.75rem; letter-spacing:6px; text-transform:uppercase; margin-top:8px;">The Atelier &bull; Intelligence Platform</div></div>', unsafe_allow_html=True)

    # METRICS
    m1, m2, m3, m4 = st.columns([1,1,1,1])
    m1.markdown(f'<div class="gold-metric"><div class="metric-label">Collection Size</div><div class="metric-value">{len(df):,}</div></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="gold-metric"><div class="metric-label">Designers</div><div class="metric-value">{df["Brand"].nunique()}</div></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="gold-metric"><div class="metric-label">Trending Note</div><div class="metric-value">{df["mainaccord1"].mode()[0].capitalize()}</div></div>', unsafe_allow_html=True)
    m4.markdown(f'<div class="gold-metric"><div class="metric-label">Avg Rating</div><div class="metric-value">{df[df["Rating Value"] > 0]["Rating Value"].mean():.2f}</div></div>', unsafe_allow_html=True)

    tab_an, tab_cat = st.tabs(["MARKET INSIGHTS", "THE COLLECTION"])

    with tab_an:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.85rem; letter-spacing:2px; font-weight:bold;'>TOP DESIGNERS</p>", unsafe_allow_html=True)
            top_b = df['Brand'].value_counts().head(10)
            fig = px.bar(x=top_b.values, y=top_b.index, orientation='h', color_discrete_sequence=['#D4AF37'])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#888", height=350, yaxis={'autorange':'reversed', 'title': ''}, xaxis={'title': ''}, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})
        with c2:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.85rem; letter-spacing:2px; font-weight:bold;'>OLFACTORY LANDSCAPE</p>", unsafe_allow_html=True)
            top_a = df['mainaccord1'].value_counts().head(10)
            fig2 = px.bar(x=top_a.values, y=top_a.index, orientation='h', color_discrete_sequence=['#C5A059'])
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#888", height=350, yaxis={'autorange':'reversed', 'title': ''}, xaxis={'title': ''}, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig2, use_container_width=True, config={'staticPlot': True})
        with c3:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.85rem; letter-spacing:2px; font-weight:bold;'>SCORE DISTRIBUTION</p>", unsafe_allow_html=True)
            score_data = pd.cut(df[df['Rating Value'] > 0]['Rating Value'], bins=[0, 3.5, 4.2, 5], labels=['Standard', 'Premium', 'Masterpiece'])
            fig3 = px.pie(score_data.value_counts().reset_index(), values='count', names='Rating Value', hole=0.6, color_discrete_sequence=['#2C2C2C', '#96792e', '#F0E68C'])
            fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#888", height=350, margin=dict(l=0,r=0,t=20,b=0), showlegend=True)
            st.plotly_chart(fig3, use_container_width=True)

    with tab_cat:
        st.markdown("<div style='text-align:center; color:#666; font-size:0.75rem; margin-bottom:12px; letter-spacing:3px; text-transform: uppercase;'>Search the Archives</div>", unsafe_allow_html=True)
        
        search_options = sorted(list(df['Name'].unique()) + list(df['Brand'].unique()))
        selected = st.selectbox("", options=search_options, index=None, placeholder="Search by brand or perfume name...", label_visibility="collapsed")
        
        # CENTERED CHECKBOX (FIXED)
        top_only = st.checkbox("Show Only Top Rated (4.5+)")

        st.markdown("<p style='text-align:center; color:#D4AF37; font-size:0.7rem; letter-spacing:2px; font-weight:bold; margin-top:20px;'>QUALITY TIER SELECTOR</p>", unsafe_allow_html=True)
        tier_choice = st.radio("", ["All Artifacts", "Masterpieces (4.5+)", "Premium (4.0 - 4.5)", "Classic Collection"], horizontal=True, label_visibility="collapsed")
        
        note_filter = st.text_input("", placeholder="Filter by notes (e.g. Vanilla, Oud)...", label_visibility="collapsed")

        filtered = df.copy()
        if selected: filtered = filtered[(filtered['Name'] == selected) | (filtered['Brand'] == selected)]
        if top_only: filtered = filtered[filtered['Rating Value'] >= 4.5]
        if tier_choice == "Masterpieces (4.5+)": filtered = filtered[filtered['Rating Value'] >= 4.5]
        elif tier_choice == "Premium (4.0 - 4.5)": filtered = filtered[(filtered['Rating Value'] >= 4.0) & (filtered['Rating Value'] < 4.5)]
        elif tier_choice == "Classic Collection": filtered = filtered[(filtered['Rating Value'] > 0) & (filtered['Rating Value'] < 4.0)]
        if note_filter: filtered = filtered[filtered['Search_Index'].str.contains(note_filter.lower())]

        st.markdown(f"<p style='text-align:center; color:#555; margin-top:30px; letter-spacing:2px; font-size:0.8rem;'>{len(filtered)} PIECES IDENTIFIED</p>", unsafe_allow_html=True)

        for _, row in filtered.head(20).iterrows():
            st.markdown(f"""
                <div class="perfume-card">
                    <div class="row-brand">{row['Brand']}</div>
                    <div class="row-name">{row['Name']}</div>
                    <div style="color:#D4AF37; font-weight:bold; font-size:1.2rem; margin-bottom:15px;">★ {row['Rating Value']:.2f} / 5.0</div>
                    <div style="color:#888; font-style:italic; font-family:'Cormorant Garamond', serif; font-size:1.15rem; margin-bottom:30px; line-height:1.6;">{row['Main Accords']}</div>
                    <a href="{row.get('url', '#')}" target="_blank" style="text-decoration:none; color:black; background:#D4AF37; padding:15px 40px; font-size:0.75rem; font-weight:bold; letter-spacing:2px; display:inline-block;">EXPLORE ON FRAGRANTICA</a>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()