import streamlit as st
import google.generativeai as genai
import os

# 1. THE LOOK: Black & White Terminal
st.set_page_config(page_title="Ibrahim's Bot", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .stTextInput input { background-color: #1a1a1a !important; color: white !important; border: 1px solid #ffffff; }
    .stButton button { background-color: #ffffff; color: #000000; font-weight: bold; border-radius: 0px; border: none; width: 100%; }
    h1 { color: #ffffff; font-family: 'Courier New', Courier, monospace; text-transform: uppercase; border-bottom: 2px solid white; padding-bottom: 10px; }
    .stChatMessage { background-color: #111111 !important; border: 1px solid #333333; border-radius: 8px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. THE DATA: Safer Loading
def load_data():
    try:
        if os.path.exists("data.txt"):
            with open("data.txt", "r", encoding="utf-8") as f:
                content = f.read().strip()
                return content if content else "No specific data provided."
    except Exception:
        pass
    return "No specific data provided."

knowledge_base = load_data()

# 3. THE AI: Simple & Clean
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # We keep the prompt simple to avoid ANY internal Google triggers
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=f"You are a helpful assistant for Ibrahim. Use this data: {knowledge_base}"
    )
else:
    st.error("Missing API Key in Secrets.")

# 4. THE UI
st.title("Hi! its Ibrahim's Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # We add a timeout/error check here
            response = model.generate_content(prompt)
            if response and response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("AI returned an empty response. Check your data.txt for weird characters.")
        except Exception as e:
            # THIS SHOWS YOU THE ACTUAL ERROR
            st.error(f"Error: {str(e)}")
