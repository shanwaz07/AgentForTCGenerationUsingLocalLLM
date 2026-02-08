"""
Unified LLM Adapter supporting multiple providers:
- Ollama (Local LLM)
- OpenAI
- KIMI (Moonshot AI)
"""

import requests
import json
import re
import os
import base64
from abc import ABC, abstractmethod


class BaseLLMAdapter(ABC):
    """Abstract base class for LLM adapters."""
    
    @abstractmethod
    def generate_test_cases(self, user_input, image_data=None, html_code=None):
        """Generate test cases for the given user input."""
        pass
    
    def create_prompt(self, user_input, image_data=None, html_code=None):
        """Create the prompt for test case generation."""
        
        # Build context sections
        image_context = ""
        html_context = ""
        
        if image_data:
            image_context = """
[IMAGE ANALYSIS REQUIRED]
A UI screenshot/image has been provided. 
CRITICAL INSTRUCTION: Analyze the visual elements in this image including:
- All buttons, labels, and UI components visible
- Form fields, input types, and validation indicators
- Navigation elements and links
- Error messages and status indicators
- Layout and responsive design elements
Generate test cases that specifically test these visible UI elements.
"""
        
        if html_code:
            html_context = f"""
[HTML CODE ANALYSIS REQUIRED]
The following HTML code has been provided:
```html
{html_code[:8000]}
```
CRITICAL INSTRUCTION: Analyze this HTML code thoroughly and generate test cases for:
- All form inputs (text, email, password, etc.) and their attributes (required, pattern, etc.)
- All buttons and their actions (submit, reset, onclick handlers)
- Form validation rules (required fields, min/max length, patterns)
- CSS classes that indicate styling or state changes
- Any JavaScript event handlers mentioned
- Accessibility attributes (aria-*, alt, title)
- Link URLs and navigation paths
Generate comprehensive test cases covering all these HTML elements.
"""
        
        context = ""
        if image_context:
            context += image_context + "\n\n"
        if html_context:
            context += html_context + "\n\n"
        
        return f"""You are a Senior QA Automation Engineer with expertise in comprehensive test coverage.

USER REQUIREMENT:
"{user_input}"

{context}
---
GENERATION REQUIREMENTS:
1. Generate 15-25 test cases MINIMUM - be EXTREMELY thorough
2. Each test case MUST be specific to the provided content (image/HTML/text)
3. Cover ALL possible scenarios:
   - Happy path (valid inputs, successful operations)
   - Error cases (invalid inputs, missing fields, wrong formats)
   - Edge cases (boundary values, extreme inputs)
   - Security tests (SQL injection, XSS, authentication)
   - UI/UX tests (responsiveness, accessibility, usability)
   - Integration scenarios (end-to-end workflows)
   - Validation tests (field requirements, format checks)
4. Each test case MUST have:
   - Unique ID (TC_001, TC_002, etc.)
   - Clear, specific title
   - Detailed description explaining what's being tested
   - Preconditions that setup the test
   - 3-7 detailed, actionable steps
   - Specific expected results
5. If HTML is provided, reference specific elements (input IDs, button names, etc.)
6. If image is provided, reference specific UI elements visible in the screenshot

Output MUST be valid JSON matching this exact schema:
{{
  "test_cases": [
    {{
      "id": "TC_001",
      "title": "Specific, descriptive title",
      "description": "Detailed explanation of what this test verifies",
      "preconditions": "Required setup before test execution",
      "steps": ["Step 1: Specific action", "Step 2: Next action", "Step 3: Verify result"],
      "expected_result": "Exact expected outcome"
    }}
  ]
}}

RETURN ONLY VALID JSON. NO MARKDOWN CODE BLOCKS. NO COMMENTS. MINIMUM 15 TEST CASES.
"""

    def clean_response(self, text):
        """Extract JSON from response text."""
        # Try to find JSON block enclosed in ```json ... ```
        json_match = re.search(r'```json\s*(\{{.*?)\s*```', text, re.DOTALL)
        if json_match:
            return json_match.group(1)
        
        # Try to find just valid JSON structure {{}}
        bracket_match = re.search(r'\{.*"test_cases".*\}', text, re.DOTALL)
        if bracket_match:
            return bracket_match.group(0)
            
        return text


