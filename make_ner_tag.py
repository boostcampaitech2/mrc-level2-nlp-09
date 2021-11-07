import warnings
import argparse
import pandas as pd

from datasets import (
    load_from_disk,
    concatenate_datasets,
)

from pororo import Pororo

warnings.filterwarnings(action='ignore')

def main(args):
    
    ner = Pororo(task="ner", lang="ko")

    train_dataset = load_from_disk('../data/train_dataset/')
    test_dataset = load_from_disk('../data/test_dataset/') 
    train_dataset_concat = concatenate_datasets(
        [
            train_dataset["train"].flatten_indices(),
            train_dataset["validation"].flatten_indices(),
        ]
    )

    train_question = []
    train_tagged = []
    test_question = []
    test_tagged = []

    for train_data in train_dataset_concat:
        train_question.append(train_data['question'])
        train_tagged.append(train_data['question'].apply(ner))
        
    train_dict = {
        "question":train_question,
        "pororo_ner":train_tagged
    }

    for test_data in test_dataset:
        test_question.append(test_data['question'])
        test_tagged.append(test_data['question'].apply(ner))
        
    test_dict = {
        "question":test_question,
        "pororo_ner":test_tagged
    }

    train_df = pd.DataFrame(train_dict)
    test_df = pd.DataFrame(test_dict)

    train_df[['question','pororo_ner']].to_csv(args.train_output_dir+'/train_tagged.csv',index=False)
    test_df[['question','pororo_ner']].to_csv(args.inference_output_dir+'/inference_tagged.csv',index=False)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--train_output_dir",
        type=str,
        default=".",
        help="decide train_output_dir",
    )
    parser.add_argument(
        "--inference_output_dir",
        type=str,
        default=".",
        help="decide inference_output_dir",
    )

    args = parser.parse_args()
    main(args)