## Training
train.py 상단에 training_args 를 직접 선언하여 중요한 argument들을 기재해뒀습니다. 따라서 학습을 위해서는 python train.py만으로도 실행이 가능합니다. 더 이상 CLI에 길게 무언가를 적을 필요가 없습니다

## Inference
<<python inference.py --output_dir /opt/ml/code/outputs/test_dataset/ --dataset_name ../data/test_dataset/ --model_name_or_path /opt/ml/code/models/train_dataset/checkpoint-2500/ --do_predict>>
의 형식으로 실행해야 합니다. 물론 이것도 train.py 처럼 직접 선언하면 CLI에 길게 적을 필요가 없습니다. 이건 나중에 바꾸겠습니당,,,,,,

## my_stop_dict.txt is updated
my_stop_dict를 elasticsearch-7.15.1/config/user_dic/ 안에 넣고 python elastic_setting.py를 다시 실행해야합니당.

## two topk types
arguments.py에는 두 가지 topk가 있습니다. 하나는 inference 과정에서 topk passage를 불러오기 위한 "top_k_retrieval"이고, 나머지 하나는 training 과정에서 negative sample수를 결정하기 위한 "ng_top_k_retrieval"입니다
"ng_top_k_retrieval"가 예를 들어 2라면 training 과정에서 positive sample 하나와 retrieve를 통해 가장 유사도가 높은 negative sample 1개 해서 총 2개의 sampling으로 훈련하게 됩니다.

"ng_top_k_retrieval"=2 Inference topk 20 LB 64.5
"ng_top_k_retrieval"=3 Inference topk 20 LB 65.0
"ng_top_k_retrieval"=3 +pororo(only in inference) Inference topk 20 LB 66.670 
"ng_top_k_retrieval"=3 +pororo(both train and inference) LB In progress 


