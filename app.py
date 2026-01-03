import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. LUXURY CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(page_title="ScentSational | Atelier", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Lato:wght@300;400;700&display=swap');

    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #1a1a1a 0%, #000000 100%);
        color: #E0E0E0;
        font-family: 'Lato', sans-serif;
    }

    h1 {
        font-family: 'Playfair Display', serif !important;
        background: linear-gradient(to bottom, #D4AF37 0%, #F0E68C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3.5rem !important;
        text-transform: uppercase;
        letter-spacing: 7px;
        margin-top: 0;
    }

    .header-frame {
        border: 1px solid rgba(212, 175, 55, 0.3);
        padding: 30px;
        margin-bottom: 25px;
        background: rgba(10, 10, 10, 0.6);
        box-shadow: 0 15px 35px rgba(0,0,0,0.8);
    }

    /* GOLD METRIC BOXES */
    .gold-metric {
        border: 1px solid rgba(212, 175, 55, 0.5);
        background-color: rgba(255, 255, 255, 0.02);
        padding: 15px;
        text-align: center;
        margin-bottom: 15px;
    }
    .metric-label { color: #D4AF37; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; }
    .metric-value { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: #F0E68C; margin-top: 5px;}

    /* PERFUME CARD */
    .perfume-card {
        border: 1px solid rgba(212, 175, 55, 0.2);
        background: linear-gradient(145deg, #0f0f0f, #050505);
        padding: 40px;
        margin: 20px auto;
        max-width: 800px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.7);
    }
    .row-brand { font-size: 1.6rem; font-weight: 900; letter-spacing: 5px; color: #D4AF37; margin-bottom: 5px; text-transform: uppercase; }
    .row-name { font-family: 'Playfair Display', serif; font-size: 1.3rem; color: #fff; margin-bottom: 10px; font-style: italic; }
    
    .sidebar-box { border: 1px solid #D4AF37; padding: 20px; background: rgba(212, 175, 55, 0.05); text-align: center; margin-top: 20px;}
    
    .stTabs [data-baseweb="tab-list"] { gap: 24px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { color: #666 !important; letter-spacing: 2px; text-transform: uppercase; font-size: 0.8rem;}
    .stTabs [aria-selected="true"] { color: #D4AF37 !important; border-bottom-color: #D4AF37 !important; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA ENGINE
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('scentsational_data.csv', sep=None, encoding='latin1', engine='python')
        df.columns = df.columns.str.strip()
        
        if 'Perfume' in df.columns: df = df.rename(columns={'Perfume': 'Name'})
        
        # FIXED: Poprawiona konwersja ocen (obsługa przecinków i kropek)
        df['Name'] = df['Name'].fillna("Unknown").astype(str).str.strip().str.title()
        df['Brand'] = df['Brand'].fillna("Unknown").astype(str).str.strip().str.upper()
        df['Rating Value'] = pd.to_numeric(df['Rating Value'].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)
        
        # FIXED: Poprawione łączenie nut zapachowych
        accord_cols = ['mainaccord1', 'mainaccord2', 'mainaccord3', 'mainaccord4', 'mainaccord5']
        existing = [c for c in accord_cols if c in df.columns]
        df['Main Accords'] = df[existing].apply(lambda x: ', '.join(x.dropna().astype(str)), axis=1)
        df['Main Accords'] = df['Main Accords'].replace('', 'Notes not archived')
        df['Search_Index'] = df['Name'].str.lower() + " " + df['Brand'].str.lower() + " " + df['Main Accords'].str.lower()
        
        return df
    except Exception as e:
        st.error(f"Data Load Error: {e}")
        return None

def main():
    df = load_data()
    if df is None: return

    # SIDEBAR
    with st.sidebar:
        st.markdown("<div class='sidebar-box'>", unsafe_allow_html=True)
        st.markdown("<p style='color:#D4AF37; font-size:0.7rem; letter-spacing:2px; font-weight:bold;'>ELITE UPGRADE</p>", unsafe_allow_html=True)
        st.write("Unlock chemical DNA search with the neural-powered Heavy Core engine.")
        st.markdown(f'<a href="https://huggingface.co/spaces/MagdalenaRomaniecka/ScentSational-Fragrantica-LFS" target="_blank" style="display:inline-block; background:#D4AF37; color:black; padding:10px 20px; text-decoration:none; font-weight:bold; font-size:0.7rem; letter-spacing:1px; margin-top:10px;">LAUNCH AI CORE</a>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # HEADER
    st.markdown('<div class="header-frame"><h1>SCENTSATIONAL</h1><p style="text-align:center; color:#888; letter-spacing:5px; font-size:0.8rem; text-transform:uppercase;">The Atelier &bull; Intelligence Platform</p></div>', unsafe_allow_html=True)

    # METRICS (PRZYWRÓCONE)
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f'<div class="gold-metric"><div class="metric-label">Collection</div><div class="metric-value">{len(df):,}</div></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="gold-metric"><div class="metric-label">Designers</div><div class="metric-value">{df["Brand"].nunique()}</div></div>', unsafe_allow_html=True)
    top_note = df['mainaccord1'].mode()[0].capitalize() if not df['mainaccord1'].empty else "N/A"
    m3.markdown(f'<div class="gold-metric"><div class="metric-label">Trending Note</div><div class="metric-value">{top_note}</div></div>', unsafe_allow_html=True)
    avg_score = df[df['Rating Value'] > 0]['Rating Value'].mean()
    m4.markdown(f'<div class="gold-metric"><div class="metric-label">Avg Rating</div><div class="metric-value">{avg_score:.2f}</div></div>', unsafe_allow_html=True)

    tab_an, tab_cat = st.tabs(["MARKET ANALYSIS", "THE COLLECTION"])

    with tab_an:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.75rem; font-weight:bold; letter-spacing:2px;'>PRESTIGE HOUSES</p>", unsafe_allow_html=True)
            top_b = df['Brand'].value_counts().head(10)
            fig = px.bar(x=top_b.values, y=top_b.index, orientation='h', color_discrete_sequence=['#D4AF37'])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#888", height=350, yaxis={'autorange':'reversed'}, margin=dict(l=0,r=10,t=0,b=0), xaxis_title="")
            st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})

        with c2:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.75rem; font-weight:bold; letter-spacing:2px;'>CORE ACCORDS</p>", unsafe_allow_html=True)
            top_a = df['mainaccord1'].value_counts().head(10)
            fig2 = px.bar(x=top_a.values, y=top_a.index, orientation='h', color_discrete_sequence=['#C5A059'])
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#888", height=350, yaxis={'autorange':'reversed'}, margin=dict(l=0,r=10,t=0,b=0), xaxis_title="")
            st.plotly_chart(fig2, use_container_width=True, config={'staticPlot': True})

        with c3:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.75rem; font-weight:bold; letter-spacing:2px;'>SCORE DISTRIBUTION</p>", unsafe_allow_html=True)
            # FIXED: Wykres Donut (Pierścieniowy) zamiast histogramu
            score_data = pd.cut(df[df['Rating Value'] > 0]['Rating Value'], bins=[0, 3.5, 4.2, 5], labels=['Standard', 'Premium', 'Elite'])
            pie_counts = score_data.value_counts().reset_index()
            fig3 = px.pie(pie_counts, values='count', names='Rating Value', hole=0.6, color_discrete_sequence=['#856a35', '#C5A059', '#D4AF37'])
            fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#888", height=350, margin=dict(l=0,r=0,t=20,b=0))
            st.plotly_chart(fig3, use_container_width=True)

    with tab_cat:
        # PRZYWRÓCONY SELECTBOX Z PODPOWIEDZIAMI
        search_options = sorted(list(df['Name'].unique()) + list(df['Brand'].unique()))
        selected = st.selectbox("Search archives by name or brand...", options=search_options, index=None, placeholder="Type to explore...")
        
        col_f1, col_f2 = st.columns([1,1])
        with col_f1: top_only = st.checkbox("Show Only Top Rated (4.5 ★+)")
        with col_f2: note_filter = st.text_input("Filter by specific notes (e.g. Vanilla, Oud)...")

        filtered = df.copy()
        if selected: filtered = filtered[(filtered['Name'] == selected) | (filtered['Brand'] == selected)]
        if top_only: filtered = filtered[filtered['Rating Value'] >= 4.5]
        if note_filter: filtered = filtered[filtered['Search_Index'].str.contains(note_filter.lower())]

        st.markdown(f"<p style='text-align:center; color:#555; margin-top:20px; letter-spacing:2px;'>{len(filtered)} PIECES IDENTIFIED</p>", unsafe_allow_html=True)

        for _, row in filtered.head(25).iterrows():
            st.markdown(f"""
                <div class="perfume-card">
                    <div class="row-brand">{row['Brand']}</div>
                    <div class="row-name">{row['Name']}</div>
                    <div style="color:#D4AF37; font-weight:bold; font-size:1.1rem; margin-bottom:10px;">★ {row['Rating Value']:.2f} / 5.0</div>
                    <div style="color:#888; font-style:italic; margin: 15px 0; font-size:1rem;">{row['Main Accords']}</div>
                    <a href="{row.get('url', '#')}" target="_blank" style="text-decoration:none; color:black; background:#D4AF37; padding:12px 35px; font-size:0.75rem; font-weight:bold; letter-spacing:2px; display:inline-block; margin-top:15px;">EXPLORE ON FRAGRANTICA</a>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()