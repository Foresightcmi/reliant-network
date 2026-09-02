# -*- coding: utf-8 -*-
import json
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "directory.db")

NICHE_PRICING_MATRIX = {
    "luxury_restrooms": {
        "name": "Luxury Restroom Trailers",
        "base_lead_price": 85,
        "contract_range": [2500, 12000],
        "deposit_pct": 0.15
    },
    "commercial_cold_storage": {
        "name": "Commercial Mobile Cold Storage",
        "base_lead_price": 125,
        "contract_range": [3500, 18000],
        "deposit_pct": 0.15
    },
    "heavy_crane_rigging": {
        "name": "Heavy Crane & Rigging Rental",
        "base_lead_price": 175,
        "contract_range": [5000, 35000],
        "deposit_pct": 0.15
    }
}

class MultiNicheRevenueSplitter:
    def __init__(self):
        self.db_path = DB_PATH

    def calculate_lead_brokerage(self, niche_id, estimated_contract_value):
        config = NICHE_PRICING_MATRIX.get(niche_id, NICHE_PRICING_MATRIX["luxury_restrooms"])
        base_lead_fee = config["base_lead_price"]
        
        # Scale lead fee dynamically if contract value is high-ticket
        if estimated_contract_value > 10000:
            final_lead_fee = int(base_lead_fee * 1.4)
        elif estimated_contract_value > 20000:
            final_lead_fee = int(base_lead_fee * 1.8)
        else:
            final_lead_fee = base_lead_fee

        deposit_fee = round(estimated_contract_value * config["deposit_pct"], 2)

        return {
            "niche_id": niche_id,
            "niche_name": config["name"],
            "estimated_contract_value": estimated_contract_value,
            "pay_per_lead_fee": final_lead_fee,
            "estimated_15pct_booking_deposit": deposit_fee,
            "operator_net_take_home": round(estimated_contract_value - deposit_fee, 2)
        }

    def get_portfolio_financial_summary(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT SUM(amount) as total_rev FROM payouts WHERE status = 'COMPLETED'")
        total_rev = cursor.fetchone()["total_rev"] or 0

        cursor.execute("""
        SELECT niche_id, COUNT(*) as vendor_count, SUM(subscription_active) as active_subscribers
        FROM vendors GROUP BY niche_id
        """)
        niche_breakdown = [dict(r) for r in cursor.fetchall()]

        cursor.execute("SELECT COUNT(*) FROM leads")
        total_leads = cursor.fetchone()[0]

        total_mrr = sum((r["active_subscribers"] or 0) * 99 for r in niche_breakdown)

        conn.close()

        return {
            "total_banked_cash_flow": total_rev,
            "portfolio_active_mrr": total_mrr,
            "total_brokered_leads": total_leads,
            "niche_portfolio_breakdown": niche_breakdown
        }

if __name__ == "__main__":
    splitter = MultiNicheRevenueSplitter()
    summary = splitter.get_portfolio_financial_summary()
    print("Portfolio Financial Summary:", json.dumps(summary, indent=2))
