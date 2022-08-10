# Third party
from decouple import config
from etria_logger import Gladsheim
from motor.motor_asyncio import AsyncIOMotorClient


class MongoDBInfrastructure:

    client = None
    url = config("MONGO_CONNECTION_URL")

    @classmethod
    def get_client(cls):
        if cls.client is None:
            try:
                cls.client = AsyncIOMotorClient(cls.url)
            except Exception as ex:
                Gladsheim.error(error=ex)
                raise ex
        return cls.client
