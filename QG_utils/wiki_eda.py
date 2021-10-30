import pandas as pd
wiki_df = pd.read_json('../data/wikipedia_documents_del.json', orient='index')
# context_id = 3
len(wiki_df['text'].unique())

from collections import defaultdict
group_by_answer = defaultdict(str)

for index, row in wiki_df.iterrows():
    group_by_answer[row['title']] += row['text']
    break

print(group_by_answer)