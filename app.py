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
# 2. CUSTOM CSS (DARK LUXURY THEME)
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    /* Headers - Gold Color */
    h1, h2, h3 {
        color: #D4AF37 !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 300;
    }
    /* Sidebar Background */
    [data-testid="stSidebar"] {
        background-color: #161a24;
        border-right: 1px solid #333;
    }
    /* Metric Cards Styling */
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
    /* Link Styling */
    a {
        color: #D4AF37 !important;
        text-decoration: none;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. DATA LOADING & PROCESSING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    file_path = "scentsational_data.csv"
    try:
        # Attempt 1: Load with standard UTF-8 encoding
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        # Attempt 2: Fallback to ISO-8859-1 (common for Excel CSVs)
        try:
            df = pd.read_csv(file_path, encoding='ISO-8859-1')
        except Exception as e:
            st.error(f"⚠️ Critical Error: Could not load data. Details: {e}")
            return pd.DataFrame()
    except FileNotFoundError:
        st.error(f"⚠️ File '{file_path}' not found. Please upload the dataset.")
        return pd.DataFrame()
    
    # Clean column names (remove whitespace)
    df.columns = [c.strip() for c in df.columns]
    
    # Ensure numeric columns are properly typed
    if 'Rating' in df.columns:
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    
    return df

df = load_data()

# -----------------------------------------------------------------------------
# 4. SIDEBAR FILTERS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🎚️ Refine Search")
    
    # Text Search
    search_query = st.text_input("🔍 Search Brand or Scent", placeholder="e.g. Tom Ford...")
    
    st.markdown("---")
    
    # Strict Mode Toggle
    strict_mode = st.checkbox("⚡ Strict Mode (4.5+ only)", value=False)
    
    # Notes Filter (Extract unique accords)
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
# 5. FILTERING LOGIC
# -----------------------------------------------------------------------------
if not df.empty:
    filtered_df = df.copy()

    # Apply Strict Mode Filter
    if strict_mode and 'Rating' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Rating'] >= 4.5]

    # Apply Text Search Filter
    if search_query:
        mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
        filtered_df = filtered_df[mask]

    # Apply Notes Filter
    if selected_accords and 'Accords' in filtered_df.columns:
        for note in selected_accords:
            filtered_df = filtered_df[filtered_df['Accords'].astype(str).str.contains(note, case=False)]
else:
    filtered_df = pd.DataFrame()

# -----------------------------------------------------------------------------
# 6. MAIN DASHBOARD UI
# -----------------------------------------------------------------------------

st.title("✨ ScentSational | The Atelier")
st.markdown("*\"Scent is the brother of breath.\"* — **Yves Saint Laurent**")
st.markdown("---")

if filtered_df.empty:
    st.warning("No fragrances found matching your criteria.")
else:
    # --- KPI Metrics Section ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Fragrances", f"{len(filtered_df):,}")
    with col2:
        val = filtered_df['Rating'].mean() if 'Rating' in filtered_df.columns else 0
        st.metric("Average Rating", f"{val:.2f} ⭐")
    with col3:
        if 'Name' in filtered_df.columns and 'Rating' in filtered_df.columns:
            top_scent = filtered_df.sort_values(by='Rating', ascending=False).iloc[0]['Name']
        else:
            top_scent = "N/A"
        st.metric("Top Selection", top_scent)

    st.markdown("### 📊 Market Insights")
    
    # --- Charts Section ---
    tab1, tab2 = st.tabs(["📈 Score Distribution", "🏆 Top Designers"])
    
    with tab1:
        if 'Rating' in filtered_df.columns:
            fig = px.histogram(filtered_df, x="Rating", nbins=20, color_discrete_sequence=['#D4AF37'])
            fig.update_layout(
                title="Quality Distribution",
                plot_bgcolor="rgba(0,0,0,0)", 
                paper_bgcolor="rgba(0,0,0,0)", 
                font_color="#e0e0e0"
            )
            st.plotly_chart(fig, use_container_width=True)
            
    with tab2:
        if 'Brand' in filtered_df.columns:
            top_brands = filtered_df['Brand'].value_counts().head(10).reset_index()
            top_brands.columns = ['Brand', 'Count']
            fig = px.bar(top_brands, x='Count', y='Brand', orientation='h', color_discrete_sequence=['#C0C0C0'])
            fig.update_layout(
                title="Top Designers by Volume",
                plot_bgcolor="rgba(0,0,0,0)", 
                paper_bgcolor="rgba(0,0,0,0)", 
                font_color="#e0e0e0", 
                yaxis={'categoryorder':'total ascending'}
            )
            st.plotly_chart(fig, use_container_width=True)

    # --- Data Table Section ---
    st.markdown("### 🔍 Curated Collection")
    st.dataframe(filtered_df, use_container_width=True, height=500, hide_index=True)