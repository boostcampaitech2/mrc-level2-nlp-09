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