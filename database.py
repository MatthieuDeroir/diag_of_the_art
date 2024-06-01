from supabase import create_client, Client
import os
from dotenv import load_dotenv
from dto import UserDTO

# Load environment variables from .env file
load_dotenv()

def init_supabase() -> Client:
    """
    Initialize the Supabase client using environment variables.

    Returns:
        Client: Initialized Supabase client.

    Raises:
        ValueError: If Supabase URL or Key are not found in environment variables.
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("Supabase URL and Key must be set in environment variables.")
    supabase = create_client(url, key)
    return supabase

def fetch_additional_context(supabase: Client, prompt: str) -> str:
    """
    Fetch additional context from Supabase based on the provided prompt.

    Args:
        supabase (Client): The Supabase client.
        prompt (str): The prompt to fetch additional context for.

    Returns:
        str: The additional context related to the prompt.
    """
    return "Additional context related to the prompt."
    try:
        response = supabase.from_("context").select("context_data").ilike("prompt", f"%{prompt}%").execute()
        if response.status_code != 200 or not response.data:
            raise ValueError(f"Error fetching context or no context found: {response.error_message}")
        context_data = response.data[0]["context_data"]
        return context_data
    except Exception as e:
        raise ValueError(f"Error fetching additional context: {e}")

def fetch_user_info(supabase: Client, user_id: str) -> UserDTO:
    """
    Fetch user information from Supabase for a given user ID.

    Args:
        supabase (Client): The Supabase client.
        user_id (str): The user ID to fetch information for.

    Returns:
        UserDTO: A data transfer object containing user information.

    Raises:
        ValueError: If there's an error fetching user info or no data is found.
    """
    try:
        response = supabase.from_("user").select("*").eq("id", user_id).execute()
        if response.status_code != 200 or not response.data:
            raise ValueError(f"Error fetching user info or no data found: {response.error_message}")

        user_data = response.data[0]
        
        return UserDTO(
            user_id=user_data["user_id"],
            login=user_data["login"],
            email=user_data.get("email"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            doctor_name=user_data.get("doctor_name"),
            created_at=user_data.get("created_at"),
            updated_at=user_data.get("updated_at"),
            first_login=user_data.get("first_login"),
            diagnosis=user_data.get("diagnosis"),
            treatment=user_data.get("treatment"),
            notes=user_data.get("notes"),
            settings_tone=user_data.get("settings_tone"),
            settings_depth=user_data.get("settings_depth"),
            settings_format=user_data.get("settings_format"),
            settings_mood=user_data.get("settings_mood"),
            settings_language=user_data.get("settings_language")
        )
    except Exception as e:
        raise ValueError(f"Error fetching user info: {e}")
