import pandas as pd
import sys

qg_df = pd.read_csv('/opt/ml/code/merge_wiki_qg_id.tsv',delimiter='\t')
qg_df.columns = ['questions','answer','document_id']
wiki_df = pd.read_json("/opt/ml/data/merge_wiki.json")

for answer, d_id in zip(qg_df['answer'],qg_df['document_id']):
    print(answer,d_id)
    docs = wiki_df.loc['text'][d_id]
    start_idx = docs.find(answer)
    print(start_idx)
    print(docs[start_idx:start_idx+len(answer)])
    sys.exit()
