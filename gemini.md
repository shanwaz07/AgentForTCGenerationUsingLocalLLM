# Project Constitution (gemini.md)

## Data Schemas

### Core Domain: Test Case Generation

**1. Input Payload (User Request)**
```json
{
  "request_id": "uuid",
  "user_input": "string (The feature description or requirement)",
  "template_id": "string (default: 'standard_v1')"
}
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
  "test_cases": [
    { "id": "TC_001", ... },
    { "id": "TC_002", ... }
  ]
}
```

## Behavioral Rules
1.  **Protocol Adherence**: Strictly follow B.L.A.S.T. and A.N.T. protocols.
2.  **Data-First**: Define schemas before building tools.
3.  **Self-Annealing**: Analyze -> Patch -> Test -> Update Architecture.
4.  **No Guessing**: Probability is for LLMs; Logic is for Code.
5.  **Ollama Interaction**:
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
