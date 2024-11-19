from sqlalchemy import Boolean, Column, Integer, String

from .db import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    short_url = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)
