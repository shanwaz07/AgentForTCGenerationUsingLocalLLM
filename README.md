# Agent TC Generator - README

## 📖 What Is This Project?

This is a **Test Case Generator** that uses **Artificial Intelligence** to automatically create test cases for software testing. Instead of writing test cases manually (which takes a lot of time), you simply describe what feature you want to test, and the AI writes the test cases for you.

**Example:**
- You type: "User Login with Password"
- AI generates: 5-10 detailed test cases covering different scenarios (valid login, wrong password, empty fields, etc.)

---

## 🎯 Who Is This For?

- **QA Engineers** who want to save time writing test cases
- **Software Testers** who need comprehensive test coverage quickly
- **Teams** who want consistent, well-structured test documentation

---

## 🏗️ How Does It Work? (Simple Explanation)

Think of this project like a **restaurant**:

1. **You (Customer)** → Tell the waiter what you want
2. **Frontend (Waiter)** → Takes your order and sends it to the kitchen
3. **Backend (Kitchen Manager)** → Receives the order and asks the chef to cook
4. **Ollama + Llama 3.2 (Chef)** → Prepares the food (generates test cases)
5. **Backend (Kitchen Manager)** → Checks the food quality and sends it back
6. **Frontend (Waiter)** → Delivers the finished dish to you

---

## 📊 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER (You)                              │
│                                                                 │
│  "I want test cases for User Login with 2FA"                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ (1) User types feature description
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Web Browser)                       │
│                     index.html + JavaScript                     │
│                                                                 │
│  • Beautiful Leoforce-branded interface                        │
│  • Input box for feature description                           │
│  • Display area for test cases                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ (2) Sends HTTP request to backend
                             │     POST /api/generate
                             │     { "user_input": "User Login..." }
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (Python Flask)                       │
│                         app.py                                  │
│                                                                 │
│  • Receives user request                                       │
│  • Validates input                                             │
│  • Calls Ollama Adapter                                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ (3) Calls Ollama Adapter
                             │     generate_test_cases("User Login...")
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   OLLAMA ADAPTER (Python)                       │
│                    ollama_adapter.py                            │
│                                                                 │
│  • Creates a smart prompt for the AI                           │
│  • Sends request to Ollama API                                 │
│  • Cleans up AI response (removes markdown, fixes JSON)        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ (4) Sends prompt to Ollama
                             │     "You are a QA Engineer. Generate
                             │      test cases for: User Login..."
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OLLAMA (Local AI Server)                     │
│                    Running on port 11434                        │
│                                                                 │
│  • Runs Llama 3.2 AI model locally on your computer           │
│  • Generates intelligent test cases                            │
│  • Returns JSON response                                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ (5) Returns generated test cases
                             │     { "test_cases": [...] }
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   OLLAMA ADAPTER (Python)                       │
│                                                                 │
│  • Validates JSON format                                       │
│  • Fixes any formatting issues                                 │
│  • Returns clean data                                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ (6) Returns to Backend
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (Python Flask)                       │
│                                                                 │
│  • Receives test cases from Adapter                            │
│  • Sends HTTP response to Frontend                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ (7) Sends response back
                             │     { "test_cases": [...] }
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Web Browser)                       │
│                                                                 │
│  • Receives test cases                                         │
│  • Displays them in beautiful cards                            │
│  • Shows: ID, Title, Steps, Expected Result                    │
└─────────────────────────────────────────────────────────────────┘
                             │
                             │ (8) User sees the results!
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         USER (You)                              │
│                                                                 │
│  ✅ TC_001: Verify Login with Valid Credentials                │
│  ✅ TC_002: Verify Login with Invalid Password                 │
│  ✅ TC_003: Verify Login with Empty Fields                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Step-by-Step: What Happens When You Click "Generate"

### **Step 1: You Type Your Request**
- You open the web page at `http://localhost:5000`
- You type something like: **"User Login with Email and Password"**
- You click the **"Generate Test Cases"** button

### **Step 2: Frontend Sends Request**
- The JavaScript code in `index.html` takes your text
- It creates a package (JSON) that looks like this:
  ```json
  {
    "user_input": "User Login with Email and Password"
  }
  ```
- It sends this package to the Backend using HTTP POST

### **Step 3: Backend Receives Request**
- The Flask server (`app.py`) is listening on port 5000
- It receives your request at the `/api/generate` endpoint
- It checks: "Did the user actually type something?" (validation)
- If yes, it calls the Ollama Adapter

