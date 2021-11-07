# Question Generation  

## Set Environment
```
git clone https://github.com/codertimo/KorQuAD-Question-Generation.git
mv KorQuAD-Question-Generation korquad_qg
```

korquad_qg/dataset.py에 추가할 내용
``` python
def load_wiki_dataset(dataset_path):
    wiki_data_frame = pd.read_csv(dataset_path)
    examples = []
    cnt=0
    for idx in range(len(wiki_data_frame)):
        text = wiki_data_frame["text"][idx]
        title = wiki_data_frame["title"][idx]
        document_id = wiki_data_frame["document_id"][idx]

        example = QAExample(text, title)
        tmp = [example,document_id]
        examples.append(tmp)

    return examples
``` 
## Generate
```
# wikipedia data를 context, title, document_id로 정리
python make_wiki_title.py

# Generate question
python question_generation.py

# Save question generation in pickle
python make_qg_pickle.py
``` 