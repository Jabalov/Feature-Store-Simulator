from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from feature_serving.config import Base
from sqlalchemy.sql import func

class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    feature_group_id = Column(Integer, ForeignKey("feature_groups.id"))
    data_type = Column(String)
    description = Column(Text)
    transformation = Column(Text)
    source_table = Column(String)
    version = Column(Integer, default=1)
    ttl_days = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())
    last_updated = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
