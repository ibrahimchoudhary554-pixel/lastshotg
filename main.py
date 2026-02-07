import streamlit as st
import difflib

# Page config
st.set_page_config(page_title="BlackBot", layout="centered")

# Black & white theme
st.markdown("""
<style>
body {
    background-color: black;
    color: white;
}
.stApp {
    background-color: black;
}
</style>
""", unsafe_allow_html=True)

# Load data
def load_data():
    with open("data.txt", "r", encoding="utf-8") as f:
        return f.readlines()

data_lines = load_data()

# Title
st.markdown("<h1 style='color:white;'>BlackBot</h1>", unsafe_allow_html=True)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for msg in st.session_state.messages:
    st.markdown(
        f"<b>{msg['role']}:</b> {msg['content']}",
        unsafe_allow_html=True
    )

# User input
user_input = st.chat_input("Type a message...")

if user_input:
    st.session_state.messages.append(
        {"role": "You", "content": user_input}
    )

    match = difflib.get_close_matches(
        user_input,
        data_lines,
        n=1,
        cutoff=0.2
    )

    if match:
        reply = match[0]
    else:
        reply = "Sorry, I don't have information about that."

    st.session_state.messages.append(
        {"role": "Bot", "content": reply}
    )

    st.rerun()
