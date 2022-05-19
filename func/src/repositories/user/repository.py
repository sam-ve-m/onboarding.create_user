# Jormungandr
from ...infrastructures.mongo_db.infrastructure import MongoDBInfrastructure
from ...infrastructures.env_config import config

# Third party
from etria_logger import Gladsheim


class UserRepository:

    infra = MongoDBInfrastructure

    @classmethod
    async def __get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            database = mongo_client[config("MONGODB_DATABASE_NAME")]
            collection = database[config("MONGODB_USER_COLLECTION")]
            return collection
        except Exception as ex:
            message = f'UserRepository::_get_collection::Error when trying to get collection'
            Gladsheim.error(error=ex, message=message)
            raise ex

    @classmethod
    async def insert_one_user(cls, user: dict):
        collection = await cls.__get_collection()
        try:
            await collection.insert_one(user)
        except Exception as ex:
            message = f'UserRepository::insert_one_user::with this query::"user":{user}'
            Gladsheim.error(error=ex, message=message)
            raise ex

    @classmethod
    async def find_one_by_email(cls, email: str) -> bool:
        collection = await cls.__get_collection()
        try:
            result = await collection.find_one({'email': email}, {'_id': True})
            return result
        except Exception as ex:
            message = f'UserRepository::find_one_by_email::with this query::"email":{email}'
            Gladsheim.error(error=ex, message=message)
            raise ex
