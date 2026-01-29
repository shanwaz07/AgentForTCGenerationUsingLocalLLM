import requests
import json
import sys

def check_ollama():
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.2",
        "prompt": "Hello via Python!",
        "stream": False
    }
    
    print(f"Testing connection to {url} with model 'llama3.2'...")
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        print("Success!")
        print(f"Response: {data.get('response')}")
        return True
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Ollama. Is it running on port 11434?")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Error: API request failed - {e}")
        # Check if it's a model not found error
        if response.status_code == 404:
            print("Model 'llama3.2' not found. Please run 'ollama pull llama3.2'")
        return False

if __name__ == "__main__":
    success = check_ollama()
    if not success:
        sys.exit(1)
