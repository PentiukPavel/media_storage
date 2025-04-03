from pydantic import BaseModel


class MediaFileRetrieve(BaseModel):
    id: int
    file_url: str
    filename: str
    owner_id: int
