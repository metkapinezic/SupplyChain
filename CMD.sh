#connect to elasticsearch
cd elasticsearch
docker-compose up -d
sleep 240


#run the application
cd ..
cd Application
docker cp elasticsearch-es01-1:usr/share/elasticsearch/config/certs/ca/ ./
docker-compose up -d

#dash runs on http://localhost:8050/ 
