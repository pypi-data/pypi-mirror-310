from transformers import AutoTokenizer

def preprocess_data(tokenizer, examples):
    # Tokenize context and question
    tokenized_input = tokenizer(examples['question'], examples['context'], truncation=True, padding="max_length", max_length=512)

    # Add start and end positions for question answering (use answer span)
    # We find the start and end positions of the answer in the context
    answer_start = examples['context'].find(examples['answer'])
    answer_end = answer_start + len(examples['answer'])

    tokenized_input['start_positions'] = answer_start
    tokenized_input['end_positions'] = answer_end

    return tokenized_input


import torch
from torch.utils.data import Dataset

# Custom Dataset class for Question Answering
class QADataset(Dataset):
    def __init__(self, df):
        self.data = df
        self.input_ids = [item['input_ids'] for item in df]
        self.attention_mask = [item['attention_mask'] for item in df]
        self.start_positions = [item['start_positions'] for item in df]
        self.end_positions = [item['end_positions'] for item in df]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return {
            'input_ids': torch.tensor(self.input_ids[idx]),
            'attention_mask': torch.tensor(self.attention_mask[idx]),
            'start_positions': torch.tensor(self.start_positions[idx]),
            'end_positions': torch.tensor(self.end_positions[idx])
        }

# Create Dataset

def prepare_QADataset(df):
    qa_dataset = QADataset(df)
    return qa_dataset 