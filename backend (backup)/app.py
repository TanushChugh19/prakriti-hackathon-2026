import os
import pathlib
import sys

import torch
from flask import Flask, jsonify, request
from flask_cors import CORS
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# BASE_DIR = pathlib.Path(__file__).resolve().parent
# MODEL_PATH = str(BASE_DIR / "trained_model")

if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "trained_model")

if not pathlib.Path(MODEL_PATH).exists():
    raise FileNotFoundError(f"Could not find trained model directory:\n{MODEL_PATH}")

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

print("Loading model...")
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model.to(device)

id2label = model.config.id2label

print("Model loaded successfully.")
print(f"Using device: {device}")
print(id2label)

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Emotion Signal API Running"


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing text"}), 400

    text = data["text"]

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = torch.softmax(outputs.logits, dim=1)[0]

    prediction = torch.argmax(probabilities).item()

    emotion = id2label[prediction]

    scores = {
        id2label[i]: round(float(probabilities[i]) * 100, 2)
        for i in range(len(probabilities))
    }

    return jsonify(
        {
            "emotion": emotion,
            "confidence": scores[emotion],
            "scores": scores,
        }
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
