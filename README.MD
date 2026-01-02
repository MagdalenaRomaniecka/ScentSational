# ScentSational: AI Perfume Concierge

**A "Dark Luxury" AI-powered recommendation engine helping users discover their signature scent.**

> "Scent is the brother of breath."

### 🎯 Project Goal
To eliminate the overwhelming complexity of choosing a perfume by using Artificial Intelligence. Unlike traditional filters, ScentSational uses Natural Language Processing (NLP) and image embedding logic to understand the *vibe* of a fragrance, acting as a personal digital concierge.

---

## 📊 Data Insights (Exploratory Data Analysis)

Before training the AI model, we analyzed the underlying structure of the `perfumes_dataset.csv`.

### 1. The Olfactory Landscape
An analysis of the most dominant main accords present in the dataset. Citrus, Woody, and Fruity notes dominate the landscape.

![Olfactory Landscape Chart](assets/olfactory_landscape.png)

### 2. Top Designers by Volume
A view of the fragrance houses with the highest number of entries in our database.

![Top Designers Chart](assets/top_designers.png)

---

## 📚 Data Source
The application is powered by a curated dataset (`perfumes_dataset.csv`) specifically processed for this project.
* **Source:** Consolidated data aggregating olfactory notes, popularity ratings, and visual assets (images) from public fragrance databases.
* **Preprocessing:** The raw data underwent rigorous cleaning and feature engineering to make it suitable for NLP vectorization (SBERT).

---

## 🧠 The AI Engine (How It Works)

The recommendation system utilizes a **Hybrid Similarity Approach**, combining textual analysis with visual cues.

1.  **Vectorization**:
    * **SBERT & TF-IDF**: We utilize Sentence-BERT to generate dense vector embeddings for perfume descriptions and accords.
    * **Image Embeddings**: Visual features of perfume bottles are mapped into the same vector space.
2.  **Cosine Similarity**: The core logic calculates the angular distance between the user's input "hero" perfume and the rest of the database.
3.  **Optimization**: Heavy matrix calculations are pre-computed and stored in `hybrid_similarity.npy` for real-time performance.

---

## 🛠️ Tech Stack

* **Language**: Python 3.9+
* **Framework**: Streamlit (with Custom CSS for "Dark Luxury" UI)
* **AI & Machine Learning**:
    * Sentence-Transformers (SBERT)
    * Scikit-learn (Cosine Similarity, TF-IDF)
    * NumPy (Matrix operations)
* **Data Manipulation**: Pandas
* **Visualization**: Plotly (used for EDA charts shown above)

---

## 📂 Project Structure

```text
ScentSational/
├── assets/                  # Images for README and UI
│   ├── olfactory_landscape.png
│   └── top_designers.png
├── app.py                   # Main Streamlit application logic
├── perfumes_dataset.csv     # Primary dataset (Source of Truth)
├── hybrid_similarity.npy    # Pre-calculated AI model weights
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation