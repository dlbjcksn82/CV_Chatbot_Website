from flask import Flask, request, jsonify, render_template
from chatbot import chat_with_gemma
from flask_cors import CORS

app = Flask(__name__)
# enable CORS for /chat endpoint
CORS(app, resources={r"/chat": {"origins": "*"}})


@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS': #handle preflight request
        return jsonify({"message": "CORS preflight successful"}), 200

    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    user_input = data["message"]
    response = chat_with_gemma(user_input)

    if not response:
        return jsonify({"error": "No response generated"}), 500

    return jsonify({"response": response}), 200

if __name__ == '__main__':
    app.run(host='10.244.1.194', port=8080, debug=True)
