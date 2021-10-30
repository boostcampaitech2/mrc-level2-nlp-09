import pandas as pd
import sys

qg_df = pd.read_csv('/opt/ml/code/merge_wiki_qg_id.tsv',delimiter='\t',header=None)
qg_df.columns = ['questions','answer','document_id']
wiki_df = pd.read_json("/opt/ml/data/merge_wiki.json")
#print(qg_df.head(5))

answers = []
new_docs = []
for answer, d_id in zip(qg_df['answer'],qg_df['document_id']):
    #print(answer,d_id)
    new_answer = {}
    docs = wiki_df.loc['text'][d_id]
    start_idx = docs.find(answer)
    new_answer['answer_start']=[start_idx]
    new_answer['text']=[answer]
    answers.append(new_answer)
    new_docs.append(docs)
    #print(start_idx)
    #print(docs[start_idx:start_idx+len(answer)])
    
output_df = pd.DataFrame({'context' : new_docs, 'question' : qg_df['questions'], 'answers' : answers, 'document_id' : qg_df['document_id']})
output_df.to_csv("qgtrain.csv",mode='w')