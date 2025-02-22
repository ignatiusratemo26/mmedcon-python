from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
import logging

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://www.mmedcon.com"}}) 

logging.basicConfig(level=logging.INFO)

load_dotenv()

client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'),)

@app.route('/hello', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello World"})


# fetching data from wix and storing it in a dataframe
@app.route('/fetch_casestudies', methods=['GET'])
def fetch_casestudies():

    response = requests.get(os.getenv('FETCH_CASE_STUDIES'))
    if response.status_code == 200:

        data = response.json().get('items', [])

        df = pd.DataFrame(data) # Converting WIX data to Pandas DataFrame
        return jsonify({"data": df.to_dict(orient='records')})
    else:
        return jsonify({"error": "Failed to fetch data"}), 500
    

@app.route('/ask', methods=['POST'])
def ask_chatgpt():
    data = request.json
    question = data.get('question')

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        response = client.chat.completions.create(
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