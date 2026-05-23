from flask import Flask, request, jsonify
from core.brain import GalacticBrain
from universes.procedural import Universe
from urspirit.poetry import create_poem

app = Flask(__name__)

brain = GalacticBrain()
universe = Universe()

@app.route("/")
def home():
    return "🌌 Galactic AI Wonderland 🌌"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt")

    return jsonify({
        "brain": brain.think(prompt),
        "universe": universe.generate(),
        "poem": create_poem(prompt)
    })

if __name__ == "__main__":
    app.run(debug=True)