from flask import Flask, render_template, request, jsonify, send_from_directory
from tinydb import TinyDB, Query
import os
import logging

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024

# Persisted lightweight memory for explicit "remember this" commands.
os.makedirs("core", exist_ok=True)
db = TinyDB("core/brain.json")
Fact = Query()

def remember_fact(text):
    msg = text.lower()
    if "merk dir" not in msg or " ist " not in msg:
        return None
    try:
        parts = msg.split("merk dir", 1)[1].split(" ist ", 1)
        fact, value = parts[0].strip(), parts[1].strip()
        if not fact or not value:
            return "Bitte nutze: Merk dir [Sache] ist [Wert]."
        db.upsert({"fact": fact, "val": value}, Fact.fact == fact)
        return f"Gespeichert: {fact} ist {value}."
    except (IndexError, ValueError):
        return "Fehler beim Speichern. Syntax: Merk dir [Sache] ist [Wert]."

def get_ai_reply(text):
    remembered = remember_fact(text)
    if remembered:
        return remembered
    msg = text.lower()
    for item in db.all():
        if item.get("fact") and item["fact"] in msg:
            return f"Erinnerung: {item['fact']} ist nach meinen gespeicherten Daten {item.get('val', '')}."

    if os.getenv("AI_ENABLED", "true").strip().lower() != "true":
        raise RuntimeError("Die KI ist in Render mit AI_ENABLED=false deaktiviert.")
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY fehlt in den Render Environment Variables.")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
    if not model:
        raise RuntimeError("OPENAI_MODEL ist nicht konfiguriert.")

    from openai import OpenAI
    memory_context = "\\n".join(
        f"- {item.get('fact', '')}: {item.get('val', '')}" for item in db.all()[-50:]
    )
    instructions = (
        "Du bist Galactic AI, ein hilfreicher deutschsprachiger KI-Assistent für Recherche, "
        "Analyse, Programmierung und kreative Aufgaben. Antworte präzise und ehrlich. "
        "Erfinde keine Quellen oder ausgeführten Aktionen. Nutze gespeicherte Fakten nur, "
        "wenn sie zur Frage passen.\nGespeicherte Fakten:\n" + memory_context
    )
    response = OpenAI(api_key=api_key).responses.create(
        model=model,
        instructions=instructions,
        input=text,
    )
    return response.output_text or "Die KI hat keine Textantwort zurückgegeben."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/engine")
def engine():
    return render_template("game_engine.html")

@app.route("/health")
@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "project": "Galactic AI",
        "ai_enabled": os.getenv("AI_ENABLED", "true").lower() == "true",
        "openai_configured": bool(os.getenv("OPENAI_API_KEY", "").strip()),
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    })

@app.route("/chat", methods=["POST"])
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    text = str(data.get("msg") or data.get("message") or "").strip()
    if not text:
        return jsonify({"ok": False, "error": "Bitte gib eine Nachricht ein."}), 400
    if len(text) > 12000:
        return jsonify({"ok": False, "error": "Nachricht ist zu lang (max. 12.000 Zeichen)."}), 413
    try:
        reply = get_ai_reply(text)
        return jsonify({"ok": True, "reply": reply}), 200
    except RuntimeError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 503
    except Exception:
        app.logger.exception("Galactic AI provider request failed")
        return jsonify({"ok": False, "error": "Die KI-Anfrage ist fehlgeschlagen. Prüfe API-Key, Modellfreigabe, Guthaben und Render-Logs."}), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "10000")), debug=False)
