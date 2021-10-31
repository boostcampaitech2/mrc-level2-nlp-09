import time
import numpy as np
import pandas as pd
import argparse

from tqdm.auto import tqdm
from contextlib import contextmanager
from typing import List, Tuple, NoReturn, Any, Optional, Union

from datasets import (
    Dataset,
    load_from_disk,
    concatenate_datasets,
)

from elasticsearch import Elasticsearch
from elastic_setting import preprocess
#from pororo import Pororo

@contextmanager
def timer(name):
    t0 = time.time()
    yield
    print(f"[{name}] done in {time.time() - t0:.3f} s")


def elastic_setting(index_name="origin-wiki-index"):
    config = {"host": "localhost", "port": 9200}
    es = Elasticsearch([config])
    print("elastic serach ping :", es.ping())

    return es, index_name


def search_es(es, index_name, question_text, topk, tagged):
    # index: index to search, body: query to search
    query = {
            "query": {
                "bool": {
                    "must":[
                        {"match": {"document_text": question_text}}
                    ],
                    "should":[
                        {"match": {"document_text": ' '.join([i[0] for i in tagged if i[1]!='O'])}}
                    ],
                }
            }
        }
    #
    #query = {"query": {"match": {"document_text": question_text}}}
    res = es.search(index=index_name, body=query, size=topk)  # size: default 10, top k

    return res


class SparseRetrieval:
    def __init__(self) -> NoReturn:

        # run_elastic_search.py를 먼저 실행시켜야합니다. 처음 한 번이면 될 것입니다!
        self.es, self.index_name = elastic_setting(index_name="origin-wiki-index")

        # 삽입된 문서 1개 확인(es 결과 확인)
        # print(self.es.get(index=self.index_name, id=1))

    def retrieve_ES(
        self, query_or_dataset: Union[str, Dataset], topk: Optional[int] = 1, ner_path="train_tagged.csv"
    ) -> Union[Tuple[List, List], pd.DataFrame]:

        # Retrieve한 Passage를 pd.DataFrame으로 반환합니다.
        total = []
        with timer("query exhaustive search"):
            doc_scores, doc_indices, doc = self.get_relevant_doc_bulk_ES(
                query_or_dataset["question"], topk=topk, ner_path=ner_path
            )
        for idx, example in enumerate(tqdm(query_or_dataset, desc="ES retrieval: ")):
            # topK_context = ""
            # for i in range(min(topk, len(doc[idx]))):
            #     topK_context += doc[idx][i]["_source"]["document_text"]
            topK_context = []
            for i in range(min(topk, len(doc[idx]))):
                topK_context.append(doc[idx][i]["_source"]["document_text"])
            tmp = {
                # Query와 해당 id를 반환합니다.
                "question": example["question"],
                "id": example["id"],
                # Retrieve한 Passage의 id, context를 반환합니다.
                "context_id": doc_indices[idx],
                "context": topK_context,
            }
            if "context" in example.keys() and "answers" in example.keys():
                # validation 데이터를 사용하면 ground_truth context와 answer도 반환합니다.
                tmp["original_context"] = preprocess(example["context"])
                tmp["answers"] = example["answers"]
            total.append(tmp)

        cqas = pd.DataFrame(total)
        return cqas

    def get_relevant_doc_bulk_ES(
        self, queries: List, topk: Optional[int] = 1, ner_path=""
    ) -> Tuple[List, List]:

        doc = []
        doc_scores = []
        doc_indices = []

        df = pd.read_csv(ner_path)
        df['pororo_ner'] = df['pororo_ner'].apply(eval)

        for question, tagged in tqdm(zip(queries, df['pororo_ner']), desc="get_relevant_doc_bulk_ES: "):

            documents = search_es(self.es, self.index_name, question, topk, tagged)
            doc.append(documents["hits"]["hits"])

            doc_score = []
            doc_indice = []

            for hit in documents["hits"]["hits"]:
                doc_score.append(hit["_score"])
                doc_indice.append(hit["_id"])

            doc_scores.append(doc_score)
            doc_indices.append(doc_indice)

        return doc_scores, doc_indices, doc


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--dataset_name", default="../data/train_dataset/", type=str, help=""
    )

    args = parser.parse_args()

    # Test sparse
    org_dataset = load_from_disk(args.dataset_name)
    full_ds = concatenate_datasets(
        [
            org_dataset["train"].flatten_indices(),
            org_dataset["validation"].flatten_indices(),
        ]
    )  # train dev 를 합친 4192 개 질문에 대해 모두 테스트
    print("*" * 40, "query dataset", "*" * 40)
    print(full_ds)

    retriever = SparseRetrieval()

    def topk_experiment(topK_list):
        result_dict = {}
        # retriever.get_sparse_embedding()
        for topK in tqdm(topK_list):
            result_retriever = retriever.retrieve_ES(full_ds, topk=topK, ner_path="/opt/ml/code/train_tagged.csv")
            correct = 0
            for index in range(len(result_retriever)):
                if (
                    result_retriever["original_context"][index]
                    in result_retriever["context"][index]
                ):
                    correct += 1
            result_dict[topK] = correct / len(result_retriever)
        return result_dict

    topK_list = [1, 5, 10, 15]
    result = topk_experiment(topK_list)
    print(result)
