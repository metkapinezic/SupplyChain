from elasticsearch import Elasticsearch, helpers
import csv
import warnings
import os

# Define the path to the directory where certificates are located inside the Docker container
certs_path = "/usr/share/elasticsearch/config/certs"

# Connection to the cluster
es = Elasticsearch(
    hosts="https://elastic:datascientest@elasticsearch-es01-1:9200",
    ca_certs=os.path.join(certs_path, 'ca/ca.crt')
)

# Determine if running in Docker container or locally
running_in_docker = os.environ.get("DOCKER_ENV", False)

# Define the input file path based on the environment
if running_in_docker:
    input_file = "/app/output/app_reviews.csv"  # Path inside the Docker container
else:
    input_file = "./output/app_reviews.csv"  # Local path

# Read and insert data
with open(input_file, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index='bestatm_reviews')