import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. APP CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ScentSational | Atelier",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. DARK LUXURY STYLE (CSS)
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    h1, h2, h3 {
        color: #D4AF37 !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 300;
    }
    [data-testid="stSidebar"] {
        background-color: #161a24;
        border-right: 1px solid #333;
    }
    div[data-testid="metric-container"] {
        background-color: #1e2530;
        border: 1px solid #333;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    div[data-testid="metric-container"] label {
        color: #D4AF37 !important;
    }
    a {
        color: #D4AF37 !important;
        text-decoration: none;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. DATA LOADING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    # We use 'latin1' encoding to prevent UnicodeDecodeError and ParserError
    # This is the most robust method for Kaggle/Legacy datasets
    try:
        df = pd.read_csv("scentsational_data.csv", encoding='latin1')
        
        # Clean column names
        df.columns = [c.strip() for c in df.columns]
        
        # Convert numeric columns
        if 'Rating' in df.columns:
            df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

# -----------------------------------------------------------------------------
# 4. SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🎚️ Refine Search")
    
    search_query = st.text_input("🔍 Search Brand or Scent", placeholder="e.g. Tom Ford...")
    
    st.markdown("---")
    
    strict_mode = st.checkbox("⚡ Strict Mode (4.5+ only)", value=False)
    
    # Notes Filter
    all_accords = []
    if not df.empty and 'Accords' in df.columns:
        raw_accords = df['Accords'].dropna().astype(str).tolist()
        for r in raw_accords:
            parts = [x.strip() for x in r.split(',')]
            all_accords.extend(parts)
        unique_accords = sorted(list(set(all_accords)))
    else:
        unique_accords = []

    selected_accords = st.multiselect("🧪 Filter by Notes", unique_accords[:50])

    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #666; font-size: 0.8em;'>© 2026 ScentSational</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. FILTERING
# -----------------------------------------------------------------------------
if not df.empty:
    filtered_df = df.copy()

    if strict_mode and 'Rating' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Rating'] >= 4.5]

    if search_query:
        mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
        filtered_df = filtered_df[mask]

    if selected_accords and 'Accords' in filtered_df.columns:
        for note in selected_accords:
            filtered_df = filtered_df[filtered_df['Accords'].astype(str).str.contains(note, case=False)]
else:
    filtered_df = pd.DataFrame()

# -----------------------------------------------------------------------------
# 6. DASHBOARD
# -----------------------------------------------------------------------------

st.title("✨ ScentSational | The Atelier")
st.markdown("*\"Scent is the brother of breath.\"* — **Yves Saint Laurent**")
st.markdown("---")

if filtered_df.empty:
    st.warning("No fragrances found matching your criteria.")
else:
    # KPI
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Fragrances", f"{len(filtered_df):,}")
    with col2:
        val = filtered_df['Rating'].mean() if 'Rating' in filtered_df.columns else 0
        st.metric("Average Rating", f"{val:.2f} ⭐")
    with col3:
        if 'Name' in filtered_df.columns and 'Rating' in filtered_df.columns:
            top = filtered_df.sort_values(by='Rating', ascending=False).iloc[0]['Name']
        else:
            top = "N/A"
        st.metric("Top Selection", top)

    st.markdown("### 📊 Market Insights")
    
    # Charts
    tab1, tab2 = st.tabs(["📈 Score Distribution", "🏆 Top Designers"])
    
    with tab1:
        if 'Rating' in filtered_df.columns:
            fig = px.histogram(filtered_df, x="Rating", nbins=20, color_discrete_sequence=['#D4AF37'])
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#e0e0e0")
            st.plotly_chart(fig, use_container_width=True)
            
    with tab2:
        if 'Brand' in filtered_df.columns:
            top = filtered_df['Brand'].value_counts().head(10).reset_index()
            top.columns = ['Brand', 'Count']
            fig = px.bar(top, x='Count', y='Brand', orientation='h', color_discrete_sequence=['#C0C0C0'])
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#e0e0e0", yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

    # Table
    st.markdown("### 🔍 Curated Collection")
    st.dataframe(filtered_df, use_container_width=True, height=500, hide_index=True)