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