class OllamaAdapter(BaseLLMAdapter):
    """Adapter for Ollama (Local LLM)."""
    
    def __init__(self, model="llama3.2", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
    
    def generate_test_cases(self, user_input, image_data=None, html_code=None):
        prompt = self.create_prompt(user_input, image_data, html_code)
        
        # Note: Ollama with standard models cannot actually "see" images
        # The prompt mentions the image but the LLM analyzes based on text context
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
        
        try:
            print(f"[OllamaAdapter] Generating test cases with prompt length: {len(prompt)}")
            print(f"[OllamaAdapter] Has image: {bool(image_data)}, Has HTML: {bool(html_code)}")
            
            response = requests.post(self.api_url, json=payload, timeout=180)
            response.raise_for_status()
            raw_text = response.json().get('response', '')
            
            print(f"[OllamaAdapter] Raw response length: {len(raw_text)}")
            
            cleaned_text = self.clean_response(raw_text)
            result = json.loads(cleaned_text)
            
            # Validate minimum test cases
            if 'test_cases' in result:
                print(f"[OllamaAdapter] Generated {len(result['test_cases'])} test cases")
                if len(result['test_cases']) < 10:
                    print(f"[OllamaAdapter] Warning: Only {len(result['test_cases'])} test cases generated")
            
            return result
            
        except requests.exceptions.ConnectionError:
            return {"error": "Cannot connect to Ollama. Please ensure Ollama is running on port 11434."}
        except requests.exceptions.Timeout:
            return {"error": "Ollama request timed out. The model may be loading or the request is too complex."}
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if "404" in error_msg:
                return {"error": f"Model '{self.model}' not found. Please run 'ollama pull {self.model}'"}
            return {"error": f"Ollama API Error: {error_msg}"}
        except json.JSONDecodeError:
            return {"error": "Failed to parse LLM output as JSON", "raw_output": raw_text}


class OpenAIAdapter(BaseLLMAdapter):
    """Adapter for OpenAI API."""
    
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.openai.com/v1/chat/completions"
    
    def generate_test_cases(self, user_input, image_data=None, html_code=None):
        if not self.api_key:
            return {"error": "OpenAI API key is not provided. Please enter your API key in settings."}
        
        prompt = self.create_prompt(user_input, image_data, html_code)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Build messages
        messages = [
            {"role": "system", "content": "You are a Senior QA Automation Engineer. Return only valid JSON with comprehensive test coverage. Generate 15-25 test cases minimum based on the provided content."},
            {"role": "user", "content": prompt}
        ]
        
        # If image is provided and using vision-capable model, add it
        if image_data and self.model in ["gpt-4-vision-preview", "gpt-4-turbo", "gpt-4o"]:
            # For vision models, we can include the image
            messages[1]["content"] = [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}
            ]
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1,
            "max_tokens": 4000
        }
        
        try:
            print(f"[OpenAIAdapter] Generating test cases with model: {self.model}")
            print(f"[OpenAIAdapter] Has image: {bool(image_data)}, Has HTML: {bool(html_code)}")
            
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=90)
            
            if response.status_code == 401:
                return {"error": "Invalid OpenAI API key. Please check your API key and try again."}
            elif response.status_code == 429:
                return {"error": "OpenAI rate limit exceeded or insufficient quota. Please check your billing status."}
            elif response.status_code == 500:
                return {"error": "OpenAI server error. Please try again later."}
            
            response.raise_for_status()
            data = response.json()
            
            raw_text = data['choices'][0]['message']['content']
            cleaned_text = self.clean_response(raw_text)
            
            result = json.loads(cleaned_text)
            if 'test_cases' in result:
                print(f"[OpenAIAdapter] Generated {len(result['test_cases'])} test cases")
            
            return result
            
        except requests.exceptions.Timeout:
            return {"error": "OpenAI request timed out. Please try again."}
        except requests.exceptions.RequestException as e:
            return {"error": f"OpenAI API Error: {str(e)}"}
        except (json.JSONDecodeError, KeyError) as e:
            return {"error": "Failed to parse OpenAI response", "raw_output": str(e)}


