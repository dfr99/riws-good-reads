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

## Init Poetry environment
cd ../code/python
poetry install
poetry shell
poetry run crawl

## Generate request body for bulk data on Elastic index
cd data
python bulk_elastic.py

## Start Elasticsearch
sudo systemctl start elasticsearch
sudo systemctl enable elasticsearch

## Check if Elastic server is up
curl -X GET 'http://localhost:9200'
