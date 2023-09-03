# SupplyChain Sentiment Analysis of Reviews for ATM companies

The objective of this project is to demonstrate and provide a live and updated dashboard of ATM companies from which you can asses the sentiment of reviews for each company (or a group) based on the factors within the supply chain process of ATM services.

This is a repository for an application that is running in 6 steps and is triggered by simply running docker-compose up within the Application folder. 

The back end of the application works in several steps. Those steps are marked from 01 - 06 and contain webscrapping of reviews from Trustpilotm; data modelling, transformation and cleaning of webscrapped data into organised and readable tables meant for further analyis; uploading organised dataset to elasticsearch database, running the sentiment analysis and outputting the dashboard using Dash accesible on port 8050.

#Step 1 & 2: Webscraping
  - 01-mainpage.py runs through the main page of the list of ATM companies ( https://www.trustpilot.com/categories/atm ), and ouputs a file called atm.csv, which contains a list of companies details (company_name,trustscore,total_reviews,domain) and allocates company id (company_id,company_name,trustscore,total_reviews,domain).
  - 02-subpage.py runs through the subpages of the list of companies and extracts all the review details per company in a reviews.csv file. The file contains the following data per company: company_name, review_star, review_title, reviewer_name, review_text,experience_date, review_date, reply_date, reply_text.

#Step 3: Organising data in a single file
  - 03-transformation.py python script reads the output from webscrapping (atm.csv, reviews.csv) and joins relevant data into a single output app_reviews.csv with columns company_name, review_star, review_title, reviewer_name, review_text, experience_date, review_date, reply_date, reply_text

#Step 4: Upload data to Elasticsearch
  - 04-esconnect.py connects to elasticsearch previously set up using docker-compose file (services: setup, es01, es02, es03, kibana)
  - To run the script locally you must first 
    - run "docker-compose up - d setup, es01, es02, es03, kibana"
    - access kibana from Docker or from any browser: http://localhost:5601
    - once in kibana User: elastic, Password : datascientest
    - create an Index name "atm_reviews"
    - run the 04-esconnect.py file to import the CSV data into Elasticsearch
  - The step is automated in docker-compose.yml file under service import_to_elasticsearch, where all the dependenciesa are specified

#Step 5: Sentiment analysis
  - This step is depended on a sucessful connection and data upload to elasticsearch
  - 05-sentiment.py:
      - runs through each of the reviews and allocates its sentiment score and  label (positive, negative, neutral), then outputs dataframe with review id, company id, company name, review text, sentiment score, and sentiment label (exports reviews_sentiments.csv)
      - creates a string of all reviews, counts and outputs 20 words based on their appearance
      - creates manually defined buckets based on the most used words (bank account, customer service, and credit) and outputs a dataframe containing company details, sentiment scores, and labels, and counts words within the buckets (exports word_analysis.csv)
   
#Step 6: Dash application
  - Final step of the application is the dashboard running on http://0.0.0.0:8050/ 
  - 06-dashboard.py takes the output of the sentiment analysis step and creates data visualisation of the output
  - The visual report is avaialble using the link from docker or running the 06-dashboard.py script locally
  - If you run the sript locally before using docker-compose, make sure to kill the service running on port by checking if the port is busy "lsof -i :8050" and then running "kill <PID>", replacing the PID with the current service id
  - The main elements of the dashboard:
    - number, showing total reviews processed
    - dropdown menu where you can filter data for one or multiple companies
    - horisontal bar chart showing the count of reviews per company devided by the sentiment label
    - vertical bar chart showing the distribution of sentiment labels per company
    - horisontal bar chart showing the count of reviews and sentiment labels per word bucket (supply chain step) 
    - vertical bar chart showing the distribution of sentiment labels per topic of the reviews 
  
