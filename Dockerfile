FROM python:3.9.6-slim-buster
WORKDIR /usr/app
COPY . /usr/app

EXPOSE 8080

ENV HOST=0.0.0.0
ENV PORT=8080

RUN pip install requests
RUN pip install pandas
RUN pip install google-cloud-storage
RUN pip install google-cloud-pubsub
RUN pip install flask
RUN pip install gunicorn
RUN mkdir data
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 chfeur_forex_request:app
