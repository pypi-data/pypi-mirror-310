from typing import TypedDict

class Reason(TypedDict):
    fr_fr: str
    en_gb: str
    es_sp: str

class User(TypedDict):
    id: int
    username: str
    displayname: str

class BlacklistUser(TypedDict):
    isBlacklisted: bool
    user: User
    reasons: Reason