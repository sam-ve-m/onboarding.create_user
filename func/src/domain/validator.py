# Jormungandr
from .exceptions import InvalidEmail

# Standards
from re import search

# Third party
from etria_logger import Gladsheim
from pydantic import BaseModel, validator


class UserParams(BaseModel):
    email: str
    nickname: str

    @validator("email")
    def validate_email(email: str):
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not search(regex, email):
            Gladsheim.error(message=f"Validator::validate_email::Invalid email format::{email}")
            raise InvalidEmail
        return email
