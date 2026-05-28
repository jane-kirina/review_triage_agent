from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    Text,
    Numeric,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.sql import func

from src.db.database import Base


class App(Base):
    __tablename__ = "apps"

    app_id = Column(Text, primary_key=True)
    app_name = Column(Text, nullable=False)
    description = Column(Text)
    score = Column(Numeric)
    ratings_count = Column(BigInteger)
    downloads = Column(BigInteger)
    content_rating = Column(Text)
    categories = Column(Text)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    app_id = Column(Text, ForeignKey("apps.app_id"), index=True)

    review_text = Column(Text, nullable=False)
    review_score = Column(Integer)
    review_date = Column(DateTime)
    helpful_count = Column(Integer)

    review_hash = Column(Text, nullable=False, unique=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("review_hash", name="uq_reviews_review_hash"),
    )