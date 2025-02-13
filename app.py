from flask import Flask, jsonify, request
from flask_cors import CORS
import openai
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app) 

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/hello', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello World"})

@app.route('/ask', methods=['POST'])
def ask_chatgpt():
    data = request.json
    question = data.get('question')

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ],
            max_tokens=150
        )
        answer = response.choices[0].message['content'].strip()
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)