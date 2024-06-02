import streamlit as st

def initialize_session():
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Bienvenue dans votre safe space"}]

def display_messages():
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

def get_user_input():
    return st.chat_input()
