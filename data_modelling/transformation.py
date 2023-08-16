import pandas as pd
import sqlite3

#read webscrapping data
df_atm = pd.read_csv('/Users/metka/Desktop/DST/SupplyChain/csv_files/atm.csv')
df_company_details = pd.read_csv('/Users/metka/Desktop/DST/SupplyChain/csv_files/company_details.csv')
df_reviews = pd.read_csv('/Users/metka/Desktop/DST/SupplyChain/csv_files/reviews.csv')


# CREATE ATMCOMPANIES_WITHID

# Merge the df_atm and DataFrame and df_company_detailson 'company_name'
atmcompanies_withid_df = pd.merge(df_atm, df_company_details, on='company_name')

# Select relevant columns
columns = [
    'company_id',
    'company_name',
    'trustscore',
    'domain',
    'rating_class',
    'star_5',
    'star_4',
    'star_3',
    'star_2',
    'star_1'
]
atmcompanies_withid_df = atmcompanies_withid_df[columns]

# Export DataFrame to CSV without the index column
#atmcompanies_withid_df.to_csv('atmcompanies_withid.csv', index=False)


# CREATE REVEWS WITH ALL IDS

# Generate review IDs using pandas DataFrame method
df_reviews_withid = df_reviews.reset_index().rename(columns={'index': 'review_id'})

# Merge df_reviews_withid with atmcompanies_withid_df on 'company_name'
merged_reviews_df = pd.merge(df_reviews_withid, atmcompanies_withid_df, on='company_name')

# Select relevant columns
columns = [
    'review_id',
    'company_id',
    'company_name',
    'review_star',
    'review_title',
    'reviewer_name',
    'review_text',
    'experience_date',
    'review_date',
    'reply_date',
    'reply_text',
    'trustscore',
    'domain',
    'rating_class',
    'star_5',
    'star_4',
    'star_3',
    'star_2',
    'star_1'
]
merged_reviews_df = merged_reviews_df[columns]


# Export merged DataFrame to CSV without the index column
#merged_reviews_df.to_csv('reviews_withallids.csv', index=False)

