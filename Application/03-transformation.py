import csv
import json
import pandas as pd
import os

# Define the base directory based on where the script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define the output directory
output_dir = os.path.join(base_dir, 'output')
os.makedirs(output_dir, exist_ok=True)

# Read webscraping data
atm_csv_path = os.path.join(output_dir, 'atm.csv')
df_atm = pd.read_csv(atm_csv_path)

reviews_csv_path = os.path.join(output_dir, 'reviews.csv')
df_reviews = pd.read_csv(reviews_csv_path)

# CREATE COMPANIES

# Select relevant columns
columns = [
    'company_id',
    'company_name'
]
companies_df = df_atm[columns]

# CREATE REVEWS JOIN COMPANIES

# Generate review IDs using pandas DataFrame method
app_reviews = df_reviews.reset_index().rename(columns={'index': 'review_id'})

# Merge df_reviews_withid with atmcompanies_withid_df on 'company_name'
merged_reviews_df = pd.merge(app_reviews, companies_df, on='company_name')

# Select relevant columns
columns = [
    'review_id',
    'company_id',
    'company_name',
    'review_text'
]
merged_reviews_df = merged_reviews_df[columns]

# Export merged DataFrame to CSV without the index column
app_reviews_output_path = os.path.join(output_dir, 'app_reviews.csv')
merged_reviews_df.to_csv(app_reviews_output_path, index=False)