# from supabase import create_client, Client
# import os
# from dotenv import load_dotenv
# from dto import UserDTO

# # Load environment variables from .env file
# load_dotenv()

# def init_supabase() -> Client:
#     url = os.getenv("SUPABASE_URL")
#     key = os.getenv("SUPABASE_KEY")
#     if not url or not key:
#         raise ValueError("Supabase URL and Key must be set in environment variables.")
#     supabase = create_client(url, key)
#     return supabase


# def fetch_user_info(supabase: Client, user_id: str) -> UserDTO:
#     try:
#         response = supabase.from_("user").select("*").eq("id", user_id).execute()
#         if response.status_code != 200 or not response.data:
#             raise ValueError(f"Error fetching user info or no data found: {response.error_message}")

#         user_data = response.data[0]
        
#         return UserDTO(
#             user_id=user_data["user_id"],
#             login=user_data["login"],
#             email=user_data.get("email"),
#             first_name=user_data.get("first_name"),
#             last_name=user_data.get("last_name"),
#             doctor_name=user_data.get("doctor_name"),
#             created_at=user_data.get("created_at"),
#             updated_at=user_data.get("updated_at"),
#             first_login=user_data.get("first_login"),
#             diagnosis=user_data.get("diagnosis"),
#             treatment=user_data.get("treatment"),
#             notes=user_data.get("notes"),
#             settings_tone=user_data.get("settings_tone"),
#             settings_depth=user_data.get("settings_depth"),
#             settings_format=user_data.get("settings_format"),
#             settings_mood=user_data.get("settings_mood"),
#             settings_language=user_data.get("settings_language")
#         )
#     except Exception as e:
#         raise ValueError(f"Error fetching user info: {e}")

from supabase import create_client, Client
import os
from dotenv import load_dotenv
from dto import UserDTO


# Load environment variables from .env file
load_dotenv()

def init_supabase() -> Client:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)

    if not url or not key:
        raise ValueError("Supabase URL and Key must be set in environment variables.")
    return supabase

def fetch_additional_context(supabase: Client, prompt: str) -> str:
    # Dummy implementation for fetching additional context from Supabase
    # Replace this with actual Supabase query logic
    context = "Additional context fetched from Supabase related to the prompt."
    return context


def fetch_user_info(supabase: Client, user_id: str) -> UserDTO:
  
    try:
        response = supabase.table("users").select("*").eq("id", user_id).execute()

        # Assuming the first item in data list is the user's data
        user_data = response.data[0]

        # Map the data from the query to the UserDTO fields
        return UserDTO(
            id=str(user_data['id']),
            login=user_data['login'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            doctor_name=user_data['doctor'],
            created_at=user_data['created_at'],
            updated_at=user_data['updated_at'],
            first_login=user_data['first_login'],
            diagnosis=user_data['diagnosis'],
            treatment=user_data['treatment'],
            notes=user_data['notes'],
            settings_tone=user_data.get('setting_tone'),  # use .get for optional fields
            settings_depth=user_data.get('settings_depth'),
            settings_format=user_data.get('settings_format'),
            settings_mood=user_data.get('settings_mood'),
            settings_language=user_data.get('settings_language')
        )
    except Exception as e:
        raise ValueError(f"Error fetching user info: {e}")


    
 

