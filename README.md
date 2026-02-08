# Agent TC Generator - README

## 📖 What Is This Project?

This is a **Test Case Generator** that uses **Artificial Intelligence** to automatically create comprehensive test cases for software testing. Instead of writing test cases manually (which takes a lot of time), you simply describe what feature you want to test, upload a screenshot, or paste HTML code, and the AI writes detailed test cases for you.

**Examples:**
- **Text:** Type "User Login with Password" → AI generates 15-20 detailed test cases
- **Image:** Upload a UI screenshot → AI analyzes the interface and creates test cases
- **HTML:** Paste HTML code → AI tests all elements in the code

---

## 🎯 Who Is This For?

- **QA Engineers** who want to save time writing test cases
- **Software Testers** who need comprehensive test coverage quickly
- **Developers** who want to ensure their features are well-tested
- **Teams** who want consistent, well-structured test documentation

---

## 🏗️ How Does It Work? (Simple Explanation)

Think of this project like a **modern restaurant with multiple chefs**:

1. **You (Customer)** → Tell the waiter what you want (text, image, or HTML)
2. **Frontend (Waiter)** → Takes your order and shows it on a split-screen display
3. **Backend (Kitchen Manager)** → Receives the order and picks the right chef
4. **Choose Your Chef (AI Provider)**:
   - 👨‍🍳 **Local Chef (Ollama)** - Works in the back kitchen, no delivery fee
   - 👨‍🍳 **Gourmet Chef (OpenAI)** - World-famous, can look at your photos
   - 👨‍🍳 **Asian Chef (KIMI)** - Specializes in complex recipes
   - 👨‍🍳 **Speed Chef (Groq)** - Super fast, gets food ready in seconds
5. **Chef Cooks** → Prepares 15-20 dishes (test cases) based on your order
6. **Kitchen Manager** → Checks quality, packages for takeaway (Excel file)
7. **Waiter Serves** → Delivers the feast on a beautiful split-screen platter

---

## 📊 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER (You)                              │
│                                                                 │
│  Input Options:                                                │
│  📝 "Login with 2FA" | 🖼️ Screenshot | 📄 HTML Code           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ (1) Choose input type (Text/Image/HTML)
                             │     Pick your chef (Ollama/OpenAI/KIMI/Groq)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Web Browser)                       │
│                     Split-Screen Interface                      │
│                                                                 │
│  ┌─────────────────┐  ┌──────────────────────────────────────┐ │
│  │  INPUT (30%)    │  │  RESULTS (70%)                       │ │
│  │  • Text area    │  │  • Test Case Cards                   │ │
│  │  • Image upload │  │  • Download Excel button             │ │
│  │  • HTML editor  │  │                                      │ │
│  │  • Generate btn │  │                                      │ │
│  └─────────────────┘  └──────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ (2) Sends HTTP request to backend
                             │     POST /api/generate
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (Python Flask)                       │
│                         app.py                                  │
│                                                                 │
│  • Receives user request (text/image/html)                     │
│  • Validates input                                             │
│  • Routes to selected AI Adapter                               │
│  • Handles Excel export requests                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ (3) Calls selected AI Adapter
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              AI ADAPTER (Python) - Pick Your Chef!              │
│                   llm_adapter.py                                │
│                                                                 │
│  👨‍🍳 OllamaAdapter    - Local Llama 3.2 (Free, Private)         │
│  👨‍🍳 OpenAIAdapter    - GPT-3.5/4 (Vision, Powerful)            │
│  👨‍🍳 KimiAdapter      - Moonshot AI (Chinese-optimized)         │
│  👨‍🍳 GroqAdapter      - Llama 3.1 Instant (Ultra-fast)          │
│                                                                 │
│  • Creates smart prompt with image/HTML context                │
│  • Sends request to AI service                                 │
│  • Cleans up AI response (removes markdown, fixes JSON)        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ (4) AI generates 15-25 test cases
                             │     Covers: happy path, errors, security,
                             │     UI/UX, boundary cases, integrations
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AI SERVICE (Cloud or Local)                  │
│                                                                 │
│  • Analyzes your input (text/image/HTML)                       │
│  • Generates comprehensive test scenarios                      │
│  • Returns structured JSON response                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ (5) Returns to Backend
                             │     { "test_cases": [...] }
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (Python Flask)                       │
│                                                                 │
│  • Receives test cases from Adapter                            │
│  • Can export to Excel format                                  │
│  • Sends HTTP response to Frontend                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ (6) Sends response back
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Web Browser)                       │
│                                                                 │
│  • Displays test cases in beautiful cards                      │
│  • Shows: ID, Title, Description, Preconditions, Steps         │
│  • Offers 📥 Download Excel button                             │
└─────────────────────────────────────────────────────────────────┘
                             │
                             │ (7) User sees the results!
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         USER (You)                              │
│                                                                 │
│  ✅ TC_001: Verify Login with Valid Credentials                │
│  ✅ TC_002: Verify Login with Invalid Password                 │
│  ✅ TC_003: Verify Login with Empty Fields                     │
│  ✅ ... (15-25 comprehensive test cases!)                      │
│                                                                 │
│  📥 Download as Excel file                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🌟 Key Features

