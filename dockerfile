FROM selenium/standalone-chrome
WORKDIR /code/
#install pip
RUN sudo apt update
RUN sudo apt install python3-pip -y
# install dependecies for pycopg2
RUN sudo apt-get install libpq-dev python-dev -y
#install all pip packages
COPY requirements.txt /code/
RUN sudo pip3 install -r requirements.txt
#copy spider pipelines to /code/ and crawl comments spider
COPY . /code/
CMD [ "scrapy", "crawl", "nyse"]