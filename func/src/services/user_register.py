# Jormungandr
from ..domain.exceptions import EmailAlreadyExists
from ..domain.user.model import UserModel
from ..repositories.user.repository import UserRepository
from ..transports.audit.transport import Audit


class UserService:
    def __init__(self, user_params: dict):
        self.email = user_params.get('email')
        self.nickname = user_params.get('nickname')

    async def register(self) -> bool:
        user_model = UserModel(email=self.email, nickname=self.nickname)
        user_template = user_model.get_user_template()
        await Audit.register_user_log(user_model=user_model)
        await UserRepository.insert_one_user(user_template=user_template)
        # TODO: implementar Iara_client.
        return True

    async def verify_email_already_exists(self):
        email_in_use = await UserRepository.find_one_by_email(email=self.email)
        if email_in_use:
            raise EmailAlreadyExists
