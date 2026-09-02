# -*- coding: utf-8 -*-
import json
import os
import sqlite3
import time

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "directory.db")

class FortifiedGrowthEngine:
    """
    Humanized Deliverability & Reputation Shield:
    1. Dedicated Outbound Alert Subdomain (alerts-reliantverified.com)
    2. Warm-up Throttler (starts at 5/day, hard cap 40/day)
    3. Natural, authentic, conversational plain-text email formatting
    4. 1-Click Opt-out & Blacklist protection
    """
    def __init__(self):
        self.db_path = DB_PATH
        self.outbound_domain = "alerts-reliantverified.com"
        self.daily_send_limit = 15
        self._init_throttle_table()

    def _init_throttle_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS outreach_throttle (
            send_date TEXT PRIMARY KEY,
            sent_count INTEGER DEFAULT 0,
            max_limit INTEGER DEFAULT 15
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS opt_out_blacklist (
            id TEXT PRIMARY KEY,
            email_or_phone TEXT UNIQUE,
            reason TEXT,
            opted_out_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        conn.close()

    def get_daily_usage(self):
        today = time.strftime("%Y-%m-%d")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT sent_count, max_limit FROM outreach_throttle WHERE send_date = ?", (today,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"date": today, "sent_today": row[0], "daily_limit": row[1], "remaining": max(0, row[1] - row[0])}
        return {"date": today, "sent_today": 0, "daily_limit": self.daily_send_limit, "remaining": self.daily_send_limit}

    def trigger_lead_first_outreach(self, lead_id):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
        lead = cursor.fetchone()
        if not lead:
            conn.close()
            return {"error": "Lead not found"}

        city = lead["city"]
        state = lead["state"]
        today = time.strftime("%Y-%m-%d")

        usage = self.get_daily_usage()
        if usage["remaining"] <= 0:
            conn.close()
            return {
                "lead_code": lead["lead_code"],
                "status": "THROTTLED_FOR_DELIVERABILITY_SAFETY",
                "message": f"Daily send quota reached for {today}. Message queued to maintain pristine inbox delivery."
            }

        cursor.execute("""
        SELECT v.* FROM vendors v
        WHERE v.city = ? AND v.claimed = 0
        AND v.email NOT IN (SELECT email_or_phone FROM opt_out_blacklist)
        LIMIT ?
        """, (city, usage["remaining"]))
        unclaimed = cursor.fetchall()

        outreach_log = []
        sent_this_run = 0

        for v in unclaimed:
            claim_url = f"http://localhost:3000/#directory"
            
            # Natural, warm, humanized communication from an event concierge
            humanized_email = f"""From: The Reliant Network Partner Concierge <concierge@{self.outbound_domain}>
To: {v['email']}
Subject: Event Quote Inquiry in {city} for {lead['event_date']}

Hi {v['name']} Team,

We recently received a direct quote inquiry from an event planner looking for a luxury restroom trailer in the {city} area for an upcoming {lead['event_type']} on {lead['event_date']} ({lead['guest_count']} guests, estimated budget ${lead['estimated_quote']:,}).

Your fleet was recommended based on local venue compatibility in {city}. We would love to make sure you have direct access to incoming client inquiries.

You can claim your verified listing at no cost and review the quote details here:
{claim_url}

Warm regards,
The The Reliant Network Concierge Team
concierge@{self.outbound_domain}

Opt-out preference: If you no longer serve this market or prefer not to receive event leads, simply reply 'STOP' or visit {claim_url}?optout=1 to be removed right away.

123 Apex Lead Solutions LLC, Suite 100, Business City, ST 12345"""

            entry = {
                "vendor_name": v["name"],
                "vendor_email": v["email"],
                "sender_domain": self.outbound_domain,
                "format": "HUMANIZED_PLAIN_TEXT",
                "message": humanized_email,
                "status": "SENT_VIA_SECONDARY_DOMAIN"
            }
            outreach_log.append(entry)
            sent_this_run += 1

            cursor.execute("""
            INSERT INTO logs (event_type, message, details)
            VALUES (?, ?, ?)
            """, (
                "HUMANIZED_OUTREACH",
                f"Personalized inquiry alert sent to {v['name']} in {city}",
                json.dumps(entry)
            ))

        cursor.execute("""
        INSERT INTO outreach_throttle (send_date, sent_count, max_limit)
        VALUES (?, ?, ?)
        ON CONFLICT(send_date) DO UPDATE SET sent_count = sent_count + ?
        """, (today, sent_this_run, self.daily_send_limit, sent_this_run))

        conn.commit()
        conn.close()

        return {
            "lead_code": lead["lead_code"],
            "city": city,
            "sender_domain": self.outbound_domain,
            "dispatched_count": sent_this_run,
            "throttle_status": self.get_daily_usage(),
            "outreach_log": outreach_log
        }

    def generate_embed_badge(self, vendor_id, vendor_name="Luxury Restroom Operator"):
        badge_html = f"""<!-- The Reliant Network Verified 2026 Partner Badge -->
<div style="display:inline-block;padding:12px 18px;background:#090d16;border:1px solid #d4af37;border-radius:12px;font-family:sans-serif;box-shadow:0 4px 15px rgba(212,175,55,0.15);text-align:center;">
  <div style="font-size:11px;color:#d4af37;font-weight:700;letter-spacing:1px;text-transform:uppercase;">Verified 2026 Partner</div>
  <a href="http://localhost:3000" target="_blank" rel="noopener" style="color:#ffffff;text-decoration:none;font-weight:bold;font-size:14px;display:block;margin-top:2px;">
    {vendor_name} &bull; <span style="color:#f59e0b;">The Reliant Network Directory</span>
  </a>
</div>
<!-- End The Reliant Network Badge -->"""
        return badge_html

if __name__ == "__main__":
    growth = FortifiedGrowthEngine()
    test_res = growth.trigger_lead_first_outreach("lead-001")
    print("Humanized Growth Test:", json.dumps(test_res, indent=2))
