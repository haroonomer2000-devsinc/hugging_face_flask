from flask import Flask, request, jsonify
from transformers import pipeline
from functools import wraps
from flask import abort

app = Flask(__name__)

model = pipeline("fill-mask", model="bert-base-uncased")

def check_auth(token):
    return token == "f2b77caf8c87de875317b4f18e2e71a1"

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth or not check_auth(auth):
            return abort(401)
        return f(*args, **kwargs)
    return decorated

@app.route('/api/generate', methods=['POST'])
@requires_auth
def generate_text():
    data = request.get_json()
    if 'input_text' not in data:
        return jsonify({"error": "Missing input_text parameter"}), 400

    input_text = data['input_text']
    try:
        # Generate text from model
        result = model(input_text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
