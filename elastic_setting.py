import argparse
import json
import warnings
import re

from elasticsearch import Elasticsearch
from tqdm import tqdm


warnings.filterwarnings("ignore")  # default: show warnings


"""
    elasticsearch를 실행하기 전에 본 파일을 먼저 실행시켜주세요!
    data가 변경되지 않았을 경우 실행하지 않아도 됩니다.
"""


def set_index_and_server(args):
    # Connect to elasticsearch
    config = {"host": "localhost", "port": 9200}
    es = Elasticsearch([config],timeout=30)
    print("Ping Elasticsearch :", es.ping())

    # Make index
    if es.indices.exists(args.index_name):
        print("Index already exists. Creating a new one after deleting it...")
        es.indices.delete(index=args.index_name)

    with open("./elastic_setting.json", "r") as f:
        body = json.load(f)
    es.indices.create(index=args.index_name, body=body)
    print("Index creation has been completed")

    return es


def insert_wiki_data(es, index_name):
    # Load wiki data
    wiki_articles = load_wiki_data(args)

    # Inserting wiki data
    for i, rec in enumerate(tqdm(wiki_articles)):
        try:
            es.index(index=index_name, id=i, body=rec)
        except:
            print(f"Unable to load document {i}.")

    # Show and count data
    # sample_doc = es.get(index=index_name,id=1)
    # print(sample_doc)
    n_records = es.count(index=index_name)["count"]
    print(f"Succesfully loaded {n_records} into {index_name}")

    return


def preprocess(text):
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"\\n", " ", text)
    text = re.sub(r"\'", "", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"#", " ", text)
    text = re.sub(
        r"[^a-zA-Z0-9가-힣ㄱ-ㅎㅏ-ㅣぁ-ゔァ-ヴー々〆〤一-龥<>()\s\.\?!》《≪≫\'<>〈〉:‘’%,『』「」＜＞・\"-“”∧]",
        "",
        text,
    )
    return text


def load_wiki_data(args):
    # Load wiki data
    if args.index_name == "origin-wiki-index":
        dataset_path = "../data/wikipedia_documents.json"

    with open(dataset_path, "r") as f:
        wiki = json.load(f)

    wiki_contexts = list(dict.fromkeys([v["text"] for v in wiki.values()]))
    wiki_contexts = [preprocess(text) for text in wiki_contexts]
    wiki_articles = [
        {"document_text": wiki_contexts[i]} for i in range(len(wiki_contexts))
    ]

    return wiki_articles


def main(args):
    print("Start to Set Elastic Search")
    es = set_index_and_server(args)
    insert_wiki_data(es=es, index_name=args.index_name)
    print("Finish")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--index_name",
        type=str,
        default="origin-wiki-index",
        help="Elastic search index name",
    )

    args = parser.parse_args()
    main(args)
