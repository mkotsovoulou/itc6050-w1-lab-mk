# ITC 6050 - Week 1 Lab

## Create a Venv with your packages
python3 -m venv .venv


## Activate the Virtula python Environment
source .venv/bin/activate

## INSTALL all libraries
python3 -m pip install --upgrade pip
pip install 'dlt[postgres]' dbt-core dbt-postgres streamlit pandas requests psycopg2-binary python-dotenv tomli sqlalchemy

# 1. Load data into Postgres
python pipeline.py

# 2. Transform with dbt
cd analytics
dbt run
cd ..

# 3. Launch dashboard
streamlit run dashboard.py


----------------

GraphQL API → dlt → raw.github_issues (Postgres) → dbt → analytics.stg_github_issues → Streamlit

Extract → Load → Transform
  dlt  →  dlt  →   dbt

Data Extract & Load Tool (dlt)
Data Build Tool(dbt)

dbt's job starts after the data lands in Postgres. As long as the column names match what your SQL model expects (number, title, state, repo, author, created_at, closed_at), dbt works fine regardless of whether the data came from REST, GraphQL, a CSV, or anything else.

## View your model
cd analytics
dbt docs generate
dbt docs serve