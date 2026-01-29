import requests
import json
import re

class OllamaAdapter:
    def __init__(self, model="llama3.2", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"

    def clean_response(self, text):
        """
        Attempts to extract JSON from the response text.
        """
        # Try to find JSON block enclosed in ```json ... ```
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            return json_match.group(1)
        
        # Try to find just valid JSON structure {}
        bracket_match = re.search(r'\{.*\}', text, re.DOTALL)
        if bracket_match:
            return bracket_match.group(0)
            
        return text

    def generate_test_cases(self, user_input):
        prompt = f"""
You are a Senior QA Automation Engineer.
Your task is to generate comprehensive test cases for the following feature/requirement:

"{user_input}"

Output MUST be a valid JSON object matching this schema:
{{
  "test_cases": [
    {{
      "id": "TC_001",
      "title": "Concise Title",
      "description": "What is being tested",
      "preconditions": "Setup required",
      "steps": ["Step 1", "Step 2"],
      "expected_result": "Success criteria"
    }}
  ]
}}

RETURN ONLY JSON. NO MARKDOWN. NO COMMENTS.
"""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json" # Llama 3 supports json mode
        }

        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            raw_text = response.json().get('response', '')
            
            # Even with format='json', sometimes we verify
            cleaned_text = self.clean_response(raw_text)
            
            return json.loads(cleaned_text)
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Ollama API Error: {str(e)}"}
        except json.JSONDecodeError:
            return {"error": "Failed to parse LLM output as JSON", "raw_output": raw_text}

if __name__ == "__main__":
    # Quick test
    adapter = OllamaAdapter()
    res = adapter.generate_test_cases("Login Page")
    print(json.dumps(res, indent=2))
