FROM ubuntu:18.04
RUN apt-get update && apt-get install python3-pip -y && pip3 install elasticsearch && pip3 install docker && docker-compose up -d && docker cp elasticsearch-es01-1:usr/share/elasticsearch/config/certs/ca/ ./
ADD bulk_script.py /es-conn/bulk_script.py
WORKDIR /es-conn/
EXPOSE 9200 9300
CMD python3 bulk_script.py