#connect to elasticsearch
cd elasticsearch
docker-compose up -d
cd Application
docker cp elasticsearch-es01-1:usr/share/elasticsearch/config/certs/ca/ ./

#step 1 webscrapping
run mainpage.py
run subpage.py

#step 3 transformation
run transformation.py

#step 4 push data to elasticsearch
run esconnect.py

#step 5 run sentiment analysis
run sentiment.py

#step 6 run dash
pip install dash
run dashboard.py


#dash runs on http://localhost:8050/ 
