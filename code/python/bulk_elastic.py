# -*- coding: utf-8 -*-
import json
import unicodedata

with open('good_reads.json', 'r') as file:
	data = json.load(file)

with open('good_reads_elastic.json', 'w') as file:
	elastic_id = 1
	for item in data:
		file.write(json.dumps({"create": {"_id": elastic_id}}))
		file.write("\n")
		file.write(json.dumps(item))
		file.write("\n")
		elastic_id += 1
