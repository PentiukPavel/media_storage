from pydantic import BaseModel


class MediaFileRetrieve(BaseModel):
    id: int
    image_url: str
    filename: str
