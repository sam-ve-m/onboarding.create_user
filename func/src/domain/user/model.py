# Jormungandr
from ..enums.user.features import Features
from ..enums.user.level import UserLevel
from ..enums.user.view_type import ViewType

# Standards
from datetime import datetime
from uuid import uuid4


class Scope:
    def __init__(self):
        self.user_level = UserLevel.PROSPECT
        self.view_type = ViewType.DEFAULT
        self.features = [Features.DEFAULT]


class UserModel:
    def __init__(self, email: str, nickname: str):
        self.email = email
        self.nickname = nickname
        self.unique_id = str(uuid4())
        self.created_at = datetime.utcnow()
        self.scope = Scope()
        self.is_active_user = False
        self.must_to_first_login = True
        self.token_valid_after = datetime.utcnow()
        self.terms = {}

    def to_dict(self) -> dict:
        user_metadata = {
            "email": self.email,
            "nick_name": self.nickname,
            "unique_id": self.unique_id,
            "created_at": self.created_at,
            "scope": {
                "user": self.scope.user_level,
                "view_type": self.scope.view_type,
                "features": self.scope.features,
            },
            "is_active_user": self.is_active_user,
            "must_do_first_login": self.must_to_first_login,
            "token_valid_after": self.token_valid_after,
            "terms": self.terms,
        }
        return user_metadata

    def get_audit_prospect_user_template(self) -> dict:
        prospect_user_template = {
            "unique_id": self.unique_id,
            "email": self.email,
            "nick_name": self.nickname,
            "create_user_time_stamp": int(datetime.utcnow().timestamp()),
        }
        return prospect_user_template
