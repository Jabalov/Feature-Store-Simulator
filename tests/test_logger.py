import pytest
from tracker.logger import update_last_updated, log_retrieval
from tracker.db import get_db_conn

def test_update_last_updated():
    conn = get_db_conn()
    update_last_updated(conn, ["tenure_months"], run_id="test_run")

def test_log_retrieval():
    conn = get_db_conn()
    log_retrieval("online", "0001-XYZ", ["monthly_charges"])
