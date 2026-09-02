# -*- coding: utf-8 -*-
import sqlite3
import json
import os
import time
import sys

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scraper"))

from ad_library_ingest import FortifiedAdSpendIngest
from auto_suburb_expander import AutoSuburbExpander

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'directory.db')

def run_hourly_broker_cycle():
    """
    Fortified 24h Autonomous Cadence Loop:
    1. Ingests Ad-Spend Intelligence with Anomaly Protection
    2. Runs Anti-Thin-Content Suburb Expander (6 Dynamic Dimensions)
    3. Reconciles Banked Cash Flow & Active $99/mo MRR Subscriptions
    4. Records Telemetry in SQLite Logs
    """
    # 1. Run Ad Spend Intelligence Ingestion (With Anomaly Circuit Breaker)
    ad_agent = FortifiedAdSpendIngest()
    ad_res = ad_agent.ingest_ad_spenders()

    # 2. Run Anti-Thin-Content Suburb Expander
    suburb_agent = AutoSuburbExpander()
    suburb_res = suburb_agent.expand_winning_suburbs()

    # 3. Calculate Live Banked Telemetry
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) as total_revenue FROM payouts WHERE status = 'COMPLETED'")
    total_rev = cursor.fetchone()['total_revenue'] or 0

    cursor.execute("SELECT COUNT(*) as total_leads FROM leads")
    total_leads = cursor.fetchone()['total_leads']

    cursor.execute("SELECT COUNT(*) as total_vendors FROM vendors")
    total_vendors = cursor.fetchone()['total_vendors']

    cursor.execute("SELECT COUNT(*) as active_subscribers FROM vendors WHERE subscription_active = 1")
    active_subs = cursor.fetchone()['active_subscribers']

    cursor.execute("SELECT COUNT(*) as pending_anomalies FROM anomaly_queue WHERE status = 'PENDING_REVIEW'")
    pending_anomalies = cursor.fetchone()['pending_anomalies']

    log_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_revenue_banked": total_rev,
        "active_mrr": active_subs * 99,
        "total_leads_brokered": total_leads,
        "total_directory_listings": total_vendors,
        "ad_spenders_monitored": ad_res["normal_classified_spenders"],
        "anomalies_held_in_queue": pending_anomalies,
        "indexed_sitemap_urls": suburb_res["total_indexed_urls"],
        "status": "HEALTHY_FORTIFIED_CADENCE_ACTIVE"
    }

    cursor.execute("""
    INSERT INTO logs (event_type, message, details)
    VALUES (?, ?, ?)
    """, ("CADENCE_LOOP_COMPLETE", "Fortified 24h Marketing Agent Cadence Cycle complete", json.dumps(log_entry)))

    conn.commit()
    conn.close()
    return log_entry

if __name__ == '__main__':
    res = run_hourly_broker_cycle()
    print(json.dumps(res))
