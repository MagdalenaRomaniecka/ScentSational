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
        font-size: 3.8rem !important;
        text-transform: uppercase;
        letter-spacing: 7px;
        margin-bottom: 0px;
    }

    .header-frame {
        border: 1px solid rgba(212, 175, 55, 0.3);
        padding: 40px;
        margin-bottom: 30px;
        background: rgba(10, 10, 10, 0.6);
        box-shadow: 0 15px 35px rgba(0,0,0,0.8);
    }

    /* GOLD METRIC BOXES */
    .gold-metric {
        border: 1px solid #D4AF37;
        background-color: rgba(255, 255, 255, 0.02);
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-label { color: #D4AF37; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px; }
    .metric-value { font-family: 'Playfair Display', serif; font-size: 2rem; color: #F0E68C; }

    /* PERFUME CARD */
    .perfume-card {
        border: 1px solid rgba(212, 175, 55, 0.2);
        background: rgba(15, 15, 15, 0.9);
        padding: 40px;
        margin: 20px auto;
        max-width: 800px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .row-brand { font-size: 1.8rem; font-weight: 900; letter-spacing: 5px; color: #D4AF37; margin-bottom: 5px; }
    .row-name { font-family: 'Playfair Display', serif; font-size: 1.4rem; color: #fff; margin-bottom: 15px; }
    
    .sidebar-box { border: 1px solid #D4AF37; padding: 20px; background: rgba(212, 175, 55, 0.05); text-align: center; }
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
        
        # Proper Cleaning
        df['Name'] = df['Name'].fillna("Unknown").astype(str).str.title()
        df['Brand'] = df['Brand'].fillna("Unknown").astype(str).str.upper()
        df['Rating Value'] = pd.to_numeric(df['Rating Value'], errors='coerce').fillna(0)
        
        # Accords handling
        accord_cols = ['mainaccord1', 'mainaccord2', 'mainaccord3', 'mainaccord4', 'mainaccord5']
        existing = [c for c in accord_cols if c in df.columns]
        df['Main Accords'] = df[existing].apply(lambda x: ', '.join(x.dropna().astype(str)), axis=1)
        df['Search_Field'] = df['Name'] + " " + df['Brand'] + " " + df['Main Accords'].str.lower()
        
        return df
    except:
        return None

def main():
    df = load_data()
    if df is None: return

    # SIDEBAR
    with st.sidebar:
        st.markdown("<div class='sidebar-box'>", unsafe_allow_html=True)
        st.markdown("<p style='color:#D4AF37; font-size:0.7rem; letter-spacing:2px;'>ELITE UPGRADE</p>", unsafe_allow_html=True)
        st.write("Unlock chemical DNA search with Heavy Core.")
        st.link_button("LAUNCH AI CORE", "https://huggingface.co/spaces/MagdalenaRomaniecka/ScentSational-Fragrantica-LFS")
        st.markdown("</div>", unsafe_allow_html=True)

    # HEADER
    st.markdown('<div class="header-frame"><h1>SCENTSATIONAL</h1><p style="text-align:center; color:#888; letter-spacing:4px;">THE ATELIER</p></div>', unsafe_allow_html=True)

    # METRICS (BACK BY POPULAR DEMAND)
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f'<div class="gold-metric"><div class="metric-label">Collection</div><div class="metric-value">{len(df):,}</div></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="gold-metric"><div class="metric-label">Brands</div><div class="metric-value">{df["Brand"].nunique()}</div></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="gold-metric"><div class="metric-label">Top Note</div><div class="metric-value">{df["mainaccord1"].mode()[0].title()}</div></div>', unsafe_allow_html=True)
    m4.markdown(f'<div class="gold-metric"><div class="metric-label">Avg Rating</div><div class="metric-value">{df["Rating Value"].replace(0, pd.NA).mean():.2f}</div></div>', unsafe_allow_html=True)

    tab_an, tab_cat = st.tabs(["MARKET ANALYSIS", "THE COLLECTION"])

    with tab_an:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.8rem;'>PRESTIGE HOUSES</p>", unsafe_allow_html=True)
            top_b = df['Brand'].value_counts().head(10)
            fig = px.bar(x=top_b.values, y=top_b.index, orientation='h', color_discrete_sequence=['#D4AF37'])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#888", height=350, yaxis={'autorange':'reversed'}, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})

        with c2:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.8rem;'>CORE ACCORDS</p>", unsafe_allow_html=True)
            top_a = df['mainaccord1'].value_counts().head(10)
            fig2 = px.bar(x=top_a.values, y=top_a.index, orientation='h', color_discrete_sequence=['#C5A059'])
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#888", height=350, yaxis={'autorange':'reversed'}, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig2, use_container_width=True, config={'staticPlot': True})

        with c3:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.8rem;'>SCORE DISTRIBUTION</p>", unsafe_allow_html=True)
            # FIXED: SCORE DISTRIBUTION AS PIE CHART
            score_bins = pd.cut(df[df['Rating Value'] > 0]['Rating Value'], bins=[0, 3, 4, 5], labels=['Below 3', '3-4', '4-5'])
            pie_df = score_bins.value_counts().reset_index()
            fig3 = px.pie(pie_df, values='count', names='Rating Value', color_discrete_sequence=['#D4AF37', '#C5A059', '#856a35'])
            fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#888", height=350, margin=dict(l=0,r=0,t=30,b=0))
            st.plotly_chart(fig3, use_container_width=True)

    with tab_cat:
        # SMART SEARCH WITH AUTO-SUGGESTIONS
        search_options = sorted(list(df['Name'].unique()) + list(df['Brand'].unique()))
        selected = st.selectbox("Search archives...", options=search_options, index=None, placeholder="Search brand or name...")
        
        col_f1, col_f2 = st.columns([1,1])
        top_only = col_f1.checkbox("Show Only Top Rated (4.5+)")
        note_search = st.text_input("Filter by specific notes (e.g. Vanilla, Oud)...")

        filtered = df.copy()
        if selected: filtered = filtered[(filtered['Name'] == selected) | (filtered['Brand'] == selected)]
        if top_only: filtered = filtered[filtered['Rating Value'] >= 4.5]
        if note_search: filtered = filtered[filtered['Search_Field'].str.contains(note_search.lower())]

        st.markdown(f"<p style='text-align:center; color:#555;'>{len(filtered)} PIECES IDENTIFIED</p>", unsafe_allow_html=True)

        for _, row in filtered.head(20).iterrows():
            st.markdown(f"""
                <div class="perfume-card">
                    <div class="row-brand">{row['Brand']}</div>
                    <div class="row-name">{row['Name']}</div>
                    <div style="color:#D4AF37; font-weight:bold;">★ {row['Rating Value']:.2f} / 5.0</div>
                    <div style="color:#888; font-style:italic; margin: 15px 0;">{row['Main Accords']}</div>
                    <a href="{row.get('url', '#')}" target="_blank" style="text-decoration:none; color:#000; background:#D4AF37; padding:10px 30px; font-size:0.8rem; font-weight:bold; letter-spacing:2px; display:inline-block;">EXPLORE ON FRAGRANTICA</a>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()