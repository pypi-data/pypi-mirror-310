import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Embedding, LSTM, Dense, Attention, Bidirectional, Input
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