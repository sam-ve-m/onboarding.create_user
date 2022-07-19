# Jormungandr
from ..domain.exceptions import EmailAlreadyExists
from ..domain.user.model import UserModel
from ..repositories.user.repository import UserRepository
from ..transports.audit.transport import Audit


# Third party
from etria_logger import Gladsheim


class UserService:
    def __init__(self, user_params: dict):
        self.email = user_params.get('email')
        self.nickname = user_params.get('nickname')

    async def register(self):
        user_model = UserModel(email=self.email, nickname=self.nickname)
        user = user_model.to_dict()
        await Audit.register_user_log(user_model=user_model)
        await UserRepository.insert_one_user(user=user)
        # TODO Avisar ao Kafka da Iara, para enviar o email de confirmação, aguardar o client que sera feito pelo marcao
        return True

    async def verify_email_already_exists(self):
        email_in_use = await UserRepository.find_one_by_email(email=self.email)
        if email_in_use:
            Gladsheim.warning(message="UserService::verify_email_already_exists:: Email already exists")
            raise EmailAlreadyExists
