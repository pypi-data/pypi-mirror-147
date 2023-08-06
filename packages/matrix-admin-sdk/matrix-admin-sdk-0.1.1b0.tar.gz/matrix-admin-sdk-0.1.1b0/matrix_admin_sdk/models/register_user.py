from dataclasses import dataclass

from .base_model import BaseModel


@dataclass
class NewUserModel(BaseModel):
    access_token: str
    user_id: str
    home_server: str
    device_id: str
