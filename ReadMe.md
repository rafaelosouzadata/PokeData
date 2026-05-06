# ⚡ PokeData
> A data engineering project focused on the complete ELT lifecycle, from API ingestion to final visualization.

[![Status](https://img.shields.io/badge/status-under__development-orange)](#)

## 🏗️ Architecture & Stack
The project is containerized with **Docker** and follows a modern data stack approach:

- **Python (httpx/pandas):** Extraction from PokeAPI and loading into the database.
- **PostgreSQL:** Primary Data Warehouse.
- **dbt (data build tool):** Data transformation, documentation, and testing.
- **Metabase:** BI Layer for dashboards and insights.
- **Docker & Docker-compose:** Infrastructure orchestration.

## 🚀 Key Features
- **Automated Ingestion:** Python scripts to fetch and normalize data.
- **Data Modeling:** Modular SQL transformations using dbt.
- **Visualization:** Interactive dashboards showing Pokémon attributes, types, and stats distributions.

## 🛠️ How to Run (TBA)
*The setup instructions for Docker-compose will be available soon.*

---
## 📈 Insights Preview
(Space for a screenshot of your Metabase dashboard here!)