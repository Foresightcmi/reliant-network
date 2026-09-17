# -*- coding: utf-8 -*-
"""
Autonomous Operator Outreach Generator (Frey Chu Methodology)
Provides permission-first cold email and SMS outreach drafts for unverified operators.
Operates at $0 marginal cost with Check-Behind Supervision for the Entrepreneur.
"""

import os
import sys
import json
import sqlite3
import argparse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "directory.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def list_unclaimed_operators(city=None, limit=20):
    conn = get_db()
    cursor = conn.cursor()
    if city:
        cursor.execute("SELECT id, name, city, state, email, phone, rating, review_count FROM vendors WHERE claimed = 0 AND city LIKE ? LIMIT ?", (f"%{city}%", limit))
    else:
        cursor.execute("SELECT id, name, city, state, email, phone, rating, review_count FROM vendors WHERE claimed = 0 LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def generate_cold_outreach(vendor):
    city = vendor.get("city", "Atlanta")
    state = vendor.get("state", "GA")
    name = vendor.get("name", "Local Fleet")
    rating = vendor.get("rating", 4.9)
    claim_url = f"https://reliant-network.vercel.app/claim?id={vendor.get('id', '')}"
    badge_url = f"https://reliant-network.vercel.app/badge-generator.html"

    sms = f"Hey {name} team! Just tried reaching you regarding your luxury restroom fleet in {city}. Are you currently taking on new commercial or wedding rentals for upcoming weekends?"

    email_touchpoint_1 = f"""Subject: Quick question regarding {name} / {city} fleet radius

Hi {name} Team,

I was reviewing top-rated commercial sanitation and luxury restroom providers in {city} today and noticed that your directory profile on The Reliant Network ({rating}★ rating) is currently unclaimed.

Because it's unclaimed, your direct phone and booking link are not displaying when event planners and general contractors in {city} search our directory.

I put together a quick visibility summary of how many client quote inquiries are coming through your service radius. Would you be open to me sending that over?

Best regards,

Operations Concierge
The Reliant Network
https://reliant-network.vercel.app
"""

    email_touchpoint_2_fomo = f"""Subject: Missed customer quote request in {city} — {name}

Hi {name} Team,

An event coordinator in {city} just submitted a quote request on The Reliant Network for a luxury restroom trailer (Estimated booking value: $2,200 - $3,500).

Because your listing on our directory is currently unclaimed, our system automatically routed this inquiry to a verified competitor in your territory.

We route customer quote requests in {city} every week. You can claim your profile for free in 45 seconds to receive future inquiries directly:

👉 Claim Your Fleet Profile (Free): {claim_url}
👉 Get Your Vetted 2026 Partner Badge: {badge_url}

Best regards,

Operations Concierge
The Reliant Network
"""

    return {
        "vendor": name,
        "city": city,
        "phone": vendor.get("phone", "N/A"),
        "email": vendor.get("email", "N/A"),
        "touchpoint_1_sms": sms,
        "touchpoint_1_email": email_touchpoint_1,
        "touchpoint_2_fomo": email_touchpoint_2_fomo
    }

def main():
    parser = argparse.ArgumentParser(description="Operator Outreach Generator")
    parser.add_argument("--list-unclaimed", action="store_true", help="List unclaimed operators")
    parser.add_argument("--city", type=str, help="Filter by city (e.g. Atlanta, Dallas)")
    parser.add_argument("--generate-drafts", action="store_true", help="Generate outreach drafts")
    parser.add_argument("--limit", type=int, default=5, help="Number of operators to process")
    args = parser.parse_args()

    if args.list_unclaimed:
        operators = list_unclaimed_operators(city=args.city, limit=args.limit)
        print(f"\n[FOUND {len(operators)} UNCLAIMED OPERATORS in {args.city or 'All Cities'}]:")
        for o in operators:
            print(f" - {o['name']} ({o['city']}, {o['state']}) | Phone: {o['phone']} | Email: {o['email']}")
        return

    if args.generate_drafts:
        operators = list_unclaimed_operators(city=args.city, limit=args.limit)
        print(f"\n{'='*70}\nFREY CHU OPERATOR OUTREACH CAMPAIGN DRAFTS\n{'='*70}\n")
        for o in operators:
            draft = generate_cold_outreach(o)
            print(f"--- OPERATOR: {draft['vendor']} ({draft['city']}) ---")
            print(f"PHONE: {draft['phone']} | EMAIL: {draft['email']}")
            print(f"\n[TOUCHPOINT 1 - CURIOSITY SMS]:\n{draft['touchpoint_1_sms']}\n")
            print(f"[TOUCHPOINT 1 - PERMISSION EMAIL]:\n{draft['touchpoint_1_email']}\n")
            print(f"[TOUCHPOINT 2 - MISSED LEAD FOMO EMAIL]:\n{draft['touchpoint_2_fomo']}\n")
            print("-" * 70)
        return

    # Default: Show quick demo
    operators = list_unclaimed_operators(city="Atlanta", limit=2)
    if operators:
        draft = generate_cold_outreach(operators[0])
        print("\n[SAMPLE FREY CHU OUTREACH DRAFT]:")
        print(draft['touchpoint_1_email'])

if __name__ == "__main__":
    main()