### **1. 📝 Multiple Input Types**
- **Text:** Describe your feature in plain English
- **Image:** Upload a UI screenshot (drag-drop, paste, or file picker)
- **HTML:** Paste code directly or upload HTML files

### **2. 🤖 Multiple AI Providers**
Choose the "chef" that fits your needs:

| Provider | Type | Best For | Image Support |
|----------|------|----------|---------------|
| **Ollama** | Local (Free) | Privacy, no internet needed | ❌ Text description only |
| **OpenAI** | Cloud | Best quality, vision capabilities | ✅ Yes (GPT-4 Vision) |
| **KIMI** | Cloud | Chinese language, fast responses | ❌ Text description only |
| **Groq** | Cloud | Ultra-fast inference | ❌ Text description only |

### **3. 🎨 Modern Split-Screen UI**
- **Left Side (30%):** Clean input area with tabs for Text/Image/HTML
- **Right Side (70%):** Spacious results area showing generated test cases
- **Responsive:** Works on desktop and mobile

### **4. 📊 Comprehensive Test Coverage**
Each generation produces **15-25 test cases** covering:
- ✅ Happy path (everything works correctly)
- ❌ Error cases (invalid inputs, failures)
- 🔒 Security tests (authentication, injection attacks)
- 🎨 UI/UX tests (responsiveness, accessibility)
- 📏 Boundary value tests (min/max values)
- 🔗 Integration scenarios

### **5. 📥 Excel Export**
Download your test cases as a professionally formatted Excel file with:
- Sheet 1: All test cases with proper formatting
- Sheet 2: Summary with metadata
- Leoforce branding and colors

---

## 🔧 Step-by-Step: What Happens When You Click "Generate"

### **Step 1: You Choose Your Input**
- Open the web page at `http://localhost:5000`
- Select a tab: **📝 Text**, **🖼️ Image**, or **📄 HTML**
- Provide your input (type description, upload image, or paste code)
- Click the **"Generate Test Cases"** button

### **Step 2: Frontend Sends Request**
- JavaScript collects your input
- For images: Converts to the right format for upload
- For HTML: Packages the code with any context
- Sends to the Backend via HTTP POST

### **Step 3: Backend Receives Request**
- Flask server (`app.py`) receives the request
- Checks which AI provider you selected
- Validates that API keys are provided if needed
- Calls the appropriate AI Adapter

### **Step 4: AI Adapter Creates Smart Prompt**
- The `llm_adapter.py` creates a detailed instruction for the AI
- Includes your input + context about images/HTML
- Explicitly tells the AI: "Generate 15-25 test cases minimum"
- Specifies coverage requirements (happy path, errors, security, etc.)

