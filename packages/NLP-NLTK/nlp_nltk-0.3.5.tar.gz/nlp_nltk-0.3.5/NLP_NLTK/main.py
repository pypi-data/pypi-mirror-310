def load_conll_data(file_path):
    sentences = []
    sentence = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:  # New sentence
                if sentence:
                    sentences.append(sentence)
                    sentence = []
            else:
                parts = line.split()
                if len(parts) == 4 and parts[0] != "-DOCSTART-":  # Skip DOCSTART
                    word, pos, chunk, ner = parts
                    sentence.append((word, pos, ner))
    return sentences


def word_features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]
    
    features = {
        'word': word.lower(),
        'postag': postag,
        'is_upper': word.isupper(),
        'is_title': word.istitle(),
        'is_digit': word.isdigit(),
    }
    if i > 0:
        prev_word = sent[i-1][0]
        prev_postag = sent[i-1][1]
        features.update({
            '-1:word': prev_word.lower(),
            '-1:postag': prev_postag,
        })
    else:
        features['BOS'] = True  # Beginning of Sentence
    
    if i < len(sent)-1:
        next_word = sent[i+1][0]
        next_postag = sent[i+1][1]
        features.update({
            '+1:word': next_word.lower(),
            '+1:postag': next_postag,
        })
    else:
        features['EOS'] = True  # End of Sentence
    
    return features

from collections import Counter

def extract_entities(words, labels):
    entities = []
    entity = []
    current_label = None

    for word, label in zip(words, labels):
        if label.startswith("B-"):  # Beginning of a new entity
            if entity:
                entities.append((current_label, " ".join(entity)))
            entity = [word]
            current_label = label[2:]
        elif label.startswith("I-") and label[2:] == current_label:  # Continuation of an entity
            entity.append(word)
        else:
            if entity:
                entities.append((current_label, " ".join(entity)))
            entity = []
            current_label = None

    if entity:
        entities.append((current_label, " ".join(entity)))

    return entities


def evaluate_dataset(sentences, y_true, y_pred):
    results = {"PER": Counter(), "LOC": Counter(), "ORG": Counter()}
    for sentence, true_labels, pred_labels in zip(sentences, y_true, y_pred):
        words = [token[0] for token in sentence]
        true_entities = extract_entities(words, true_labels)
        pred_entities = extract_entities(words, pred_labels)

        for entity_type, entity in true_entities:
            if entity_type in results:
                if entity in [e[1] for e in pred_entities if e[0] == entity_type]:
                    results[entity_type]["correct"] += 1
                else:
                    results[entity_type]["missed"] += 1

        for entity_type, entity in pred_entities:
            if entity_type in results:
                if entity not in [e[1] for e in true_entities if e[0] == entity_type]:
                    results[entity_type]["false_positive"] += 1

    return results


# ===========================================================================================================================================

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

# ===========================================================================================================================================
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Embedding, LSTM, Dense, Attention, Bidirectional, Input, Layer
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


# Define the AttentionLayer
class AttentionLayer(Layer):
    def __init__(self, lstm_units):
        super(AttentionLayer, self).__init__()
        self.lstm_units = lstm_units
        self.lstm = Bidirectional(LSTM(self.lstm_units, return_sequences=True))  # Create LSTM layer here

    def call(self, inputs):
        text_embedded, aspect_embedded = inputs
        
        # Process the text using a Bi-directional LSTM
        lstm_out = self.lstm(text_embedded)  # Apply LSTM to text embeddings
        
        # Aspect representation as query
        query = tf.reduce_mean(aspect_embedded, axis=1)  # shape: (batch_size, 128)
        
        # Ensure the query shape is compatible for matmul
        query = tf.expand_dims(query, axis=1)  # shape: (batch_size, 1, 128)
        
        # Attention mechanism
        attention_scores = tf.matmul(lstm_out, query, transpose_b=True)  # shape: (batch_size, seq_len, 1)
        attention_weights = tf.nn.softmax(attention_scores, axis=1)
        
        # Weighted sum of LSTM outputs based on attention weights
        context_vector = tf.reduce_sum(attention_weights * lstm_out, axis=1)  # shape: (batch_size, lstm_units * 2)
        
        return context_vector

# Model Architecture
def build_model(vocab_size, embedding_dim, max_seq_len, lstm_units):
    # Input layers
    review_input = Input(shape=(max_seq_len,))
    aspect_input = Input(shape=(max_seq_len,))
    
    # Embedding layer
    embedding_layer = Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_seq_len)
    review_embedded = embedding_layer(review_input)
    aspect_embedded = embedding_layer(aspect_input)
    
    # Attention layer
    attention_layer = AttentionLayer(lstm_units)
    context_vector = attention_layer([review_embedded, aspect_embedded])
    
    # Fully connected layer
    dense_layer = Dense(64, activation='relu')(context_vector)
    output_layer = Dense(4, activation='softmax')(dense_layer)  # 4 classes for polarity

    # Model
    model = tf.keras.models.Model(inputs=[review_input, aspect_input], outputs=output_layer)
    return model