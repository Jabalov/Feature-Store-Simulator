from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from feature_serving.config import SessionLocal
from feature_serving.models import feature_groups
from feature_serving.schemas import feature_group as schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.FeatureGroupResponse)
def create_feature_group(fg: schemas.FeatureGroupCreate, db: Session = Depends(get_db)):
    db_fg = feature_groups.FeatureGroup(**fg.dict())
    db.add(db_fg)
    db.commit()
    db.refresh(db_fg)
    return db_fg

@router.get("/{id}", response_model=schemas.FeatureGroupResponse)
def get_feature_group(id: int, db: Session = Depends(get_db)):
    fg = db.query(feature_groups.FeatureGroup).filter_by(id=id).first()
    if not fg:
        raise HTTPException(status_code=404, detail="Feature Group Not Found")
    return fg
