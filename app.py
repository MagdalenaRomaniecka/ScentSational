import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import re

# -----------------------------------------------------------------------------
# 1. UI CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(page_title="ScentSational | Atelier", layout="wide")
st.cache_data.clear()

st.markdown("""
    <style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=Montserrat:wght@300;400;500;600;700&display=swap');

    /* GLOBAL FONT ENFORCEMENT */
    html, body, [class*="css"], .stMarkdown, .stRadio, .stSelectbox, .stTextInput, .stMultiSelect, div, span, p {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 400 !important; 
        color: #E0E0E0 !important;
        font-size: 0.9rem !important;
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

    /* --- WIDGET STYLING & ALIGNMENT --- */
    
    /* 1. INPUTS (Search & Notes) */
    .stSelectbox, .stMultiSelect { width: 100%; }
    
    /* Golden Borders */
    .stSelectbox div[data-baseweb="select"] > div,
    .stMultiSelect div[data-baseweb="select"] > div {
        border: 1px solid rgba(212, 175, 55, 0.4) !important;
        background-color: rgba(10, 10, 10, 0.6) !important;
    }

    /* Hide standard labels */
    .stSelectbox label, .stMultiSelect label { display: none; }

    /* 2. RADIO BUTTONS (TIER SELECTOR) - COMPACT & CENTERED */
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
        gap: 15px; /* Tighter gap for unification */
    }
    div[data-testid="stRadio"] label p {
        font-size: 0.85rem !important;
        color: #D4AF37 !important;
        font-weight: 500 !important;
    }

    /* 3. TOGGLE SWITCH - CENTERED */
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

    /* METRICS */
    .gold-metric {
        border: 1px solid rgba(212, 175, 55, 0.2);
        background-color: rgba(255, 255, 255, 0.01);
        padding: 10px;
        text-align: center;
        margin-bottom: 5px;
    }
    .metric-label { color: #D4AF37 !important; font-size: 0.6rem !important; text-transform: uppercase; letter-spacing: 2px; font-weight: 600 !important; }
    .metric-value { font-family: 'Cormorant Garamond', serif !important; font-size: clamp(1.5rem, 3vw, 2rem) !important; color: #F0E68C !important; font-weight: 300; margin-top: 0px; }

    /* CARDS */
    .perfume-card {
        border: 1px solid rgba(212, 175, 55, 0.15);
        background: rgba(12, 12, 12, 0.9);
        padding: clamp(20px, 4vw, 40px);
        margin: 20px auto;
        max-width: 850px;
        text-align: center;
        box-shadow: 0 15px 40px rgba(0,0,0,0.6);
        border-radius: 4px;
    }
    .row-brand { font-size: clamp(1.2rem, 4vw, 1.6rem) !important; font-weight: 600 !important; letter-spacing: 3px; color: #D4AF37 !important; margin-bottom: 5px; }
    .row-name { font-family: 'Cormorant Garamond', serif !important; font-size: clamp(1.2rem, 4vw, 1.6rem) !important; color: #fff !important; margin-bottom: 15px; font-style: italic; }
    
    [data-testid="stSidebar"] { background-color: #080808 !important; border-right: 1px solid rgba(212, 175, 55, 0.15); }
    .sidebar-gold-box { border: 1px solid #D4AF37; padding: 20px; background: rgba(212, 175, 55, 0.03); text-align: center; margin-bottom: 20px; }

    .stTabs [data-baseweb="tab-list"] { gap: 30px; justify-content: center; margin-bottom: 30px;}
    .stTabs [data-baseweb="tab"] { letter-spacing: 2px; text-transform: uppercase; font-size: 0.75rem !important;}
    .stTabs [aria-selected="true"] { color: #D4AF37 !important; border-bottom-color: #D4AF37 !important; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('scentsational_data.csv', sep=None, encoding='latin1', engine='python')
        df.columns = df.columns.str.strip()
        if 'Perfume' in df.columns: df = df.rename(columns={'Perfume': 'Name'})
        
        # --- DATA CLEANING ---
        df['Name'] = df['Name'].astype(str).str.strip()
        df['Brand'] = df['Brand'].astype(str).str.strip()
        
        # Remove artifacts
        df['Name'] = df['Name'].str.replace(r'^\d+\s*-\s*', '', regex=True)
        df['Brand'] = df['Brand'].str.replace(r'^\d+\s*-\s*', '', regex=True)
        df['Name'] = df['Name'].str.replace(r'^0+\s+', '', regex=True)
        df = df[~df['Name'].str.match(r'^\d+$')]
        
        # Title Case
        df['Name'] = df['Name'].str.replace('-', ' ').str.title()
        df['Brand'] = df['Brand'].str.replace('-', ' ').str.title()
        
        df = df[df['Name'].str.len() > 1]
        df['Rating Value'] = pd.to_numeric(df['Rating Value'].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)
        
        accord_cols = ['mainaccord1', 'mainaccord2', 'mainaccord3', 'mainaccord4', 'mainaccord5']
        existing = [c for c in accord_cols if c in df.columns]
        df['Main Accords'] = df[existing].apply(lambda x: ', '.join(x.dropna().astype(str)), axis=1)
        df['Search_Index'] = df['Name'].str.lower() + " " + df['Brand'].str.lower() + " " + df['Main Accords'].str.lower()
        df = df.sort_values(by=['Brand', 'Name'])
        return df
    except Exception as e:
        return None

def get_all_notes(df):
    notes_set = set()
    if 'Main Accords' in df.columns:
        for accords in df['Main Accords'].dropna():
            parts = [x.strip() for x in accords.split(',')]
            for p in parts:
                if p:
                    notes_set.add(p.capitalize())
    return sorted(list(notes_set))

def main():
    df = load_data()
    if df is None: return
    all_notes_list = get_all_notes(df)

    with st.sidebar:
        st.markdown('<div class="sidebar-gold-box">', unsafe_allow_html=True)
        st.markdown("<p style='color:#D4AF37; font-size:0.8rem; font-weight:bold; letter-spacing:2px;'>AI ENGINE</p>", unsafe_allow_html=True)
        st.write("Unlock chemical DNA search.")
        st.markdown(f'<a href="https://huggingface.co/spaces/MagdalenaRomaniecka/ScentSational-Fragrantica-LFS" target="_blank" style="display:inline-block; background:#D4AF37; color:black; padding:12px 25px; text-decoration:none; font-weight:bold; font-size:0.7rem; letter-spacing:2px; margin-top:10px;">LAUNCH AI CORE</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="header-frame"><h1>SCENTSATIONAL</h1><div class="sub-header">The Atelier &bull; Intelligence Platform</div></div>', unsafe_allow_html=True)

    # TABS
    tab_an, tab_cat = st.tabs(["MARKET INSIGHTS", "DISCOVER SCENTS"])

    with tab_an:
        m1, m2, m3, m4 = st.columns([1,1,1,1])
        m1.markdown(f'<div class="gold-metric"><div class="metric-label">Collection Size</div><div class="metric-value">{len(df):,}</div></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="gold-metric"><div class="metric-label">Designers</div><div class="metric-value">{df["Brand"].nunique()}</div></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="gold-metric"><div class="metric-label">Trending Note</div><div class="metric-value">{df["mainaccord1"].mode()[0].capitalize()}</div></div>', unsafe_allow_html=True)
        m4.markdown(f'<div class="gold-metric"><div class="metric-label">Avg Rating</div><div class="metric-value">{df[df["Rating Value"] > 0]["Rating Value"].mean():.2f}</div></div>', unsafe_allow_html=True)
        
        st.write("") 

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.75rem; letter-spacing:2px; font-weight:bold;'>TOP DESIGNERS</p>", unsafe_allow_html=True)
            top_b = df['Brand'].value_counts().head(10)
            fig = px.bar(x=top_b.values, y=top_b.index, orientation='h', color_discrete_sequence=['#D4AF37'])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#888", height=300, yaxis={'autorange':'reversed', 'title': ''}, xaxis={'title': ''}, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})
        with c2:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.75rem; letter-spacing:2px; font-weight:bold;'>OLFACTORY LANDSCAPE</p>", unsafe_allow_html=True)
            top_a = df['mainaccord1'].value_counts().head(10)
            fig2 = px.bar(x=top_a.values, y=top_a.index, orientation='h', color_discrete_sequence=['#C5A059'])
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#888", height=300, yaxis={'autorange':'reversed', 'title': ''}, xaxis={'title': ''}, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig2, use_container_width=True, config={'staticPlot': True})
        with c3:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.75rem; letter-spacing:2px; font-weight:bold;'>SCORE DISTRIBUTION</p>", unsafe_allow_html=True)
            score_data = pd.cut(df[df['Rating Value'] > 0]['Rating Value'], bins=[0, 3.5, 4.2, 5], labels=['Standard', 'Premium', 'Masterpiece'])
            fig3 = px.pie(score_data.value_counts().reset_index(), values='count', names='Rating Value', hole=0.6, color_discrete_sequence=['#2C2C2C', '#96792e', '#F0E68C'])
            fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#888", height=300, margin=dict(l=0,r=0,t=20,b=0), showlegend=True)
            st.plotly_chart(fig3, use_container_width=True)

    # --- TAB 2: DISCOVER (Central Alignment Strategy) ---
    with tab_cat:
        st.write("") 

        # We create 3 columns: Left Spacer, CENTER STAGE (60%), Right Spacer
        # This keeps everything tightly aligned in the middle.
        fill_left, center_stage, fill_right = st.columns([1, 4, 1])

        with center_stage:
            # 1. Tier Selector
            st.markdown("<p style='text-align:center; color:#666; font-size:0.7rem; letter-spacing:2px; margin-bottom: 5px; text-transform:uppercase;'>Select Quality Grade</p>", unsafe_allow_html=True)
            tier_choice = st.radio(
                "TIER_SELECTOR", 
                ["All Artifacts", "Masterpieces (4.5+)", "Premium (4.0+)", "Classics"],
                horizontal=True,
                label_visibility="collapsed"
            )
            
            st.write("") 
            
            # 2. Search & Notes - Combined Row
            col_s1, col_s2 = st.columns([1.5, 1], gap="medium")
            
            with col_s1:
                selected = st.selectbox(
                    "SEARCH_HIDDEN",
                    options=sorted(list(df['Name'].unique()) + list(df['Brand'].unique())),
                    index=None,
                    placeholder="🔍 Search Brand or Name...",
                    label_visibility="collapsed"
                )
                
            with col_s2:
                selected_notes = st.multiselect(
                    "NOTES_HIDDEN",
                    options=all_notes_list,
                    placeholder="🧪 Filter by Notes...",
                    label_visibility="collapsed"
                )

            # 3. Strict Mode Toggle
            top_only = st.toggle("Strict Mode (4.5+ Only)")

        # Logic
        filtered = df.copy()
        if selected: filtered = filtered[(filtered['Name'] == selected) | (filtered['Brand'] == selected)]
        
        if top_only: 
            filtered = filtered[filtered['Rating Value'] >= 4.5]
        
        if tier_choice == "Masterpieces (4.5+)": filtered = filtered[filtered['Rating Value'] >= 4.5]
        elif tier_choice == "Premium (4.0+)": filtered = filtered[(filtered['Rating Value'] >= 4.0) & (filtered['Rating Value'] < 4.5)]
        elif tier_choice == "Classics": filtered = filtered[(filtered['Rating Value'] > 0) & (filtered['Rating Value'] < 4.0)]
        
        if selected_notes:
            for note in selected_notes:
                filtered = filtered[filtered['Search_Index'].str.contains(note.lower())]

        st.markdown(f"""
            <div style='text-align:center; margin-top:30px; margin-bottom:20px; border-top:1px solid #333; padding-top:20px;'>
                <span style='color:#666; font-size:0.8rem; letter-spacing:2px; text-transform:uppercase;'>
                    {len(filtered)} Olfactory Signatures Found
                </span>
            </div>
        """, unsafe_allow_html=True)

        for _, row in filtered.head(20).iterrows():
            st.markdown(f"""
                <div class="perfume-card">
                    <div class="row-brand">{row['Brand']}</div>
                    <div class="row-name">{row['Name']}</div>
                    <div style="color:#D4AF37; font-weight:bold; font-size:1.1rem; margin-bottom:15px;">★ {row['Rating Value']:.2f}</div>
                    <div style="color:#888; font-style:italic; font-family:'Cormorant Garamond', serif; font-size:1rem; margin-bottom:25px;">{row['Main Accords']}</div>
                    <a href="{row.get('url', '#')}" target="_blank" style="text-decoration:none; color:000; background:#D4AF37; padding:12px 30px; font-size:0.7rem; font-weight:600; letter-spacing:1px; border-radius:2px; display:inline-block;">FRAGRANTICA</a>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
