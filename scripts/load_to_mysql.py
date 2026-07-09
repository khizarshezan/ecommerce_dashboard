# ============================================
# Project 1: E-Commerce Sales Dashboard
# Script 2: Load Clean Data into MySQL
# ============================================

import pandas as pd
import mysql.connector
from mysql.connector import Error
import numpy as np

# ---- CONFIG ----
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root1234"
DB_NAME = "khizar_portfolio"
CLEAN_DATA_PATH = r"E:\ecommerce_dashboard\data\amazon_sales_clean.csv"

def create_database():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f" Database '{DB_NAME}' ready!")
        conn.close()
    except Error as e:
        print(f" Error: {e}")

def clean_value(val):
    if val is None:
        return None
    if isinstance(val, float) and np.isnan(val):
        return None
    return val

def load_data():
    try:
        print("Loading cleaned data...")
        df = pd.read_csv(CLEAN_DATA_PATH)
        df = df.where(pd.notnull(df), None)
        print(f"Rows to load: {len(df)}")

        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS amazon_sales")
        cursor.execute("""
            CREATE TABLE amazon_sales (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id VARCHAR(50),
                date DATE,
                status VARCHAR(50),
                fulfillment VARCHAR(50),
                sales_channel VARCHAR(50),
                ship_service_level VARCHAR(50),
                category VARCHAR(100),
                size VARCHAR(20),
                courier_status VARCHAR(50),
                qty INT,
                currency VARCHAR(10),
                amount FLOAT,
                ship_city VARCHAR(100),
                ship_state VARCHAR(100),
                ship_postal_code VARCHAR(20),
                ship_country VARCHAR(50),
                b2b VARCHAR(10),
                month INT,
                month_name VARCHAR(20),
                year INT
            )
        """)
        print(" Table created!")

        insert_query = """
            INSERT INTO amazon_sales 
            (order_id, date, status, fulfillment, sales_channel,
             ship_service_level, category, size, courier_status,
             qty, currency, amount, ship_city, ship_state,
             ship_postal_code, ship_country, b2b, month, month_name, year)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        rows = []
        for _, row in df.iterrows():
            rows.append((
                clean_value(row.get('Order ID')),
                clean_value(row.get('Date')),
                clean_value(row.get('Status')),
                clean_value(row.get('Fulfilment')),
                clean_value(row.get('Sales Channel ')),
                clean_value(row.get('ship-service-level')),
                clean_value(row.get('Category')),
                clean_value(row.get('Size')),
                clean_value(row.get('Courier Status')),
                clean_value(row.get('Qty')),
                clean_value(row.get('currency')),
                clean_value(row.get('Amount')),
                clean_value(row.get('ship-city')),
                clean_value(row.get('ship-state')),
                clean_value(row.get('ship-postal-code')),
                clean_value(row.get('ship-country')),
                clean_value(row.get('B2B')),
                clean_value(row.get('Month')),
                clean_value(row.get('Month_Name')),
                clean_value(row.get('Year')),
            ))

        cursor.executemany(insert_query, rows)
        conn.commit()
        print(f" {cursor.rowcount} rows inserted into MySQL!")
        conn.close()

    except Error as e:
        print(f" Error: {e}")

create_database()
load_data()
