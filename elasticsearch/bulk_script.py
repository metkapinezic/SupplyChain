from elasticsearch import Elasticsearch, helpers
import csv
import json
import warnings
warnings.filterwarnings("ignore")

# Connection to the cluster

es = Elasticsearch(hosts = "https://elastic:datascientest@localhost:9200", 
                    ca_certs="./ca/ca.crt")

with open('/Users/dunghoang/GitHub/SupplyChain/csv_files/reviews_withallids.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index='atm_reviews')


#display some documents from our atm_reviews index
filename = "docu"

query = {
  "query": {
    "match_all": {}
  }
}

response = es.search(index="atm_reviews", body=query)

# Saving the request and response in a json file
with open("./query/{}.json".format("q_" + filename + "_response"), "w") as f:
  json.dump(dict(response), f, indent=2)

with open("./query/{}.json".format("q_" + filename + "_request"), "w") as f:
  json.dump(query, f, indent=2)
