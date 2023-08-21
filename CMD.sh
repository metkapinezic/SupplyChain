#connect to elasticsearch
cd elasticsearch
docker-compose up -d
sleep 240


#step 1 webscrapping
cd ..
cd Application
docker cp elasticsearch-es01-1:usr/share/elasticsearch/config/certs/ca/ ./

# we just have to do docker-compose again and docker-compose up -d, no need to specify which file to run
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
