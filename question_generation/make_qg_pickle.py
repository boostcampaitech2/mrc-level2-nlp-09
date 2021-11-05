import pandas as pd
import sys

qg_df = pd.read_csv('/opt/ml/code/merge_wiki_qg_id.tsv',delimiter='\t',header=None)
qg_df.columns = ['question','answers','document_id']
wiki_df = pd.read_json("/opt/ml/data/merge_wiki.json")
#print(qg_df.head(5))

answers = []
new_docs = []
question = []
ids = []
cnt=0
for answer, d_id, q in zip(qg_df['answers'],qg_df['document_id'],qg_df['question']):
    if q.find(answer) == -1:
        new_answer = {}
        docs = wiki_df.loc['text'][d_id]
        start_idx = docs.find(answer)
        new_answer['answer_start']=[start_idx]
        new_answer['text']=[answer]
        answers.append(new_answer)
        new_docs.append(docs)
        question.append(q)
        ids.append(d_id)
        cnt+=1

    
print(cnt)    
output_df = pd.DataFrame({'context' : new_docs, 'question' : question, 'answers' : answers, 'document_id' : ids})
output_df.to_pickle('qg_merge_wiki_noans.pkl')