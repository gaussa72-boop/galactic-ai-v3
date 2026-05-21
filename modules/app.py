from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# --------------------
# IONOS KI
# --------------------

def ionos_ai(msg):

    responses = [
        "IONOS-7 analysiert den Quantenstrom.",
        "Der Multiversumkern reagiert.",
        "Singularitätsdaten werden neu berechnet.",
        "Kosmische Parameter verändern sich.",
        "Der goldene Kern pulsiert."
    ]

    return random.choice(responses)


# --------------------
# ROUTES
# --------------------

@app.route("/")
def loader():
    return render_template("loader.html")


@app.route("/portal")
def portal():
    return render_template("portal.html")


@app.route("/chat", methods=["POST"])
def chat():

    msg = request.json["msg"]

    reply = ionos_ai(msg)

    return jsonify({"reply": reply})


# --------------------

if __name__ == "__main__":
    app.run(debug=True)