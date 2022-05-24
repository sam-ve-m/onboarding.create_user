# Jormungandr
from ...domain.exceptions import ErrorOnSendAuditLog
from ...domain.enums.queue.types import QueueTypes
from ...domain.user.model import UserModel

# Third party
from decouple import config
from etria_logger import Gladsheim
from persephone_client import Persephone




class Audit:
    audit_client = Persephone
    partition = QueueTypes.PROSPECT_USER.value
    topic = config("PERSEPHONE_TOPIC_USER")
    schema_name = config("PERSEPHONE_SCHEMA")

    @classmethod
    async def register_user_log(cls, user_model: UserModel):
        message = user_model.get_audit_prospect_user_template()
        (
            success,
            status_sent_to_persephone
        ) = await cls.audit_client.send_to_persephone(
            topic=cls.topic,
            partition=cls.partition,
            message=message,
            schema_name=cls.schema_name,
        )
        if not success:
            Gladsheim.error(message="Audit::register_user_log::Error on trying to register log")
            raise ErrorOnSendAuditLog
