from pyspark.sql import SparkSession
from feature_retrieval.redis_writer import write_features_to_redis
from feature_retrieval.config import OFFLINE_STORE_BASE
import os
from datetime import datetime
import argparse

spark = SparkSession.builder.appName("RedisSync").getOrCreate()

import os

def get_available_features(base_path):
    return [
        name for name in os.listdir(base_path)
        if os.path.isdir(os.path.join(base_path, name))
    ]

def sync_parquet_to_redis(feature_name: str, date: str):
    path = os.path.join(OFFLINE_STORE_BASE, feature_name, f"date={date}")
    try:
        df = spark.read.parquet(path)
        for row in df.collect():
            entity_id = row["entity_id"]
            value = row[feature_name]
            if value is not None:
                write_features_to_redis(entity_id, {feature_name: value})
    except Exception as e:
        print(f"[ERROR] Syncing {feature_name}: {e}")

def sync_all_features(date: str):
    feature_list = get_available_features(OFFLINE_STORE_BASE)
    for feature in feature_list:
        sync_parquet_to_redis(feature, date)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str, default=datetime.today().strftime("%Y-%m-%d"))
    args = parser.parse_args()

    print(f"Syncing features to Redis for date: {args.date}")
    sync_all_features(args.date)
    print("Sync complete.")
