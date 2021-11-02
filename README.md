## Training
train.py 상단에 training_args 를 직접 선언하여 중요한 argument들을 기재해뒀습니다. 따라서 학습을 위해서는 python train.py만으로도 실행이 가능합니다. 더 이상 CLI에 길게 무언가를 적을 필요가 없습니다

## Inference
<<python inference.py --output_dir ./outputs/test_dataset/ --dataset_name ../data/test_dataset/ --model_name_or_path ./models/train_dataset/checkpoint-2500/ --do_predict>>
의 형식으로 실행해야 합니다. --model_name_or_path는 저장된 가장 좋은 파라미터 파일이 들어있는 폴더를 넣어주면 됨

## two topk types
arguments.py에는 두 가지 topk가 있습니다. 하나는 inference 과정에서 topk passage를 불러오기 위한 "top_k_retrieval"이고, 나머지 하나는 training 과정에서 negative sample수를 결정하기 위한 "ng_top_k_retrieval"입니다
"ng_top_k_retrieval"가 예를 들어 2라면 training 과정에서 positive sample 하나와 retrieve를 통해 가장 유사도가 높은 negative sample 1개 해서 총 2개의 sampling으로 훈련하게 됩니다.

"ng_top_k_retrieval"=2 Inference topk 20 LB 64.5 \\
"ng_top_k_retrieval"=3 Inference topk 20 LB 65.0 \\
"ng_top_k_retrieval"=3 +pororo(only in inference) Inference topk 20 LB 66.670 78.130 \\
"ng_top_k_retrieval"=3 +pororo(both train and inference) Inference topk 20 LB 66.250 79.700 \\

## Experiment
1. negative sample 개수 조정 (default 3) (서동건) \\
arguments.py의 ng_top_k_retrieval을 5로 변경 

2. QG dataset 포함 범위 조정 (default x) (박재형, 박성호) \\
train.py의 318 ~ 325번 줄과 329번 줄의 주석을 해제하고 319번 줄의 qg_dataset[1:500]에서 뒤 숫자를 조정(500, 700, 1000, 1200)

3. max_seq_length (default 384) (김다영) \\
arguments.py의 max_seq_length를 512로 조정

4. learning rate (default 1e-5) (최석민) \\
train.py 62번줄 learning rate 5e-5로 변경

5. Reader 모델 변경 (default klue/roberta-large) (정민지) \\
arguments.py의 model_name_or_path를 monologg/koelectra-base-v3-discriminator로 변경 \\
-> 에러 뜨면 바로 알려주셈

## 주의사항
train.py 125번줄 wandb 이름 본인 실험에 맞게 바꿔서 돌릴것 \\
파일 경로 다 상대경로로 바꾸긴 햇는데 혹시 모르니 한 번 더 확인 바람 \\
제시한 변수이외에 다른 거 만지지 말것 \\
에러가 뜨면 서동건에게 말해주세요 \\