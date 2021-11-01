## Training
train.py 상단에 training_args 를 직접 선언하여 중요한 argument들을 기재해뒀습니다. 따라서 학습을 위해서는 python train.py만으로도 실행이 가능합니다. 더 이상 CLI에 길게 무언가를 적을 필요가 없습니다

## Inference
<<python inference.py --output_dir /opt/ml/code/outputs/test_dataset/ --dataset_name ../data/test_dataset/ --model_name_or_path /opt/ml/code/models/train_dataset/checkpoint-2500/ --do_predict>>
의 형식으로 실행해야 합니다. 물론 이것도 train.py 처럼 직접 선언하면 CLI에 길게 적을 필요가 없습니다. 이건 나중에 바꾸겠습니당,,,,,,