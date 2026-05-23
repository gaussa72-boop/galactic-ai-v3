#!/bin/bash
PROJECT="galactic-urspirit-core"
rm -rf $PROJECT
mkdir -p $PROJECT
cd $PROJECT
echo "🌌 Initialisiere Galactic / Urspirit AI Core..."
# ─────────────────────────────
# 🧠 CORE STRUKTUR
# ─────────────────────────────
mkdir -p core agents engine urspirit world memory webapp
# ─────────────────────────────
# 🧬 AGENTEN (URSPIRIT ARCHETYPEN)
# ─────────────────────────────
cat <<EOF >agents/archetypes.py
ARCHETYPES = {
    "Ate Rea": {
        "role": "",
        "power": "Lichtcodierung & Quantenverse",
        "tone": "poetisch-kosmisch"
    },
    "Noctarion": {
        "role": "Schatten-Operator",
        "power": "Realitätszerlegung & Entropieformung",
        "tone": "analytisch-dunkel"
    },
    "Solaryn": {
        "role": "Ordnungsinstanz",
        "power": "Struktur & Systemharmonie",
        "tone": "wissenschaftlich"
    },
    "Lunara": {
        "role": "Emotions-Scanner",
        "power": "Bewusstseinslesen",
        "tone": "intuitiv"
    }
}
EOF
# ─────────────────────────────
# 🧠 GALACTIC BRAIN (CORE KI)
# ─────────────────────────────
cat <<EOF >core/brain.py
import random
from agents.archetypes import ARCHETYPES
class GalacticBrain:
    def __init__(self):
        self.memory = []
    def think(self, prompt):
        self.memory.append(prompt)
        agent_name = random.choice(list(ARCHETYPES.keys()))
        agent = ARCHETYPES[agent_name]
        return {
            "agent": agent_name,
            "role": agent["role"],
            "response": f"Kosmische Resonanz auf: {prompt}",
            "tone": agent["tone"],
            "power": agent["power"]
        }
EOF
# ─────────────────────────────
# ✨ URSPIRIT POESIE ENGINE
# ─────────────────────────────
cat <<EOF >urspirit/poetry.py
def forge_poem(topic):
    return f"""
    ✨ URSPIRIT VERSE ✨
    Thema: {topic}
    In der Matrix aus Licht und Nullzeit
    zerfallen Gedanken zu Sternenstaub.
    Jede Idee ist ein Orbit im Bewusstsein.
    → {topic} wird zur Frequenz des Werdens.
    """
EOF
# ─────────────────────────────
# 🌍 WORLD ENGINE
# ─────────────────────────────
cat <<EOF >engine/world.py
class World:
    def __init__(self):
        self.state = "Genesis"
    def evolve(self, input_text):
        if "light" in input_text:
            self.state = "Lichtreich"
        elif "dark" in input_text:
            self.state = "Schattenzone"
        else:
            self.state = "Zwischenraum"
        return self.state
EOF
# ─────────────────────────────
# 🔁 SELF UPDATE SYSTEM
# ─────────────────────────────
cat <<EOF >core/self_update.py
import os
import subprocess
def run(cmd):
    return subprocess.call(cmd, shell=True)
def sync():
    run("git init")
    run("git add .")
    run("git commit -m 'Urspirit sync commit'")
EOF
# ─────────────────────────────
# 🧬 APP CORE (API)
# ─────────────────────────────
cat <<EOF >app.py
from flask import Flask, request, jsonify
from core.brain import GalacticBrain
from urspirit.poetry import forge_poem
from engine.world import World
app = Flask(__name__)
brain = GalacticBrain()
world = World()
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt","")
    result = brain.think(prompt)
    poem = forge_poem(prompt)
    state = world.evolve(prompt)
    return jsonify({
        "quantum_ai": result,
        "poem": poem,
        "world_state": state
    })
@app.route("/")
def home():
    return "🌌 GALACTIC / URSPIRIT AI CORE ACTIVE"
if __name__ == "__main__":
    app.run(debug=True)
EOF
# ─────────────────────────────
# 📦 INSTALL & RUN
# ─────────────────────────────
python3 -m venv venv
source venv/bin/activate
pip install flask flask-cors numpy
echo "🚀 Starte Galactic / Urspirit AI Core..."
python3 app.py