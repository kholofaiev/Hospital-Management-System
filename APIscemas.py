from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import date, time, UTC, timedelta, datetime

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

import jwt
from fastapi.security import OAuth2PasswordBearer
from werkzeug.security import generate_password_hash, check_password_hash



class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8'
    )
    
    flask_secret_key: SecretStr
    database_url: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

settings = Settings() # type: ignore

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/token")


def create_access_token(data:dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.flask_secret_key.get_secret_value(),
        algorithm=settings.algorithm
    )
    return encoded_jwt
    
    
def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.flask_secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
            options={"require":["exp", "sub"]}
        )
    except jwt.InvalidTokenError:
        return None
    else:
        return payload.get("sub")
  
    
class UserBase(BaseModel):
    name: str =  Field(min_length=1, max_length=15)
    lastname: str = Field(min_length=1, max_length=15)
    category: str = Field(min_length=6, max_length=7)
    specialty: Optional[str] = None
    dob: Optional[date] = None
    

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=163)

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str

class AppointmentBase(BaseModel): 
    doctor_id: int
    patient_id: int
    appointment_date: date
    appointment_time: time


class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    diagnosis: Optional[str] = None
    prescription: Optional[str] = None
    status: Optional[str] = "opened"
    model_config = ConfigDict(from_attributes=True)

class AppointmentResponse(AppointmentBase):
    id: int
    diagnosis: Optional[str] = None
    prescription: Optional[str] = None
    status: Optional[str] = "opened"
    model_config = ConfigDict(from_attributes=True)