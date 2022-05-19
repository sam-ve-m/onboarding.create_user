# Jormungandr
from ...domain.exceptions import ErrorOnSendAuditLog
from ...domain.enums.queue.types import QueueTypes
from ...infrastructures.env_config import config

# Third party
from etria_logger import Gladsheim
from persephone_client import Persephone


class Audit:
    audit_client = Persephone

    @classmethod
    async def register_user_log(cls, user):
        partition = QueueTypes.PROSPECT_USER.value
        topic = config("PERSEPHONE_TOPIC_USER")
        schema_name = config("PERSEPHONE_SCHEMA")
        (
            success,
            status_sent_to_persephone
        ) = await cls.audit_client.send_to_persephone(
            topic=topic,
            partition=partition,
            message=user,
            schema_name=schema_name,
        )
        if not success:
            Gladsheim.error(message="Audit::register_user_log::Error on trying to register log")
            raise ErrorOnSendAuditLog
