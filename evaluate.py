from typing import List
import numpy as np
import pickle
import json
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

with open("tokenizer/tokenizer.pickle", "rb") as handle:
    tokenizer: Tokenizer = pickle.load(handle)

with open("data/intents.json", "r", encoding="utf-8") as f:
    intents_json = json.load(f)

intents = intents_json["intents"]

labels = []

for intent in intents:
    if intent["tag"] not in labels:
        labels.append(intent["tag"])


model: Sequential = load_model("chatbot_model")
max_len: int = 13



def evaluate(user_input):
    sequences = tokenizer.texts_to_sequences([user_input]) #user input u brojeve
    padded_sequences = pad_sequences(sequences, maxlen=max_len, truncating="post") #pad zbog dimenzionalnosti
    result = model.predict(padded_sequences) #predict , vrati listu sa postotcima koji odgovaraju pojedinim klasama(tagovi)
    prediction = np.argmax(result) #index gdje je postotak najveci

    tag = labels[prediction]

    for intent in intents:
        if tag == intent["tag"]:
            return np.random.choice(intent["responses"])

