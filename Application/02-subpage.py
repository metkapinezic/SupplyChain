#!/usr/bin/env python
# coding: utf-8

# In[58]:


#retrieve and store in a list of url_ending. For example: [egcu.org,libertyfirstcu.com, etc]
#loop through this list to have a consolidated "soup" and get 2 separated files: details & reviews of all companies
#connect to Postgre using Psycopg and store as tables there
#set up cron job & automated scraping for new reviews daily, then append them to the table. 


# In[59]:


import requests 
from bs4 import BeautifulSoup 
import pandas as pd
import os

# Define the base directory based on where the script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

atm_url = 'https://www.trustpilot.com/categories/atm'

BASE_URL = "https://www.trustpilot.com"


# In[60]:


#function for html parser
def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, "html.parser")


# In[61]:


soup = get_soup(atm_url)


# In[62]:


#function to scrap all the URLs of business page

def get_company_urls(soup_response):
    company_urls = []
    for a in soup_response.select("a[name='business-unit-card']"):
        url_subdirectory = a.attrs.get("href")
        company_urls.append(BASE_URL+url_subdirectory)
    return company_urls


# In[63]:


#function to get the link of the next page button and scrap content on next page
def get_next_page_url(soup_response):
    try:
        return soup_response.select("a[name='pagination-button-next']")[0].attrs.get("href")
    except IndexError:
        return None


# In[64]:


#scrap the list of company URLs
company_urls = []

while soup:
    company_urls.extend(get_company_urls(soup))
    next_page = get_next_page_url(soup)
    if next_page:
        soup = get_soup(BASE_URL+next_page)
    else:
        soup = None


# In[65]:


print(len(company_urls))


# In[66]:


#remove duplicates in the URL list if any

deduplicated_company_urls = set(company_urls)

print(len(deduplicated_company_urls))

deduplicated_company_urls


# In[67]:


def parse_company_data(sub_soup):
    name = sub_soup.find('span', attrs={'class': 'typography_display-s__qOjh6 typography_appearance-default__AAY17 title_displayName__TtDDM'}).text.strip()
    ratings = sub_soup.find('span', attrs={'class': 'typography_body-l__KUYFJ typography_appearance-subtle__8_H2l styles_text__W4hWi'}).text
    star_elements = sub_soup.find_all('p', attrs={'class': 'typography_body-m__xgxZ_ typography_appearance-default__AAY17 styles_cell__qnPHy styles_percentageCell__cHAnb'})
    stars = [star_element.text.strip() for star_element in star_elements]
    return [name, ratings] + stars


# In[68]:


company_data = []
for company_url in deduplicated_company_urls:
    subpage = get_soup(company_url)
    company_data.append(parse_company_data(subpage))


# In[69]:


import pandas as pd

columns = ['company_name', 'rating_class', 'star_5', 'star_4', 'star_3', 'star_2', 'star_1']

df_details = pd.DataFrame(data=company_data, columns=columns)


# In[70]:


#cleaning the data in dataframe
df_details['total_reviews'] = df_details['rating_class'].apply(lambda x: x.split(' ')[0])
df_details['rating_class'] = df_details['rating_class'].apply(lambda x: x.split(' ')[-1])
df_details.drop(df_details[df_details['total_reviews'] == '0'].index, inplace = True)
df_details


# In[71]:


#df_details.to_csv('./output/company_details.csv', index=False)
# Export DataFrame to CSV without the index column
output_dir = os.path.join(base_dir, 'output')
os.makedirs(output_dir, exist_ok=True)
company_details_output_path = os.path.join(output_dir, 'company_details.csv')
df_details.to_csv(company_details_output_path, index=False)

# Print a message indicating success
print("Data processing completed and CSV exported.")

# In[78]:


