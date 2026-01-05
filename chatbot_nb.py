import json
import random
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load dataset
with open("data/intents.json", encoding="utf-8") as f:
    data = json.load(f)

sentences = []
labels = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        sentences.append(pattern.lower())
        labels.append(intent["tag"])

# Vectorizer & Model
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(sentences)

model = MultinomialNB()
model.fit(X, labels)

def chatbot_response(text):
    X_test = vectorizer.transform([text.lower()])
    
    probs = model.predict_proba(X_test)[0]
    max_prob = np.max(probs)
    predicted_index = np.argmax(probs)
    predicted_tag = model.classes_[predicted_index]

    word_count = len(text.split())

    if word_count > 2 and max_prob < 0.25:
        return "Maaf, saya belum memahami pertanyaan tersebut."

    if word_count <= 2 and max_prob < 0.15:
        return "Maaf, saya belum memahami pertanyaan tersebut."

    for intent in data["intents"]:
        if intent["tag"] == predicted_tag:
            return random.choice(intent["responses"])



import pickle

# simpan model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

# simpan vectorizer
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("Model dan vectorizer berhasil disimpan.")
