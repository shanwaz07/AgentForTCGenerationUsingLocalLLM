# Logic SOP: Test Case Generation

## Goal
Generate structured Test Cases (JSON) from unstructured User Input using Ollama (Llama 3.2).

## Prompt Strategy
The prompt must always:
1.  Assign Persona: QA Automation Expert.
2.  Provide Input: The user's feature description.
3.  Enforce Schema: Explicitly request JSON format matching `gemini.md` schema.
4.  Forbid conversational filler ("Here is the JSON...").

## Template
```text
You are a Senior QA Automation Engineer.
Your task is to generate comprehensive test cases for the following feature/requirement:

"{user_input}"

Output MUST be a valid JSON object matching this schema:
{{
  "test_cases": [
    {{
      "id": "TC_XXX",
      "title": "Concise Title",
      "description": "What is being tested",
      "preconditions": "Setup required",
      "steps": ["Step 1", "Step 2"],
      "expected_result": "Success criteria"
    }}
  ]
}}

RETURN ONLY JSON. NO MARKDOWN. NO COMMENTS.
```

## Error Handling

### 1. JSONDecodeError (Parsing Failures)
**Symptom**: LLM returns markdown-wrapped JSON or conversational text.

**Self-Annealing Strategy**:
- **Primary**: Use `format='json'` parameter in Ollama API call (Llama 3.2 native support).
- **Fallback Layer 1**: Regex extraction for markdown blocks: `r'```json\s*(\{.*?\})\s*```'`
- **Fallback Layer 2**: Extract any valid JSON structure: `r'\{.*\}'`
- **Failure Response**: Return `{"error": "Failed to parse LLM output as JSON", "raw_output": text}`

**Learning**: Even with `format='json'`, occasional wrapping occurs. Always implement defensive parsing.

### 2. ConnectionError (Ollama Unavailable)
**Symptom**: `requests.exceptions.ConnectionError` when calling `http://localhost:11434`.

**Self-Annealing Strategy**:
- Catch exception in `ollama_adapter.py`
- Return structured error: `{"error": "Ollama API Error: [details]"}`
- Backend returns HTTP 500 with error payload
- Frontend displays user-friendly message: "Connection failed. Is Ollama running?"

**Prevention**: Always run `ollama list` verification before starting the server.

### 3. Timeout Handling
**Current**: No explicit timeout set (uses requests default).

**Recommendation**: Add `timeout=60` to `requests.post()` call for long-running inference.

### 4. Model Not Found (404)
**Symptom**: HTTP 404 from Ollama API.

**Self-Annealing Strategy**:
- Check `response.status_code == 404`
- Return error: "Model 'llama3.2' not found. Please run 'ollama pull llama3.2'"
- Log to `findings.md` if this occurs in production

## Maintenance Notes
- **Last Updated**: 2026-01-29
- **Error Count**: 0 (No production errors logged yet)
- **Next Review**: After first 100 test case generations
