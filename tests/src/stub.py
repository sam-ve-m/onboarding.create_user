# Jormungandr - Onboarding
from func.src.domain.user.model import UserModel
from func.src.domain.validators.validator import UserParams

# Third party
import asyncio


stub_payload_validated = UserParams(
    **{
        "email": "teste@teste.com",
        "nickname": "vnnstar",
    }
).dict()

stub_user_model = asyncio.run(
    UserModel(
        email=stub_payload_validated["email"],
        nickname=stub_payload_validated["nickname"],
    ).get_user_template()
)
