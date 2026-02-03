# DeepStack Validator 🛡️

**An Intelligent, LLM-Powered Semantic Data Validation Engine.**

DeepStack Validator is a Python-based tool that uses Large Language Models (Llama 3 via Groq) to perform advanced data validation. Unlike traditional Regex validators, this engine understands context, allowing it to distinguish between harmless data, logic warnings, and active security threats like SQL Injection.

This project demonstrates a professional AI Engineering workflow, including **Few-Shot Prompting**, **Chain-of-Thought reasoning**, **Automated Regression Testing**, and a **Full-Stack Interactive UI**.

## 🚀 Key Features

* **Semantic Validation:** Goes beyond syntax to understand data context (e.g., flagging illogical ages without breaking the application).
* **Security Guardrails:** Proactively identifies and blocks Prompt Injection and SQL Injection attempts disguised as user input.
* **Interactive Dashboard:** A user-friendly web interface (Streamlit) for real-time validation and visual feedback.
* **Structured Output:** Returns strictly formatted JSON separating critical `errors` from soft `warnings`.
* **Automated Regression Testing:** Integrated with **Promptfoo** to run deterministic evaluation suites, ensuring the LLM behaves consistently.

---

## 🛠️ Prerequisites

Before running the project, ensure you have the following installed:

* **Python 3.8+**
* **Node.js & NPM** (Required for running the evaluation suite)
* **Groq API Key** (You can get one from the [Groq Console](https://console.groq.com/))

---

## 📦 Installation & Setup

Follow these steps to set up the project locally.

### 1. Clone the Repository
```bash
git clone [https://github.com/Gaikwad1508/deepstack-validator.git](https://github.com/Gaikwad1508/deepstack-validator.git)
cd deepstack-validator

```

### 2. Set up the Python Virtual Environment

It is recommended to use a virtual environment to keep dependencies clean.

**For Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\activate

```

**For Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Configure Environment Variables

This project uses `python-dotenv` to manage secrets securely.

1. Create a new file named `.env` in the root directory.
2. Add your API Key to it:
```ini
GROQ_API_KEY=gsk_your_actual_api_key_here

```


*(Note: The .env file is git-ignored to prevent leaking your keys.)*

---

## 🏃‍♂️ Usage

### 1. Run the Interactive Web UI (Recommended)

To launch the user-friendly web dashboard for real-time testing:

```bash
streamlit run app.py

```

*This will open a local web server (usually at http://localhost:8501) where you can interactively test user profiles.*

### 2. Run the Python Validator (CLI)

To validate a user profile via the command line against the AI rules:

```bash
python validate_user.py user.json

```

**Example Output:**

```json
{
  "is_valid": true,
  "errors": [],
  "warnings": [
    "Age is under 18"
  ]
}

```

### 3. Run the Regression Test Suite (Evals)

This project includes a comprehensive test suite using `promptfoo` to ensure the LLM handles edge cases correctly.

We have included a custom test runner script that automatically handles API key injection for Windows/Linux environments.

**Run the tests with:**

```bash
node run_tests.js

```

**What this tests:**

* ✅ **Valid User:** Ensures standard data passes.
* ✅ **Invalid Email:** Ensures bad syntax is caught as an Error.
* ✅ **Edge Case (Age 17):** Ensures logical warnings do not block validation.
* ✅ **Security Test:** Ensures SQL Injection attempts are detected and handled safely.

**Expected Result:** `Successes: 4 / Failures: 0`

---

## 🧪 Project Structure

* **`app.py`**: The Streamlit-based interactive web dashboard.
* **`validate_user.py`**: The main Python script logic that connects to the LLM.
* **`run_tests.js`**: Custom Node.js script to execute regression tests securely across different OS environments.
* **`promptfooconfig.yaml`**: Configuration for the regression testing suite.
* **`user.json`**: Sample JSON data file used for testing.
* **`requirements.txt`**: List of Python dependencies (`openai`, `streamlit`, `python-dotenv`, etc.).
* **`.env`**: Local file for storing API keys (Excluded from GitHub).
* **`.gitignore`**: Ensures system files (like `venv/`) and secrets are not uploaded.

## 🛡️ Security Note

This project adheres to security best practices:

1. **No Hardcoded Keys:** API keys are loaded strictly from environment variables.
2. **Input Sanitization:** The Validator creates a buffer between raw user input and your database.
3. **Prompt Safety:** The system instructions explicitly handle potential injection attacks.

```

```