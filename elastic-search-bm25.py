import os
from subprocess import Popen, PIPE, STDOUT
from elasticsearch import Elasticsearch
import json
import pandas as pd
from tqdm import tqdm
import time
import re
import pprint



INDEX_NAME = "document"


INDEX_SETTINGS = {
  "settings" : {
    "index":{
      "analysis":{
        "analyzer":{
          "korean":{
            "type":"custom",
            "tokenizer":"nori_tokenizer",
            "filter": [ "shingle" ],

          }
        }
      }
    }
  },
  "mappings": {

      "properties" : {
        "content" : {
          "type" : "text",
          "analyzer": "korean",
          "search_analyzer": "korean"
        },
        "title" : {
          "type" : "text",
          "analyzer": "korean",
          "search_analyzer": "korean"
        }
      }

  }
}
try:
    es.transport.close()
except:
    pass
es = Elasticsearch()
es.info()
if es.indices.exists(INDEX_NAME, request_timeout=10):
    es.indices.delete(index=INDEX_NAME, request_timeout=10)
es.indices.create(index=INDEX_NAME, request_timeout=10)
#es.indices.create(index=INDEX_NAME)

'''
# 172.17.0.2
es_server = Popen(['/opt/ml/elasticsearch-7.15.1/bin/elasticsearch'], stdout=PIPE, stderr=STDOUT, preexec_fn=lambda:os.setuid(1))

INDEX_NAME = "toy_index"
INDEX_SETTINGS = {
    "settings": {
        "analysis": {
            "analyzer": {
                "nori_analyzer": {
                    "type": "custom",
                    "tokenizer": "nori_tokenizer",
                    "decompound_mode": "mixed"
                }
            },
        }
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {"document_text": {"type": "text", "analyzer": "nori_analyzer"}},
    },
}


es = Elasticsearch()
#es = Elasticsearch('localhost:9200')

print(es.info())
print('elastic ping', es.ping())
print(es.indices.create(index=INDEX_NAME,ignore=400))
'''
