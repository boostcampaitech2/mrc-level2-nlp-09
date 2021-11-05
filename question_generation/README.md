## Question Generation  
* git clone https://github.com/codertimo/KorQuAD-Question-Generation.git 하기
* korquad_qg 디렉토리 안에 dataset.py 안에 다음 내용 추가  
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
* make_wiki_title.py라는 파일을 실행시켜 context, title, document_id를 가지는 csv 파일을 만든다.  
* 위 git 주소에서 학습된 QG 모델을 다운받고 question_generation.py를 실행시킨다.  
* 나온 결과를 이용해서 make_qg_pickle.py를 실행시켜 question_generation한 결과를 피클 파일로 변환한다.  