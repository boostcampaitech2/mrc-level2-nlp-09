import pandas as pd

wiki_df = pd.read_json('/opt/ml/data/merge_wiki.json',orient='index')

texts = []
titles = []
documents_id = []

for i in range(len(wiki_df)):
    wiki_context = wiki_df['text'][i]
    wiki_title = wiki_df['title'][i]
    wiki_docuemnts_id = wiki_df['document_id'][i]

    if wiki_title in wiki_context:
        texts.append(wiki_context)
        titles.append(wiki_title)
        documents_id.append(wiki_docuemnts_id)

wiki_qa_df = pd.DataFrame(data={'text':texts,'title':titles,'document_id':documents_id})
wiki_qa_df.head()

wiki_qa_df.to_csv('merge_wiki_text_title.csv')