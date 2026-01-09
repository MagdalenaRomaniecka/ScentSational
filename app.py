<div align="center">

# ✨ ScentSational | The Atelier
### The Dark Luxury Fragrance Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.9%2B-FFD700?style=flat-square&logo=python&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000?style=flat-square)

<br>

<p align="center">
  <i>"Scent is the brother of breath."</i>
  <br>
  — <b>Yves Saint Laurent</b>
</p>

<br>

<a href="https://scentsational-zbznjhgc4xv7faddappdc2b.streamlit.app/" target="_blank">
  <img src="https://img.shields.io/badge/🚀_LAUNCH_LIVE_APP-000000?style=for-the-badge&logo=streamlit&logoColor=D4AF37&labelColor=000000&color=000000" alt="Launch App" height="50">
</a>

</div>

---

## 💎 Project Overview

**ScentSational** is not just a database, it is a digital concierge designed for the modern connoisseur. Prioritizing **minimal elegance over complexity**, this project implements a **"Dark Luxury" design system** to provide a seamless, high-end user experience.

The platform solves the "paradox of choice" in the perfume market by aggregating data, standardizing olfactory notes, and offering **intuitive discovery modes** in a mobile-responsive environment.

---

## 🏗️ Architecture & Ecosystem

This project utilizes a **Decoupled Architecture** strategy to optimize performance. The system is split into two specialized units:

### 1. 🏛️ The Atelier (Lite Version)
* **Role:** Frontend, Analytics Dashboard, Rule-based Recommendation.
* **Focus:** Speed, Mobile Responsiveness, Data Visualization.
* **Hosting:** Streamlit Cloud.
* **Live App:** [📲 Open Application](https://scentsational-zbznjhgc4xv7faddappdc2b.streamlit.app/)

### 2. 🧠 The AI Core (Heavy Version)
* **Role:** **NLP Engine & Vector Embeddings**.
* **Concept:** Unlocking the **"Olfactory DNA"** of scent using Neural Networks to understand semantic relationships (e.g., mapping "rainy forest" to *Petrichor*).
* **Focus:** Deep Learning, Semantic similarity search.
* **Hosting:** Hugging Face Spaces (GPU/LFS support).
* **Live Model:** [🤗 Launch AI Core](https://huggingface.co/spaces/MagdalenaRomaniecka/ScentSational-Fragrantica-LFS)

> *Note: This repository links to the AI Core via the application interface, ensuring a lightweight frontend experience while offloading heavy computational tasks.*

---

## 🚀 Key Features

* **📊 Market Insights:** Interactive analytics featuring Top Designers and Score Distribution in a high-contrast gold theme.
* **🔍 Discover Scents:** A streamlined search engine allowing exploration of over 24,000 fragrances.
* **🎚️ Smart Filtering:** Horizontal Quality Tier selector and intelligent autocomplete for olfactory notes.
* **⚡ Strict Mode:** A dedicated toggle to instantly filter for the "Crème de la Crème" (Rating 4.5+).

---

## 📊 Analytics & Insights

The application provides a deep dive into the fragrance market through three key visualizations, styled in the platform's signature "Dark Luxury" aesthetic.

### 1. The Olfactory Landscape
We mapped the frequency of primary accords across the database. The market is currently dominated by **Citrus, Woody, and Fruity** profiles.

<div align="center">
  <img src="assets/olfactory_landscape.png" alt="Olfactory Landscape Chart" width="600">
</div>
<br>

### 2. Top Designer Analysis
We analyzed market presence by brand volume, highlighting a mix of high-volume commercial giants alongside heritage luxury houses.

<div align="center">
  <img src="assets/top_designers.png" alt="Top Designers Chart" width="600">
</div>
<br>

### 3. Quality Distribution
The "Score Distribution" reveals a discerning community. Only **18.2%** of fragrances achieve the "Masterpiece" status (4.5+ rating).

<div align="center">
  <img src="assets/score_distribution.png" alt="Score Distribution Chart" width="600">
</div>

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

* **Source:** [Fragrantica Fragrance Dataset (Kaggle)](https://www.kaggle.com/datasets/olgagmiufana1/fragrantica-com-fragrance-dataset).
* **Dataset Type:** Static dataset (2024 version). Used for analytical demonstration purposes.
* **Preprocessing:** Raw data underwent regex cleaning to ensure consistency in brand names and accords.

**License**
This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.

---

<div align="center">

## 👩‍💻 Author

Created by **Magdalena Romaniecka**
<br>
*Data Analyst & Web Analytics Enthusiast*

&copy; 2026 | Built with 💚 and Python.

<br>

[![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?style=flat&logo=github&logoColor=white)](https://github.com/MagdalenaRomaniecka)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/magdalena-romaniecka/)

</div>