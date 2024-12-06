import pydantic



class Reason(pydantic.BaseModel):
    fr_fr: str
    en_gb: str
    es_sp: str

class User(pydantic.BaseModel):
    id: int
    username: str
    blacklisted_reasons: Reason

class UserBlacklist(pydantic.BaseModel):
    isBlacklisted: bool
    user: User


class MetadataEvent(pydantic.BaseModel):
    add: bool
    remove: bool

class Metadata(pydantic.BaseModel):
    event: MetadataEvent
    webhook_url: str

class UserBlacklistWebhook(pydantic.BaseModel):
    user: User
    reason: Reason
    metadata: dict