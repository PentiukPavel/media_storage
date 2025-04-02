from pydantic import BaseModel


class MediaFileCreate(BaseModel):
    filename: str


class MediaFileRetrieve(MediaFileCreate):
    id: int
    image_url: str
