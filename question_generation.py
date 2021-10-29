import sys

from pandas.core.indexes.base import ensure_index
sys.path.append("..")
import random
from argparse import ArgumentParser
import pandas as pd
import torch
from tokenizers import SentencePieceBPETokenizer
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import GPT2LMHeadModel

from QG.korquad_qg.config import QGConfig
from QG.korquad_qg.dataset import (MAX_QUESTION_SPACE, MIN_QUESTION_SPACE, QGDecodingDataset, load_wiki_dataset)

model = GPT2LMHeadModel.from_pretrained("taeminlee/kogpt2")
model.load_state_dict(torch.load('/opt/ml/code/QG/model/QG_kogpt2.pth', map_location="cpu"))
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = model.to(device)

tokenizer = SentencePieceBPETokenizer.from_file(
    vocab_filename="/opt/ml/code/QG/tokenizer/vocab.json", merges_filename="/opt/ml/code/QG/tokenizer/merges.txt", add_prefix_space=False
)

examples_list = load_wiki_dataset('/opt/ml/code/wiki_text_title.csv')
random.shuffle(examples_list)
examples=[]
d_id=[]
for i in examples_list:
    examples.append(i[0])
    d_id.append(i[1])

dataset = QGDecodingDataset(examples, tokenizer, 512)
dataloader = DataLoader(dataset, batch_size=1)

model = model.to(device)
model.eval()

generated_results = []

for i, batch in tqdm(enumerate(dataloader), desc="generate", total=len(dataloader)):
    input_ids, attention_mask = (v.to(device) for v in batch)
    origin_seq_len = input_ids.size(-1)

    decoded_sequences = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_length=origin_seq_len + MAX_QUESTION_SPACE,
        min_length=origin_seq_len + MIN_QUESTION_SPACE,
        pad_token_id=0,
        bos_token_id=1,
        eos_token_id=2,
        num_beams=5,
        repetition_penalty=1.3,
        no_repeat_ngram_size=3,
        num_return_sequences=1,
    )

    for decoded_tokens in decoded_sequences.tolist():
        decoded_question_text = tokenizer.decode(decoded_tokens[origin_seq_len:])
        decoded_question_text = decoded_question_text.split("</s>")[0].replace("<s>", "")
        generated_results.append(
            (i, examples[i].answer, examples[i].question, decoded_question_text, d_id[i])
        )

with open('question_generation_id.tsv', "w") as f:
    for context, answer, question, generated_question,d_id in generated_results:
        f.write(f"{generated_question}\t{answer}\t{d_id}\n")
