import uuid
from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class PowerBIDashboard(Base):
    __tablename__ = "powerbi_dashboards"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, default="")
    embed_url: Mapped[str] = mapped_column(String(2000))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
