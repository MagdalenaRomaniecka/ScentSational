# ✨ ScentSational: AI Perfume Recommender & Market Analysis

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://scentsational-evywcwtgnrevjgm4ubxappy.streamlit.app/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MagdalenaRomaniecka/ScentSational/blob/main/perfume_analysis.ipynb)

> An AI-powered perfume recommendation system that blends chemical note analysis (TF-IDF) with semantic understanding of fragrance descriptions (SBERT) to find your perfect scent match. Includes market segmentation via K-Means clustering.

This repository contains the complete process for building a hybrid content-based recommendation system, from raw data exploration to a deployed interactive web application.

---

## 🖥️ Live Application

This project is deployed as an interactive web app using Streamlit. You can select any perfume from the dataset, and the hybrid AI model will instantly recommend 10 similar scents.

[**🚀 Click here to try the live demo!**](https://scentsational-evywcwtgnrevjgm4ubxappy.streamlit.app/)

*(Optional: Add a screenshot of your running app here)*
`![App Screenshot](images/app_screenshot.png)`

---

## 🚀 Quick Start (Run Locally)

Want to test the recommender on your own machine?

1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/MagdalenaRomaniecka/ScentSational.git](https://github.com/MagdalenaRomaniecka/ScentSational.git)
    cd ScentSational
    ```

2.  **Install dependencies:**
    (You may want to create a virtual environment first: `python -m venv venv`)
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
    The app will open in your browser automatically!

---

## 🧠 How It Works: The AI Model

This system is a **hybrid model** that combines two NLP techniques to understand both the *ingredients* and the *feeling* of a perfume:

1.  **Ingredient Matching (TF-IDF):** A classic `TfidfVectorizer` analyzes the raw scent notes (e.g., "Vanilla," "Rose," "Sandalwood"). This is great for finding literal matches.
2.  **Semantic Matching (SBERT):** A `Sentence-BERT` transformer model (`all-MiniLM-L6-v2`) converts the *marketing descriptions* (e.g., "a warm, sensual scent for a winter evening") into numerical vectors. This captures the "vibe" and context.

The similarity scores from both models are combined to create a final, robust recommendation.

### 📈 Project Insights

Beyond the recommender, the analysis notebook (`perfume_analysis.ipynb`) includes a deep dive into the market:

* **Market Segmentation:** Using **K-Means clustering** (k=8, determined by the elbow method), I identified 8 distinct "Scent Families" from the data.
* **Dominant Notes:** A WordCloud visualization revealed that **Musk, Amber, and Vanilla** are the most dominant notes in the dataset.

*(Place your `klastry.png` or `cloud perfume.png` here)*
`![Market Clusters](images/klastry.png)`

---

## 🛠️ Tech Stack

* **Data Analysis & ML:** Pandas, NumPy, Scikit-learn (K-Means, PCA, TF-IDF, Cosine Similarity)
* **Deep Learning (NLP):** Sentence-Transformers (SBERT)
* **Data Visualization:** Matplotlib, Seaborn, WordCloud
* **Web Application:** Streamlit

---

## 📂 Repository Structure

* `perfume_analysis.ipynb`: The main Jupyter Notebook with all EDA, clustering, and model building steps.
* `app.py`: The Streamlit application script.
* `requirements.txt`: Required Python libraries for the Streamlit app.
* `data/perfumes_cleaned.csv`: The cleaned dataset used by the app.
* `data/hybrid_similarity.npy`: The pre-computed similarity matrix used by the app.
* `images/`: Contains charts and visuals for this README.

---

## 📬 Contact

Created by [Your Name] - connect with me on [LinkedIn](https://www.linkedin.com/in/YOUR-PROFILE-URL)!