### **Step 4: Ollama Adapter Creates Smart Prompt**
- The `ollama_adapter.py` file creates a special instruction for the AI
- It tells the AI: "You are a Senior QA Engineer. Generate test cases for this feature..."
- It also tells the AI: "Return your answer in JSON format only, no extra text"

### **Step 5: Request Goes to Ollama**
- Ollama is a program running on your computer (port 11434)
- It's like having ChatGPT, but running locally
- Ollama loads the **Llama 3.2** AI model (2GB file)
- The AI "thinks" about your request and generates test cases

### **Step 6: AI Generates Test Cases**
- Llama 3.2 analyzes your feature description
- It creates multiple test cases covering:
  - ✅ Happy path (everything works)
  - ❌ Error cases (wrong password, empty fields)
  - 🔒 Security cases (SQL injection, etc.)
- It formats everything as JSON

### **Step 7: Ollama Adapter Cleans Response**
- Sometimes the AI adds extra text like "Here are the test cases:"
- The Adapter removes this extra text
- It uses **regex** (pattern matching) to extract only the JSON part
- It validates: "Is this valid JSON? Can we use it?"

### **Step 8: Backend Sends Response**
- The Backend receives the clean JSON from the Adapter
- It sends it back to the Frontend as an HTTP response

### **Step 9: Frontend Displays Results**
- JavaScript receives the JSON data
- It creates beautiful **Test Case Cards** for each test case
- Each card shows:
  - **ID**: TC_001, TC_002, etc.
  - **Title**: "Verify Login with Valid Credentials"
  - **Description**: What is being tested
  - **Preconditions**: Setup needed
  - **Steps**: 1, 2, 3... (ordered list)
  - **Expected Result**: What should happen

### **Step 10: You See the Results!**
- The test cases appear on your screen
- You can read them, copy them, or use them in your testing
- Total time: **5-15 seconds** (depending on your computer)

---

## 📁 Project Structure (What Each File Does)

```
Agent_TC_Generator_using_Local_LLM/
│
├── frontend/                    # What the user sees
│   ├── index.html              # The web page (UI)
│   └── leoforce_logo.png       # Company logo
│
├── backend/                     # The server (brain)
│   └── app.py                  # Flask server - handles requests
│
├── tools/                       # Helper scripts
│   ├── ollama_adapter.py       # Talks to Ollama AI
│   └── test_ollama.py          # Tests if Ollama is working
│
├── architecture/                # Documentation
│   └── logic_sop.md            # How the prompt works
│
├── .tmp/                        # Temporary files (can be deleted)
│
├── gemini.md                    # Project rules and data format
├── task_plan.md                 # What we built and why
├── findings.md                  # Technical discoveries
├── progress.md                  # Build history
├── BLAST.md                     # Development protocol
├── requirements.txt             # Python packages needed
└── README.md                    # This file!
```

### **File Explanations (Simple Language)**

| File | What It Does |
|------|--------------|
| **`frontend/index.html`** | The web page you see in your browser. Has input box, buttons, and displays test cases. |
| **`backend/app.py`** | The Python server. Receives requests from the web page and sends them to Ollama. |
| **`tools/ollama_adapter.py`** | The "translator" between our app and the AI. Creates smart prompts and cleans responses. |
| **`tools/test_ollama.py`** | A simple script to check if Ollama is running correctly. |
| **`gemini.md`** | The "rulebook" - defines what format test cases should have. |
| **`requirements.txt`** | List of Python libraries needed (Flask, requests, etc.). |

---

## 🚀 How to Run This Project

### **Prerequisites (What You Need)**

1. **Python 3.8 or higher** installed on your computer
2. **Ollama** installed and running
3. **Llama 3.2 model** downloaded in Ollama

### **Step 1: Install Ollama**

1. Download Ollama from: https://ollama.ai
2. Install it on your computer
3. Open a terminal and run:
   ```bash
   ollama pull llama3.2
   ```
   (This downloads the AI model - about 2GB)

### **Step 2: Install Python Dependencies**

Open a terminal in the project folder and run:
```bash
pip install -r requirements.txt
```

This installs:
- **Flask** (web server)
- **Flask-CORS** (allows frontend to talk to backend)
- **requests** (makes HTTP calls to Ollama)

### **Step 3: Start the Server**

Run this command:
```bash
python backend/app.py
```

