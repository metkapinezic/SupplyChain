import pandas as pd

#read webscrapping data
df_atm = pd.read_csv('atm.csv')
df_reviews = pd.read_csv('reviews.csv')

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
merged_reviews_df.to_csv('app_reviews.csv', index=False)