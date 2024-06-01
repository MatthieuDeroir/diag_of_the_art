from supabase import create_client, Client
import os
from dotenv import load_dotenv
from dto import UserDTO

# Load environment variables from .env file
load_dotenv()

def init_supabase() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("Supabase URL and Key must be set in environment variables.")
    supabase = create_client(url, key)
    return supabase

def fetch_user_info(supabase: Client, user_id: str) -> UserDTO:
    try :
        response = supabase.from_("user").select("*").eq("user_id", user_id).execute()
        if response.error:
            raise ValueError(f"Error fetching user info: {response.error.message}")
        
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
