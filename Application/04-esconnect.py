from elasticsearch import Elasticsearch, helpers
import csv
import warnings
warnings.filterwarnings("ignore")

# Connection to the cluster

es = Elasticsearch(hosts = "https://elastic:datascientest@localhost:9200", 
                    ca_certs="./elasticsearch/ca/ca.crt")

with open('app_reviews.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index='bestatm_reviews')

