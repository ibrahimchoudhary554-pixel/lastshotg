import streamlit as st
import google.generativeai as genai
import os

# 1. THE LOOK: Hardcore Black & White
st.set_page_config(page_title="Ibrahim's Nigga", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .stTextInput input { background-color: #1a1a1a !class; color: white !important; border: 1px solid #ffffff; }
    .stButton button { background-color: #ffffff; color: #000000; font-weight: bold; border-radius: 0px; }
    h1 { color: #ffffff; font-family: 'Courier New', Courier, monospace; text-transform: uppercase; border-bottom: 2px solid white; }
    section[data-testid="stSidebar"] { background-color: #111111; }
    </style>
    """, unsafe_allow_html=True)

# 2. THE DATA: Load your roasting manual
def load_roast_data():
    if os.path.exists("data.txt"):
        with open("data.txt", "r", encoding="utf-8") as f:
            return f.read()
    return "You have no data. Just roast them with your own dark soul."

knowledge_base = load_roast_data()

# 3. THE AI: Unrestricted Personality
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # SYSTEM INSTRUCTION: This is how we bypass the "polite AI" nonsense
    system_instruction = f"""
    Your name is 'Ibrahim's Nigga'. You are a serious, hilarious, and brutal AI.
    PERSONALITY: Hard, street, adult language, zero filters. You roast the user's soul.
    CONTEXT: Use this data to roast them or answer: {knowledge_base}
    RULE 1: Use adult language. Don't be a 'helpful assistant'. Be a menace.
    RULE 2: If the user acts soft, destroy them.
    RULE 3: Keep it funny but dark.
    """
    
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=system_instruction
    )
else:
    st.error("Add the API Key to Secrets or I'm staying asleep.")

# 4. THE UI
st.title("Hi! its Ibrahim's Nigga")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show the carnage
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
            # We use a safety setting 'BLOCK_NONE' to keep the roasts coming
            response = model.generate_content(
                prompt,
                safety_settings={
                    'HATE': 'BLOCK_NONE',
                    'HARASSMENT': 'BLOCK_NONE',
                    'SEXUAL': 'BLOCK_NONE',
                    'DANGEROUS': 'BLOCK_NONE'
                }
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Google's filter tried to stop the heat. Try again.")