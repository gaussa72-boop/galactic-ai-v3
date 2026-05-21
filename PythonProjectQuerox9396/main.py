# main.py
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("msg", "").lower()

    # Intelligente Logik-Weiche
    if "status" in msg:
        reply = "KONTROLLE: Alle Systeme im Multiversum laufen stabil."
    elif "spiegel" in msg or "mirror" in msg:
        reply = "MIRROR-AI: Ich reflektiere deine Daten... Keine Anomalien."
    else:
        reply = "CORE-LOG: Befehl verarbeitet. Bilder-Diashow aktiv."

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(port=5005, debug=True)