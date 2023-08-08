from elasticsearch import Elasticsearch, helpers
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Connection to the cluster

##!! dont forget to change the path to ca.crt

es = Elasticsearch(hosts = "https://elastic:datascientest@localhost:9200", 
                   ca_certs="/Users/metka/Desktop/DST/SupplyChain/elasticsearch/ca/ca.crt") 



# Define the search query to retrieve all documents
search_query = {
    "query": {
        "match_all": {}
    }
}

# Execute the search query
response = es.search(index="reviews", body=search_query)

# Initialize the VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Analyze sentiment for each document and print the results
for hit in response["hits"]["hits"]:
    review_text = hit["_source"]["review_text"]
    sentiment_scores = analyzer.polarity_scores(review_text)

    sentiment_label = ""
    if sentiment_scores["compound"] >= 0.05:
        sentiment_label = "Positive"
    elif sentiment_scores["compound"] <= -0.05:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    print(f"Review: {review_text}")
    print(f"Sentiment: {sentiment_label}")
    print("---")

#This code prints out the reviews and its sentiment

