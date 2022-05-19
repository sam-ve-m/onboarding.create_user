# Jormungandr
from ..domain.exceptions import EmailAlredyExists
from ..domain.user.model import UserModel
from ..repositories.user.repository import UserRepository
from ..transports.audit.transport import Audit
from ..transports.social.transport import Social

# Third party
from etria_logger import Gladsheim


class UserService:
    def __init__(self, user_params: dict):
        self.email = user_params.get('email')
        self.nickname = user_params.get('nickname')

    async def register(self):
        user = UserModel(email=self.email, nickname=self.nickname).to_dict()
        await Audit.register_user_log(user=user)
        await Social.register_user(user=user)
        await UserRepository.insert_one_user(user=user)
        return True

    async def verify_email_alredy_exists(self):
        email_in_use = await UserRepository.find_one_by_email(email=self.email)
        if email_in_use:
            Gladsheim.error(message="UserService::verify_email_alredy_exists:: Email alredy exists")
            raise EmailAlredyExists
