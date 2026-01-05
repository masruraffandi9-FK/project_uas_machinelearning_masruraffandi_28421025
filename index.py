from flask import Flask, request, jsonify
import pickle
import json
import random
import numpy as np
import os

app = Flask(__name__)

# ===== API KEY (dari environment variable) =====
API_KEY = os.environ.get("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")

# ===== Load model & data =====
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
data = json.load(open("data/intents.json"))

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

@app.route("/api/chat", methods=["POST"])
def chat():
    # ===== CEK API KEY =====
    client_key = request.headers.get("X-API-KEY")
    if client_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    user_input = request.json.get("message", "")
    response = chatbot_response(user_input)
    return jsonify({"response": response})