You should see:
```
Starting Flask Server on port 5000...
* Running on http://127.0.0.1:5000
```

### **Step 4: Open the Web Page**

1. Open your web browser
2. Go to: `http://localhost:5000`
3. You should see the Leoforce-branded interface

### **Step 5: Generate Test Cases!**

1. Type a feature description (e.g., "Shopping Cart Checkout")
2. Click "Generate Test Cases"
3. Wait 5-15 seconds
4. See your test cases appear!

---

## 🧪 Example Test Case Output

**Input:** "User Login with Email and Password"

**Output:**

```
┌─────────────────────────────────────────────────────────┐
│ TC_001: Verify Login with Valid Credentials            │
├─────────────────────────────────────────────────────────┤
│ Description: Ensure user can login with correct email  │
│              and password                               │
│                                                         │
│ Preconditions: User has a registered account           │
│                                                         │
│ Steps:                                                  │
│   1. Navigate to login page                            │
│   2. Enter valid email address                         │
│   3. Enter correct password                            │
│   4. Click "Login" button                              │
│                                                         │
│ Expected Result: User is redirected to dashboard       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ TC_002: Verify Login with Invalid Password             │
├─────────────────────────────────────────────────────────┤
│ Description: Ensure system rejects wrong password      │
│                                                         │
│ Preconditions: User has a registered account           │
│                                                         │
│ Steps:                                                  │
│   1. Navigate to login page                            │
│   2. Enter valid email address                         │
│   3. Enter incorrect password                          │
│   4. Click "Login" button                              │
│                                                         │
│ Expected Result: Error message "Invalid credentials"   │
└─────────────────────────────────────────────────────────┘
```

---

## ❓ Troubleshooting (Common Problems)

### **Problem 1: "Connection failed" error**

**Cause:** Backend server is not running

**Solution:**
```bash
python backend/app.py
```

### **Problem 2: "Ollama API Error"**

**Cause:** Ollama is not running

**Solution:**
1. Open a new terminal
2. Check if Ollama is running:
   ```bash
   ollama list
   ```
3. If not, start Ollama (it usually runs automatically)

### **Problem 3: "Model 'llama3.2' not found"**

**Cause:** You haven't downloaded the AI model

**Solution:**
```bash
ollama pull llama3.2
```

### **Problem 4: Slow response (takes 30+ seconds)**

**Cause:** Your computer is processing the AI model

**Solution:**
- This is normal for the first request
- Subsequent requests will be faster
- Consider using a smaller model if your computer is slow

---

## 🎓 Technical Details (For Developers)

### **Technologies Used**

- **Frontend:** HTML5, Vanilla JavaScript, CSS3
- **Backend:** Python 3.x, Flask
- **AI:** Ollama (Llama 3.2 model)
- **Design:** Leoforce Design Language 2.0

### **API Endpoint**

```
POST http://localhost:5000/api/generate
Content-Type: application/json

Request Body:
{
  "user_input": "Feature description here"
}

Response:
{
  "test_cases": [
    {
      "id": "TC_001",
      "title": "Test title",
      "description": "What is tested",
      "preconditions": "Setup needed",
      "steps": ["Step 1", "Step 2"],
      "expected_result": "Expected outcome"
    }
  ]
}
```

### **Data Flow**

1. User Input → Frontend (JavaScript)
2. Frontend → Backend (HTTP POST)
3. Backend → Ollama Adapter (Python function call)
4. Ollama Adapter → Ollama API (HTTP POST to port 11434)
5. Ollama API → Llama 3.2 Model (AI inference)
6. Llama 3.2 → Ollama API (JSON response)
7. Ollama API → Ollama Adapter (HTTP response)
8. Ollama Adapter → Backend (Python return)
9. Backend → Frontend (HTTP response)
10. Frontend → User (Display test cases)

---

## 📝 License

This project was built following the **B.L.A.S.T. protocol** (Blueprint, Link, Architect, Stylize, Trigger) for deterministic, self-healing automation.

---

## 🤝 Contributing

This is a learning project. Feel free to:
- Add new features
- Improve the AI prompts
- Enhance the UI design
- Add export functionality (CSV, Excel, etc.)

---

## 📞 Support

If you have questions or issues:
1. Check the Troubleshooting section above
2. Review the `findings.md` file for technical details
3. Check `architecture/logic_sop.md` for prompt engineering details

---

**Built with ❤️ using Local AI (No internet required!)**
