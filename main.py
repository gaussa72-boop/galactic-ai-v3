from flask import Flask, render_template, request, jsonify
from tinydb import TinyDB, Query
import os

app = Flask(__name__)

# Datenbank für das KI-Gedächtnis
if not os.path.exists('core'): os.makedirs('core')
db = TinyDB('core/brain.json')

def get_ai_reply(text):
    msg = text.lower()
    Fact = Query()
    
    # 1. Lern-Funktion
    if "merk dir" in msg and " ist " in msg:
        try:
            parts = msg.split("merk dir")[1].split(" ist ")
            f, v = parts[0].strip(), parts[1].strip()
            db.upsert({'fact': f, 'val': v}, Fact.fact == f)
            return f"Protokoll: Information '{f}' wurde in der Quanten-Matrix gesichert."
        except:
            return "Fehler beim Speichern. Syntax: 'Merk dir [Sache] ist [Wert]'"

    # 2. Gedächtnis-Abfrage
    all_facts = db.all()
    for item in all_facts:
        if item['fact'] in msg:
            return f"Matrix-Erinnerung: {item['fact']} ist nach meinen Daten {item['val']}."

    # 3. Standard-Befehle
    if "status" in msg: return "Systeme im grünen Bereich. Diashow der Bilder 1-5 aktiv."
    if "wer bist du" in msg: return "Ich bin IONOS-7, die zentrale Instanz deines Multiversums."
    
    return "Befehl empfangen. Analysiere Datenströme..."

@app.route("/")
def index(): return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    reply = get_ai_reply(data.get("msg", ""))
    return jsonify({"reply": reply})

if __name__ == "__main__":
    print("🚀 IONOS-7 startet auf http://127.0.0.1:5005")
    app.run(port=5005, debug=True)
