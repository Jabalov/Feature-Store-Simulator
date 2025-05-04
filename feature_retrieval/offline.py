from pyspark.sql import SparkSession
from datetime import datetime
from typing import List
import os

from .config import OFFLINE_STORE_BASE

spark = SparkSession.builder.appName("FeatureRetrieverOffline").getOrCreate()

def load_feature_from_parquet(feature_name: str, entity_id: str, date: str = None):
    date = date or datetime.today().strftime("%Y-%m-%d")
    path = os.path.join(OFFLINE_STORE_BASE, feature_name, f"date={date}")
    
    try:
        df = spark.read.parquet(path)
        filtered = df.filter(df.entity_id == entity_id)
        return filtered.collect()[0].asDict()
    except Exception as e:
        print(f"[ERROR] Loading {feature_name} failed: {e}")
        return None

def get_offline_features(entity_id: str, feature_names: List[str], date: str = None):
    result = {}
    for feature in feature_names:
        data = load_feature_from_parquet(feature, entity_id, date)
        if data and feature in data:
            result[feature] = data[feature]
    return result
