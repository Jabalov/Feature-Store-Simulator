from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from feature_serving.config import Base
from sqlalchemy.sql import func


class FeatureGroup(Base):
    __tablename__ = "feature_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    owner = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
