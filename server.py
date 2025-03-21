import os
from flask import Flask, request, jsonify, render_template
from chatbot import chat_with_gpt
from flask_cors import CORS
os.environ["TOKENIZERS_PARALLELISM"] = "false"


app = Flask(__name__, static_folder="static", template_folder="templates")
# enable CORS for /chat endpoint
CORS(app, resources={r"/chat": {"origins": "*"}})


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':  # handle preflight request
        return jsonify({"message": "CORS preflight successful"}), 200

    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    user_input = data["message"]
    response = chat_with_gpt(user_input)

    if not response:
        return jsonify({"error": "No response generated"}), 500

    return jsonify({"response": response}), 200


if __name__ == '__main__':
    # Use Render's assigned port or default to 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
