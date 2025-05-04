from fastapi import FastAPI
from feature_serving.api import feature, feature_group
from feature_serving.config import Base, engine

app = FastAPI(title="Feature Store Simulator API")

app.include_router(feature.router, prefix="/feature", tags=["Feature"])
app.include_router(feature_group.router, prefix="/feature-group", tags=["Feature Group"])
