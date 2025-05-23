from datetime import datetime


class TokenEntity:
    def __init__(self
                 , id: int
                 , user_id: int
                 , token: str
                 , is_active: bool
                 , created_at: datetime
                 , expires_at: datetime):
        self.id = id
        self.user_id = user_id
        self.token = token
        self.is_active = is_active
        self.created_at = created_at
        self.expires_at = expires_at