from datetime import datetime
from sqlalchemy import func, Column, Integer, String, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from quality_gates.repositories.models.base import Base


class Trusted(Base):
    __tablename__ = 'trusted_images'
    __table_args__ = (
        UniqueConstraint('image_url', name='_image_url_uc'),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    image_name: Mapped[str] = mapped_column(String, nullable=None)
    image_url: Mapped[str] = mapped_column(String, nullable=None)
    image_status: Mapped[str] = mapped_column(String, nullable=None)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=func.now(), nullable=True)