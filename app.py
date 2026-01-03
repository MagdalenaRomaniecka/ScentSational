import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. LUXURY CONFIGURATION & RESPONSIVE CSS
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

    /* TYPOGRAPHY - RESPONSIVE HEADER */
    h1 {
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 300 !important;
        background: linear-gradient(to bottom, #D4AF37 0%, #F0E68C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: clamp(2rem, 8vw, 4rem) !important; /* Dynamic scale */
        text-transform: uppercase;
        letter-spacing: clamp(5px, 2vw, 12px);
        margin: 0;
    }

    .header-frame {
        border-bottom: 1px solid rgba(212, 175, 55, 0.2);
        padding: 20px 0; /* Reduced vertical padding */
        margin-bottom: 20px;
        background: rgba(10, 10, 10, 0.4);
    }

    /* COMPACT METRIC BOXES */
    .gold-metric {
        border: 1px solid rgba(212, 175, 55, 0.4);
        background-color: rgba(255, 255, 255, 0.01);
        padding: 10px;
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-label { color: #D4AF37; font-size: 0.6rem; text-transform: uppercase; letter-spacing: 2px; }
    .metric-value { 
        font-family: 'Cormorant Garamond', serif; 
        font-size: 1.6rem; 
        color: #F0E68C; 
        font-weight: 300;
    }

    /* RESPONSIVE PERFUME CARD */
    .perfume-card {
        border: 1px solid rgba(212, 175, 55, 0.15);
        background: rgba(10, 10, 10, 0.8);
        padding: clamp(20px, 5vw, 40px);
        margin: 15px auto;
        max-width: 750px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .row-brand { font-size: clamp(1.2rem, 4vw, 1.6rem); font-weight: 900; letter-spacing: 4px; color: #D4AF37; margin-bottom: 2px; }
    .row-name { font-family: 'Cormorant Garamond', serif; font-size: clamp(1.1rem, 3vw, 1.4rem); color: #fff; margin-bottom: 10px; font-style: italic; }
    
    .sidebar-box { border: 1px solid #D4AF37; padding: 15px; background: rgba(212, 175, 55, 0.05); text-align: center; }

    /* Fix for radio buttons visibility */
    div[data-testid="stRadio"] > div { justify-content: center; flex-wrap: wrap; gap: 10px; }
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
    except:
        return None

def main():
    df = load_data()
    if df is None: return

    # SIDEBAR
    with st.sidebar:
        st.markdown("<div class='sidebar-box'>", unsafe_allow_html=True)
        st.markdown("<p style='color:#D4AF37; font-size:0.7rem; font-weight:bold;'>AI CORE</p>", unsafe_allow_html=True)
        st.write("Chemical DNA search.")
        st.markdown(f'<a href="https://huggingface.co/spaces/MagdalenaRomaniecka/ScentSational-Fragrantica-LFS" target="_blank" style="display:inline-block; background:#D4AF37; color:black; padding:8px 15px; text-decoration:none; font-weight:bold; font-size:0.7rem; letter-spacing:1px; margin-top:5px;">LAUNCH CORE</a>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # HEADER
    st.markdown('<div class="header-frame"><h1>SCENTSATIONAL</h1><p style="text-align:center; color:#666; font-size:0.6rem; letter-spacing:4px; text-transform:uppercase;">Atelier Platform</p></div>', unsafe_allow_html=True)

    # METRICS - AUTO WRAP ON MOBILE
    m1, m2, m3, m4 = st.columns([1, 1, 1, 1])
    m1.markdown(f'<div class="gold-metric"><div class="metric-label">Collection</div><div class="metric-value">{len(df):,}</div></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="gold-metric"><div class="metric-label">Designers</div><div class="metric-value">{df["Brand"].nunique()}</div></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="gold-metric"><div class="metric-label">Trending</div><div class="metric-value">{df["mainaccord1"].mode()[0].capitalize()}</div></div>', unsafe_allow_html=True)
    m4.markdown(f'<div class="gold-metric"><div class="metric-label">Avg Rating</div><div class="metric-value">{df[df["Rating Value"] > 0]["Rating Value"].mean():.2f}</div></div>', unsafe_allow_html=True)

    tab_an, tab_cat = st.tabs(["ANALYSIS", "COLLECTION"])

    with tab_an:
        c1, c2, c3 = st.columns([1, 1, 1])
        # Charts use use_container_width=True for responsiveness
        with c1:
            top_b = df['Brand'].value_counts().head(8)
            fig = px.bar(x=top_b.values, y=top_b.index, orientation='h', color_discrete_sequence=['#D4AF37'])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#888", height=300, yaxis={'autorange':'reversed'}, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})

        with c2:
            top_a = df['mainaccord1'].value_counts().head(8)
            fig2 = px.bar(x=top_a.values, y=top_a.index, orientation='h', color_discrete_sequence=['#C5A059'])
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#888", height=300, yaxis={'autorange':'reversed'}, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig2, use_container_width=True, config={'staticPlot': True})

        with c3:
            score_data = pd.cut(df[df['Rating Value'] > 0]['Rating Value'], bins=[0, 3.5, 4.2, 5], labels=['Standard', 'Premium', 'Elite'])
            fig3 = px.pie(score_data.value_counts().reset_index(), values='count', names='Rating Value', hole=0.5, color_discrete_sequence=['#856a35', '#C5A059', '#D4AF37'])
            fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#888", height=300, margin=dict(l=0,r=0,t=0,b=0), showlegend=False)
            st.plotly_chart(fig3, use_container_width=True)

    with tab_cat:
        search_options = sorted(list(df['Name'].unique()) + list(df['Brand'].unique()))
        selected = st.selectbox("Search archives...", options=search_options, index=None)
        
        tier_choice = st.radio("", ["All", "Elite (4.5+)", "Premium (4.0+)", "Standard"], horizontal=True, label_visibility="collapsed")
        
        note_filter = st.text_input("Filter by notes...", placeholder="e.g. Musk, Rose")

        filtered = df.copy()
        if selected: filtered = filtered[(filtered['Name'] == selected) | (filtered['Brand'] == selected)]
        if tier_choice == "Elite (4.5+)": filtered = filtered[filtered['Rating Value'] >= 4.5]
        elif tier_choice == "Premium (4.0+)": filtered = filtered[(filtered['Rating Value'] >= 4.0) & (filtered['Rating Value'] < 4.5)]
        elif tier_choice == "Standard": filtered = filtered[(filtered['Rating Value'] > 0) & (filtered['Rating Value'] < 4.0)]
        
        if note_filter: filtered = filtered[filtered['Search_Index'].str.contains(note_filter.lower())]

        st.markdown(f"<p style='text-align:center; color:#444; font-size:0.7rem;'>{len(filtered)} IDENTIFIED</p>", unsafe_allow_html=True)

        for _, row in filtered.head(20).iterrows():
            st.markdown(f"""
                <div class="perfume-card">
                    <div class="row-brand">{row['Brand']}</div>
                    <div class="row-name">{row['Name']}</div>
                    <div style="color:#D4AF37; font-weight:bold; font-size:1rem;">★ {row['Rating Value']:.2f}</div>
                    <div style="color:#777; font-size:0.8rem; margin: 10px 0;">{row['Main Accords']}</div>
                    <a href="{row.get('url', '#')}" target="_blank" style="text-decoration:none; color:black; background:#D4AF37; padding:10px 20px; font-size:0.7rem; font-weight:bold; display:inline-block; margin-top:10px;">EXPLORE</a>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()