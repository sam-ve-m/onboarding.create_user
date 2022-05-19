# Jormungandr
from ...domain.exceptions import ErrorOnRegisterUserSocial
from ...infrastructures.env_config import config

# Third party
from valhalla_client.main import SocialNetworkQueue, Producer
from etria_logger import Gladsheim


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
                return cls.social_client
            except Exception as ex:
                message = f'Error to get social client'
                Gladsheim.error(error=ex, message=message)
                raise ex

    @classmethod
    async def register_user(cls, user: dict):
        social_client = cls.__get_social_client()
        success, message = await social_client.create_social_network_user(
            msg={
                "user_type": user.get('user_type'),
                "nickname": user.get('nickname'),
                "unique_id": user.get('unique_id'),
                "username": "jefrey",
                "user_gender": "female",
                "region": "br"
            }
        )
        if not success:
            Gladsheim.error(message="::Social::register_ser::Error on trying to register user in Vahalla")
            raise ErrorOnRegisterUserSocial
