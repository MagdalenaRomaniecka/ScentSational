import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re

# -----------------------------------------------------------------------------
# 1. LUXURY CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
# This function MUST be the first Streamlit command in the script
st.set_page_config(page_title="ScentSational | Atelier", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Lato:wght@300;400;700&display=swap');

    /* ANIMATIONS */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #1a1a1a 0%, #000000 100%);
        color: #E0E0E0;
        font-family: 'Lato', sans-serif;
    }

    /* HEADER STYLING WITH TEXT GRADIENT */
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
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }

    .header-frame {
        border: 1px solid rgba(212, 175, 55, 0.3);
        padding: 40px;
        margin-bottom: 50px;
        background: rgba(10, 10, 10, 0.6);
        box-shadow: 0 15px 35px rgba(0,0,0,0.8), inset 0 0 20px rgba(212, 175, 55, 0.05);
        animation: fadeIn 1.5s ease-out;
    }

    /* LUXURY RESULT CARD WITH GOLD BORDER & SHADOW */
    .perfume-card {
        border: 1px solid rgba(212, 175, 55, 0.2);
        background: linear-gradient(145deg, #0f0f0f, #050505);
        padding: 45px;
        margin: 30px auto;
        max-width: 850px;
        text-align: center;
        border-radius: 2px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.9), 0 0 15px rgba(212, 175, 55, 0.03);
        transition: 0.5s ease;
        animation: fadeIn 1s ease-in-out;
    }
    .perfume-card:hover {
        border-color: rgba(212, 175, 55, 0.6);
        box-shadow: 0 0 30px rgba(212, 175, 55, 0.15);
        transform: translateY(-8px);
    }

    .row-brand {
        font-family: 'Lato', sans-serif;
        font-size: 2rem; 
        font-weight: 900;
        letter-spacing: 8px;
        color: #D4AF37;
        margin-bottom: 12px;
        text-transform: uppercase;
    }
    
    .row-name {
        font-family: 'Playfair Display', serif;
        font-size: 1.6rem;
        color: #ffffff;
        margin-bottom: 18px;
        font-style: italic;
        opacity: 0.95;
    }

    /* SIDEBAR LUXURY BOX */
    .sidebar-ai-box {
        border: 1px solid rgba(212, 175, 55, 0.5);
        padding: 25px 15px;
        background: rgba(212, 175, 55, 0.05);
        text-align: center;
        margin-top: 20px;
        border-radius: 2px;
    }

    /* CUSTOM TABS STYLE */
    .stTabs [data-baseweb="tab-list"] {
        gap: 30px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        color: #777 !important;
        font-size: 1rem;
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    .stTabs [aria-selected="true"] {
        color: #D4AF37 !important;
        border-bottom-color: #D4AF37 !important;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA ENGINE
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    try:
        # Load dataset with automatic delimiter detection
        df = pd.read_csv('scentsational_data.csv', sep=None, encoding='latin1', engine='python')
        df.columns = df.columns.str.strip()
        
        # Standardize column names
        if 'Perfume' in df.columns: df = df.rename(columns={'Perfume': 'Name'})
        
        df['Name'] = df['Name'].fillna("Unknown").astype(str).str.title()
        df['Brand'] = df['Brand'].fillna("Unknown").astype(str).str.upper()
        df['Rating Value'] = pd.to_numeric(df['Rating Value'], errors='coerce').fillna(0)
        
        # Create hidden field for smart note searching
        accord_cols = ['mainaccord1', 'mainaccord2', 'mainaccord3', 'mainaccord4', 'mainaccord5']
        existing_accords = [c for c in accord_cols if c in df.columns]
        df['All_Notes'] = df[existing_accords].apply(lambda x: ' '.join(x.dropna().astype(str)).lower(), axis=1)
        
        if 'mainaccord1' not in df.columns: df['mainaccord1'] = "Unknown"
        
        return df
    except:
        return None

def main():
    df = load_data()
    if df is None:
        st.error("Database connection failed. Please check scentsational_data.csv.")
        return

    # --- SIDEBAR (AI CORE REDIRECT) ---
    with st.sidebar:
        st.markdown("<div class='sidebar-ai-box'>", unsafe_allow_html=True)
        st.markdown("<p style='color:#D4AF37; font-size:0.75rem; font-weight:bold; letter-spacing:2px; margin-bottom:15px;'>ELITE UPGRADE</p>", unsafe_allow_html=True)
        st.write("Looking for a deeper connection? Try **ScentSational Heavy Core** to find fragrances based on chemical DNA and neural embeddings.")
        st.markdown("""
            <a href="https://huggingface.co/spaces/MagdalenaRomaniecka/ScentSational-Fragrantica-LFS" target="_blank" style="
                display: inline-block; width:100%; border: 1px solid #D4AF37; color: #000; background:#D4AF37; 
                padding: 12px; text-decoration: none; font-size: 0.75rem; font-weight: bold; letter-spacing: 2px; margin-top:15px;">
               LAUNCH AI CORE
            </a>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- HEADER ---
    st.markdown("""
        <div class="header-frame">
            <h1>SCENTSATIONAL</h1>
            <div style="text-align:center; color:#888; font-size:0.85rem; letter-spacing:5px; text-transform:uppercase; margin-top:10px;">
                The Atelier &bull; Fragrance Intelligence Platform
            </div>
        </div>
    """, unsafe_allow_html=True)

    tab_insight, tab_explore = st.tabs(["MARKET ANALYSIS", "THE COLLECTION"])

    with tab_insight:
        # THREE CHARTS LAYOUT (STATIC FOR MOBILE STABILITY)
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.8rem; font-weight:bold; letter-spacing:2px;'>PRESTIGE HOUSES</p>", unsafe_allow_html=True)
            top_b = df['Brand'].value_counts().head(8)
            fig = go.Figure(go.Bar(x=top_b.values, y=top_b.index, orientation='h', marker_color='#D4AF37'))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=350, 
                              margin=dict(l=0,r=10,t=0,b=0), font=dict(color="#999"), yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})

        with c2:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.8rem; font-weight:bold; letter-spacing:2px;'>CORE ACCORDS</p>", unsafe_allow_html=True)
            top_a = df['mainaccord1'].value_counts().head(8)
            fig2 = go.Figure(go.Bar(x=top_a.values, y=top_a.index, orientation='h', marker_color='#C5A059'))
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=350, 
                               margin=dict(l=0,r=10,t=0,b=0), font=dict(color="#999"), yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig2, use_container_width=True, config={'staticPlot': True})

        with c3:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.8rem; font-weight:bold; letter-spacing:2px;'>SCORE DISTRIBUTION</p>", unsafe_allow_html=True)
            valid_scores = df[df['Rating Value'] > 0]['Rating Value']
            fig3 = go.Figure(go.Histogram(x=valid_scores, marker_color='#D4AF37', nbinsx=15))
            fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=350, 
                               margin=dict(l=0,r=10,t=0,b=0), font=dict(color="#999"))
            st.plotly_chart(fig3, use_container_width=True, config={'staticPlot': True})

    with tab_explore:
        # SMART SEARCH (NAME, BRAND, NOTES)
        query = st.text_input("", placeholder="Search by brand, name or specific note (e.g. 'Tom Ford', 'Vanilla')...", label_visibility="collapsed")
        
        # Centered Rating Filter
        _, col_btn, _ = st.columns([1.5, 1, 1.5])
        with col_btn:
            top_filter = st.checkbox("Show Only Top Rated (4.5 ★+)")

        if query:
            q = query.lower()
            filtered = df[
                df['Brand'].str.lower().str.contains(q) | 
                df['Name'].str.lower().str.contains(q) |
                df['All_Notes'].str.contains(q)
            ]
        else:
            filtered = df

        if top_filter:
            filtered = filtered[filtered['Rating Value'] >= 4.5]

        st.markdown(f"<p style='text-align:center; color:#666; letter-spacing:3px; margin-top:20px;'>{len(filtered)} ARTIFACTS IDENTIFIED</p>", unsafe_allow_html=True)

        # GENERATING GOLDEN RESULT CARDS
        for _, row in filtered.head(25).iterrows():
            st.markdown(f"""
                <div class="perfume-card">
                    <div class="row-brand">{row['Brand']}</div>
                    <div class="row-name">{row['Name']}</div>
                    <div style="color:#D4AF37; font-size:1.1rem; margin-bottom:15px; font-weight:bold; letter-spacing:2px;">
                        ★ {row['Rating Value']:.2f} / 5.0
                    </div>
                    <div style="color:#888; font-style:italic; font-family:'Playfair Display', serif; font-size:1.1rem; margin-bottom:35px; line-height:1.6;">
                        {row.get('Main Accords', 'N/A')}
                    </div>
                    <a href="{row.get('url', '#')}" target="_blank" style="
                        text-decoration:none; color:#000; background:#D4AF37; border:1px solid #D4AF37; 
                        padding:12px 40px; font-size:0.75rem; font-weight:bold; letter-spacing:3px; text-transform:uppercase; transition:0.3s;">
                        Consult Archives
                    </a>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()