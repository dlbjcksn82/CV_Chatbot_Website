from flask import Flask, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Load OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Check if the API key is set
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print("✅ OpenAI API Key Found!")  # Confirms that the key exists
else:
    print("❌ ERROR: OPENAI_API_KEY Not Found!")  # If not found, will print an error

@app.route("/")
def test_chat():
    try:
        # Fixed test query
        test_prompt = "Can you explain why the sky is blue?"

        # Send query to OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": test_prompt}],
            max_tokens=100,
            temperature=0.7
        )
        print(response.choices[0].message.content)
        return jsonify({"response": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Use Render's assigned port or default to 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)