<div align="center">

# ✨ ScentSational | The Atelier

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://scentsational.streamlit.app)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<br>

> *"Scent is the brother of breath."*
> <br>— **Yves Saint Laurent**

<br>

</div>

## 💎 Project Overview

**ScentSational** is not just a database; it is a digital concierge designed for the modern connoisseur. Prioritizing **minimal elegance over complexity**, this project implements a "Dark Luxury" design system to provide a high-end user experience.

The platform solves the "paradox of choice" in the perfume market by aggregating data, standardizing olfactory notes, and offering **intuitive discovery modes** in a mobile-responsive environment.

---

## 📊 Analytics & Insights

The application provides a deep dive into the fragrance market through three key visualizations, styled in the platform's signature aesthetic.

### 1. The Olfactory Landscape
We mapped the frequency of primary accords across the database. The market is currently dominated by **Citrus, Woody, and Fruity** profiles.
<div align="center">
  <img src="assets/olfactory_landscape.png" width="500" alt="Olfactory Landscape" style="border-radius: 5px;">
</div>

<br>

### 2. Top Designer Analysis
We analyzed market presence by brand volume, highlighting a mix of high-volume commercial giants alongside heritage luxury houses.
<div align="center">
  <img src="assets/top_designers.png" width="500" alt="Top Designers" style="border-radius: 5px;">
</div>

<br>

### 3. Quality Distribution
The "Score Distribution" reveals a discerning community. Only **18.2%** of fragrances achieve the "Masterpiece" status (4.5+ rating).
<div align="center">
  <img src="assets/score_distribution.png" width="500" alt="Score Distribution" style="border-radius: 5px;">
</div>

---

## 🏗️ Architecture & Ecosystem

This project utilizes a **Decoupled Architecture** strategy to optimize performance. The system is split into two specialized units:

### 1. 🏛️ The Atelier (Lite Version)
![Current Repo](https://img.shields.io/badge/📍_Current_Repository-000000?style=flat-square&color=black)
* **Role:** Frontend, Analytics Dashboard, Rule-based Recommendation.
* **Focus:** Speed, Mobile Responsiveness, Data Visualization.
* **Hosting:** Streamlit Cloud.

### 2. 🧠 The AI Core (Heavy Version)
* **Role:** **NLP Engine & Vector Embeddings**.
* **Concept:** Unlocking the **"Olfactory DNA"** of scent. Unlike simple filters, this core uses Neural Networks to understand semantic relationships between notes (e.g., mapping "rainy forest" to *Petrichor* and *Oakmoss*).
* **Focus:** Deep Learning, Semantic similarity search.
* **Hosting:** Hugging Face Spaces (GPU/LFS support).
* **Live Model:** [![Hugging Face](https://img.shields.io/badge/🤗%20Launch%20AI%20Core-Hugging%20Face-orange)](https://baphomert-scentsational-fragrantica-lfs2.hf.space/)

> **Note:** This repository links to the AI Core via the application interface, ensuring a lightweight frontend experience while offloading heavy computational tasks.

---

## 🚀 Key Features

* **🔍 Discover Scents:** A streamlined search engine allowing exploration of over 24,000 fragrances.
* **🎚️ Smart Filtering:** Horizontal Quality Tier selector and intelligent autocomplete for olfactory notes.
* **⚡ Strict Mode:** A dedicated toggle to instantly filter for the "Crème de la Crème" (Rating 4.5+).

---

## 💻 Installation & Local Usage

To run this application locally:

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/MagdalenaRomaniecka/ScentSational.git](https://github.com/MagdalenaRomaniecka/ScentSational.git)
    cd ScentSational
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application**
    ```bash
    streamlit run app.py
    ```

---

## ⚖️ Data Source & Licensing

**Data Origin**
The application is powered by a curated dataset (`scentsational_data.csv`), **meticulously standardized** for this portfolio.

* **Source:** Fragrantica Fragrance Dataset by [Olga G. (Kaggle)](https://www.kaggle.com/datasets/olgagmiufana1/fragrantica-com-fragrance-dataset).
* **Dataset Type:** Static dataset (2024 version). Used for analytical demonstration purposes.
* **Preprocessing:** Raw data underwent regex cleaning to ensure consistency in brand names and accords.

**License**
This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.

---

## 👩‍💻 Author

<div align="center">

**Magdalena Romaniecka**
<br>
*Data Analyst & Web Analytics Enthusiast*

&copy; 2026 | Built with 💚 and Python.

<br>

[![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?style=flat&logo=github&logoColor=white)](https://github.com/MagdalenaRomaniecka)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/magdalena-romaniecka/)

</div>