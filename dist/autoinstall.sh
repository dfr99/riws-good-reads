#!/bin/bash

## Check dependencies
# ElasticSearch
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
sudo apt-get install -y apt-transport-https
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
sudo apt-get update && sudo apt-get install -y elasticsearch

# Python
which python
python -V

## Start Elasticsearch
sudo systemctl daemon-reload
sudo systemctl start elasticsearch
sudo systemctl enable elasticsearch

## Remove security for ElasticSearch
sudo sed -i -e 's/xpack.security.enabled:\ np,e/xpack.security.enabled:\ false/g' /etc/elasticsearch/elasticsearch.yml
sudo sed -i -e 's/xpack.security.enrollment.enabled:\ true/xpack.security.enrollment.enabled:\ false/g' /etc/elasticsearch/elasticsearch.yml

sudo systemctl restart elasticsearch

## Check if Elasticsearch server is up
curl -X GET 'http://localhost:9200'

## Create Elasticsearch Index
curl -X PUT "localhost:9200/good_reads?pretty"

## Run good_reads crawler
cd ../code/backend
poetry run crawl

## Run front
cd ../frontend
npm install
npm start

## Check if frontend is up
curl -X GET 'http://localhost:3000'
