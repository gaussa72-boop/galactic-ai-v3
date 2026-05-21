from flask import Flask, render_template, request, jsonify
from modules.ionos_ai import get_ionos_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_msg = data.get('message', '')
    ai_type = data.get('ai', 'ionos')
    
    # Beispiel-Logik für die KI-Antwort
    reply = f"Antwort von {ai_type}: Verarbeite '{user_msg}'..."
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
