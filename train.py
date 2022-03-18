import json
import pickle
with open("data/intents.json", "r", encoding="utf-8") as f:
    intents_json = json.load(f)



intents = intents_json["intents"]

training_data = {}
labels = []

for intent in intents:
    for pattern in intent["patterns"]:
        training_data[pattern] = intent["tag"]

    if intent["tag"] not in labels:
        labels.append(intent["tag"])

X = list(training_data.keys())
y = list(training_data.values())

import string

def clean_text(text: str):
    text = text.strip().lower()
    text = text.translate(text.maketrans("", "", string.punctuation))

    return text

X = list(map(clean_text, X))

from tensorflow.keras.preprocessing.text import Tokenizer

oov_token = "<OOV>"

tokenizer = Tokenizer(oov_token=oov_token)
tokenizer.fit_on_texts(X)
tokenizer.index_word

X_sequences = tokenizer.texts_to_sequences(X)

max_sentence_length = len(X_sequences[0])

for sequence in X_sequences:
    if max_sentence_length < len(sequence):
        max_sentence_length = len(sequence)

from tensorflow.keras.preprocessing.sequence import pad_sequences

X_padded_sequences = pad_sequences(X_sequences, maxlen=max_sentence_length)

def map_label_to_int(label: str):
    return labels.index(label)

y = list(map(map_label_to_int, y))

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding
from tensorflow.keras import Input

num_classes = len(labels)
vocab_size = len(tokenizer.index_word) + 1
embedding_dim = 16

model = Sequential()
model.add(Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_sentence_length))
model.add(LSTM(32, dropout=0.5))
model.add(Dense(16, activation="relu"))
model.add(Dense(16, activation="relu"))
model.add(Dense(num_classes, activation="softmax"))

model.summary()

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

import numpy as np

epochs = 500
y = np.array(y)
batch_size = 32

model.fit(X_padded_sequences, y, epochs=epochs, batch_size=batch_size)

model.save("chatbot_model")

with open("tokenizer/tokenizer.pickle", "wb") as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

# with open("tokenizer/label_encoder.pickle", "wb") as lbl_encoder:
#     pickle.dump(encoder, lbl_encoder, protocol=pickle.HIGHEST_PROTOCOL)