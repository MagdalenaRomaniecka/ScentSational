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

    /* RESPONSIVE HEADER */
    h1 {
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 300 !important;
        background: linear-gradient(to bottom, #D4AF37 0%, #F0E68C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: clamp(1.8rem, 7vw, 4rem) !important;
        text-transform: uppercase;
        letter-spacing: clamp(4px, 1.5vw, 12px);
        margin: 0;
    }

    .header-frame {
        border-bottom: 1px solid rgba(212, 175, 55, 0.2);
        padding: clamp(15px, 3vh, 30px) 0;
        margin-bottom: 25px;
        background: rgba(10, 10, 10, 0.4);
        text-align: center;
    }

    /* METRIC BOXES - MOBILE ADAPTIVE */
    .gold-metric {
        border: 1px solid rgba(212, 175, 55, 0.3);
        background-color: rgba(255, 255, 255, 0.01);
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-label { color: #D4AF37; font-size: 0.6rem; text-transform: uppercase; letter-spacing: 2px; }
    .metric-value { 
        font-family: 'Cormorant Garamond', serif; 
        font-size: clamp(1.4rem, 4vw, 2rem); 
        color: #F0E68C; 
        font-weight: 300; 
    }

    /* CENTERED LUXURY CARD */
    .perfume-card {
        border: 1px solid rgba(212, 175, 55, 0.15);
        background: rgba(10, 10, 10, 0.8);
        padding: clamp(25px, 5vw, 45px);
        margin: 20px auto;
        max-width: 800px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.7);
    }
    .row-brand { font-size: clamp(1.3rem, 5vw, 1.8rem); font-weight: 900; letter-spacing: 5px; color: #D4AF37; margin-bottom: 5px; text-transform: uppercase; }
    .row-name { font-family: 'Cormorant Garamond', serif; font-size: clamp(1.1rem, 4vw, 1.5rem); color: #fff; margin-bottom: 15px; font-style: italic; }
    
    /* MOBILE FILTER TWEAKS */
    div[data-testid="stRadio"] > div { justify-content: center; flex-wrap: wrap; gap: 10px; }
    .stSelectbox, .stTextInput { max-width: 600px; margin: 0 auto; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('scentsational_data.csv', sep=None, encoding='latin1', engine='python')
        df.columns = df.columns.str.strip()
        if 'Perfume' in df.columns: df = df.rename(columns={'Perfume': 'Name'})
        df['Name'] = df['Name'].fillna("Unknown").astype(str).str.title()
        df['Brand'] = df['Brand'].fillna("Unknown").astype(str).str.upper()
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

    # SIDEBAR
    with st.sidebar:
        st.markdown("<div style='border: 1px solid #D4AF37; padding: 20px; text-align: center;'>", unsafe_allow_html=True)
        st.markdown("<p style='color:#D4AF37; font-size:0.7rem; letter-spacing:2px; font-weight:bold;'>AI ENGINE</p>", unsafe_allow_html=True)
        st.write("Chemical DNA search.")
        st.markdown(f'<a href="https://huggingface.co/spaces/MagdalenaRomaniecka/ScentSational-Fragrantica-LFS" target="_blank" style="display:inline-block; background:#D4AF37; color:black; padding:10px 20px; text-decoration:none; font-weight:bold; font-size:0.7rem; letter-spacing:1px; margin-top:10px;">LAUNCH CORE</a>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # HEADER
    st.markdown('<div class="header-frame"><h1>SCENTSATIONAL</h1><div style="color:#888; font-size:0.7rem; letter-spacing:4px; text-transform:uppercase; margin-top:5px;">The Atelier &bull; Intelligence Platform</div></div>', unsafe_allow_html=True)

    # METRICS - AUTO WRAP ON MOBILE
    m1, m2, m3, m4 = st.columns([1,1,1,1])
    m1.markdown(f'<div class="gold-metric"><div class="metric-label">Collection</div><div class="metric-value">{len(df):,}</div></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="gold-metric"><div class="metric-label">Designers</div><div class="metric-value">{df["Brand"].nunique()}</div></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="gold-metric"><div class="metric-label">Trending</div><div class="metric-value">{df["mainaccord1"].mode()[0].capitalize()}</div></div>', unsafe_allow_html=True)
    m4.markdown(f'<div class="gold-metric"><div class="metric-label">Avg Rating</div><div class="metric-value">{df[df["Rating Value"] > 0]["Rating Value"].mean():.2f}</div></div>', unsafe_allow_html=True)

    tab_an, tab_cat = st.tabs(["MARKET INSIGHTS", "THE COLLECTION"])

    with tab_an:
        c1, c2, c3 = st.columns([1,1,1])
        with c1:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.8rem; font-weight:bold; letter-spacing:2px;'>TOP DESIGNERS</p>", unsafe_allow_html=True)
            top_b = df['Brand'].value_counts().head(8)
            fig = px.bar(x=top_b.values, y=top_b.index, orientation='h', color_discrete_sequence=['#D4AF37'])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#888", height=300, yaxis={'autorange':'reversed'}, margin=dict(l=0,r=0,t=0,b=0), xaxis_title="")
            st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})
        with c2:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.8rem; font-weight:bold; letter-spacing:2px;'>OLFACTORY LANDSCAPE</p>", unsafe_allow_html=True)
            top_a = df['mainaccord1'].value_counts().head(8)
            fig2 = px.bar(x=top_a.values, y=top_a.index, orientation='h', color_discrete_sequence=['#C5A059'])
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#888", height=300, yaxis={'autorange':'reversed'}, margin=dict(l=0,r=0,t=0,b=0), xaxis_title="")
            st.plotly_chart(fig2, use_container_width=True, config={'staticPlot': True})
        with c3:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.8rem; font-weight:bold; letter-spacing:2px;'>SCORE DISTRIBUTION</p>", unsafe_allow_html=True)
            score_data = pd.cut(df[df['Rating Value'] > 0]['Rating Value'], bins=[0, 3.5, 4.2, 5], labels=['Standard', 'Premium', 'Elite'])
            fig3 = px.pie(score_data.value_counts().reset_index(), values='count', names='Rating Value', hole=0.6, color_discrete_sequence=['#856a35', '#C5A059', '#D4AF37'])
            fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#888", height=300, margin=dict(l=0,r=0,t=20,b=0), showlegend=False)
            st.plotly_chart(fig3, use_container_width=True)

    with tab_cat:
        search_options = sorted(list(df['Name'].unique()) + list(df['Brand'].unique()))
        selected = st.selectbox("", options=search_options, index=None, placeholder="Search by brand or perfume name...", label_visibility="collapsed")
        
        _, col_check, _ = st.columns([1, 2, 1])
        with col_check:
            top_only = st.checkbox("Show Only Top Rated (4.5+)")

        tier_choice = st.radio("", ["All", "Masterpieces (4.5+)", "Premium (4.0+)", "Standard"], horizontal=True, label_visibility="collapsed")
        note_filter = st.text_input("", placeholder="Filter by notes (e.g. Vanilla, Oud)...", label_visibility="collapsed")

        filtered = df.copy()
        if selected: filtered = filtered[(filtered['Name'] == selected) | (filtered['Brand'] == selected)]
        if top_only: filtered = filtered[filtered['Rating Value'] >= 4.5]
        if tier_choice == "Masterpieces (4.5+)": filtered = filtered[filtered['Rating Value'] >= 4.5]
        elif tier_choice == "Premium (4.0+)": filtered = filtered[(filtered['Rating Value'] >= 4.0) & (filtered['Rating Value'] < 4.5)]
        elif tier_choice == "Standard": filtered = filtered[(filtered['Rating Value'] > 0) & (filtered['Rating Value'] < 4.0)]
        if note_filter: filtered = filtered[filtered['Search_Index'].str.contains(note_filter.lower())]

        st.markdown(f"<p style='text-align:center; color:#555; margin-top:20px; font-size:0.8rem;'>{len(filtered)} IDENTIFIED</p>", unsafe_allow_html=True)

        for _, row in filtered.head(20).iterrows():
            st.markdown(f"""
                <div class="perfume-card">
                    <div class="row-brand">{row['Brand']}</div>
                    <div class="row-name">{row['Name']}</div>
                    <div style="color:#D4AF37; font-weight:bold; font-size:1rem;">★ {row['Rating Value']:.2f} / 5.0</div>
                    <div style="color:#888; font-style:italic; font-size:0.95rem; margin: 15px 0;">{row['Main Accords']}</div>
                    <a href="{row.get('url', '#')}" target="_blank" style="text-decoration:none; color:black; background:#D4AF37; padding:10px 30px; font-size:0.75rem; font-weight:bold; letter-spacing:1px; display:inline-block;">EXPLORE ON FRAGRANTICA</a>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()