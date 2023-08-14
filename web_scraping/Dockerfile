FROM ubuntu:18.04
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests && pip3 install beautifulsoup4
ADD mainpage.py /web_scraping/mainpage.py
ADD subpage.py /web_scraping/subpage.py
WORKDIR /web_scraping/
CMD python3 mainpage.py; python3 subpage.py
