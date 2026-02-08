# Project Constitution (gemini.md)

## Data Schemas

### Core Domain: Test Case Generation

**1. Input Payload (User Request)**

*JSON Format (Text Only):*
```json
{
  "request_id": "uuid",
  "user_input": "string (The feature description or requirement)",
  "template_id": "string (default: 'standard_v1')",
  "provider": "string (default: 'ollama', options: 'ollama', 'openai', 'kimi')",
  "api_key": "string (required for 'openai' and 'kimi' providers)",
  "html_code": "string (optional HTML code for component testing)"
}
```

*Multipart Form Data (With Files):*
```
Content-Type: multipart/form-data

Fields:
- user_input: string
- provider: string
- api_key: string
- html_code: string (optional)
- image: File (optional, image file)
- html_file: File (optional, .html/.htm/.txt file)
```
```

**2. Test Case Structure (Internal Model)**
```json
{
  "id": "TC_001",
  "title": "Verify Login with Valid Credentials",
  "description": "Ensure user can access the dashboard with correct username and password.",
  "preconditions": "User is on the login page.",
  "steps": [
    "Enter valid username",
    "Enter valid password",
    "Click Login button"
  ],
  "expected_result": "User is redirected to Dashboard."
}
```

**3. Output Payload (API Response)**
```json
{
  "generated_at": "timestamp",
  "model_used": "llama3.2",
  "provider_used": "ollama",
  "has_image": false,
  "has_html": false,
  "test_cases": [
    { "id": "TC_001", ... },
    { "id": "TC_002", ... }
  ]
}
```

*Note:* Minimum 10 test cases expected, maximum depends on complexity (typically 10-20).

**4. Provider List Endpoint**
```json
{
  "providers": [
    {
      "id": "ollama",
      "name": "Local LLM (Ollama)",
      "description": "Run models locally using Ollama",
      "requires_api_key": false,
      "default": true
    }
  ]
}
```

**5. Excel Export Endpoint**
```http
POST /api/export/excel
Content-Type: application/json

Request Body:
{
  "test_cases": [...],
  "feature_name": "User_Login"
}

Response: Binary Excel file (.xlsx)
```
```

## Behavioral Rules
1.  **Protocol Adherence**: Strictly follow B.L.A.S.T. and A.N.T. protocols.
2.  **Data-First**: Define schemas before building tools.
3.  **Self-Annealing**: Analyze -> Patch -> Test -> Update Architecture.
4.  **No Guessing**: Probability is for LLMs; Logic is for Code.
5.  **Multi-Provider LLM Support**:
    *   Must support Ollama (default), OpenAI, KIMI, and Groq providers.
    *   API keys for cloud providers must be stored client-side (localStorage).
    *   Provider selection must be persisted across sessions.
    *   Error messages must be provider-specific (invalid key, rate limit, etc.).
6.  **Ollama Interaction**:
    *   Must use `llama3.2` model.
    *   Must enforce JSON formatting in LLM output (if model supports it) or robust parsing.
    *   Failure to connect to Ollama must be handled gracefully.

## Architectural Invariants
1.  **Layer 1 (Architecture)**: SOPs in Markdown.
2.  **Layer 2 (Navigation)**: Python Backend (FastAPI/Flask) acting as the controller.
3.  **Layer 3 (Tools)**:
    *   `ollama_client.py`: Handles raw communication with Ollama.
    *   `parser.py`: Validates and cleans LLM output.
4.  **Frontend**: Simple HTML/JS Chat Interface (Vanilla JS + CSS).
5.  **State Management**: `gemini.md` is Law; Planning files are Memory.
6.  **Intermediate Storage**: Use `.tmp/` for ephemeral files.
