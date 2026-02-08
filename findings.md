# Findings

## Research
- **Ollama API Documentation**: Confirmed that Llama 3.2 supports `format='json'` parameter for structured output.
- **Flask-CORS**: Required for local development to allow frontend-backend communication.

## Discoveries
- **JSON Mode**: Llama 3.2 has native JSON formatting support via the `format` parameter in the API call, reducing the need for extensive regex parsing.
- **Regex Fallback**: Even with `format='json'`, occasional markdown wrapping (```json...```) occurs, necessitating a cleanup function.
- **Model Availability**: User had `mistral:latest` already installed; `llama3.2` was pulled successfully (2.0 GB download).
- **Connection Handling**: Ollama runs on port 11434 by default; connection errors are gracefully handled with try-catch blocks.

## Constraints
- **Reliability > Speed**: Per B.L.A.S.T. protocol.
- **No guessing at business logic**: All schemas defined upfront.
- **Data-First**: Schema must be defined before coding.
- **Environment**: Windows OS, PowerShell terminal.
- **Local LLM Only**: No external API dependencies (OpenAI, etc.).

## Technical Learnings
- **Flask Development Server**: Runs with auto-reload in debug mode; not suitable for production.
- **CORS Requirements**: Needed when frontend and backend run on same localhost but different origins.
- **Prompt Engineering**: Explicit schema enforcement in prompts significantly improves JSON compliance.

## Multi-Provider LLM Support (Added 2026-02-08)
- **Architecture**: Created `tools/llm_adapter.py` with abstract base class and provider-specific adapters
- **Providers Supported**: 
  - Ollama (Local LLM) - default, no API key required
  - OpenAI (GPT models) - requires API key
  - KIMI/Moonshot AI - requires API key
  - Groq (Fast inference) - requires API key, added 2026-02-08
- **Frontend Storage**: API keys stored in browser localStorage (client-side only)
- **Error Handling**: Provider-specific error messages for invalid keys, rate limits, server errors
- **Security Note**: API keys are sent in request headers; for production, consider proxy pattern
- **Endpoint**: `GET /api/providers` returns available providers with metadata

## Groq Provider Added (Added 2026-02-08)
- **New Provider**: Groq (groq.com) - Ultra-fast LLM inference
- **Model**: Uses Llama 3.1 8B Instant by default
- **API URL**: `https://api.groq.com/openai/v1/chat/completions`
- **Features**: Fast inference, competitive pricing
- **API Key**: Get from console.groq.com (starts with `gsk_`)
- **Limitations**: Cannot analyze images directly (text-only)

## Unit Testing - Gmail Login Page (Added 2026-02-08)
- **Test Suite Generated**: 20 comprehensive test cases for Gmail login functionality
- **Categories Covered**:
  - Functional Tests (7): Valid/invalid credentials, Remember Me, Forgot Password
  - Security Tests (6): 2FA flow, SQL injection, XSS, email validation
  - Account Security (2): Password visibility, account lockout
  - UI/UX Tests (2): Mobile responsive, Create Account link
  - Session Tests (3): Back button, recovery email, session timeout
- **Output Files**: 
  - `.tmp/gmail_login_test_cases.json` - Machine-readable JSON format
  - `.tmp/gmail_login_test_cases.md` - Human-readable markdown format
- **Note**: Generated without LLM due to slow local response; based on standard QA test patterns

## Enhanced Test Case Generation (Added 2026-02-08)
- **Issue Fixed**: LLM was generating only 5 test cases due to ambiguous prompt
- **Solution**: Updated prompt in `tools/llm_adapter.py` to explicitly request 10-20 test cases minimum
- **Prompt Improvements**:
  - Explicit instruction: "Generate 10-20 test cases MINIMUM - be thorough"
  - Comprehensive coverage requirements (happy path, errors, security, UI/UX, boundaries)
  - Detailed steps requirement (3-5 steps per test case)
  - Increased max_tokens to 4000 for OpenAI/KIMI to accommodate more test cases

## Multi-Modal Input Support (Added 2026-02-08)
- **Image Upload Support**:
  - File picker with click-to-upload
  - Drag and drop functionality
  - Copy-paste image support (Ctrl+V)
  - Image preview with remove option
  - Max file size: 10MB
  - Supported formats: PNG, JPG, GIF
- **HTML Code Input**:
  - Textarea for direct HTML code paste
  - File upload for .html, .htm, .txt files
  - Syntax-highlighted input area (monospace font)
- **Backend Updates**:
  - Modified `/api/generate` to accept multipart/form-data
  - Image processing (base64 encoding)
  - HTML code extraction and processing
  - Enhanced adapter to include image/HTML context in prompts

## Excel Export Feature (Added 2026-02-08)
- **New Dependency**: `openpyxl` for Excel file generation
- **New Endpoint**: `POST /api/export/excel` - Exports test cases to .xlsx format
- **Frontend Updates**:
  - Download button appears in results header after test case generation
  - Button is green (success color) with 📥 icon
  - Auto-generates filename from feature description + timestamp
- **Excel File Structure**:
  - Sheet 1 "Test Cases": All test cases with formatted columns (ID, Title, Description, Preconditions, Steps, Expected Result)
  - Sheet 2 "Summary": Feature name, total count, generation metadata
  - Professional styling with Leoforce brand colors (#3E3D6D header)
  - Auto-adjusted column widths and row heights
  - Borders and alignment for readability

## Bug Fixes: Image & HTML Processing (Added 2026-02-08)
- **Issue Identified**: Image and HTML uploads were not being considered by the LLM
- **Root Causes**:
  1. Frontend was using `fetch()` on data URLs which doesn't work reliably
  2. Prompt didn't explicitly instruct the LLM to analyze image/HTML content
  3. No user feedback about Local LLM limitations with images
- **Fixes Applied**:
  1. **Frontend**: Fixed base64 to blob conversion using `atob()` and `Uint8Array`
  2. **Prompt**: Completely rewritten to explicitly demand analysis of provided content with CRITICAL INSTRUCTIONS sections
  3. **UI**: Added info box in image section warning that Ollama cannot analyze images; requires description
  4. **Adapter**: Added console logging to trace data flow; increased prompt specificity
  5. **OpenAI**: Added support for GPT-4 Vision models to actually process images
