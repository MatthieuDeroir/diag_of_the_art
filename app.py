import streamlit as st
from utils import initialize_session, display_messages, get_user_input
from api_client import get_response_from_mistral_stream
from rag import retrieve_relevant_documents
from database import init_supabase, fetch_user_info, fetch_additional_context, update_user_info
import asyncio
from dotenv import load_dotenv
import os
from dto import UserDTO
from prompt import *

is_log = False

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client
supabase = init_supabase()

# Fetch user information
user = fetch_user_info(supabase, "1")

# Page de connexion
def authenticate(username, password):
    if username == 'jean paul':
        st.session_state['authenticated'] = True
    return True if username == "jean paul" else False

# Sidebar
def show_sidebar():
    with st.sidebar:
        mistral_api_key = st.text_input("Mistral API Key", key="chatbot_api_key", type="password") or os.getenv("MISTRAL_API_KEY")
        mistral_api_url = st.text_input("Mistral API URL", value="https://api.mistral.ai/v1/chat/completions")
        "[Get a Mistral API key](https://mistral.ai/account/api-keys)"
        "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
        "[![Open in GitHub Codespaces](https://github.com/codespaces/new/streamlit/llm-examples?quickstart=1)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"
        
        page = st.sidebar.selectbox("Choisir une page", ["login", "unboarding", "conv", "dashboard", "Déconnexion"])
    if page == "login":
        show_login()
    elif page == "unboarding":
        show_unbaording()
    elif page == "conv":
        show_conv()
    elif page == "dashboard":
        show_dashboard()
    elif page == "Déconnexion":
        show_logout()

def show_conv():
    mistral_api_key = os.getenv("MISTRAL_API_KEY")
    mistral_api_url = "https://api.mistral.ai/v1/chat/completions"
    custom_preprompt = ""
        
    st.title("💬 dIAlog.")

    st.sidebar.write(f"Logged in as: {user.login}")
    st.sidebar.write(f"Full Name: {user.first_name} {user.last_name}")
    st.sidebar.write(f"Email: {user.email}")
    st.sidebar.write(f"Doctor: {user.doctor_name}")

    # Initialize session state
    initialize_session()

    # Display chat messages
    display_messages()

    # Get user input
    prompt = get_user_input()

    # Handle user input
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        if not mistral_api_key:
            st.info("Please add your Mistral API key to continue.")
            st.stop()

        # Retrieve relevant documents (RAG)
        relevant_docs = retrieve_relevant_documents(prompt)
        
        # Fetch additional context from Supabase
        additional_context = fetch_additional_context(supabase, prompt)

        # Combine retrieved documents and additional context into the prompt
        combined_prompt = f"{mega_prompt}\n\n{additional_context}\n\n{relevant_docs}\n\n{prompt}"

        placeholder = st.empty()  # Create an empty placeholder for dynamic updates

        # Run the asynchronous function using Streamlit's asyncio support
        response_content = asyncio.run(run_async_generator(
            mistral_api_key, mistral_api_url, st.session_state.messages, combined_prompt, custom_preprompt, placeholder
        ))
        st.session_state.messages.append({"role": "assistant", "content": response_content})

async def run_async_generator(api_key, api_url, messages, combined_prompt, custom_preprompt, placeholder):
    response_content = ""
    async for chunk in get_response_from_mistral_stream(api_key, api_url, messages, combined_prompt, custom_preprompt):
        response_content += chunk
        placeholder.write(response_content)  # Update the placeholder with the latest content
    return response_content

def show_unbaording():
    st.title(":rocket: Unboarding")
    pass

def show_dashboard():
    st.title(":sunglasses: Dashboard")
    pass

def show_login():
    st.title(":smile: Login")

    with st.form(key='login_form'):
        username = st.text_input("Identifiant")
        password = st.text_input("Mot de passe", type="password")
        submit_button = st.form_submit_button("Se connecter")
    
    if submit_button:
        if authenticate(username, password):
            st.success("Connexion réussie!")
            main()
        else:
            st.error("Identifiant ou mot de passe incorrect")

def show_logout():
    st.title(":cry: Logout")

def main():
    show_sidebar()

main()
