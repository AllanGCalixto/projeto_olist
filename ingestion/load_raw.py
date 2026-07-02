
import pandas as pd
import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "database" / "olist.duckdb"

TABLES = {
    "olist_customers_dataset.csv":              "customers",
    "olist_geolocation_dataset.csv":            "geolocation",
    "olist_orders_dataset.csv":                 "orders",
    "olist_order_items_dataset.csv":            "order_items",
    "olist_order_payments_dataset.csv":         "order_payments",
    "olist_order_reviews_dataset.csv":          "order_reviews",
    "olist_products_dataset.csv":               "products",
    "olist_sellers_dataset.csv":                "sellers",
    "product_category_name_translation.csv":    "product_category_name_translation",
}

conn = duckdb.connect(str(DB_PATH))
conn.execute("CREATE SCHEMA IF NOT EXISTS raw")

for arquivo, tabela in TABLES.items():
    caminho = DATA_DIR / arquivo
    df = pd.read_csv(caminho)

    conn.register("df_temp", df)
    conn.execute(f"CREATE OR REPLACE TABLE raw.{tabela} AS SELECT * FROM df_temp")
    print(f"✅ raw.{tabela} carregada ({len(df)} linhas)")

conn.close()
print("\n🎉 Ingestão concluída!")