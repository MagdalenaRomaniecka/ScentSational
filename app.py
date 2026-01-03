import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. LUXURY CONFIGURATION & MOBILE OPTIMIZATION
# -----------------------------------------------------------------------------
st.set_page_config(page_title="ScentSational | Atelier", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=Lato:wght@300;400;700&display=swap');

    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #1a1a1a 0%, #000000 100%);
        color: #E0E0E0;
        font-family: 'Lato', sans-serif;
    }

    /* CENTERED RESPONSIVE HEADER */
    h1 {
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 300 !important;
        background: linear-gradient(to bottom, #D4AF37 0%, #F0E68C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: clamp(2.2rem, 7vw, 4.2rem) !important;
        text-transform: uppercase;
        letter-spacing: clamp(6px, 1.8vw, 14px);
        margin: 0;
    }

    .header-frame {
        border-bottom: 1px solid rgba(212, 175, 55, 0.2);
        padding: 25px 0;
        margin-bottom: 25px;
        background: rgba(10, 10, 10, 0.4);
        text-align: center;
    }

    /* CENTERED METRICS */
    .gold-metric {
        border: 1px solid rgba(212, 175, 55, 0.3);
        background-color: rgba(255, 255, 255, 0.01);
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-label { color: #D4AF37; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 2.5px; font-weight: 700; }
    .metric-value { font-family: 'Cormorant Garamond', serif; font-size: clamp(1.6rem, 4vw, 2.2rem); color: #F0E68C; font-weight: 300; }

    /* PERFUME CARD - CENTERED & POLISHED */
    .perfume-card {
        border: 1px solid rgba(212, 175, 55, 0.15);
        background: rgba(10, 10, 10, 0.8);
        padding: clamp(30px, 5vw, 50px);
        margin: 25px auto;
        max-width: 850px;
        text-align: center;
        box-shadow: 0 12px 40px rgba(0,0,0,0.7);
    }
    .row-brand { font-size: clamp(1.5rem, 5vw, 2rem); font-weight: 900; letter-spacing: 6px; color: #D4AF37; margin-bottom: 6px; text-transform: uppercase; }
    .row-name { font-family: 'Cormorant Garamond', serif; font-size: clamp(1.2rem, 4vw, 1.7rem); color: #fff; margin-bottom: 15px; font-style: italic; }
    
    /* CENTERED INPUTS & RADIOS */
    div[data-testid="stRadio"] > div { justify-content: center; flex-wrap: wrap; gap: 15px; }
    div[data-testid="stRadio"] label { color: #D4AF37 !important; font-size: 0.8rem !important; letter-spacing: 1px; }
    .stSelectbox, .stTextInput { max-width: 700px; margin: 0 auto; text-align: center; }
    .stCheckbox { display: flex; justify-content: center; margin: 15px 0; }
    
    .stTabs [data-baseweb="tab-list"] { gap: clamp(15px, 4vw, 40px); justify-content: center; }
    .stTabs [data-baseweb="tab"] { color: #666 !important; letter-spacing: 2px; text-transform: uppercase; font-size: 0.85rem;}
    .stTabs [aria-selected="true"] { color: #D4AF37 !important; border-bottom-color: #D4AF37 !important; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('scentsational_data.csv', sep=None, encoding='latin1', engine='python')
        df.columns = df.columns.str.strip()
        if 'Perfume' in df.columns: df = df.rename(columns={'Perfume': 'Name'})
        df['Name'] = df['Name'].fillna("Unknown").astype(str).str.strip().str.title()
        df['Brand'] = df['Brand'].fillna("Unknown").astype(str).str.strip().str.upper()
        df['Rating Value'] = pd.to_numeric(df['Rating Value'].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)
        
        accord_cols = ['mainaccord1', 'mainaccord2', 'mainaccord3', 'mainaccord4', 'mainaccord5']
        existing = [c for c in accord_cols if c in df.columns]
        df['Main Accords'] = df[existing].apply(lambda x: ', '.join(x.dropna().astype(str)), axis=1)
        df['Search_Index'] = df['Name'].str.lower() + " " + df['Brand'].str.lower() + " " + df['Main Accords'].str.lower()
        return df
    except: return None

def main():
    df = load_data()
    if df is None: return

    # HEADER
    st.markdown('<div class="header-frame"><h1>SCENTSATIONAL</h1><div style="color:#888; font-size:0.75rem; letter-spacing:5px; text-transform:uppercase; margin-top:8px;">The Atelier &bull; Intelligence Platform</div></div>', unsafe_allow_html=True)

    # METRICS - CENTERED & RESPONSIVE
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
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#888", height=350, yaxis={'autorange':'reversed'}, margin=dict(l=0,r=0,t=0,b=0), xaxis_title="")
            st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})
        with c2:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.85rem; letter-spacing:2px; font-weight:bold;'>OLFACTORY LANDSCAPE</p>", unsafe_allow_html=True)
            top_a = df['mainaccord1'].value_counts().head(10)
            fig2 = px.bar(x=top_a.values, y=top_a.index, orientation='h', color_discrete_sequence=['#C5A059'])
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#888", height=350, yaxis={'autorange':'reversed'}, margin=dict(l=0,r=0,t=0,b=0), xaxis_title="")
            st.plotly_chart(fig2, use_container_width=True, config={'staticPlot': True})
        with c3:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.85rem; letter-spacing:2px; font-weight:bold;'>SCORE DISTRIBUTION</p>", unsafe_allow_html=True)
            score_data = pd.cut(df[df['Rating Value'] > 0]['Rating Value'], bins=[0, 3.5, 4.2, 5], labels=['Standard', 'Premium', 'Masterpiece'])
            fig3 = px.pie(score_data.value_counts().reset_index(), values='count', names='Rating Value', hole=0.6, color_discrete_sequence=['#856a35', '#C5A059', '#D4AF37'])
            fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#888", height=350, margin=dict(l=0,r=0,t=20,b=0), showlegend=True)
            st.plotly_chart(fig3, use_container_width=True)

    with tab_cat:
        st.markdown("<div style='text-align:center; color:#666; font-size:0.8rem; margin-bottom:12px; letter-spacing:3px;'>SEARCH THE ARCHIVES</div>", unsafe_allow_html=True)
        
        search_options = sorted(list(df['Name'].unique()) + list(df['Brand'].unique()))
        selected = st.selectbox("", options=search_options, index=None, placeholder="Search by brand or perfume name...", label_visibility="collapsed")
        
        top_only = st.checkbox("Show Only Top Rated (4.5+)")

        st.markdown("<p style='text-align:center; color:#D4AF37; font-size:0.75rem; letter-spacing:2px; font-weight:bold; margin-top:10px;'>QUALITY TIER SELECTOR</p>", unsafe_allow_html=True)
        tier_choice = st.radio("", ["All Artifacts", "Masterpieces (4.5+)", "Premium (4.0 - 4.5)", "Classic Collection"], horizontal=True, label_visibility="collapsed")
        
        note_filter = st.text_input("", placeholder="Filter by notes (e.g. Vanilla, Oud)...", label_visibility="collapsed")

        filtered = df.copy()
        if selected: filtered = filtered[(filtered['Name'] == selected) | (filtered['Brand'] == selected)]
        if top_only: filtered = filtered[filtered['Rating Value'] >= 4.5]
        
        if tier_choice == "Masterpieces (4.5+)": filtered = filtered[filtered['Rating Value'] >= 4.5]
        elif tier_choice == "Premium (4.0 - 4.5)": filtered = filtered[(filtered['Rating Value'] >= 4.0) & (filtered['Rating Value'] < 4.5)]
        elif tier_choice == "Classic Collection": filtered = filtered[(filtered['Rating Value'] > 0) & (filtered['Rating Value'] < 4.0)]
        
        if note_filter: filtered = filtered[filtered['Search_Index'].str.contains(note_filter.lower())]

        st.markdown(f"<p style='text-align:center; color:#555; margin-top:25px; letter-spacing:2px; font-size:0.8rem;'>{len(filtered)} PIECES IDENTIFIED</p>", unsafe_allow_html=True)

        for _, row in filtered.head(20).iterrows():
            st.markdown(f"""
                <div class="perfume-card">
                    <div class="row-brand">{row['Brand']}</div>
                    <div class="row-name">{row['Name']}</div>
                    <div style="color:#D4AF37; font-weight:bold; font-size:1.15rem; margin-bottom:12px; letter-spacing:2px;">★ {row['Rating Value']:.2f} / 5.0</div>
                    <div style="color:#888; font-style:italic; font-family:'Cormorant Garamond', serif; font-size:1.1rem; margin-bottom:25px; line-height:1.5;">{row['Main Accords']}</div>
                    <a href="{row.get('url', '#')}" target="_blank" style="text-decoration:none; color:black; background:#D4AF37; padding:12px 35px; font-size:0.75rem; font-weight:bold; letter-spacing:2px; display:inline-block;">EXPLORE ON FRAGRANTICA</a>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()