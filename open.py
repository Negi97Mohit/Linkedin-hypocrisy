# import tensorflow as tf
# from tensorflow.keras.layers import Embedding, LSTM, Dense
# from tensorflow.keras.preprocessing.text import Tokenizer
# from tensorflow.keras.preprocessing.sequence import pad_sequences

# # Define your training data (a list of strings)
# training_data = [
#     "Once upon a time, in a land far away, there lived a brave knight named Sir Lancelot.",
#     # Add more training examples here
# ]

# # Tokenize the training data
# tokenizer = Tokenizer()
# tokenizer.fit_on_texts(training_data)
# total_words = len(tokenizer.word_index) + 1

# # Create input sequences using the tokenized data
# input_sequences = []
# for line in training_data:
#     token_list = tokenizer.texts_to_sequences([line])[0]
#     for i in range(1, len(token_list)):
#         n_gram_sequence = token_list[:i+1]
#         input_sequences.append(n_gram_sequence)

# # Pad sequences for equal length
# max_sequence_len = max([len(x) for x in input_sequences])
# input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre')

# # Create predictors and labels
# predictors, labels = input_sequences[:,:-1],input_sequences[:,-1]
# labels = tf.keras.utils.to_categorical(labels, num_classes=total_words)

# # Build and compile the model
# model = tf.keras.Sequential([
#     Embedding(total_words, 100, input_length=max_sequence_len-1),
#     LSTM(150),
#     Dense(total_words, activation='softmax')
# ])
# model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# # Train the model
# model.fit(predictors, labels, epochs=100, verbose=1)

# import numpy as np

# # Function to generate text
# def generate_text(seed_text, next_words, model, max_sequence_len):
#     for _ in range(next_words):
#         token_list = tokenizer.texts_to_sequences([seed_text])[0]
#         token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
#         predicted_probs = model.predict(token_list, verbose=0)[0]
#         predicted_index = np.argmax(predicted_probs)
#         output_word = ""
#         for word, index in tokenizer.word_index.items():
#             if index == predicted_index:
#                 output_word = word
#                 break
#         seed_text += " " + output_word
#     return seed_text

# # Generate text
# generated_text = generate_text("Once upon a time,", 20, model, max_sequence_len)
# print(generated_text)


import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, GlobalAveragePooling1D, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

# Sample training data
training_data = [
    "Once upon a time, in a land far away, there lived a brave knight named Sir Lancelot.",
    # Add more training examples here
]

# Tokenize the training data
tokenizer = Tokenizer()
tokenizer.fit_on_texts(training_data)
total_words = len(tokenizer.word_index) + 1

# Generate input sequences
input_sequences = []
for line in training_data:
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i+1]
        input_sequences.append(n_gram_sequence)

# Pad sequences
max_sequence_len = max([len(x) for x in input_sequences])
input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))

# Create predictors and labels
predictors, label = input_sequences[:,:-1],input_sequences[:,-1]
label = tf.keras.utils.to_categorical(label, num_classes=total_words)

# Define Transformer architecture
def transformer_model(max_sequence_len, total_words):
    inputs = Input(shape=(max_sequence_len,))
    embedding = Embedding(total_words, 128)(inputs)
    # Transformer layers (self-attention mechanism)
    transformer = tf.keras.layers.MultiHeadAttention(num_heads=4, key_dim=128)(embedding, embedding)
    transformer = tf.keras.layers.Dropout(0.1)(transformer)
    transformer = tf.keras.layers.LayerNormalization(epsilon=1e-6)(transformer + embedding)
    transformer = tf.keras.layers.GlobalAveragePooling1D()(transformer)
    outputs = Dense(total_words, activation='softmax')(transformer)
    model = Model(inputs=inputs, outputs=outputs)
    return model

# Build and compile the model
model = transformer_model(max_sequence_len-1, total_words)
model.compile(optimizer=Adam(), loss=SparseCategoricalCrossentropy(), metrics=['accuracy'])

# Train the model
model.fit(predictors, label, epochs=50, verbose=1)

# Function to generate text
def generate_text(seed_text, next_words, max_sequence_len, model, tokenizer):
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len, padding='pre')
        predicted_probs = model.predict(token_list)[0]
        predicted_index = np.argmax(predicted_probs)
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted_index:
                output_word = word
                break
        seed_text += " " + output_word
    return seed_text

# Generate text
generated_text = generate_text("Once upon a time,", 10, max_sequence_len-1, model, tokenizer)
print(generated_text)
