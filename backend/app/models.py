from sqlalchemy import Integer, String, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Candidate(Base):
    __tablename__ = "candidates"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    role: Mapped[str] = mapped_column(String(100), nullable=False)
    department: Mapped[str] = mapped_column(String(80), nullable=False)
    experience: Mapped[int] = mapped_column(Integer, default=0)
    resume_score: Mapped[float] = mapped_column(Float, nullable=False)
    assessment_score: Mapped[float] = mapped_column(Float, nullable=False)
    technical_score: Mapped[float] = mapped_column(Float, nullable=False)
    hr_score: Mapped[float] = mapped_column(Float, nullable=False)
    skills: Mapped[dict] = mapped_column(JSON, default=dict)
    recommendations: Mapped[list] = mapped_column(JSON, default=list)
