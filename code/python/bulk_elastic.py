"""
Script to generate a JSON to use as a
body on bulk data load on Elastic index
"""

# -*- coding: utf-8 -*-
import json

with open('good_reads.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

with open('good_reads_elastic.json', 'w', encoding='utf-8') as file:
    ELASTIC_ID = 1
    for item in data:
        file.write(json.dumps({"create": {"_id": ELASTIC_ID}}))
        file.write("\n")
        file.write(json.dumps(item))
        file.write("\n")
        ELASTIC_ID += 1
