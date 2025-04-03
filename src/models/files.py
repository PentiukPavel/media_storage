from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy_utils import URLType

from core.database import Base, CommonMixin
from schemes import MediaFileRetrieve


class MedeaFile(CommonMixin, Base):

    filename: Mapped[String] = Column(String(length=100), nullable=False)
    file_url: Mapped[str] = Column(URLType, nullable=False)
    owner_id: Mapped[int] = Column(
        Integer, ForeignKey("user.id"), nullable=False
    )

    owner = relationship("User", back_populates="media_files")

    def to_read_model(self) -> MediaFileRetrieve:
        return MediaFileRetrieve(
            id=self.id,
            file_url=self.file_url,
            filename=self.filename,
            owner_id=self.owner_id,
        )
