from datetime import datetime


class ProspectUserModel:
    def __init__(self, user: dict):
        self.email = user.get('email')
        self.nickname = user.get('nickname')
        self.unique_id = user.get('unique_id')
        self.create_user_time_stamp = int(datetime.utcnow().timestamp())

    def to_dict(self) -> dict:
        prospect_user = {
            "unique_id": self.unique_id,
            "email": self.email,
            "nickname": self.nickname,
            "create_user_time_stamp": self.create_user_time_stamp
        }
        return prospect_user
