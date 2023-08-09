from elasticsearch import Elasticsearch
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

# Connection to the cluster
es = Elasticsearch(hosts = "https://elastic:datascientest@localhost:9200", ca_certs="./elasticsearch/ca/ca.crt")

# Initialize the VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Define the search query to retrieve all documents
search_query = {
    "query": {
        "match_all": {}
    },
    "size": 100  # Number of documents per page
}

# Lists to store data
review_ids = []
company_ids = []
company_names = []
review_texts = []
compound_scores = []
sentiment_labels = []

# Paginated search
page = 1
while True:
    response = es.search(index="atm_reviews", body=search_query, from_=(page - 1) * 100)
    
    if not response["hits"]["hits"]:
        break
    
    for hit in response["hits"]["hits"]:
        source = hit.get("_source", {})
        review_id = source.get("review_id", "")
        company_id = source.get("company_id", "")
        company_name = source.get("company_name", "")
        review_text = source.get("review_text", "")
        
        if review_text:
            sentiment_scores = analyzer.polarity_scores(review_text)
        
            compound_score = sentiment_scores["compound"]
            if compound_score >= 0.05:
                sentiment_label = "Positive"
            elif compound_score <= -0.05:
                sentiment_label = "Negative"
            else:
                sentiment_label = "Neutral"
            
            review_ids.append(review_id)
            company_ids.append(company_id)
            company_names.append(company_name)
            review_texts.append(review_text)
            compound_scores.append(compound_score)
            sentiment_labels.append(sentiment_label)

    page += 1

# Create data_all dictionary
data_all = {
    "Review_ID": review_ids,
    "Company_ID": company_ids,
    "Company_name": company_names,
    "Review_text": review_texts,
    "Sentiment_score": compound_scores,
    "Sentiment_label": sentiment_labels
}

# Create DataFrame
df_all = pd.DataFrame(data_all)

# Output DataFrame to a CSV file
df_all.to_csv("./sentiment_analysis/all_reviews_sentiments.csv", index=False)

# Print DataFrame
#print(df_all)