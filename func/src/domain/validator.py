# Jormungandr
from .exceptions import InvalidEmail
# from func.src.domain.exceptions import InvalidEmail

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


# email = {"email": 'vih-reis@hotmail.com'}
# email1 = {"email": 'vih-reis@hotmail.com.br'}
# email2 = {"email": 'vih-reis@teste.com'}
# email3 = {"email": 'ASHD31a2@gmail.com'}
# email5 = {"email": 'teste@teste.com'}
# email6 = {"email": 'jp@gmail.com.br'}
# email7 = {"email": 'teste_@teste.com'}
#
# a = UserParams(**email1)
# print(a)
# b = UserParams(**email)
# print(b)
# c = UserParams(**email3)
# print(c)
# d = UserParams(**email2)
# print(d)
# e = UserParams(**email5)
# print(e)
# f = UserParams(**email6)
# print(f)
# g = UserParams(**email7)
# print(g)
