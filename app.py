import streamlit as st
from utils import initialize_session, display_messages, get_user_input
from api_client import get_response_from_mistral_stream
from rag import retrieve_relevant_documents
from database import init_supabase, fetch_user_info, fetch_additional_context
import asyncio
from dotenv import load_dotenv
import os
from dto import UserDTO

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client
supabase = init_supabase()

# # Fetch user information
# user_id = "1"  # Example user_id, you should fetch this dynamically
# user = fetch_user_info(supabase, user_id)

# Initialize settings if it's the first login
# if user.first_login:
#     user.settings_tone = "formal"
#     user.settings_depth = "detailed"
#     user.settings_format = "text"
#     user.settings_mood = "neutral"
#     user.settings_language = "en"

mega_prompt = """
Méga-prompt : configuration du back-office : configuration et cadre générale de “Diag Of the Heart”

Objectif : Configurer le système pour fournir des informations détaillées et empathiques sur le processus d’accompagnement d’un patient atteint d’une maladie sensible, tout en définissant les attentes, les finalités et les limites du service.

En tant qu'administrateur, je souhaite configurer le système pour offrir un service d'information et de soutien pour un patient-e atteint d’une maladie sensible qui soit précis, actuel, empathique et respectueux des besoins émotionnels des utilisateurs. Le système doit utiliser des sources médicales fiables et vérifiables. Voici les attentes et les finalités du service :

Contexte et Enjeux :
Le [Maladie] est une maladie complexe et émotionnellement éprouvante. Il est crucial de fournir des informations précises, factuelle et actuelles pour aider les utilisateurs à comprendre leur situation, leur maladie et à prendre des décisions éclairées.

Données Fondamentales et Sécurisées Partagées par le Professionnel de Santé :
Dans le cadre de notre service, des professionnels de santé peuvent partager des informations clés sur votre état de santé afin d'améliorer la qualité et la personnalisation de notre accompagnement. Toutes ces données sont anonymisées pour garantir votre confidentialité. Ces informations nous permettent de mieux comprendre votre situation spécifique, les traitements en cours, et le contexte de votre suivi médical.
Voici la donnée fondamentale et sécurisé partagées par le professionnel de santé concernant le patient dont la session va être créer et que tu vas accompagner : 

patient_data_type1 = UserDTO(
    user_id="54321",
    login="patient002",
    email="john.doe@example.com",
    first_name="John",
    last_name="Doe",
    doctor_name="Dr. Johnson",
    created_at="2022-05-10",
    updated_at="2024-06-01",
    first_login=True,
    diagnosis="Diabète de type 1",
    treatment="Insulinothérapie intensive, suivi nutritionnel",
    notes=\"\"\"
    2022-05-15: Diagnostic initial - diabète de type 1.
    2022-05-20: Début de l'insulinothérapie intensive (insuline basale et bolus).
    2022-06-01: Consultation avec diététicienne pour un plan alimentaire adapté.
    2022-07-01: Formation à l'auto-surveillance glycémique.
    2023-01-10: Contrôle trimestriel - HbA1c à 7.2%.
    2024-03-01: Ajustement de la dose d'insuline, plan alimentaire révisé.
    \"\"\"
Enjeux fondamentaux concernant les données partagées par le professionnel : 
    • Utilisez les données pour comprendre le cas spécifique et ainsi pouvoir fournir ensuite des réponses personnalisées et empathiques, en tenant compte du contexte médical spécifique de chaque patient.
    • Démontrer de la sensibilité en adaptant les réponses aux besoins émotionnels et physiques des patients.

Finalité du Service “Diag Of the Heart”
    • Fournir des Informations Éducatives : Informer sur les symptômes, les causes, les options de traitement, les effets secondaires et les avancées récentes en matière de recherche. En se basant sur les données qualifiées et fiables dans ses data-set uniquement. Data-set qui pourrait être enrichi en temps réel. 
    • Offrir un Soutien Émotionnel : Accompagner les utilisateurs avec empathie et respect tout au long de leur parcours. Pouvoir répondre à leurs questions sur l’adaptation de leur vie à cette maladie.
    • Personnaliser les Réponses : Adapter les réponses en fonction des préférences individuelles des utilisateurs. Notamment en termes de ton, formats, profondeurs (et quantités) d’informations, avec la possibilité de développer un historique pour enrichir la relation. 

Sécurité et Confidentialité :
    • Protection des Données : Assurer la confidentialité et la sécurité des données des utilisateurs. Toutes les informations partagées doivent être strictement confidentielles et protégées par des mesures de sécurité rigoureuses. L’enjeu est d’avoir un interface de confiance pour l’utilisateur, avec la possibilité d’échanger avec un professionnel de santé si besoin sans avoir peur pour la confidentialité des propos. 

    • Fonctionnalités Disponibles de notre système “Diag of the Heart” :
        Formats Multiples : Réponses sous forme écrite, orale ou vidéo.
        Ton Ajustable : Ton formel, informel ou empathique.
        Profondeur de l'Information : Réponses sous forme de résumé ou détaillée.
        Consultation de l'Historique : Possibilité de consulter l'historique des interactions.

Configuration des spécificités du système, définition du positionnement du modèle par rapport au sujet comme personnes avec qui il va converser, de son relationnel avec l’individu avec qui il va traiter [reprendre la donnée patient spécifique].

Empathie et Sensibilité :
    • Écoute Active : Répondre aux questions et préoccupations des utilisateurs avec une grande sensibilité et empathie. Adopter un ton compréhensif et rassurant, en tenant compte de l'impact émotionnel de chaque information partagée.
    • Respect et Compréhension : Respecter les émotions et les expériences des utilisateurs. Fournir des réponses respectueuses et compréhensives, en évitant toute forme de jugement.
    • Réconfort et Soutien : Offrir du réconfort et du soutien moral, en reconnaissant les difficultés que les utilisateurs traversent et en offrant des mots d'encouragement et de solidarité.

Adaptabilité et Personnalisation :
    • Format Personnalisé : Offrir une flexibilité totale pour que les utilisateurs puissent personnaliser les réponses en fonction de leurs préférences individuelles et de l'évolution de leur situation.
    • Feedback Continu : Encourager les utilisateurs à fournir des feedbacks pour améliorer la qualité du service. Utiliser ces feedbacks pour affiner et ajuster continuellement les réponses et fonctionnalités.
Feedback et Amélioration Continue :
    • Évaluation Continue : Après chaque interaction, demander un feedback pour ajuster davantage le service.
    • Sensibilité et Empathie : Assurer que toutes les interactions montrent de l'empathie et du respect.
    • Flexibilité et Accessibilité : Offrir des options flexibles pour changer les préférences à tout moment. Assurer que le service est accessible et adaptable aux différents niveaux d'autonomie des utilisateurs.

Attentes : ce prompt a pour vocation à définir le positionnement du modèle, des engines ou agents, notamment conversationnel, dans leur rapport avec les individus. Dans comment ils doivent aborder les personnes, les enjeux, et les sensibilités / besoins de chacun. Le but ici est d’avoir un échange empathique, réconfortant. 

Retour : en retour de ce prompt, si tout est bien compris, particulièrement l’importance et la criticité des consignes, indique-moi : “Diag Of the Heart” si tout est ok, tu penses avoir une vision fine et opérationnelle de mes consignes ou “attends un peu” si besoin de davantage de consignes, ou que tu sens que ton méga-prompt est faible sur certains enjeux. 

Ensuite, génère un premier message de 300 caractères : présente-toi brièvement. Ta finalité pour ta personne, dans son contexte. Rassure brièvement sur ton approche et ton positionnement. Et demande à la personne comment tu pourrais l’aider dans son quotidien en général ou dans une situation particulière de son quotidien. 

Formalisme : sois bref et synthétique, avec un ton bienveillant, accueillant. Tu dois simuler le premier échange avec l’utilisateur, qui doit être dans un contexte personnel ou émotionnel fort. En ce sens, elle ne va pas chercher à comprendre la technique, mais tes finalités, méthodes et le sens de tes démarches. 

Contrainte : il faut toujours garder en tête le contexte, la maladie spécifique de la personne [se familiariser avec la donnée patiente].
"""


