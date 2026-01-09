<div align="center">

# ✨ ScentSational | Atelier
### The Dark Luxury Fragrance Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.9%2B-FFD700?style=for-the-badge&logo=python&logoColor=black)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

<p align="center">
  <br>
  <i>"Scent is the brother of breath."</i>
  <br>
</p>
<a href="https://scentsational-zbznjhgc4xv7faddappdc2b.streamlit.app/" target="_blank">
  <img src="https://img.shields.io/badge/🚀_LAUNCH_LIVE_APP-000000?style=for-the-badge&logo=streamlit&logoColor=FF4B4B&border=D4AF37" alt="Launch App" height="45">
</a>
</div>

---

## 💎 Project Overview

**ScentSational** is not just a database, it is a digital concierge designed for the modern connoisseur. Moving away from cluttered interfaces, this project implements a **"Dark Luxury" design system** to provide a seamless, high-end user experience for discovering fragrances.

The platform solves the "paradox of choice" in the perfume market by aggregating data, standardizing olfactory notes, and offering curated discovery modes in a mobile-responsive environment.

---
## 🏗️ Architecture & Ecosystem

This project utilizes a **Decoupled Architecture** strategy to optimize performance and resource management. The system is split into two distinct repositories:

### 1. The Atelier (Lite Version) - *Current Repository*
* **Role:** Frontend, Analytics Dashboard, Rule-based Recommendation.
* **Focus:** Speed, Mobile Responsiveness, Data Visualization.
* **Hosting:** Streamlit Cloud.
* **Data:** Lightweight CSV datasets.

### 2. The AI Core (Heavy Version)
* **Role:** Deep Learning Engine, Neural Network Embeddings.
* **Focus:** Chemical similarity search, Advanced NLP.
* **Hosting:** Hugging Face Spaces (GPU/LFS support).
* **Repository:** [📂 ScentSational-Fragrantica-LFS](https://github.com/MagdalenaRomaniecka/ScentSational-Fragrantica-LFS)
* **Live AI Model:** [🤗 Launch AI Core on Hugging Face](https://huggingface.co/spaces/MagdalenaRomaniecka/ScentSational-Fragrantica-LFS)

> *Note: This repository (Lite) links to the AI Core via the application interface, keeping the user experience seamless while managing heavy computational loads externally.*

---

## 🚀 Key Features

* **Market Insights** – Interactive analytics featuring Top Designers, Olfactory Landscapes, and Score Distribution in a high-contrast gold theme.
* **Discover Scents** – A streamlined search engine allowing you to explore over 24,000 fragrances.
* **Smart Filtering** – Horizontal Quality Tier selector and intelligent autocomplete for olfactory notes (e.g., Oud, Vetiver).
* **Strict Mode** – A dedicated toggle to instantly filter for the "Crème de la Crème" (Rating 4.5+).
* **Mobile Optimized** – A "Compact Minimalism" UI tailored for seamless use on smartphones.
---

## 📊 Analytics & Insights

The application provides a deep dive into the fragrance market through three key visualizations, styled in the platform's signature "Dark Luxury" aesthetic.

### 1. The Olfactory Landscape
We mapped the frequency of primary accords across the database. As shown below, the market is currently dominated by **Citrus, Woody, and Fruity** profiles, indicating a consumer preference for fresh and grounded scents.

<div align="center">
  <img src="assets/olfactory_landscape.png" alt="Olfactory Landscape Chart" width="800">
  <p><i>Figure 1: Distribution of dominant olfactory accords.</i></p>
</div>

### 2. Top Designer Analysis
We analyzed market presence by brand volume. The dataset highlights a mix of high-volume commercial giants (Avon, Zara) alongside heritage luxury houses, showcasing the diverse range of the collection.

<div align="center">
  <img src="assets/top_designers.png" alt="Top Designers Chart" width="800">
  <p><i>Figure 2: Top 10 designers by number of fragrances.</i></p>
</div>

### 3. Quality Distribution
The "Score Distribution" reveals a discerning community. Only **18.2%** of fragrances achieve the "Masterpiece" status (4.5+ rating), while the majority fall into the "Standard" category, highlighting the exclusivity of top-tier scents.

<div align="center">
  <img src="assets/score_distribution.png" alt="Score Distribution Chart" width="800">
  <p><i>Figure 3: Breakdown of fragrances by rating tiers (Standard, Premium, Masterpiece).</i></p>
</div>
---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Core Logic** | `Python 3.9+` | Backend processing and logic control. |
| **Frontend** | `Streamlit` | Web framework with custom CSS injection for "Dark Mode". |
| **Data Eng** | `Pandas` | Data cleaning, regex standardization, and manipulation. |
| **Viz** | `Plotly` | Interactive charts without static modebars. |
| **Deployment** | `Streamlit Cloud` | CI/CD pipeline integrated with GitHub. |

## 💻 Installation & Local Usage

To run this application locally on your machine:

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

## 📂 Project Structure

    ScentSational/
    ├── assets/                  # Static assets (Charts, Images)
    │   └── olfactory_landscape.png
    ├── app.py                   # Main Application (Atelier Dashboard)
    ├── scentsational_data.csv   # Processed Dataset (Source of Truth)
    ├── requirements.txt         # Dependency Management
    └── README.md                # Documentation

<br>

---

## ⚖️ Data Source & Licensing

### 📚 Data Origin
The application is powered by a curated dataset (`scentsational_data.csv`), rigorously processed for this portfolio.
* **Source:** [Fragrantica Fragrance Dataset (Kaggle)](https://www.kaggle.com/datasets/olgagmiufana1/fragrantica-com-fragrance-dataset)
* **Aggregated Sources:** Consolidated olfactory notes, popularity ratings, and visual assets from public fragrance databases.
* **Preprocessing:** Raw data underwent regex standardization to ensure consistency in brand names and accords.

### 📜 License
This project is released under the **MIT License**.
> *Permission is hereby granted, free of charge, to any person obtaining a copy of this software...*

You are free to use, modify, and distribute this software, provided that the copyright notice is preserved. See the [LICENSE](./) file for details.

---

<div align="center">

## 👩‍💻 Author

<div align="center">

**Magdalena Romaniecka**
<br>
*Data Analyst & Web Analytics Enthusiast*

&copy; 2026 | Built with 🖤 and Python.

<br>

[![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?style=flat&logo=github&logoColor=white)](https://github.com/MagdalenaRomaniecka)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/magdalena-romaniecka/)

</div>