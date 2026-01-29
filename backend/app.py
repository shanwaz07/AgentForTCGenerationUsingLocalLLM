from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os

# Add tools directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.ollama_adapter import OllamaAdapter

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

adapter = OllamaAdapter()

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    user_input = data.get('user_input')
    
    if not user_input:
        return jsonify({"error": "No user_input provided"}), 400

    result = adapter.generate_test_cases(user_input)
    
    if "error" in result:
        return jsonify(result), 500
        
    return jsonify(result)

if __name__ == '__main__':
    print("Starting Flask Server on port 5000...")
    app.run(debug=True, port=5000)
