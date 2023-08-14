#!/usr/bin/env python
# coding: utf-8

# In[29]:


import requests 
from bs4 import BeautifulSoup 

atm_url = 'https://www.trustpilot.com/categories/atm'

response = requests.get(atm_url)

soup = BeautifulSoup(response.content, "html.parser")

best_atm = soup.find_all('div', attrs = {'class': "paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_wrapper__2JOo2"})


# In[30]:


import pandas as pd
name = []
trustscore = []
num_review = []
domain = []

for company in best_atm:

    name.append(company.find('p', {'class': 'typography_heading-xs__jSwUz typography_appearance-default__AAY17 styles_displayName__GOhL2'}).text)
    
    try:
        trustscore_text = company.find('span', {'class': 'typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_trustScore__8emxJ'}).text
        trustscore_value = trustscore_text.split()[1]
        trustscore.append(trustscore_value)
    except AttributeError:
        trustscore.append(None)
    
    try:
        num_review_text = company.find('p', {'class': 'typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_ratingText__yQ5S7'}).text
        num_review_value = num_review_text.split('|')[1].split()[0]
        num_review.append(num_review_value)
    except AttributeError:
        num_review.append(None)
    
    domain.append(company.find('div', {'class': 'styles_wrapper___E6__ styles_categoriesLabels__FiWQ4 styles_desktop__U5iWw'}).text)

    
atm_df = pd.DataFrame(list(zip(name, trustscore, num_review, domain)), columns=['company_name', 'trustscore', 'total_reviews', 'domain'])



# In[31]:


atm_df.insert(0,'company_id', atm_df.index)

for i in range(len(atm_df)):
    text = "11{number}"
    atm_df.company_id[i] = text.format(number = i)


# In[32]:


atm_df = atm_df.dropna(subset=['total_reviews'])


# In[33]:


#atm_df.to_csv('./csv_files/atm.csv', index=False)
print(atm_df)


# In[34]:


#Create table best_atm(company_id bigint not null primary key, company_name varchar not null, trustscore float, total_reviews integer, domain varchar not null);


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

# In[36]:


#uncomment this command to add df to sql table
#execute_values(conn, atm_df, 'best_atm')

