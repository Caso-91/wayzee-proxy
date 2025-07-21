import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        user_message = data.get("message")

        if not user_message:
            return jsonify({"error": "Messaggio mancante"}), 400

        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Sei un assistente esperto in viaggi, che propone destinazioni dettagliate, adatte al profilo del viaggiatore."},
                {"role": "user", "content": user_message}
            ]
        )

        return jsonify({"response": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
