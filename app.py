# -----------------------------------------------------------------------------
# 1. LUXURY STYLING & ANIMATIONS
# -----------------------------------------------------------------------------
st.set_page_config(page_title="ScentSational | Atelier", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Lato:wght@300;400;700&display=swap');

    /* ANIMATIONS */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #1a1a1a 0%, #000000 100%);
        color: #E0E0E0;
        font-family: 'Lato', sans-serif;
    }

    /* HEADER STYLING */
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
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    .header-frame {
        border: 1px solid rgba(212, 175, 55, 0.3);
        padding: 40px;
        margin-bottom: 50px;
        background: rgba(10, 10, 10, 0.6);
        box-shadow: 0 10px 30px rgba(0,0,0,0.8), inset 0 0 20px rgba(212, 175, 55, 0.05);
        animation: fadeIn 1.5s ease-out;
    }

    /* LUXURY RESULT CARD */
    .perfume-card {
        border: 1px solid rgba(212, 175, 55, 0.2);
        background: linear-gradient(145deg, #0f0f0f, #050505);
        padding: 40px;
        margin: 25px auto;
        max-width: 800px;
        text-align: center;
        border-radius: 4px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.9);
        transition: 0.5s;
        animation: fadeIn 1s ease-in-out;
    }
    .perfume-card:hover {
        border-color: #D4AF37;
        box-shadow: 0 0 25px rgba(212, 175, 55, 0.15);
        transform: translateY(-5px);
    }

    .row-brand {
        font-size: 1.8rem; 
        font-weight: 900;
        letter-spacing: 6px;
        color: #D4AF37;
        margin-bottom: 10px;
    }
    
    .row-name {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        color: #ffffff;
        margin-bottom: 15px;
        opacity: 0.95;
    }

    /* SIDEBAR LUXURY BOX */
    .sidebar-ai-box {
        border: 1px solid #D4AF37;
        padding: 20px;
        background: rgba(212, 175, 55, 0.03);
        text-align: center;
        margin-top: 20px;
    }

    /* TABS STYLING */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        color: #666 !important;
        font-size: 0.9rem;
        letter-spacing: 2px;
    }
    .stTabs [aria-selected="true"] {
        color: #D4AF37 !important;
        border-bottom-color: #D4AF37 !important;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA LOAD & PREP
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('scentsational_data.csv', sep=None, encoding='latin1', engine='python')
        # Proste czyszczenie
        df.columns = df.columns.str.strip()
        df = df.rename(columns={'Perfume': 'Name'}) if 'Perfume' in df.columns else df
        df['Name'] = df['Name'].fillna("Unknown").astype(str).str.title()
        df['Brand'] = df['Brand'].fillna("Unknown").astype(str).str.upper()
        df['Rating Value'] = pd.to_numeric(df['Rating Value'], errors='coerce').fillna(0)
        
        # Łączenie nut do wyszukiwarki
        accord_cols = ['mainaccord1', 'mainaccord2', 'mainaccord3', 'mainaccord4', 'mainaccord5']
        df['All_Notes'] = df[accord_cols].apply(lambda x: ' '.join(x.dropna().astype(str)).lower(), axis=1)
        return df
    except:
        return None

def main():
    df = load_data()
    if df is None: return

    # SIDEBAR
    with st.sidebar:
        st.markdown("<div class='sidebar-ai-box'>", unsafe_allow_html=True)
        st.markdown("<p style='color:#D4AF37; font-size:0.7rem; letter-spacing:2px;'>UPGRADE EXPERIENCE</p>", unsafe_allow_html=True)
        st.write("Need AI-powered search? Try ScentSational Heavy Core for chemical DNA matching.")
        st.markdown("""
            <a href="https://huggingface.co/spaces/MagdalenaRomaniecka/ScentSational-Fragrantica-LFS" target="_blank" style="
                display: inline-block; width:100%; border: 1px solid #D4AF37; color: #000; background:#D4AF37; 
                padding: 10px; text-decoration: none; font-size: 0.7rem; font-weight: bold; letter-spacing: 2px;">
               LAUNCH AI CORE
            </a>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # HEADER
    st.markdown("""
        <div class="header-frame">
            <h1>SCENTSATIONAL</h1>
            <div style="text-align:center; color:#888; font-size:0.8rem; letter-spacing:5px; text-transform:uppercase;">
                The Atelier &bull; Intelligence Platform
            </div>
        </div>
    """, unsafe_allow_html=True)

    tab_insight, tab_explore = st.tabs(["ANALYSIS", "THE COLLECTION"])

    with tab_insight:
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.8rem; letter-spacing:2px;'>TOP HOUSES</p>", unsafe_allow_html=True)
            top_b = df['Brand'].value_counts().head(8)
            fig = go.Figure(go.Bar(x=top_b.values, y=top_b.index, orientation='h', marker_color='#D4AF37'))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300, 
                              margin=dict(l=0,r=0,t=0,b=0), font=dict(color="#888"), yaxis=dict(autorange="reversed"))
            # staticPlot=True zapobiega zoomowaniu na mobile
            st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})

        with c2:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.8rem; letter-spacing:2px;'>CORE ACCORDS</p>", unsafe_allow_html=True)
            top_a = df['mainaccord1'].value_counts().head(8)
            fig2 = go.Figure(go.Bar(x=top_a.values, y=top_a.index, orientation='h', marker_color='#C5A059'))
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300, 
                               margin=dict(l=0,r=0,t=0,b=0), font=dict(color="#888"), yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig2, use_container_width=True, config={'staticPlot': True})

        with c3:
            st.markdown("<p style='color:#D4AF37; text-align:center; font-size:0.8rem; letter-spacing:2px;'>RATING TRENDS</p>", unsafe_allow_html=True)
            # Przykład 3 wykresu - rozkład ocen
            fig3 = go.Figure(go.Histogram(x=df[df['Rating Value']>0]['Rating Value'], marker_color='#D4AF37', nbinsx=20))
            fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300, 
                               margin=dict(l=0,r=0,t=0,b=0), font=dict(color="#888"))
            st.plotly_chart(fig3, use_container_width=True, config={'staticPlot': True})

    with tab_explore:
        query = st.text_input("", placeholder="Search by brand, name or note (e.g. 'Tom Ford', 'Vanilla', 'Oud')...", label_visibility="collapsed")
        
        # Centrowany przycisk Top Rated
        _, col_btn, _ = st.columns([2,1,2])
        top_filter = col_btn.checkbox("View Top Rated Only (4.5+)")

        # Logika wyszukiwania rozszerzona o nuty
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

        st.markdown(f"<p style='text-align:center; color:#555; letter-spacing:2px;'>{len(filtered)} PIECES IDENTIFIED</p>", unsafe_allow_html=True)

        for _, row in filtered.head(20).iterrows():
            st.markdown(f"""
                <div class="perfume-card">
                    <div class="row-brand">{row['Brand']}</div>
                    <div class="row-name">{row['Name']}</div>
                    <div style="color:#D4AF37; font-size:0.9rem; margin-bottom:10px; font-weight:bold;">★ {row['Rating Value']:.2f}</div>
                    <div style="color:#666; font-style:italic; margin-bottom:25px;">{row.get('Main Accords', 'N/A')}</div>
                    <a href="{row.get('url', '#')}" target="_blank" style="
                        text-decoration:none; color:#D4AF37; border:1px solid #D4AF37; 
                        padding:10px 30px; font-size:0.7rem; letter-spacing:2px; text-transform:uppercase;">
                        Consult Archives
                    </a>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()