### **Step 5: AI Analyzes and Generates**
- **OpenAI with images:** Actually "sees" your screenshot and analyzes UI elements
- **Other providers:** Analyzes your text description + any HTML code
- Creates comprehensive test scenarios
- Formats output as structured JSON

### **Step 6: Adapter Cleans Response**
- Removes extra text like "Here are the test cases:"
- Uses regex to extract valid JSON
- Validates the structure

### **Step 7: Backend Sends Response**
- Receives clean test case data
- Adds metadata (provider used, has image, has HTML)
- Sends back to Frontend

### **Step 8: Frontend Displays Results**
- JavaScript receives the JSON data
- Creates beautiful **Test Case Cards** for each test case
- Shows provider badge and test case count
- Enables the **📥 Download Excel** button

### **Step 9: You See the Results!**
- Browse through 15-25 detailed test cases
- Each card shows: ID, Title, Description, Preconditions, Steps, Expected Result
- Click **Download Excel** to save as a file
- Total time: **5-30 seconds** (depending on provider)

---

## 📁 Project Structure (What Each File Does)

```
Agent_TC_Generator_using_Local_LLM/
│
├── frontend/                    # What the user sees
│   ├── index.html              # The web page with split-screen UI
│   └── leoforce_logo.png       # Company logo
│
├── backend/                     # The server (brain)
│   └── app.py                  # Flask server - handles requests & Excel export
│
├── tools/                       # Helper scripts
│   ├── llm_adapter.py          # Multi-provider AI adapter (Ollama/OpenAI/KIMI/Groq)
│   ├── excel_export.py         # Excel file generation
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
| **`frontend/index.html`** | The web page with modern split-screen design. Has tabs for Text/Image/HTML input, displays test cases in cards. |
| **`backend/app.py`** | The Python server. Receives requests, routes to AI providers, handles Excel export. |
| **`tools/llm_adapter.py`** | The "chef selector" - supports 4 different AI providers with unified interface. |
| **`tools/excel_export.py`** | Creates professionally formatted Excel files from test cases. |
| **`tools/test_ollama.py`** | A simple script to check if Ollama is running correctly. |
| **`gemini.md`** | The "rulebook" - defines data formats and behavioral rules. |
| **`requirements.txt`** | List of Python libraries needed (Flask, requests, openpyxl, etc.). |

---

## 🚀 How to Run This Project

### **Prerequisites (What You Need)**

1. **Python 3.8 or higher** installed on your computer
2. **At least one AI provider** configured:
   - **Ollama** (free, runs locally) - OR -
   - **OpenAI API key** (cloud) - OR -
   - **KIMI API key** (cloud) - OR -
   - **Groq API key** (cloud)

### **Option 1: Using Ollama (Free, Local)**

**Step 1: Install Ollama**
1. Download Ollama from: https://ollama.ai
2. Install it on your computer
3. Open a terminal and run:
   ```bash
   ollama pull llama3.2
   ```
   (This downloads the AI model - about 2GB)

**Step 2: Install Python Dependencies**
```bash
pip install -r requirements.txt
```

**Step 3: Start the Server**
```bash
python backend/app.py
```

**Step 4: Open the Web Page**
Go to: `http://localhost:5000`

---

### **Option 2: Using OpenAI (Cloud)**

**Step 1: Get API Key**
1. Go to https://platform.openai.com
2. Sign up and create an API key
3. Copy the key (starts with `sk-`)

**Step 2: Install Python Dependencies**
```bash
pip install -r requirements.txt
```

**Step 3: Start the Server**
```bash
python backend/app.py
```

**Step 4: Configure in UI**
1. Open `http://localhost:5000`
2. Click **⚙️ Settings**
3. Select **🤖 OpenAI**
4. Paste your API key
5. Click **Save Settings**

---

### **Option 3: Using Groq (Fast Cloud)**

**Step 1: Get API Key**
1. Go to https://console.groq.com
2. Sign up and create an API key
3. Copy the key (starts with `gsk_`)

