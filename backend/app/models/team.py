import uuid
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class TeamMember(Base):
    __tablename__ = "team_members"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(120))
    role: Mapped[str] = mapped_column(String(120))
    contribution: Mapped[str] = mapped_column(Text)
    skills: Mapped[str] = mapped_column(Text, default="")
    linkedin: Mapped[str] = mapped_column(String(500), default="")
    github: Mapped[str] = mapped_column(String(500), default="")
