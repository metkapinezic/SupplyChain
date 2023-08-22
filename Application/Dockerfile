FROM ubuntu:18.04
WORKDIR /application/
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests && pip3 install beautifulsoup4 && pip3 install pandas
RUN pip3 install elasticsearch && pip3 install vaderSentiment && pip3 install dash && pip3 install plotly 
COPY . .
EXPOSE 8050
CMD cd elasticsearch; docker-compose up -d; sleep 240; python3 mainpage.py; python3 subpage.py; python3 transformation.py; python3 sentiment.py; python3 dashboard.py