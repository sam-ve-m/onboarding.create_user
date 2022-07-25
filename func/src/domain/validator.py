# Jormungandr
from .exceptions import InvalidEmail

# Standards
import re
from typing import Optional

# Third party
from etria_logger import Gladsheim
from pydantic import BaseModel, validator


class UserParams(BaseModel):
    email: str
    nickname: Optional[str]

    @validator("email")
    def validate_email(cls, email: str):
        regex = r'^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{2,66})\.([a-z]{2,3}(?:\.[a-z]{2})?)$'
        if not re.search(regex, email):
            Gladsheim.error(message=f"Validator::validate_email::Invalid email format::{email}")
            raise InvalidEmail
        return email
