import streamlit as st
import pandas as pd
import pickle
import re
from sentence_transformers import SentenceTransformer, util

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="ScentSational | AI Core",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. LUXURY CSS (THE ATELIER TWIN + COMPACT MOBILE) ---
st.markdown("""
    <style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=Montserrat:wght@300;400;500;600;700&display=swap');

    /* GLOBAL STYLES */
    html, body, [class*="css"], .stMarkdown, div, span, p {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 400 !important; 
        color: #E0E0E0 !important;
        font-size: 0.95rem !important;
    }

    /* BACKGROUND */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #1a1a1a 0%, #000000 100%);
    }

    /* HIDE SYSTEM ELEMENTS */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stTextInput label {display: none;}

    /* --- TYPOGRAPHY --- */
    h1 {
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 300 !important;
        background: linear-gradient(to bottom, #D4AF37 0%, #F0E68C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: clamp(2.2rem, 6vw, 4rem) !important; 
        text-transform: uppercase;
        letter-spacing: clamp(2px, 1vw, 6px);
        margin: 0;
        padding-top: 10px;
    }
    
    .sub-header {
        font-family: 'Montserrat', sans-serif !important;
        color: #888;
        font-size: 0.75rem !important;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 20px;
        text-align: center;
    }

    /* INTRO TEXT */
    .intro-text {
        font-family: 'Cormorant Garamond', serif !important;
        font-style: italic;
        font-size: clamp(1.2rem, 3vw, 1.5rem) !important;
        color: #D4AF37 !important;
        text-align: center;
        max-width: 800px;
        margin: 0 auto 10px auto;
        line-height: 1.5;
        padding: 0 15px;
    }
    
    .intro-hint {
        color: #666 !important;
        font-size: 0.8rem !important;
        text-align: center;
        margin-bottom: 30px;
        font-style: italic;
    }

    /* --- SIDEBAR COMPACTING --- */
    section[data-testid="stSidebar"] {
        background-color: #080808 !important;
        border-right: 1px solid rgba(212, 175, 55, 0.15);
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
    }
    section[data-testid="stSidebar"] .stElementContainer {
        margin-bottom: 0.5rem !important;
    }
    
    .stSelectbox div[data-baseweb="select"] > div {
        border: 1px solid rgba(212, 175, 55, 0.4) !important;
        background-color: rgba(10, 10, 10, 0.8) !important;
        color: #fff !important;
        min-height: 38px !important;
    }
    .stSelectbox label { 
        display: block !important; 
        color: #D4AF37 !important; 
        font-size: 0.65rem !important;
        text-transform: uppercase; 
        letter-spacing: 1px;
        margin-bottom: 2px !important;
    }
    
    /* Dropdown Options */
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul {
        background-color: #080808 !important;
        border: 1px solid #333 !important;
    }
    li[aria-selected="true"] {
        background-color: #222 !important;
        color: #D4AF37 !important;
    }

    /* --- SEARCH INPUT --- */
    .stTextInput > div > div > input {
        background-color: rgba(15, 15, 15, 0.8);
        color: #FFF !important; 
        border: 1px solid rgba(212, 175, 55, 0.5);
        text-align: center;
        padding: 18px 20px;
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 1.3rem !important;
        font-style: italic;
        border-radius: 4px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #D4AF37;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.2);
        background-color: rgba(20, 20, 20, 1);
    }
    ::placeholder { color: #666 !important; opacity: 1; }

    /* --- PERFUME CARD STYLING --- */
    .perfume-card {
        border: 1px solid rgba(212, 175, 55, 0.15);
        background: rgba(12, 12, 12, 0.8);
        padding: 25px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        border-radius: 4px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        transition: transform 0.3s ease;
        backdrop-filter: blur(10px);
        position: relative;
    }
    .perfume-card:hover {
        transform: translateY(-5px);
        border-color: rgba(212, 175, 55, 0.5);
        background: rgba(15, 15, 15, 0.9);
    }

    /* EMBLEM */
    .brand-emblem {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        border: 1px solid #D4AF37;
        color: #D4AF37;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Montserrat', sans-serif;
        font-size: 0.8rem;
        font-weight: bold;
        margin: 0 auto 15px auto;
        background: rgba(212, 175, 55, 0.05);
        letter-spacing: 0;
        text-transform: uppercase;
    }

    .row-brand { 
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.9rem !important; 
        font-weight: 600 !important; 
        letter-spacing: 2px; 
        color: #D4AF37 !important; 
        margin-bottom: 5px; 
        text-transform: uppercase;
    }
    .row-name { 
        font-family: 'Cormorant Garamond', serif !important; 
        font-size: 1.4rem !important; 
        color: #fff !important; 
        margin-bottom: 5px; 
        font-style: italic; 
    }
    .row-meta {
        font-size: 0.65rem !important;
        color: #888 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 15px;
        border-bottom: 1px solid #222;
        padding-bottom: 10px;
        display: inline-block;
        width: 80%;
    }
    .row-rating {
        color: #D4AF37;
        font-weight: bold;
        font-size: 1rem;
        margin-bottom: 10px;
    }
    .row-notes {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 0.9rem !important;
        color: #AAA !important;
        font-style: italic;
        margin-bottom: 15px;
        line-height: 1.4;
    }
    
    /* MATCH BAR CSS */
    .match-wrapper { width: 100%; margin-bottom: 15px; padding: 0 10px; }
    .match-header { display: flex; justify-content: space-between; font-size: 0.6rem !important; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
    .bar-bg { width: 100%; height: 2px; background-color: #333; border-radius: 1px; }
    .bar-fill { height: 100%; background-color: #D4AF37; border-radius: 1px; box-shadow: 0 0 8px rgba(212, 175, 55, 0.6); }
    .match-explain { font-size: 0.55rem !important; color: #555 !important; text-align: center; margin-top: 5px; font-style: italic; }

    /* BUTTON */
    a.gold-btn {
        text-decoration: none; color: #000 !important; background: #D4AF37; padding: 12px 25px; 
        font-size: 0.75rem !important; font-weight: 600 !important; letter-spacing: 1px; 
        border-radius: 2px; display: inline-block; font-family: 'Montserrat', sans-serif !important;
        transition: 0.3s; text-transform: uppercase; width: 100%;
    }
    a.gold-btn:hover { background: #F0E68C; box-shadow: 0 0 15px rgba(212, 175, 55, 0.4); }
    
    /* FOOTER */
    .custom-footer {
        text-align: center; color: #444; font-size: 0.6rem !important; margin-top: 80px; 
        padding-top: 20px; border-top: 1px solid #111; letter-spacing: 0.5px; opacity: 0.7;
    }
    .custom-footer a { color: #555 !important; text-decoration: none; }
    .custom-footer a:hover { color: #777 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIC & DATA CLEANING ---
@st.cache_resource
def load_data():
    try:
        df = pd.read_csv('scentsational_data.csv', sep=None, engine='python', encoding='latin1')
        df.columns = df.columns.str.strip()
        
        # MAPPING
        cols = df.columns.tolist()
        brand_col = next((c for c in cols if 'brand' in c.lower()), 'Brand')
        name_col = next((c for c in cols if 'perfume' in c.lower() or 'name' in c.lower()), 'Name')
        rating_col = next((c for c in cols if 'rating' in c.lower()), 'Rating Value')
        gender_col = next((c for c in cols if 'gender' in c.lower()), 'Gender')
        year_col = next((c for c in cols if 'year' in c.lower() or 'date' in c.lower() or 'launch' in c.lower()), 'Year')

        df = df.rename(columns={
            brand_col: 'Brand', name_col: 'Name',
            rating_col: 'Rating Value', gender_col: 'Gender', year_col: 'Year'
        })
        
        # Combine Notes
        accord_cols = ['mainaccord1', 'mainaccord2', 'mainaccord3', 'mainaccord4', 'mainaccord5']
        existing_accords = [c for c in accord_cols if c in df.columns]
        if existing_accords:
             df['Main Accords'] = df[existing_accords].apply(lambda x: ', '.join(x.dropna().astype(str)), axis=1)
        else:
             notes_col = next((c for c in cols if 'accord' in c.lower() or 'note' in c.lower()), 'Main Accords')
             df = df.rename(columns={notes_col: 'Main Accords'})
        
        # Clean Data
        df['Rating Value'] = df['Rating Value'].astype(str).str.replace(',', '.')
        df['Rating Value'] = pd.to_numeric(df['Rating Value'], errors='coerce').fillna(0)
        
        def clean_str(x): return str(x).replace('-', ' ').title() if pd.notna(x) else ""
        df['Brand'] = df['Brand'].apply(clean_str)
        df['Name'] = df['Name'].apply(clean_str)
        
        if 'Gender' not in df.columns: df['Gender'] = "Unisex"
        else: df['Gender'] = df['Gender'].fillna("Unisex")
        
        if 'Year' in df.columns:
            df['Year'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0).astype(int)
            df['Year'] = df['Year'].apply(lambda x: str(x) if x > 1000 else "")
        else:
            df['Year'] = ""
            
        if 'Main Accords' not in df.columns: df['Main Accords'] = "Notes Unavailable"
        
        with open('scent_embeddings.pkl', 'rb') as f:
            embeddings = pickle.load(f)
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        return df, embeddings, model
    except Exception as e:
        st.error(f"System Error: {e}")
        return None, None, None

def get_initials(text):
    if not text: return "SC"
    words = str(text).split()
    if not words: return "SC"
    if len(words) == 1:
        return words[0][:2].upper()
    return (words[0][0] + words[-1][0]).upper()

df, embeddings, model = load_data()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<p style='color:#D4AF37; font-size:0.7rem; font-weight:bold; letter-spacing:2px; text-align:center; margin-bottom:5px;'>SETTINGS</p>", unsafe_allow_html=True)
    
    # 1. GENDER
    gender_option = "All"
    if df is not None:
        genders = ["All"] + sorted([g for g in df['Gender'].astype(str).unique() if g != 'nan'])
        gender_option = st.selectbox("Gender", genders)
    
    # 2. RATING FILTER (SIMPLIFIED & REORDERED)
    rating_options = {
        0.0: "Any Rating (Show All)",
        4.0: "★ 4.0+",
        3.0: "★ 3.0+",
        2.0: "★ 2.0+",
        1.0: "★ 1.0+"
    }
    rating_labels = list(rating_options.values())
    default_idx = 0
    
    selected_label = st.selectbox("Minimum Rating Score", rating_labels, index=default_idx)
    min_rating = [k for k, v in rating_options.items() if v == selected_label][0]
    
    # 3. NOTES
    note_search = "All Notes"
    if df is not None:
         all_notes = ','.join(df['Main Accords'].astype(str)).replace('nan','').split(',')
         all_notes = [n.strip().title() for n in all_notes if len(n)>2]
         if all_notes:
            top_notes = pd.Series(all_notes).value_counts().head(50).index.tolist()
            top_notes.sort()
            note_search = st.selectbox("Dominant Note", ["All Notes"] + top_notes)

    st.markdown("---")
    st.markdown(f"""
    <div style="text-align:center;">
        <a href="https://scentsational-zbznjhgc4xv7faddappdc2b.streamlit.app/" target="_blank" style="color:#888; text-decoration:none; font-size:0.6rem; letter-spacing:1px; display:block; margin-bottom:5px;">OPEN ATELIER APP</a>
        <a href="https://github.com/MagdalenaRomaniecka/ScentSational-Fragrantica-LFS" target="_blank" style="color:#888; text-decoration:none; font-size:0.6rem; letter-spacing:1px; display:block;">VIEW ON GITHUB</a>
    </div>
    """, unsafe_allow_html=True)

# --- 5. MAIN UI ---
st.markdown("<h1>SCENTSATIONAL</h1>", unsafe_allow_html=True)
st.markdown('<div class="sub-header">The Intelligence Platform</div>', unsafe_allow_html=True)

# INTRO TEXT
st.markdown("""
<div class="intro-text">
    Unlock the chemical DNA of scent.<br>
    Describe a <b>specific note harmony</b>, a <b>fleeting memory</b>, or a <b>vivid mood</b>.
</div>
<div class="intro-hint">
    Try: "Old library with cognac", "Walk in a rainy forest", "Warm Spicy Vanilla", or "Fresh Citrus & Wood".
</div>
""", unsafe_allow_html=True)

with st.expander("👁️ How AI Matches Vibe? (Click to learn)"):
    st.markdown("""
    <div style="text-align:center; color:#AAA; font-size:0.8rem; line-height:1.6;">
        <b>Smart Precision Search:</b><br><br>
        1. <b>Precision Match:</b> We score every word. "Warm Vanilla" ranks higher than just "Vanilla".<br>
        2. <b>Vibe Match:</b> AI Analysis of the concept/feeling (e.g. "Mysterious").<br>
        3. <b>Visual Match:</b> Names matching your description.<br>
        <i>*Results are filtered by your rating preference in the sidebar.</i>
    </div>
    """, unsafe_allow_html=True)

query = st.text_input("Search", placeholder="Type your olfactory vision here...")

if query and df is not None:
    st.write("")
    with st.spinner("Decoding Vibe..."):
        # 1. AI Search (Wide Net)
        query_vec = model.encode(query, convert_to_tensor=True)
        hits = util.semantic_search(query_vec, embeddings, top_k=80) 
        
        st.markdown(f"<div style='text-align:center; color:#666; font-size:0.7rem; letter-spacing:2px; margin-bottom:30px; text-transform:uppercase;'>Olfactory Matches: <i>'{query}'</i></div>", unsafe_allow_html=True)
        
        # 2. Process
        processed_results = []
        query_words = set(re.split(r'\W+', query.lower()))
        query_words = {w for w in query_words if len(w) > 2} 

        for hit in hits[0]:
            idx = hit['corpus_id']
            row = df.iloc[idx]
            
            # FILTERS
            if gender_option != "All" and str(row['Gender']) != str(gender_option): continue
            if note_search != "All Notes" and note_search.lower() not in str(row['Main Accords']).lower(): continue
            
            # RATING CHECK
            rating_val = float(row.get('Rating Value', 0))
            if rating_val < min_rating: continue
            
            # --- HIERARCHY LOGIC V10.0 ---
            
            # 1. Complex Match
            notes_text = str(row['Main Accords']).lower()
            match_count = 0
            for word in query_words:
                if word in notes_text:
                    match_count += 1
            
            # 2. Visual Match
            name_text = (str(row['Name']) + " " + str(row['Brand'])).lower()
            name_match = 0
            for word in query_words:
                if word in name_text:
                    name_match = 1
            
            row['ai_score'] = hit['score']
            row['match_count'] = match_count
            row['name_match'] = name_match
            processed_results.append(row)
            
        # 3. SORTING STRATEGY
        processed_results.sort(key=lambda x: (x['match_count'], x['ai_score'], x['name_match'], float(x.get('Rating Value', 0))), reverse=True)
        
        display_results = processed_results[:15]
        
        if not display_results:
             st.warning(f"No matches found with Rating {min_rating}+. Try lowering the rating filter.")
        else:
            col1, col2, col3 = st.columns([1,1,1])
            cols = [col1, col2, col3]
            
            for i, row in enumerate(display_results):
                current_col = cols[i % 3]
                
                brand = str(row['Brand']).replace('"', '').replace("'", "")
                name = str(row['Name']).replace('"', '').replace("'", "")
                notes = str(row['Main Accords']).replace("-", " ").replace('"', '')
                if len(notes) > 50: notes = notes[:50] + "..."
                
                rating = float(row.get('Rating Value', 0))
                link = row.get('url', '#')
                
                gender = str(row.get('Gender', 'Unisex')).capitalize()
                year = str(row.get('Year', ''))
                meta_info = f"{gender}"
                if year: meta_info += f" &bull; {year}"
                
                initials = get_initials(brand)
                raw_score = row['ai_score']
                visual_score = int(min(98, max(50, raw_score * 180)))
                
                card_html = f"""<div class="perfume-card"><div class="brand-emblem">{initials}</div><div style="width:100%"><div class="row-brand">{brand}</div><div class="row-name">{name}</div><div class="row-meta">{meta_info}</div><div class="row-rating">★ {rating:.2f}</div><div class="match-wrapper"><div class="match-header"><span>Vibe Match</span><span>{visual_score}%</span></div><div class="bar-bg"><div class="bar-fill" style="width:{visual_score}%"></div></div><div class="match-explain">Analyzed via Scent Profile</div></div><div class="row-notes">{notes}</div></div><a href="{link}" target="_blank" class="gold-btn">FRAGRANTICA</a></div>"""
                
                with current_col:
                    st.markdown(card_html, unsafe_allow_html=True)

# --- 6. FOOTER ---
st.markdown("""
<div class="custom-footer">
    ScentSational AI Core v12.0 &bull; Developed by Magdalena Romaniecka &bull; 2026<br>
    Data Source: <a href="https://www.kaggle.com/datasets/olgagmiufana1/fragrantica-com-fragrance-dataset" target="_blank">Fragrantica Dataset (Kaggle)</a> &bull; Powered by Hugging Face
</div>
""", unsafe_allow_html=True)