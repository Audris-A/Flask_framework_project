FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN apt-get update || : && apt-get install python -y

RUN apt-get install -y \
    python3-pip

RUN pip3 install matplotlib && \
    pip3 install pandas && \
    pip3 install pymongo && \
    pip3 install datetime && \
    pip3 install numpy && \
    pip3 install flask && \
    pip3 install plotly && \
    pip3 install Flask-PyMongo

COPY ./project /app

WORKDIR /app

RUN apt-get update
RUN apt-get -y install curl gnupg
RUN curl -sL https://deb.nodesource.com/setup_11.x  | bash -
RUN apt-get -y install nodejs
RUN npm install
