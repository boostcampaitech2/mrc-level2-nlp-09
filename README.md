
## Training  
1. feat/exp/kfold pull 받기  
2. make_ner_tag.py 돌려서 train_tagged.csv, inference_tagged.csv 생성
3. make_folds.py 돌려서 fold1.csv ~  fold5.csv 생성
4. elastic_setting.py 돌리기 (../data/wikipedia_documents.json) 이 형식 맞춰놓기  
5. elastic_retriever.py 돌릴필요는 없는데 안에 파일 경로 확인 필수!!  
	inference_tagged.csv (code 디렉 안에)  
	train_tagged.csv (code 디렉 안에)  
6. trian.py 돌리면 되는데 있어야 되는 파일들  
	qg_dataset 디렉 만들기 (data디렉안에 만들기)  
	fold1.csv ~  fold5.csv (code 디렉 안에)  
	delete_qg_sort.pkl (data 디렉 안에)  
	train_tagged.csv (code 디렉 안에) 


## Inference
<<python inference.py --output_dir ./outputs/test_dataset/ --dataset_name ../data/test_dataset/ --model_name_or_path ./models/train_dataset/ --do_predict>>
의 형식으로 실행해야 합니다. --model_name_or_path는 저장된 가장 좋은 파라미터 파일이 들어있는 폴더를 넣어주면 됨

## 주의사항
train.py 125번줄 wandb 이름 본인 실험에 맞게 바꿔서 돌릴것 \\
파일 경로 다 상대경로로 바꾸긴 햇는데 혹시 모르니 한 번 더 확인 바람 \\
제시한 변수이외에 다른 거 만지지 말것 \\
에러가 뜨면 서동건에게 말해주세요 \\

# KLUE Open-Domain Question Answering, Naver Boostcamp AI Tech 2기
## Competition Abstract
🤓 KLUE MRC(Machine Reading Comprehension) Dataset으로 Open-Domain Question Answering을 수행하는 Task.  
🤓 질문에 관련된 문서를 찾아주는 Retriever와 관련된 문서를 읽고 답변을 하는 Reader로 구성.  
🤓 Leaderboard에서 Public 240개, Private 360개로 평가가 이루어짐.  
🤓 하루 10회로 모델 제출 제한

## [Team Portfolio](/)
## [Competition Report(PDF)](/)
## Our solutions
- Retreiver
  - Elastic search
  - Pororo NER
- Augmentation
  - Negative Sampling
  - Question Generation
- Post Processing
  - Top-k Passages Seperate
  - Answer scroing with softmax
  - Similiarity scoring with KSS(Korean Sentence Spliter)
  - Other post-processing via Mecab
- Ensemble
  - Hard voting
  - Post processing 

## 최종 순위 2등!
<img src="competition_results/capture.png" width="80%">

--- 
## Docs 


## Quickstart
### Installation
```
pip install -r requirements.txt
```
### Train model
```python
# default wandb setting in train.py
run = wandb.init(project= 'klue', entity= 'quarter100', name= f'Any training name')
```

```
python train.py
```
Models are saved in "./models/train_dataset_{experiment_name}/".
### Inference
```
python inference.py --output_dir ./outputs/test_dataset/ --dataset_name ../data/test_dataset/ --model_name_or_path ./models/train_dataset/ --do_predict
```
Prediction csv files are saved in "./outputs/test_dataset/".
### Ensemble
Check hard_voting.ipynb.  
Ensemble result is saved in "./submission_fold_total.csv".

## Members

[김다영](https://github.com/keemdy), [김다인](https://github.com/danny980521), [박성호](https://github.com/naem1023), [박재형](https://github.com/Jay-Ppark), [서동건](https://github.com/donggunseo), [정민지](https://github.com/minji-o-j), [최석민](https://github.com/RockMiin)

## Advisors
[박채훈 멘토님](https://github.com/ddehun)
