# Jormungandr
from ...domain.exceptions import ErrorOnRegisterUserSocial
from ...domain.user.model import UserModel

# Third party
from decouple import config
from etria_logger import Gladsheim
from valhalla_client.main import SocialNetworkQueue, Producer


class Social:
    social_client = None

    @classmethod
    def __get_social_client(cls) -> SocialNetworkQueue:
        if cls.social_client is None:
            try:
                producer = Producer(
                    host=config("VALHALLA_HOST"), port=int(config("VALHALLA_PORT"))
                )
                cls.social_client = SocialNetworkQueue(producer=producer)

            except Exception as ex:
                message = f'Error to get social client'
                Gladsheim.error(error=ex, message=message)
                raise ex
        return cls.social_client

    @classmethod
    async def register_user(cls, user_model: UserModel):
        msg = user_model.get_social_prospect_user_template_()
        social_client = cls.__get_social_client()
        success, message = await social_client.create_social_network_user(
            msg=msg
        )
        if not success.value:
            Gladsheim.error(message="::Social::register_ser::Error on trying to register user in Vahalla")
            raise ErrorOnRegisterUserSocial
