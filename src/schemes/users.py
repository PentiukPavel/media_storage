from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str


class Code(BaseModel):
    code: str


class UserRetrieve(BaseModel):
    id: int
    email: str
