import argparse
import json
import os
import time
import re
from subprocess import Popen, PIPE, STDOUT

from datasets import load_from_disk
from elasticsearch import Elasticsearch
#from prepare_dataset import make_custom_dataset
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm


def populate_index(es_obj, index_name, evidence_corpus):

    for i, rec in enumerate(tqdm(evidence_corpus)):
        try:
            index_status = es_obj.index(index=index_name, id=i, body=rec)
        except:
            print(f'Unable to load document {i}.')
            
    n_records = es_obj.count(index=index_name)['count']
    print(f'Succesfully loaded {n_records} into {index_name}')
    return

def preprocess(text):
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r"\\n", " ", text)
    text = re.sub(r"\'", "", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r'#', ' ', text)
    text = re.sub(r"[^a-zA-Z0-9가-힣ㄱ-ㅎㅏ-ㅣぁ-ゔァ-ヴー々〆〤一-龥<>()\s\.\?!》《≪≫\'<>〈〉:‘’%,『』「」＜＞・\"-“”∧]", "", text)
    return text


def set_datas(args) :

    dataset_path = "../data/wikipedia_documents.json"
    
    with open(dataset_path, "r", encoding="utf-8") as f:
        wiki = json.load(f)
    wiki_contexts = list(dict.fromkeys([v['text'] for v in wiki.values()]))
    wiki_contexts = [preprocess(text) for text in wiki_contexts]
    
    wiki_articles = [{"document_text" : wiki_contexts[i]} for i in range(len(wiki_contexts))]
    return wiki_articles


def set_index_and_server(args) :
    """
    es_server = Popen([args.path_to_elastic],
                    stdout=PIPE, stderr=STDOUT,
                    preexec_fn=lambda: os.setuid(1)  # as daemon
                    )
    time.sleep(30)
    """
    config = {'host':'localhost', 'port':9200}
    es = Elasticsearch([config])

    index_config = {
        "settings": {
            "analysis": {
                "filter":{
                    "my_stop_filter": {
                        "type" : "stop",
                        "stopwords_path" : "user_dic/my_stop_dic.txt"
                    }
                },
                "analyzer": {
                    "nori_analyzer": {
                        "type": "custom",
                        "tokenizer": "nori_tokenizer",
                        "decompound_mode": "mixed",
                        "filter" : ["my_stop_filter"]
                    }
                }
            }
        },
        "mappings": {
            "dynamic": "strict", 
            "properties": {
                "document_text": {"type": "text", "analyzer": "nori_analyzer"}
                }
            }
        }

    print('elastic serach ping :', es.ping())
    if es.indices.exists(args.index_name):
        es.indices.delete(index=args.index_name)
    print(es.indices.create(index=args.index_name, body=index_config, ignore=400))

    return es


def main(args) :
    print('Start to Set Elastic Search')
    wiki_articles = set_datas(args)
    es = set_index_and_server(args)
    populate_index(es_obj=es, index_name=args.index_name, evidence_corpus=wiki_articles)
    print('Finish')


if __name__ == '__main__' :
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_to_elastic', type=str, default='elasticsearch-7.15.1/bin/elasticsearch', help='Path to Elastic search')
    parser.add_argument('--index_name', type=str, default='wiki-index', help='Elastic search index name[wiki-index, wiki-index-split-400, wiki-index-split-800, wiki-index-split-1000]')

    args = parser.parse_args()
    main(args)