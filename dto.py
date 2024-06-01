from dataclasses import dataclass
from typing import Optional

@dataclass
class UserDTO:
    id: str
    login: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    doctor_name: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    first_login: Optional[bool] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    notes: Optional[str] = None
    settings_tone: Optional[str] = None
    settings_depth: Optional[str] = None
    settings_format: Optional[str] = None
    settings_mood: Optional[str] = None
    settings_language: Optional[str] = None
    
