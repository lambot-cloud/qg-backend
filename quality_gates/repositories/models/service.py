from datetime import datetime
from sqlalchemy import func, Column, Integer, String, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from quality_gates.repositories.models.base import Base


class Service(Base):
    __tablename__ = 'services'
    __table_args__ = (
        UniqueConstraint('information_system', 'service_name', name='_is_service_unique_pair_uc'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    information_system: Mapped[str] = mapped_column(String, nullable=False)
    service_name: Mapped[str] = mapped_column(String, nullable=False)
    monitoring: Mapped[str] = mapped_column(Boolean, nullable=True)
    observability: Mapped[str] = mapped_column(Boolean, nullable=True)
    unit_testing_enabled: Mapped[str] = mapped_column(Boolean, nullable=True)
    unit_testing: Mapped[str] = mapped_column(String, nullable=True, server_default=str("Not running"))
    description: Mapped[str] = mapped_column(String, nullable=True)
    update_date: Mapped[str] = mapped_column(String, nullable=True, server_default=str("Not running"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=func.now(), nullable=True)
    git_url: Mapped[str] = mapped_column(String, nullable=True)
    git_branch: Mapped[str] = mapped_column(String, nullable=True)
    ci_pipeline_url: Mapped[str] = mapped_column(String, nullable=True)
    cm_key: Mapped[str] = mapped_column(String, nullable=True)
    qg_status: Mapped[str] = mapped_column(String, nullable=True)
    platform: Mapped[str] = mapped_column(String, nullable=True)
    zone: Mapped[str] = mapped_column(String, nullable=True)
