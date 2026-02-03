import streamlit as st
import json
import os
from dotenv import load_dotenv
from validate_user import get_validation_prompt, client, MODEL_NAME

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(page_title="DeepStack Validator", page_icon="🛡️", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("🛡️ DeepStack AI Validator")
st.markdown("### Intelligent Semantic Data Validation Engine")
st.markdown("Enter user details below to check for **Logical Errors**, **Security Threats**, and **Data Consistency**.")

# Form
with st.form("validation_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name", placeholder="e.g. Abhishek Gaikwad")
        email = st.text_input("Email Address", placeholder="e.g. abhishek@example.com")
        age = st.number_input("Age", min_value=0, max_value=120, value=22)
    
    with col2:
        country = st.text_input("Country Code (ISO)", placeholder="e.g. IN")
        phone = st.text_input("Phone Number", placeholder="e.g. +919876543210")
    
    st.markdown("---")
    submitted = st.form_submit_button("🔍 Validate Profile")

# Logic
if submitted:
    # Check if API Key is present
    if not os.getenv("GROQ_API_KEY"):
        st.error("⚠️ API Key missing! Please set GROQ_API_KEY in your .env file.")
    else:
        user_data = {
            "name": name,
            "email": email,
            "age": age,
            "country": country,
            "phone": phone
        }
        
        with st.spinner("🤖 AI is analyzing for security threats and logic..."):
            try:
                # 1. Generate Prompt
                prompt = get_validation_prompt(user_data)
                
                # 2. Call LLM
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": "Output only JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0
                )
                
                # 3. Parse Response
                content = response.choices[0].message.content.strip()
                if content.startswith("```"): 
                    content = content.replace("```json", "").replace("```", "")
                
                result = json.loads(content)
                
                # 4. Display UI Results
                if result["is_valid"]:
                    st.success("✅ **Validation Passed**")
                    if result.get("warnings"):
                        st.warning(f"⚠️ **Warnings:** {', '.join(result['warnings'])}")
                    else:
                        st.markdown('<div class="success-box">User data is clean and secure.</div>', unsafe_allow_html=True)
                else:
                    st.error("❌ **Validation Failed**")
                    for err in result.get("errors", []):
                        st.markdown(f"🔴 {err}")
                
                # Show Raw JSON
                with st.expander("View Raw JSON Response"):
                    st.json(result)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Sidebar Info
st.sidebar.title("About")
st.sidebar.info(
    """
    This tool uses **Llama-3** to perform:
    - 🧠 **Semantic Analysis**
    - 🛡️ **SQL Injection Detection**
    - ⚠️ **Logical Warning Checks**
    
    Built with Python & Streamlit.
    """
)