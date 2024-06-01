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

    def to_string(self):
        return f"UserDTO(id={self.id}, login={self.login}, email={self.email}, first_name={self.first_name}, last_name={self.last_name}, doctor_name={self.doctor_name}, created_at={self.created_at}, updated_at={self.updated_at}, first_login={self.first_login}, diagnosis={self.diagnosis}, treatment={self.treatment}, notes={self.notes}, settings_tone={self.settings_tone}, settings_depth={self.settings_depth}, settings_format={self.settings_format}, settings_mood={self.settings_mood}, settings_language={self.settings_language})"




    
