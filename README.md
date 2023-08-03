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
