# ============================================
# Project 1: E-Commerce Sales Dashboard
# Script 1: Data Cleaning
# ============================================

import pandas as pd
import os

# ---- FILE PATH ----
RAW_DATA_PATH = r"E:\ecommerce_dashboard\data\archive\Amazon Sale Report.csv"
CLEAN_DATA_PATH = r"E:\ecommerce_dashboard\data\amazon_sales_clean.csv"

print("Loading dataset...")
df = pd.read_csv(RAW_DATA_PATH, encoding='unicode_escape', low_memory=False)

print(f"Original shape: {df.shape}")
print(f"\nColumn names:\n{df.columns.tolist()}")
print(f"\nFirst 5 rows:\n{df.head()}")
print(f"\nMissing values:\n{df.isnull().sum()}")

# ---- CLEANING STEPS ----

# 1. Drop completely empty rows
df.dropna(how='all', inplace=True)

# 2. Drop unnecessary columns
cols_to_drop = ['index', 'Unnamed: 22']
for col in cols_to_drop:
    if col in df.columns:
        df.drop(columns=[col], inplace=True)

# 3. Clean column names (strip spaces)
df.columns = df.columns.str.strip()

# 4. Convert Date column to datetime
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Month'] = df['Date'].dt.month
    df['Month_Name'] = df['Date'].dt.strftime('%B')
    df['Year'] = df['Date'].dt.year

# 5. Fill missing Amount with 0
if 'Amount' in df.columns:
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)

# 6. Fill missing Qty with 0
if 'Qty' in df.columns:
    df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce').fillna(0)

# 7. Drop rows where Amount is 0
df = df[df['Amount'] > 0]

# 8. Strip whitespace from string columns
str_cols = df.select_dtypes(include='object').columns
df[str_cols] = df[str_cols].apply(lambda x: x.str.strip() if x.dtype == "object" else x)

print(f"\nCleaned shape: {df.shape}")
print(f"\nCleaned data sample:\n{df.head()}")

# ---- SAVE CLEANED DATA ----
df.to_csv(CLEAN_DATA_PATH, index=False)
print(f"\n Cleaned data saved to: {CLEAN_DATA_PATH}")