**Step 2-4:** Same as OpenAI above, but select **⚡ Groq** in settings.

---

## 🧪 Example Test Case Output

**Input:** "User Login with Email and Password"

**Output:** 15-20 test cases including:

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

[... 13-18 more test cases covering security, UI/UX, 
     boundary cases, and integration scenarios ...]
```

---

## ❓ Troubleshooting (Common Problems)

### **Problem 1: "Connection failed" error**

**Cause:** Backend server is not running

**Solution:**
```bash
python backend/app.py
```

---

### **Problem 2: "Ollama API Error"**

**Cause:** Ollama is not running

**Solution:**
1. Check if Ollama is running:
   ```bash
   ollama list
   ```
2. If not, start Ollama (it usually runs automatically)
3. Make sure you pulled the model:
   ```bash
   ollama pull llama3.2
   ```

---

### **Problem 3: "Model 'llama3.2' not found"**

**Cause:** You haven't downloaded the AI model

**Solution:**
```bash
ollama pull llama3.2
```

---

### **Problem 4: Invalid API Key error (OpenAI/KIMI/Groq)**

**Cause:** API key is missing or incorrect

**Solution:**
1. Open the web app
2. Click **⚙️ Settings**
3. Select your provider
4. Enter a valid API key
5. Click **Save Settings**

---

### **Problem 5: Slow response (takes 30+ seconds)**

**Cause:** 
- Local LLM (Ollama) is processing on your computer
- Or using a slower cloud provider

**Solution:**
- This is normal for the first request with Ollama
- Switch to **Groq** in Settings for ultra-fast responses
- Subsequent requests will be faster

---

### **Problem 6: Images not being analyzed**

**Cause:** Most providers (Ollama, Groq, KIMI) cannot "see" images

**Solution:**
- **For OpenAI:** Make sure you're using GPT-4 Vision model
- **For other providers:** Describe the image in the text box below the upload area

---

## 🎓 Technical Details (For Developers)

### **Technologies Used**

- **Frontend:** HTML5, Vanilla JavaScript, CSS3
- **Backend:** Python 3.x, Flask
- **AI Providers:** 
  - Ollama (Local Llama 3.2)
  - OpenAI (GPT-3.5/4)
  - KIMI (Moonshot AI)
  - Groq (Llama 3.1 Instant)
- **Excel Export:** openpyxl
- **Design:** Leoforce Design Language 2.0

### **API Endpoints**

```
GET  /api/providers           → List available AI providers
POST /api/generate            → Generate test cases
     Request: { user_input, provider, api_key, html_code }
     or multipart/form-data with image
     
POST /api/export/excel        → Export to Excel
     Request: { test_cases, feature_name }
     Response: .xlsx file download
```

### **Data Flow**

1. User Input → Frontend (JavaScript)
2. Frontend → Backend (HTTP POST /api/generate)
3. Backend → AI Adapter (Python function call)
4. AI Adapter → AI Service (HTTP POST)
5. AI Service → AI Model (Inference)
6. AI Model → AI Service (JSON response)
7. AI Service → AI Adapter (HTTP response)
8. AI Adapter → Backend (Python return)
9. Backend → Frontend (HTTP response)
10. Frontend → User (Display + Excel export option)

---

## 📝 License

This project was built following the **B.L.A.S.T. protocol** (Blueprint, Link, Architect, Stylize, Trigger) for deterministic, self-healing automation.

---

## 🤝 Contributing

This is a learning project. Feel free to:
- Add new AI providers
- Improve the AI prompts
- Enhance the UI design
- Add more export formats (PDF, CSV, etc.)

---

## 📞 Support

If you have questions or issues:
1. Check the Troubleshooting section above
2. Review the `findings.md` file for technical details
3. Check `architecture/logic_sop.md` for prompt engineering details

---

**Built with ❤️ using AI - Multiple providers, Maximum flexibility!**
