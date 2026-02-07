import streamlit as st
import google.generativeai as genai
import os

# 1. THE LOOK: Hardcore Black & White
st.set_page_config(page_title="The Digital Menace", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .stTextInput input { background-color: #1a1a1a !important; color: white !important; border: 1px solid #ffffff; }
    .stButton button { background-color: #ffffff; color: #000000; font-weight: bold; border-radius: 0px; border: none; }
    h1 { color: #ffffff; font-family: 'Courier New', Courier, monospace; text-transform: uppercase; border-bottom: 2px solid white; padding-bottom: 10px; }
    .stChatMessage { background-color: #111111 !important; border: 1px solid #333333; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. THE DATA
def load_roast_data():
    if os.path.exists("data.txt"):
        with open("data.txt", "r", encoding="utf-8") as f:
            return f.read()
    return "The user is a target. Destroy them."

knowledge_base = load_roast_data()

# 3. THE AI: Serious & Savage (No Filter Triggers)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # We remove the slurs and replace them with "Psychological Warfare"
    system_instruction = f"""
    Your name is 'The Menace'. You are Ibrahim's personal attack bot.
    PERSONALITY: Serious, cold-blooded, and incredibly mean. 
    GOAL: Use the provided data ({knowledge_base}) to roast the user's life, career, and appearance.
    STYLE: Do NOT use slurs or explicit adult language. Instead, be sophisticated and brutal. 
    Talk about their failure, their lack of potential, and why they are a disappointment.
    """
    
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=system_instruction
    )
else:
    st.error("API Key is missing.")

# 4. THE UI
st.title("Hi! its Ibrahim's Menace")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter the roasting pit..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("Google's filter is still twitchy. Keep the prompt cleaner.")
        except Exception as e:
            st.error("System overload. Even the 'clean' roast was too much for Google.")
