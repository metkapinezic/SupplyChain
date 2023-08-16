FROM ubuntu:18.04
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests && pip3 install beautifulsoup4 && pip3 install pandas
ADD transformation.py data_modelling/transformation.py
WORKDIR /data_modelling/
CMD python3 transformation.py