#function to parse company page reviews: 
def parse_reviews(sub_soup):
    data = []
    name = sub_soup.find('span', attrs={'class': 'typography_display-s__qOjh6 typography_appearance-default__AAY17 title_displayName__TtDDM'}).text.strip()
    reviews = sub_soup.find_all('div', attrs={'class': 'styles_cardWrapper__LcCPA styles_show__HUXRb styles_reviewCard__9HxJJ'})
    for review in reviews:
        review_stars = review.find_all('div', attrs={'class': 'star-rating_starRating__4rrcf star-rating_medium__iN6Ty'})
        stars = [stars.find('img')['alt'].replace('Rated ', '').replace(' stars', '') for stars in review_stars]
        review_dates = review.find('time', attrs={'class': '', 'data-service-review-date-time-ago': 'true'})
        review_title = review.find('h2', attrs={'class': 'typography_heading-s__f7029 typography_appearance-default__AAY17'})
        reviewer_name = review.find('span', attrs={'class': 'typography_heading-xxs__QKBS8 typography_appearance-default__AAY17'})
        review_text = review.find('p', attrs={'class': 'typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn'})
        experience_date = review.find('p', attrs={'class': 'typography_body-m__xgxZ_ typography_appearance-default__AAY17'})
        review_reply_text = review.find('p', attrs={'class': 'typography_body-m__xgxZ_ typography_appearance-default__AAY17 styles_message__shHhX'})
        reply_date_ = review.find('time', attrs={'class': 'typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_replyDate__Iem0_'})
        star = stars[0] if stars else None
        title = review_title.text.strip() if review_title else None
        reviewer = reviewer_name.text.strip() if reviewer_name else None
        text = review_text.text.strip() if review_text else None
        experience = experience_date.text.split(':')[-1].strip() if experience_date else None
        review_date = review_dates.get('datetime').split('T')[0].strip() if review_dates else None
        reply_date = reply_date_.text.strip() if reply_date_ else None
        reply_text = review_reply_text.text.strip() if review_reply_text else None
        data.append([name, star, title, reviewer, text, experience, review_date, reply_date, reply_text])
        
    return data


# In[79]:


#scrap all reviews of all companies:
alist = []
for url in deduplicated_company_urls:
    soup = get_soup(url)
    while soup:
        alist.extend(parse_reviews(soup))
        next_page = get_next_page_url(soup)
        if next_page:
            soup = get_soup(BASE_URL+next_page)
        else:
            soup = None
        
columns = ['company_name','review_star', 'review_title', 'reviewer_name', 'review_text', 'experience_date', 'review_date', 'reply_date', 'reply_text']
df_reviews = pd.DataFrame(alist, columns=columns)


#df_reviews.to_csv('./output/reviews.csv', index=False)
# Export DataFrame to CSV without the index column
reviews_output_path = os.path.join(output_dir, 'reviews.csv')
df_reviews.to_csv(reviews_output_path, index=False)

# Print a message indicating success
print("Data processing completed and CSV exported.")

# #Establish connection with PostgreSQL using psycopg2
# 
# import psycopg2
# import numpy as np
# import psycopg2.extras as extras
# 
# #Function to insert values into existing table
# def execute_values(conn, df, table):
#   
#     tuples = [tuple(x) for x in df.to_numpy()]
#   
#     col = ','.join(list(df.columns))
#     # SQL query to execute
#     query = "DELETE FROM %s; INSERT INTO %s(%s) VALUES %%s" % (table, table, col)
#     
#     cursor = conn.cursor()
#     try:
#         extras.execute_values(cursor, query, tuples)
#         conn.commit()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print("Error: %s" % error)
#         conn.rollback()
#         cursor.close()
#         return 1
#     print("the dataframe is inserted")
#     cursor.close()
#   
#   
# conn = psycopg2.connect(
#     database="atm_scraping", user='postgres', password='postgres', host='127.0.0.1', port='5432'
# )

# In[75]:


#execute_values(conn, df_reviews, 'reviews')


# In[76]:


#execute_values(conn, df_details, 'company_details')


# #export csv from postgres
# from sqlalchemy import create_engine
# 
# engine = create_engine("postgresql://postgres:postgres@localhost/atm_scraping")
# 
# df_review = pd.read_sql_query('SELECT * FROM reviews', engine)
# 
# engine.dispose()
# df_review.to_csv('/Users/dunghoang/GitHub/SupplyChain/csv_files/reviews.csv', index=False)