class KimiAdapter(BaseLLMAdapter):
    """Adapter for KIMI (Moonshot AI) API."""
    
    def __init__(self, api_key, model="moonshot-v1-8k"):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.moonshot.cn/v1/chat/completions"
    
    def generate_test_cases(self, user_input, image_data=None, html_code=None):
        if not self.api_key:
            return {"error": "KIMI API key is not provided. Please enter your API key in settings."}
        
        prompt = self.create_prompt(user_input, image_data, html_code)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = [
            {"role": "system", "content": "You are a Senior QA Automation Engineer. Return only valid JSON with comprehensive test coverage. Generate 15-25 test cases minimum based on the provided content."},
            {"role": "user", "content": prompt}
        ]
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1,
            "max_tokens": 4000
        }
        
        try:
            print(f"[KimiAdapter] Generating test cases")
            print(f"[KimiAdapter] Has image: {bool(image_data)}, Has HTML: {bool(html_code)}")
            
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=90)
            
            if response.status_code == 401:
                return {"error": "Invalid KIMI API key. Please check your API key and try again."}
            elif response.status_code == 429:
                return {"error": "KIMI rate limit exceeded or insufficient quota. Please check your billing status."}
            elif response.status_code == 500:
                return {"error": "KIMI server error. Please try again later."}
            
            response.raise_for_status()
            data = response.json()
            
            raw_text = data['choices'][0]['message']['content']
            cleaned_text = self.clean_response(raw_text)
            
            result = json.loads(cleaned_text)
            if 'test_cases' in result:
                print(f"[KimiAdapter] Generated {len(result['test_cases'])} test cases")
            
            return result
            
        except requests.exceptions.Timeout:
            return {"error": "KIMI request timed out. Please try again."}
        except requests.exceptions.RequestException as e:
            return {"error": f"KIMI API Error: {str(e)}"}
        except (json.JSONDecodeError, KeyError) as e:
            return {"error": "Failed to parse KIMI response", "raw_output": str(e)}


class GroqAdapter(BaseLLMAdapter):
    """Adapter for Groq API (Fast LLM inference)."""
    
    def __init__(self, api_key, model="llama-3.1-8b-instant"):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
    
    def generate_test_cases(self, user_input, image_data=None, html_code=None):
        if not self.api_key:
            return {"error": "Groq API key is not provided. Please enter your API key in settings."}
        
        prompt = self.create_prompt(user_input, image_data, html_code)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = [
            {"role": "system", "content": "You are a Senior QA Automation Engineer. Return only valid JSON with comprehensive test coverage. Generate 15-25 test cases minimum based on the provided content."},
            {"role": "user", "content": prompt}
        ]
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1,
            "max_tokens": 4000
        }
        
        try:
            print(f"[GroqAdapter] Generating test cases with model: {self.model}")
            print(f"[GroqAdapter] Has image: {bool(image_data)}, Has HTML: {bool(html_code)}")
            
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=90)
            
            if response.status_code == 401:
                return {"error": "Invalid Groq API key. Please check your API key and try again."}
            elif response.status_code == 429:
                return {"error": "Groq rate limit exceeded. Please wait a moment and try again."}
            elif response.status_code == 500:
                return {"error": "Groq server error. Please try again later."}
            
            response.raise_for_status()
            data = response.json()
            
            raw_text = data['choices'][0]['message']['content']
            cleaned_text = self.clean_response(raw_text)
            
            result = json.loads(cleaned_text)
            if 'test_cases' in result:
                print(f"[GroqAdapter] Generated {len(result['test_cases'])} test cases")
            
            return result
            
        except requests.exceptions.Timeout:
            return {"error": "Groq request timed out. Please try again."}
        except requests.exceptions.RequestException as e:
            return {"error": f"Groq API Error: {str(e)}"}
        except (json.JSONDecodeError, KeyError) as e:
            return {"error": "Failed to parse Groq response", "raw_output": str(e)}


class LLMProvider:
    """Factory class to get the appropriate LLM adapter."""
    
    PROVIDERS = {
        "ollama": OllamaAdapter,
        "openai": OpenAIAdapter,
        "kimi": KimiAdapter,
        "groq": GroqAdapter
    }
    
    @classmethod
    def get_adapter(cls, provider, **kwargs):
        """Get an adapter instance for the specified provider."""
        provider = provider.lower()
        
        if provider not in cls.PROVIDERS:
            raise ValueError(f"Unknown provider: {provider}. Available: {list(cls.PROVIDERS.keys())}")
        
        adapter_class = cls.PROVIDERS[provider]
        
        if provider == "ollama":
            return adapter_class(
                model=kwargs.get("model", "llama3.2"),
                base_url=kwargs.get("base_url", "http://localhost:11434")
            )
        elif provider == "openai":
            return adapter_class(
                api_key=kwargs.get("api_key"),
                model=kwargs.get("model", "gpt-3.5-turbo")
            )
        elif provider == "kimi":
            return adapter_class(
                api_key=kwargs.get("api_key"),
                model=kwargs.get("model", "moonshot-v1-8k")
            )
        elif provider == "groq":
            return adapter_class(
                api_key=kwargs.get("api_key"),
                model=kwargs.get("model", "llama-3.1-8b-instant")
            )
