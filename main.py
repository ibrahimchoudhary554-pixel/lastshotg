import streamlit as st
import google.generativeai as genai
import os

# 1. UI Setup
st.set_page_config(page_title="Ibrahim's Bot", layout="centered")
st.markdown("<style>.stApp { background-color: #000; color: #fff; }</style>", unsafe_allow_html=True)

# 2. Setup API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # We use the legacy name which is most compatible with v1beta
    model = genai.GenerativeModel('models/gemini-pro')
else:
    st.error("API Key missing.")

# 3. Chat Logic
st.title("Hi! its Ibrahim's Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Type here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Simple, clean request
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
