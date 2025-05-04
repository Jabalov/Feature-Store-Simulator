from pydantic import BaseModel
from typing import Dict, List, Optional

class FeatureCreate(BaseModel):
    name: str
    description: Optional[str]
    data_type: str
    owner: str
    feature_group_id: int

class FeatureResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    data_type: str
    owner: str
    feature_group_id: int
    last_updated: Optional[str]

class FeatureValueResponse(BaseModel):
    entity_id: str
    source: str
    features: Dict[str, Optional[str]]
    freshness_seconds: Optional[Dict[str, float]] = None
