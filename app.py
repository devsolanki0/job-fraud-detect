from flask import Flask, render_template, request
import pickle
import re
import string

app = Flask(__name__)

# Load model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', ' amount ', text)
    text = re.sub(r'http\S+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    confidence = ""

    if request.method == "POST":
        message = request.form["message"]
        cleaned = clean_text(message)
        vector = vectorizer.transform([cleaned])
        prediction = model.predict(vector)
        prob = model.predict_proba(vector)[0][1]

        if prediction[0] == 1:
            result = "🔴 FRAUD ALERT!"
            confidence = f"Confidence: {round(prob*100,2)}%"
        else:
            result = "🟢 Likely Legitimate Job Message"
            confidence = f"Confidence: {round((1-prob)*100,2)}%"

    return render_template("index.html", result=result, confidence=confidence)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)