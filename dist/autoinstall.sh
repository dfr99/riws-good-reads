#!/bin/bash

## Install ElasticSearch
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
sudo apt-get install -y apt-transport-https
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
sudo apt-get update && sudo apt-get install -y elasticsearch

## Check Python version
which $1
$1 -V

## Install Poetry
curl -sSL https://install.python-poetry.org | $1 -
poetry --version

## Start Elasticsearch
sudo systemctl daemon-reload
sudo systemctl enable elasticsearch
sudo systemctl start elasticsearch

## Remove security for ElasticSearch
if sudo grep -Fxq '## Remove security' /etc/elasticsearch/elasticsearch.yml
then
	true
else
	echo '## Remove security' | sudo tee -a /etc/elasticsearch/elasticsearch.yml > /dev/null
fi

if sudo grep -Fxq 'xpack.security.enabled: true' /etc/elasticsearch/elasticsearch.yml
then
	## Replace configuration
	sudo sed -i -e 's/xpack.security.enabled:\ true/xpack.security.enabled:\ false/g' /etc/elasticsearch/elasticsearch.yml
elif sudo grep -Fxq 'xpack.security.enabled: false' /etc/elasticsearch/elasticsearch.yml
then
	true
else
	## Add configuration
	echo 'xpack.security.enabled: false' | sudo tee -a /etc/elasticsearch/elasticsearch.yml > /dev/null
fi

if sudo grep -Fxq 'xpack.security.enrollment.enabled: true' /etc/elasticsearch/elasticsearch.yml
then
	## Replace configuration
	sudo sed -i -e 's/xpack.security.enrollment.enabled:\ true/xpack.security.enrollment.enabled:\ false/g' /etc/elasticsearch/elasticsearch.yml
elif sudo grep -Fxq 'xpack.security.enrollment.enabled: false' /etc/elasticsearch/elasticsearch.yml
then
	true
else
	## Add configuration
	echo 'xpack.security.enrollment.enabled: false' | sudo tee -a /etc/elasticsearch/elasticsearch.yml > /dev/null
fi

## Allow CORS
if sudo grep -Fxq '## Allow CORS' /etc/elasticsearch/elasticsearch.yml
then
	true
else
	echo '## Allow CORS' | sudo tee -a /etc/elasticsearch/elasticsearch.yml > /dev/null
fi

if sudo grep -Fxq 'http.cors.enabled: true' /etc/elasticsearch/elasticsearch.yml
then
	true
else
	echo 'http.cors.enabled: true' | sudo tee -a /etc/elasticsearch/elasticsearch.yml > /dev/null
fi

if sudo grep -Fxq 'http.cors.allow-origin: "*"' /etc/elasticsearch/elasticsearch.yml
then
	true
else
	echo 'http.cors.allow-origin: "*"' | sudo tee -a /etc/elasticsearch/elasticsearch.yml > /dev/null
fi

if sudo grep -Fxq 'http.cors.allow-methods: OPTIONS, HEAD, GET, POST, PUT, DELETE' /etc/elasticsearch/elasticsearch.yml
then
	true
else
	echo 'http.cors.allow-methods: OPTIONS, HEAD, GET, POST, PUT, DELETE' | sudo tee -a /etc/elasticsearch/elasticsearch.yml > /dev/null
fi

if sudo grep -Fxq 'http.cors.allow-headers: X-Requested-With, X-Auth-Token, Content-Type, Content-Length' /etc/elasticsearch/elasticsearch.yml
then
	true
else
	echo 'http.cors.allow-headers: X-Requested-With, X-Auth-Token, Content-Type, Content-Length' | sudo tee -a /etc/elasticsearch/elasticsearch.yml > /dev/null
fi

if sudo grep -Fxq 'http.cors.allow-credentials: true' /etc/elasticsearch/elasticsearch.yml
then
	true
else
	echo 'http.cors.allow-credentials: true' | sudo tee -a /etc/elasticsearch/elasticsearch.yml > /dev/null
fi

## Check if Elasticsearch configuration is added
sudo tail -n 9 /etc/elasticsearch/elasticsearch.yml

## Restart Elasticsearch
sudo systemctl restart elasticsearch

## Check if Elasticsearch server is up
curl -X GET 'http://localhost:9200'

## Ensure that index not exists
curl -X DELETE 'localhost:9200/good_reads?pretty'

## Create Elasticsearch Index
curl -X PUT 'localhost:9200/good_reads?pretty'


## Run good_reads crawler
cd ../code/backend
echo 'GOOD_READS_LIST='${2} > ./good_reads/spiders/.env
poetry install
poetry run crawl

## Run frontend
cd ../frontend
npm install
npm start
