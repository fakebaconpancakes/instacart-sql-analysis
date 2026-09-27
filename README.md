# Instacart E-Commerce Analytics

> **Turning grocery-order data into decisions about retention, merchandising, and fulfillment capacity.**

An end-to-end, cloud-connected analytics project that combines **SQL**, **Python**, **DuckDB**, **MotherDuck**, and **Streamlit** to investigate customer behavior and operational demand in Instacart's grocery delivery marketplace.

The project is designed as an analytics product rather than a collection of isolated queries: a 32M+ row local dataset is prepared and uploaded to a cloud database, business questions are translated into reusable SQL, and the results are surfaced through an executive-facing dashboard with interactive charts and methodology notes.

**View the Live Interactive Dashboard:** [https://abtesting-advertising-experimentation.streamlit.app/](https://mbxnc26c75dneuj8yrcuog.streamlit.app/)

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-Analytics-4479A1?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Streamlit](https://img.shields.io/badge/App-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![DuckDB](https://img.shields.io/badge/Query%20Engine-DuckDB-FFF000)](https://duckdb.org/)

## Project at a glance

| Area | Implementation |
| --- | --- |
| **Business domain** | Grocery delivery and e-commerce |
| **Primary goal** | Identify opportunities to improve retention, basket growth, and fulfillment planning |
| **Data source** | Instacart order history and product catalog tables |
| **Data preparation** | Python ETL loads CSV files into SQLite |
| **Analytics layer** | Modular SQL using joins, CTEs, aggregations, conditional segmentation, and self-joins |
| **Application layer** | Streamlit dashboard with tables, interactive Plotly charts, and expandable SQL logic |
| **Cloud data platform** | MotherDuck cloud database accessed through DuckDB |
| **Deployment model** | Streamlit application securely queries the cloud database at runtime |

## Business questions answered

### 1. Which customers are most valuable to retain?

The dashboard uses an interpretable **Recency & Frequency segmentation** model:

- **Loyal Customer** — more than 10 orders and an average reorder interval below 14 days
- **At Risk** — an average reorder interval above 28 days
- **Casual Shopper** — customers outside those rule-based segments

This provides a practical starting point for lifecycle marketing and retention campaigns while keeping the business rules visible in SQL.

### 2. Which products and combinations drive repeat behavior?

The project identifies:

- The **top 10 products** most frequently included in prior orders
- The **top 10 product pairs** purchased together, using an order-level self-join
- High-reorder products that behave like habitual grocery staples

The product affinity analysis filters out very low-volume products before ranking reorder rates, reducing the risk of promoting statistically noisy results.

### 3. When should operations prepare for peak demand?

Hourly and day-of-week demand analyses reveal the shape of the marketplace workload. The dashboard visualizes order volume by:

- Hour of day, from midnight through 23:00
- Instacart's day-of-week encoding, from 0 through 6

These outputs can support shopper scheduling, delivery capacity planning, inventory replenishment windows, and platform-maintenance decisions.

## Analytical highlights

The included dashboard communicates findings such as:

- A sustained **midday demand plateau**, indicating the core window for shopper and dispatch capacity
- A low-volume overnight period that may be suitable for maintenance, restocking, and inventory audits
- Higher demand on the busiest days of the week, supporting differentiated staffing plans
- Strong affinity among produce and staple grocery products, creating opportunities for cross-sell recommendations and targeted promotions

The exact values are generated from the project dataset and displayed in the Streamlit application.

## Cloud architecture

The project separates data preparation from application delivery. The dataset is uploaded to MotherDuck once, while the deployed Streamlit application connects to the cloud database and executes analytical SQL without requiring the full dataset to be packaged with the application.

```text
[32M+ Row Local Database / Parquet]
                  |
                  | Run upload_to_motherduck.py once
                  v
          [MotherDuck Cloud Database]
                  |
                  | Execute SQL queries through DuckDB
                  v
            [Streamlit Cloud App]
                  |
                  v
        Interactive tables and charts
```

This architecture demonstrates a practical modern analytics workflow:

- **Decoupled storage and presentation** — the dashboard does not need to load the complete dataset into application memory.
- **Cloud-native analytical querying** — MotherDuck handles the SQL workload close to the deployed application.
- **Reproducible publishing workflow** — the local database can be rebuilt with the ETL script and republished with the upload script.
- **Fast user interaction** — query results are returned on demand so users can explore the dashboard without waiting for a local data import on every session.
- **Secure configuration** — the MotherDuck token is injected through Streamlit secrets rather than hardcoded in the application.

For supported dashboard interactions, the intended experience is near-instant feedback, with lightweight queries designed to return in well under a second depending on the deployed environment and current cloud workload.

## Local-to-cloud data flow

```text
Instacart CSV files
        |
        v
Python ETL (db_setup.py)
        |
        v
SQLite database (data/instacart.db)
        |
        +--> upload_to_motherduck.py (run once per data refresh)
        |          |
        |          v
        |      MotherDuck Cloud Database
        |
        v
Reusable SQL analysis files (queries/)
        |
        v
Streamlit Cloud dashboard (app.py)
        |
        v
DuckDB executes SQL in the cloud
        |
        v
Tables + Plotly visualizations + business interpretation
```

## Repository structure

```text
.
├── app.py                         # Streamlit executive dashboard
├── db_setup.py                    # CSV-to-SQLite ETL pipeline
├── upload_to_motherduck.py        # Uploads local tables to MotherDuck
├── requirements.txt               # Python dependencies
├── queries/
│   ├── customer_segmentation.sql  # Rule-based customer segments
│   ├── daily_demand.sql           # Orders by day of week
│   ├── hourly_demand.sql          # Orders by hour of day
│   ├── product_affinity.sql       # Product reorder-rate analysis
│   ├── product_pairs.sql          # Frequently co-purchased products
│   └── top_products.sql            # Most frequently ordered products
├── src/
│   └── database.py                # Cached connection and SQL helpers
├── data/
│   └── data_csv/                  # Source CSV files
└── Figures/
    └── instacart.png              # Dashboard image asset
```

## Technical decisions

### Reproducible ETL

`db_setup.py` discovers CSV files in `data/data_csv/`, derives table names from filenames, and loads each file into SQLite with pandas. This keeps ingestion simple, repeatable, and easy to extend when new source tables are added.

### Modular SQL

Each business question has its own SQL file instead of being embedded inside the dashboard. This separation makes the logic easier to review, test, optimize, and reuse in another BI tool or notebook.

### Cloud-based analytical querying

The project uses DuckDB as the SQL interface and MotherDuck as the cloud-hosted analytical database. The local database is published with `upload_to_motherduck.py`, and the Streamlit application connects directly to the MotherDuck database at runtime. This keeps the deployed application lightweight while centralizing the analytical data and query execution.

The database connection is cached with Streamlit so repeated interactions do not recreate the connection. This is especially useful in a cloud deployment, where connection setup and data transfer should be minimized for a responsive user experience.

### Explainable analysis

The dashboard exposes the SQL behind analyses through expandable sections and documents the reasoning behind segmentation and product-affinity choices. This makes the output auditable for both technical and non-technical stakeholders.

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/fakebaconpancakes/instacart-sql-analysis.git
cd instacart-sql-analysis
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare the local database

The repository expects the Instacart CSV files under `data/data_csv/`. To rebuild the SQLite database:

```bash
python db_setup.py
```

### 5. Configure MotherDuck

The dashboard connects to the `instacart_db` MotherDuck cloud database through the `MOTHERDUCK_TOKEN` Streamlit secret. Create `.streamlit/secrets.toml` locally for development or add the same secret in the Streamlit Cloud application settings:

```toml
MOTHERDUCK_TOKEN = "your-token-here"
```

Never commit this file or expose the token publicly. It is ignored by Git in this repository.

To publish or refresh the local database in MotherDuck:

```bash
python upload_to_motherduck.py
```

The upload step is intentionally separate from the dashboard. It is run when the source data changes; normal dashboard usage queries the already-published cloud tables.

### 6. Launch the dashboard

```bash
streamlit run app.py
```

For a hosted deployment, connect the repository to Streamlit Cloud, configure the `MOTHERDUCK_TOKEN` secret, and use `app.py` as the application entry point.

The application opens an executive dashboard with three areas:

1. **Overview** — business context and database previews
2. **Basic Analysis** — top products and product-pair results
3. **Business Discussion** — customer segmentation, product affinity, and demand forecasting

## Data model

The project works with the standard Instacart relational structure:

| Table | Purpose |
| --- | --- |
| `orders` | Customer orders, order sequence, day, hour, and reorder interval |
| `order_products__prior` | Products included in customers' prior orders |
| `order_products__train` | Training split supplied with the source dataset |
| `products` | Product catalog and aisle/department relationships |
| `aisles` | Aisle reference data |
| `departments` | Department reference data |

The dashboard intentionally uses `order_products__prior` for the historical product-order analysis and uses `orders` for timing and customer cadence analysis.

## Skills demonstrated

- Translating ambiguous business questions into measurable metrics
- SQL joins, CTEs, aggregations, `CASE` expressions, `HAVING`, and self-joins
- Customer segmentation using behavioral features
- Product affinity and reorder-rate analysis
- Time-series-style demand profiling by hour and weekday
- Python data ingestion and database automation
- DuckDB analytical querying and MotherDuck connectivity
- Streamlit application development
- Plotly visualization and executive communication
- Documenting assumptions, limitations, and business implications

## Limitations and next iterations

This project is intentionally transparent about what it does and does not measure:

- The source data does not include product prices or order revenue, so the segmentation model uses **recency and frequency** rather than monetary value.
- The customer segments are rule-based business categories and should be validated with statistical testing and historical retention outcomes.
- A production version would calculate all dashboard metrics at runtime, add query-result caching, and include automated data-quality checks.
- Future work could add RFM scoring, cohort retention, basket-size analysis, recommendation evaluation, and a proper deployment workflow with environment-based configuration.


## License and dataset note

This repository is an educational and portfolio project built from the publicly available Instacart Market Basket Analysis dataset. Instacart is a registered trademark of Instacart, and this project is not affiliated with or endorsed by Instacart.
