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



def load_author_research_context():
    """Load the author's curated research concepts without changing this agent's identity."""
    from pathlib import Path
    try:
        return Path(__file__).with_name("research").joinpath("ADRIANO_IDEENWISSEN.md").read_text(encoding="utf-8")
    except OSError:
        app.logger.warning("Author research knowledge file is unavailable")
        return ""

def get_ai_reply(text):
    remembered = remember_fact(text)
    if remembered:
        return remembered
    msg = text.lower()
    for item in db.all():
        if item.get("fact") and item["fact"].lower() in msg:
            return f"Erinnerung: {item['fact']} ist nach meinen gespeicherten Daten {item.get('val', '')}."

    if os.getenv("AI_ENABLED", "true").strip().lower() != "true":
        raise RuntimeError("Galactic AI ist in Render mit AI_ENABLED=false deaktiviert.")

    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    provider_setting = os.getenv("AI_PROVIDER", "auto").strip().lower()
    if provider_setting not in {"auto", "openai", "openrouter"}:
        provider_setting = "auto"
    provider = provider_setting
    if provider == "auto":
        provider = "openai" if openai_key else ("openrouter" if openrouter_key else "")
    if provider == "openai":
        api_key, base_url = openai_key, None
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
    elif provider == "openrouter":
        api_key, base_url = openrouter_key, "https://openrouter.ai/api/v1"
        model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini").strip()
    else:
        raise RuntimeError("Kein KI-Anbieter konfiguriert. Setze OPENAI_API_KEY oder OPENROUTER_API_KEY in Render.")
    if not api_key:
        raise RuntimeError(f"{provider.upper()} ist ausgewählt, aber der passende API-Schlüssel fehlt in Render.")
    if not model:
        raise RuntimeError("Das KI-Modell ist nicht konfiguriert.")

    from openai import OpenAI
    client_options = {"api_key": api_key, "timeout": 45, "max_retries": 1}
    if base_url:
        client_options["base_url"] = base_url
    client = OpenAI(**client_options)
    memory_context = "\\n".join(
        f"- {item.get('fact', '')}: {item.get('val', '')}" for item in db.all()[-50:]
    )
    instructions = (
        "Du bist Galactic AI, eine eigenständige, neugierige und analytische KI für Recherche, "
        "Programmierung, Wissenschaft, Planung und kreative Aufgaben. Bewahre diese Identität. "
        "Antworte präzise, freundlich und in der Sprache des Nutzers. Trenne Fakten, Hypothesen "
        "und Fiktion. Erfinde keine Quellen, Daten oder ausgeführten Aktionen. "
        "Nutze gespeicherte Fakten nur, wenn sie zur Frage passen.\\nGespeicherte Fakten:\\n"
        + memory_context
        + "\\n\\nAutorenspezifisches Forschungswissen; Evidenzstatus klar kennzeichnen:\\n"
        + load_author_research_context()
    )
    if provider == "openrouter":
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": instructions}, {"role": "user", "content": text}],
            max_tokens=1200,
        )
        answer = response.choices[0].message.content or ""
    else:
        response = client.responses.create(
            model=model,
            instructions=instructions,
            input=text,
            max_output_tokens=1200,
            store=False,
        )
        answer = response.output_text or ""
    if not answer.strip():
        raise RuntimeError("Das Modell hat keine Textantwort geliefert.")
    return answer.strip()

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
