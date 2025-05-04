from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lit
import os
from datetime import datetime
from tracker.db import get_db_conn
from tracker.logger import log_materialization, update_last_updated
import time



spark = SparkSession.builder \
    .appName("TelcoFeatureEngineering") \
    .config("spark.hadoop.io.native.lib.available", "false") \
    .getOrCreate()

df = spark.read.csv("data/raw/Telco-Customer-Churn.csv", header=True, inferSchema=True)

df = df.withColumn("TotalCharges", when(col("TotalCharges") == " ", None).otherwise(col("TotalCharges").cast("float")))
tenure_df = df.select(col("customerID").alias("entity_id"), col("tenure").alias("tenure_months"))

fiber_df = df.select(
    col("customerID").alias("entity_id"),
    when(col("InternetService") == "Fiber optic", lit(1)).otherwise(lit(0)).alias("has_fiber_optic")
)

monthly_df = df.select(col("customerID").alias("entity_id"), col("MonthlyCharges").alias("monthly_charges"))

output_base = "data/processed/offline_store/telco"
today = datetime.today().strftime("%Y-%m-%d")

try:
    start = time.time()
    tenure_df.write.mode("overwrite").parquet(f"{output_base}/tenure_months/date={today}")
    fiber_df.write.mode("overwrite").parquet(f"{output_base}/has_fiber_optic/date={today}")
    monthly_df.write.mode("overwrite").parquet(f"{output_base}/monthly_charges/date={today}")

    print("✅ Features written to offline store")    
    duration = time.time() - start
    conn = get_db_conn()
    update_last_updated(conn, ["tenure_months", "has_fiber_optic", "monthly_charges"], run_id="run_20250422")
except Exception as e:
    conn = get_db_conn()
    from tracker.logger import log_materialization
    log_materialization(conn, feature_name=["tenure_months", "has_fiber_optic", "monthly_charges"], run_id="run_20250422", status="failed", error_message=str(e))
    raise