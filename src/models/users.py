from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, relationship

from core.database import Base, CommonMixin
from schemes import UserRetrieve


class User(CommonMixin, Base):

    email: Mapped[String] = Column(
        String(length=250),
        index=True,
        unique=True,
        nullable=False,
    )

    media_files = relationship(
        "MedeaFile", back_populates="owner", uselist=True
    )

    def to_read_model(self) -> UserRetrieve:
        return UserRetrieve(
            id=self.id,
            email=self.email,
        )
