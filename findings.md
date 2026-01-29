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
