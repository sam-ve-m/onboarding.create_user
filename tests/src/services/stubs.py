# Jormungandr - Onboarding
from func.src.domain.user.model import UserModel
from func.src.domain.validators.validator import UserParams

# Third party
import asyncio


stub_payload_validated = UserParams(
    **{
        "email": "teste@teste.com",
        "nick_name": "vnnstar",
    }
)

stub_user_model = UserModel(
        email=stub_payload_validated.email,
        nick_name=stub_payload_validated.nick_name,
    )


stub_user_model_template = asyncio.run(stub_user_model.get_user_template())
