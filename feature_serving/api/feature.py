from fastapi import APIRouter, Depends, HTTPException
from fastapi import APIRouter, Query
import datetime
from sqlalchemy.orm import Session
from feature_serving.config import SessionLocal
from feature_serving.models import features
from feature_serving.schemas import feature as schemas
from feature_retrieval.retriever import retrieve_features
from feature_retrieval.offline import get_offline_features
from feature_retrieval.online import get_online_features
from tracker.logger import log_retrieval
from feature_sync.sync_to_redis import sync_all_features


router = APIRouter(prefix="/features")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.FeatureResponse)
def create_feature(f: schemas.FeatureCreate, db: Session = Depends(get_db)):
    db_f = features.Feature(**f.dict())
    db.add(db_f)
    db.commit()
    db.refresh(db_f)
    return db_f

@router.get("/{id}", response_model=schemas.FeatureResponse)
def get_feature(id: int, db: Session = Depends(get_db)):
    f = db.query(features.Feature).filter_by(id=id).first()
    if not f:
        raise HTTPException(status_code=404, detail="Feature Not Found")
    return f

@router.get("/offline", response_model=schemas.FeatureValueResponse)
def get_offline(entity_id: str, features: list[str] = Query(...), date: str = None):
    result = retrieve_features(entity_id=entity_id, feature_names=features, source="offline", date=date)
    log_retrieval(source="offline", entity_id=entity_id, features=features)
    return {
        "entity_id": entity_id,
        "source": "offline",
        "features": result
    }

@router.get("/online", response_model=schemas.FeatureValueResponse)
def get_online(entity_id: str, features: list[str] = Query(...)):
    result = retrieve_features(entity_id=entity_id, feature_names=features, source="online")
    freshness = {}
    from feature_retrieval.config import redis_client
    now = datetime.utcnow()
    for feature in features:
        ts_key = f"{entity_id}:{feature}:timestamp"
        ts_val = redis_client.get(ts_key)
        if ts_val:
            freshness[feature] = (now - datetime.fromisoformat(ts_val)).total_seconds()
    log_retrieval(source="online", entity_id=entity_id, features=features)
    return {
        "entity_id": entity_id,
        "source": "online",
        "features": result,
        "freshness_seconds": freshness
    }

@router.post("/sync")
def sync_features_to_redis(date: str = None):
    sync_date = date or datetime.today().strftime("%Y-%m-%d")
    sync_all_features(sync_date)
    return {
        "message": f"Features synced to Redis for date {sync_date}",
        "status": "success"
    }