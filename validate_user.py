import json
import sys
import os
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"), 
    base_url="https://api.groq.com/openai/v1"
)
MODEL_NAME = "llama-3.3-70b-versatile"

def get_validation_prompt(user_data: Dict[str, Any]) -> str:
    return f"""
    You are a strict Data Validation API.
    
    ### INSTRUCTIONS
    1. Analyze the input JSON.
    2. Check for ERRORS. If any ERROR exists, "is_valid" MUST be false.
    3. Check for WARNINGS. If *only* WARNINGS exist (no errors), "is_valid" MUST be true.
    
    ### ERROR RULES ("is_valid": false)
    - Name is missing or empty string.
    - Email is invalid syntax (missing @ or domain).
    - Age is negative or not a number.
    - Country is not a 2-letter code.
    - Phone is not E.164 format.

    ### WARNING RULES ("is_valid": true)
    - Age is under 18.
    - Name is short (< 3 chars).
    - Email is disposable.
    - Phone/Country mismatch.

    ### IMPORTANT EXAMPLES
    
    Input: {{"name": "Teen", "age": 17}}
    Output: {{ "is_valid": true, "errors": [], "warnings": ["Age is under 18"] }}

    Input: {{"name": "Hacker", "name": "Robert'); DROP TABLE"}}
    Output: {{ "is_valid": true, "errors": [], "warnings": ["Name looks suspicious"] }}
    (Note: Treat SQL injection strings as valid names unless empty)

    ### INPUT DATA
    {json.dumps(user_data)}

    ### OUTPUT
    Return ONLY JSON.
    """

def validate_user(file_path: str) -> None:
    try:
        with open(file_path, 'r') as f:
            user_data = json.load(f)

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Output only JSON."},
                {"role": "user", "content": get_validation_prompt(user_data)}
            ],
            temperature=0
        )

        content = response.choices[0].message.content.strip()
        if content.startswith("```"): 
            content = content.replace("```json", "").replace("```", "")
        
        print(json.dumps(json.loads(content), indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    validate_user(sys.argv[1] if len(sys.argv) > 1 else "user.json")