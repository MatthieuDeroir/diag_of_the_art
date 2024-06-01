import streamlit as st
from utils import initialize_session, display_messages, get_user_input
from api_client import get_response_from_mistral_stream
from rag import retrieve_relevant_documents
from database import init_supabase, fetch_user_info

import asyncio
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client
supabase = init_supabase()

# Fetch user information
user_id = "1"  # Example user_id, you should fetch this dynamically
user = fetch_user_info(supabase, user_id)

# Initialize settings if it's the first login
if user.first_login:
    user.settings_tone = "formal"
    user.settings_depth = "detailed"
    user.settings_format = "text"
    user.settings_mood = "neutral"
    user.settings_language = "en"

# Sidebar
with st.sidebar:
    mistral_api_key = st.text_input("Mistral API Key", key="chatbot_api_key", type="password") or os.getenv("MISTRAL_API_KEY")
    mistral_api_url = st.text_input("Mistral API URL", value="https://api.mistral.ai/v1/chat/completions")
    "[Get a Mistral API key](https://mistral.ai/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/new/streamlit/llm-examples?quickstart=1)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"
    custom_preprompt = st.text_input("Custom Pre-prompt")

st.title("💬 Chatbot")

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
    if not mistral_api_key:
        st.info("Please add your Mistral API key to continue.")
        st.stop()

    # Retrieve relevant documents (RAG)
    relevant_docs = retrieve_relevant_documents(prompt)
    
    # Fetch additional context from Supabase
    additional_context = fetch_additional_context(supabase, prompt)

    # Combine retrieved documents and additional context into the prompt
    combined_prompt = f"{additional_context}\n\n{relevant_docs}\n\n{prompt}"

    # Define an async generator function for streaming the response
    async def response_generator():
        try:
            async for response_chunk in get_response_from_mistral_stream(
                mistral_api_key, mistral_api_url, st.session_state.messages, combined_prompt, custom_preprompt
            ):
                if "choices" in response_chunk:
                    for choice in response_chunk["choices"]:
                        chunk_content = choice.get("message", {}).get("content", "")
                        if chunk_content:
                            yield chunk_content
        except Exception as e:
            st.error(f"Error: {str(e)}")

    # Function to run the async generator and update the UI
    async def run_async_generator():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        response_content = ""
        async for chunk in response_generator():
            response_content += chunk
            st.write(response_content)  # Update the UI with the latest content
        
        st.session_state.messages.append({"role": "assistant", "content": response_content})
    
    # Run the asynchronous function using Streamlit's asyncio support
    asyncio.run(run_async_generator())
