from pydantic import BaseModel

class FeatureGroupCreate(BaseModel):
    name: str
    description: str
    owner: str

class FeatureGroupResponse(FeatureGroupCreate):
    id: int
