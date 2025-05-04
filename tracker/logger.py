from datetime import datetime
from typing import List
import traceback
from feature_retrieval.config import redis_client
from tracker.db import get_db_conn

def update_last_updated(conn, feature_names: List[str], run_id=None):
    now = datetime.utcnow()
    cursor = conn.cursor()
    for name in feature_names:
        cursor.execute("UPDATE features SET last_updated = %s WHERE name = %s", (now, name))
        log_materialization(
            conn=conn,
            feature_name=name,
            run_id=run_id,
            status="success",
            duration=0.0
        )
    conn.commit()
    cursor.close()
    print(f"[✓] Updated last_updated for: {feature_names}")

def log_materialization(conn, feature_name, run_id=None, status="success", duration=0.0, error_message=None):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO materialization_log (feature_name, run_id, status, duration_seconds, error_message)
        VALUES (%s, %s, %s, %s, %s)
    """, (feature_name, run_id, status, duration, error_message))
    conn.commit()
    cursor.close()
    print(f"[LOG] Feature: {feature_name} → {status}")

def log_retrieval(source: str, entity_id: str, features: List[str]):
    conn = get_db_conn()
    cursor = conn.cursor()
    now = datetime.utcnow()

    for feature in features:
        freshness = None
        if source == "online":
            ts_key = f"{entity_id}:{feature}:timestamp"
            ts_value = redis_client.get(ts_key)
            if ts_value:
                freshness = (now - datetime.fromisoformat(ts_value)).total_seconds()

        cursor.execute("""
            INSERT INTO retrieval_log (source, entity_id, feature_name, freshness_seconds)
            VALUES (%s, %s, %s, %s)
        """, (source, entity_id, feature, freshness))
    
    conn.commit()
    cursor.close()
    print(f"[LOG] Retrieval from {source} for entity {entity_id} and features {features}")