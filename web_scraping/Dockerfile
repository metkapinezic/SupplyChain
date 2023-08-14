FROM ubuntu:18.04
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests && pip3 install beautifulsoup4
ADD mainpage.ipynb /web_scraping/mainpage.ipynb
ADD subpage.ipynb /web_scraping/subpage.ipynb
WORKDIR /web_scraping/
CMD python3 mainpage.py; python3 subpage.py
