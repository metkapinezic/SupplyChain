from elasticsearch import Elasticsearch, helpers
import csv
import warnings
import os

warnings.filterwarnings("ignore")

# Determine if running in Docker container or locally
running_in_docker = os.environ.get("DOCKER_ENV", False)

# Connection to the cluster
if running_in_docker:
   es = Elasticsearch(hosts="https://elastic:datascientest@application-es01-1:9200",
                       verify_certs=False)
else:
   es = Elasticsearch(hosts="https://elastic:datascientest@localhost:9200",
                       verify_certs=False)

# Define the input file path based on the environment
if running_in_docker:
    input_file = "/app/output/app_reviews.csv"  # Path inside the Docker container
else:
   input_file = "./output/app_reviews.csv"  # Local path

print("Running in Docker:", running_in_docker)
print("Input file:", input_file)
print("Elasticsearch connection:", es.ping())

# Read and insert data
with open(input_file, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index='bestatm_reviews')