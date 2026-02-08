from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import sys
import os
import base64
import io
from datetime import datetime

# Add tools directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.llm_adapter import LLMProvider
from tools.excel_export import generate_excel

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', '.tmp', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/providers', methods=['GET'])
def get_providers():
    """Get list of available LLM providers."""
    return jsonify({
        "providers": [
            {
                "id": "ollama",
                "name": "Local LLM (Ollama)",
                "description": "Run models locally using Ollama",
                "requires_api_key": False,
                "default": True
            },
            {
                "id": "openai",
                "name": "OpenAI",
                "description": "Use OpenAI GPT models",
                "requires_api_key": True,
                "default": False
            },
            {
                "id": "kimi",
                "name": "KIMI (Moonshot AI)",
                "description": "Use KIMI AI models",
                "requires_api_key": True,
                "default": False
            },
            {
                "id": "groq",
                "name": "Groq",
                "description": "Ultra-fast LLM inference with Llama models",
                "requires_api_key": True,
                "default": False
            }
        ]
    })


@app.route('/api/generate', methods=['POST'])
def generate():
    """Generate test cases using the selected LLM provider."""
    
    # Check if request has files (multipart/form-data)
    if request.content_type and 'multipart/form-data' in request.content_type:
        user_input = request.form.get('user_input', '')
        provider = request.form.get('provider', 'ollama')
        api_key = request.form.get('api_key', '')
        html_code = request.form.get('html_code', '')
        
        # Handle image upload
        image_data = None
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and image_file.filename:
                # Read image and convert to base64
                image_bytes = image_file.read()
                image_data = base64.b64encode(image_bytes).decode('utf-8')
        
        # Handle HTML file upload
        if 'html_file' in request.files:
            html_file = request.files['html_file']
            if html_file and html_file.filename:
                html_code = html_file.read().decode('utf-8', errors='ignore')
    else:
        # JSON request
        data = request.json or {}
        user_input = data.get('user_input', '')
        provider = data.get('provider', 'ollama')
        api_key = data.get('api_key', '')
        html_code = data.get('html_code', '')
        image_data = data.get('image_data')
    
    if not user_input and not html_code:
        return jsonify({"error": "No user_input or html_code provided"}), 400
    
    # Validate provider
    valid_providers = ['ollama', 'openai', 'kimi', 'groq']
    if provider not in valid_providers:
        return jsonify({
            "error": f"Invalid provider '{provider}'. Valid options: {', '.join(valid_providers)}"
        }), 400
    
    # Check if API key is required but not provided
    if provider in ['openai', 'kimi', 'groq'] and not api_key:
        provider_name = "OpenAI" if provider == 'openai' else "KIMI"
        return jsonify({
            "error": f"{provider_name} API key is required. Please enter your API key in settings."
        }), 400
    
    try:
        # Get the appropriate adapter
        adapter = LLMProvider.get_adapter(provider, api_key=api_key)
        
        # Generate test cases with optional image and HTML code
        result = adapter.generate_test_cases(
            user_input=user_input,
            image_data=image_data,
            html_code=html_code
        )
        
        if "error" in result:
            return jsonify(result), 500
        
        # Add metadata to response
        result["provider_used"] = provider
        result["has_image"] = bool(image_data)
        result["has_html"] = bool(html_code)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route('/api/export/excel', methods=['POST'])
def export_excel():
    """Export test cases to Excel format."""
    data = request.json
    test_cases = data.get('test_cases', [])
    feature_name = data.get('feature_name', 'Test_Cases')
    
    if not test_cases:
        return jsonify({"error": "No test cases provided"}), 400
    
    try:
        # Generate Excel file
        excel_buffer = generate_excel(test_cases, feature_name)
        
        # Create safe filename
        safe_filename = "".join(c for c in feature_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_filename = safe_filename.replace(' ', '_')[:50]  # Limit length
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_filename}_{timestamp}.xlsx"
        
        # Send file
        excel_buffer.seek(0)
        return send_file(
            excel_buffer,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({"error": f"Failed to generate Excel: {str(e)}"}), 500


if __name__ == '__main__':
    print("Starting Flask Server on port 5000...")
    print("Supported LLM providers: Ollama (default), OpenAI, KIMI")
    print("Features: Text input, Image upload, HTML code upload, Excel export")
    app.run(debug=True, port=5000)
