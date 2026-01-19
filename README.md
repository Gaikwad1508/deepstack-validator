# DeepStack Validator 🛡️

**An Intelligent, LLM-Powered Semantic Data Validation Engine.**

DeepStack Validator is a Python-based tool that uses Large Language Models (Llama 3 via Groq) to perform advanced data validation. Unlike traditional Regex validators, this engine understands context, allowing it to distinguish between harmless data, logic warnings, and active security threats like SQL Injection.

This project demonstrates a professional AI Engineering workflow, including **Few-Shot Prompting**, **Chain-of-Thought reasoning**, and **Automated Regression Testing**.

## 🚀 Key Features

* **Semantic Validation:** Goes beyond syntax to understand data context (e.g., flagging illogical ages without breaking the application).
* **Security Guardrails:** Proactively identifies and blocks Prompt Injection and SQL Injection attempts disguised as user input.
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

For Windows (PowerShell):

```bash
python -m venv venv
.\venv\Scripts\activate
```

For Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
This project uses python-dotenv to manage secrets securely.

1. Create a new file named .env in the root directory.

2. Add your API Key to it:

```bash
GROQ_API_KEY=gsk_your_actual_api_key_here
```

(Note: The .env file is git-ignored to prevent leaking your keys.)

## 🏃‍♂️ Usage
### 1. Run the Python Validator
To validate a user profile against the AI rules, run the Python script passing the input JSON file.

```bash
python validate_user.py user.json
```

### Example Output: 
The script will output a clean JSON response.

```bash

{
  "is_valid": true,
  "errors": [],
  "warnings": [
    "Age is under 18"
  ]
}
```

### 2. Run the Regression Test Suite (Evals)
This project includes a comprehensive test suite using promptfoo to ensure the LLM handles edge cases correctly.

Run the tests with the following command:

```bash

npx promptfoo@0.60.0 eval --no-cache
```

#### What this tests:

✅ Valid User: Ensures standard data passes.

✅ Invalid Email: Ensures bad syntax is caught as an Error.

✅ Edge Case (Age 17): Ensures logical warnings do not block validation.

✅ Security Test: Ensures SQL Injection attempts are detected and handled safely.

### Expected Result:
```bash
Successes: 4
Failures: 0
```

## 🧪 Project Structure
* validate_user.py: The main Python script. It loads the environment variables, constructs the Few-Shot prompt, and queries the Groq API.

* promptfooconfig.yaml: The configuration file for the regression testing suite. It defines the prompts and test cases.

* user.json / test_input.json: Sample JSON data files used for testing.

* requirements.txt: List of Python dependencies (openai, python-dotenv, etc.).

* .env: Local file for storing API keys (Excluded from GitHub).

* .gitignore: Ensures system files and secrets are not uploaded.

## 🛡️ Security Note
* This project adheres to security best practices:

* No Hardcoded Keys: API keys are loaded strictly from environment variables.

* Input Sanitization: The Validator creates a buffer between raw user input and your database.