# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from .qa_chain import get_bot_response  # Import the updated qa_chain

app = Flask(__name__)
CORS(app, resources={r"/chatbot": {"origins": "*"}})

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.json
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "⚠️ Please enter a message."})

    try:
        # Call the qa_chain function
        reply = get_bot_response(user_message)
    except Exception as e:
        # Fallback mock reply if anything goes wrong
        print(f"Unexpected error in /chatbot: {e}")
        reply = f"[MOCK RESPONSE] You said: {user_message}"

    return jsonify({"reply": reply})

@app.route("/", methods=["GET"])
def home():
    return "Chatbot backend is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
