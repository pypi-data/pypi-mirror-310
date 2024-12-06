import pydantic

class User(pydantic.BaseModel):
    id: int
    username: str
    displayname: str=None

class Reason(pydantic.BaseModel):
    fr: str
    en: str
    es: str

class UserBlacklist(pydantic.BaseModel):
    isBlacklisted: bool
    user: User
    reason: Reason

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