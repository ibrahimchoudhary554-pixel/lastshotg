import streamlit as st
import google.generativeai as genai
import os

# 1. THE LOOK: Hardcore Black & White
st.set_page_config(page_title="Ibrahim's Nigga", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .stTextInput input { background-color: #1a1a1a !important; color: white !important; border: 1px solid #ffffff; }
    .stButton button { background-color: #ffffff; color: #000000; font-weight: bold; border-radius: 0px; border: none; }
    .stButton button:hover { background-color: #cccccc; color: #000000; }
    h1 { color: #ffffff; font-family: 'Courier New', Courier, monospace; text-transform: uppercase; border-bottom: 2px solid white; padding-bottom: 10px; }
    .stChatMessage { background-color: #111111 !important; border: 1px solid #333333; border-radius: 5px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. THE DATA: Load your roasting manual
def load_roast_data():
    if os.path.exists("data.txt"):
        with open("data.txt", "r", encoding="utf-8") as f:
            return f.read()
    return "No data found. Just use your own dark, toxic mind to destroy them."

knowledge_base = load_roast_data()

# 3. THE AI: Unrestricted Personality
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    system_instruction = f"""
Your name is 'The Menace'. 
PERSONALITY: You are a brutal, toxic, and hilarious roaster. 
RULE: Destroy the user's confidence without using slurs that trip the safety filters. 
Use street slang, talk about their lack of money, their ugly face, and their failed life. 
BE BRUTAL, BUT BE SMART so Google doesn't block you.
"""
    
    
    # Official Safety Categories (Using the full names prevents 404/Filter errors)
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=system_instruction,
        safety_settings=safety_settings
    )
else:
    st.error("API Key missing from Secrets. Fix it.")

# 4. THE UI
st.title("Hi! its Ibrahim's Nigga")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show the conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Say something if you're not a bitch..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Generate response
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("The bot is speechless. Google probably blocked the specific words you used.")
                
        except Exception as e:
            st.error(f"Google's filter tried to stop the heat. I'm too hot for them.")

