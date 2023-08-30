# SupplyChain
#Step 1 & 2: Webscraping & arrange data on Postgres:
  - Install Postgres & PgAdmin4 
  - Create Server/Database: user: postgres, password: postgres
  - Create tables on database as in atm_scraping.sql file
  - Run ATM-webscrapping.ipynb notebook
  - Run subpage_details.ipynb notebook
  - Run subpage_reviews.ipynb notebook
  - Download reviews table as csv if you want. Done!

#Step 3: Organising relational database
  - Run the python script that connects to your warehouse
  - Scripts imports webscrapig data and transforms csv files in 2 relational files containing company details and their reviews

#Step 4: Arrange data on Elasticsearch: 
  - run the followings command in Bash:
    - cd elasticsearch
    - docker-compose up -d
    - docker cp elasticsearch-es01-1:usr/share/elasticsearch/config/certs/ca/ ./
  - access kibana from Docker or from any browser: http://localhost:5601
  - once in kibana User: elastic, Password : datascientest
  - create an Index name "atm_reviews"
  - run the bulk_script.py file to import the CSV data into Elasticsearch

#Step 5: Sentiment analysis
  - before running the sentiment script:
      - make sure that you set up the connection to elasticsearch from step 4 and - run pip install elasticsearch vaderSentiment 
  - sentiment script:
      - runs through each of the reviews and allocates its sentiment score and  label (positive, negative, neutral), then outputs dataframe with review id, company id, company name, review text, sentiment score, and sentiment label (exports reviews_sentiments.csv)
      - creates a string of all reviews, counts and outputs 20 words based on their appearance
      - creates manually defined buckets based on the most used words (bank account, customer service, and credit) and outputs a dataframe containing company details, sentiment scores, and labels, and counts words within the buckets (exports word_analysis.csv)
   
#Step 6: Dash application
  - in the sentiment_anslysis folder you can run a dash app script and review it on http://localhost:8050/ 
  - main elements of the application:
    - dropdown menu where you can filter data for one or multiple companies
    - horizontal bar chart showing the count of reviews per company distributed by the sentiment label
    - bar chart showing the distribution of sentiment labels per topic (word buckets) of the reviews 
  
