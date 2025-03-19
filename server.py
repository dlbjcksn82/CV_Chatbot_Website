from flask import Flask, request, jsonify
from chatbot import chat_with_gemma

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    response = chat_with_gemma(user_input)

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
