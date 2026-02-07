import streamlit as st
import google.generativeai as genai
import os

# 1. THE LOOK: Professional Black & White
st.set_page_config(page_title="Ibrahim's Data Bot", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .stTextInput input { background-color: #1a1a1a !important; color: white !important; border: 1px solid #ffffff; }
    .stButton button { background-color: #ffffff; color: #000000; font-weight: bold; border-radius: 0px; border: none; width: 100%; }
    .stButton button:hover { background-color: #cccccc; }
    h1 { color: #ffffff; font-family: 'Courier New', Courier, monospace; text-transform: uppercase; border-bottom: 2px solid white; padding-bottom: 10px; }
    .stChatMessage { background-color: #111111 !important; border: 1px solid #333333; border-radius: 8px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. THE DATA: Loading your specific info
def load_data():
    if os.path.exists("data.txt"):
        with open("data.txt", "r", encoding="utf-8") as f:
            return f.read()
    return "No specific data provided."

knowledge_base = load_data()

# 3. THE AI: Serious Assistant (No Safety Triggers)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # We switch to a helpful, serious tone to avoid the filter nightmare
    system_instruction = f"""
    Your name is 'Ibrahim's Assistant'. 
    PERSONALITY: You are a highly professional, serious, and efficient AI assistant.
    YOUR MISSION: Provide clear and accurate answers based on the provided data: {knowledge_base}
    TONE: Direct, sophisticated, and helpful. No jokes, no roasts—just pure data processing.
    """
    
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=system_instruction
    )
else:
    st.error("Missing GEMINI_API_KEY in Streamlit Secrets.")

# 4. THE UI
st.title("Hi! its Ibrahim's Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask a question about the data..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Generate the response
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("Empty response received. Try rephrasing.")
                
        except Exception as e:
            st.error("An error occurred. Please ensure your prompt is professional.")
