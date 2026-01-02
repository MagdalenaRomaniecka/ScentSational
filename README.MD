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

</div>

---

## 💎 Project Overview

**ScentSational** is not just a database; it is a digital concierge designed for the modern connoisseur. Moving away from cluttered interfaces, this project implements a **"Dark Luxury" design system** to provide a seamless, high-end user experience for discovering fragrances.

The platform solves the "paradox of choice" in the perfume market by aggregating data, standardizing olfactory notes, and offering curated discovery modes in a mobile-responsive environment.

---

## 🚀 Key Features

* **📱 Mobile-First Design:** A fully responsive interface where layouts (columns, images, typography) adapt fluidly between Desktop and Mobile devices.
* **🔍 Smart Discovery Engine:** Advanced filtering logic that allows users to search by Brand, Name, or Olfactory profile using fuzzy matching.
* **📊 Market Intelligence:** Interactive dashboards powered by Plotly to visualize trends in the fragrance industry.
* **🛡️ Robust Data Pipeline:** Custom CSV parsing engine capable of handling various delimiters and encoding standards automatically.

---

## 📊 Analytics & Insights

Before deployment, the underlying dataset (`scentsational_data.csv`) underwent rigorous Exploratory Data Analysis (EDA).

### The Olfactory Landscape
We mapped the frequency of primary accords across the database. As shown below, the market is currently dominated by **Citrus, Woody, and Fruity** profiles, indicating a consumer shift towards fresh and grounded scents.

<div align="center">
  <img src="assets/olfactory_landscape.png" alt="Olfactory Landscape Chart" width="800">
  <p><i>Figure 1: Distribution of dominant olfactory accords in the curated dataset.</i></p>
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

---

## 📂 Project Structure

```text
ScentSational/
├── assets/                  # Static assets (Charts, Images)
│   └── olfactory_landscape.png
├── app.py                   # Main Application (Atelier Dashboard)
├── scentsational_data.csv   # Processed Dataset (Source of Truth)
├── requirements.txt         # Dependency Management
└── README.md                # Documentation



---

## ⚖️ Data Source & Licensing

### 📚 Data Origin
The application is powered by a curated dataset (`scentsational_data.csv`), rigorously processed for this portfolio.
* **Aggregated Sources:** Consolidated olfactory notes, popularity ratings, and visual assets from public fragrance databases.
* **Preprocessing:** Raw data underwent regex standardization to ensure consistency in brand names and accords.

### 📜 License
This project is released under the **MIT License**.
> *Permission is hereby granted, free of charge, to any person obtaining a copy of this software...*

You are free to use, modify, and distribute this software, provided that the copyright notice is preserved. See the [LICENSE](LICENSE) file for details.

---

<div align="center">

## 👩‍💻 Author

**Magdalena Romaniecka**
<br>
*Data Engineer & Web Analytics Specialist*

<br>

> *"Building bridges between raw data and luxury user experiences."*

<br>

[![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?style=flat&logo=github&logoColor=white)](https://github.com/MagdalenaRomaniecka)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/magdalena-romaniecka/)

<br>
<hr width="50%">

Copyright © 2026 Magdalena Romaniecka. All Rights Reserved.

</div>