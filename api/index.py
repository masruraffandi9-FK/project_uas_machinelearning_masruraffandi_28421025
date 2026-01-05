from flask import Flask, request, jsonify
import pickle
import json
import random
import numpy as np

app = Flask(__name__)

# load model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
data = json.load(open("intents.json"))

def chatbot_response(text):
    X_test = vectorizer.transform([text.lower()])
    probs = model.predict_proba(X_test)[0]
    max_prob = np.max(probs)
    predicted_tag = model.classes_[np.argmax(probs)]

    if max_prob < 0.35:
        return "Maaf, saya belum memahami pertanyaan tersebut."

    for intent in data["intents"]:
        if intent["tag"] == predicted_tag:
            return random.choice(intent["responses"])

    return "Maaf, saya belum memahami pertanyaan tersebut."

@app.route("/", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    response = chatbot_response(user_input)
    return jsonify({"response": response})

# ⚠️ JANGAN app.run()
