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
Create a file named ".env", paste the following and then complete what is missing:
```
DB_USER=yourusername
DB_PASS=yourpassword
DB_NAME=yourbankname
DB_HOST=localhost
DB_PORT=5432
```

Go into dbt/ file and create a file names "profiles.yml", paste the following and complete with the same information as you did on previously step:
```
pokedata:
  outputs:

    dev:
      type: postgres
      threads: 1
      host: db
      port: 5432
      user: yourusername
      pass: yourpassword
      dbname: yourbankname
      schema: public

  target: dev
```

---
## 📈 Insights Preview
(Space for a screenshot of your Metabase dashboard here!)