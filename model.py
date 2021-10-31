from transformers import AutoTokenizer, AutoModel, AutoConfig
import torch.nn as nn
import torch.nn.functional as F
import torch
from dataclasses import dataclass
from typing import Optional, Tuple
from collections import OrderedDict, UserDict
from typing import Any, BinaryIO, ContextManager, Dict, List, Optional, Tuple, Union
from dataclasses import fields




class Model(nn.Module):
    def __init__(self, MODEL_NAME):
        super().__init__()

        self.tokenizer= AutoTokenizer.from_pretrained(MODEL_NAME)
        self.config= AutoConfig.from_pretrained(MODEL_NAME)
        self.base_model= AutoModel.from_pretrained(MODEL_NAME, config= self.config)

        self.base_hdim= self.config.hidden_size

        self.lstm= nn.LSTM(input_size= self.base_hdim, hidden_size= self.base_hdim, num_layers= 2, dropout= 0.2, batch_first= True, bidirectional= True)
        self.dense_layer= nn.Linear(2*self.base_hdim, 2)

    def forward(self, input_ids, attention_mask, return_dict=None, start_positions= None, end_positions= None):
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        outputs= self.base_model(input_ids= input_ids, attention_mask= attention_mask, return_dict= return_dict)[0] # batch * hdim
        hidden, (last_hidden, last_cell)= self.lstm(outputs) # maybe .. hidden : batch * seq_len * hdim

        logits= self.dense_layer(hidden) # maybe .. output : batch * seq_len * 2
        
        start_logits, end_logits = logits.split(1, dim=-1)
        start_logits = start_logits.squeeze(-1).contiguous()
        end_logits = end_logits.squeeze(-1).contiguous()

        total_loss = None

        if start_positions is not None and end_positions is not None:
            # If we are on multi-GPU, split add a dimension
            if len(start_positions.size()) > 1:
                start_positions = start_positions.squeeze(-1)
            if len(end_positions.size()) > 1:
                end_positions = end_positions.squeeze(-1)
            # sometimes the start/end positions are outside our model inputs, we ignore these terms
            ignored_index = start_logits.size(1)
            start_positions = start_positions.clamp(0, ignored_index)
            end_positions = end_positions.clamp(0, ignored_index)

            loss_fct = nn.CrossEntropyLoss(ignore_index=ignored_index)
            start_loss = loss_fct(start_logits, start_positions)
            end_loss = loss_fct(end_logits, end_positions)
            total_loss = (start_loss + end_loss) / 2
        # print('---------', start_logits.shape, end_logits.shape, type(total_loss), total_loss)
        if not return_dict:
            output = (start_logits, end_logits) + outputs[2:]
            return ((total_loss,) + output) if total_loss is not None else output



        return {
            'loss': total_loss,
            'start_logits': start_logits,
            'end_logits': end_logits,
        }

        