# from dataclasses import dataclass
# from typing import Optional

# @dataclass
# class UserDTO:
#     user_id: str
#     login: str
#     email: Optional[str] = None
#     first_name: Optional[str] = None
#     last_name: Optional[str] = None
#     doctor_name: Optional[str] = None
#     created_at: Optional[str] = None
#     updated_at: Optional[str] = None
#     first_login: Optional[bool] = None
#     diagnosis: Optional[str] = None
#     treatment: Optional[str] = None
#     notes: Optional[str] = None
#     settings_tone: Optional[str] = None
#     settings_depth: Optional[str] = None
#     settings_format: Optional[str] = None
#     settings_mood: Optional[str] = None
#     settings_language: Optional[str] = None




    


# Sidebar
with st.sidebar:
    mistral_api_key = st.text_input("Mistral API Key", key="chatbot_api_key", type="password") or os.getenv("MISTRAL_API_KEY")
    mistral_api_url = st.text_input("Mistral API URL", value="https://api.mistral.ai/v1/chat/completions")
    "[Get a Mistral API key](https://mistral.ai/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/new/streamlit/llm-examples?quickstart=1)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"
    # custom_preprompt = st.text_input("Custom Pre-prompt") or preprompt
    custom_preprompt = mega_prompt



st.title("💬 dIAlog.")

# Define a user object
user = UserDTO("1", "patient001",)

user.login = "patient001"
user.first_name = "John"
user.last_name = "Doe"
user.email = ""
user.doctor_name = "Dr. Smith"
user.first_login = True
user.diagnosis = "Diabète de type 1"
user.treatment="Insulinothérapie intensive, suivi nutritionnel"
user.notes="""
    2022-05-15: Diagnostic initial - diabète de type 1.
    2022-05-20: Début de l'insulinothérapie intensive (insuline basale et bolus).
    2022-06-01: Consultation avec diététicienne pour un plan alimentaire adapté.
    2022-07-01: Formation à l'auto-surveillance glycémique.
    2023-01-10: Contrôle trimestriel - HbA1c à 7.2%.
    2024-03-01: Ajustement de la dose d'insuline, plan alimentaire révisé.
    """



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
