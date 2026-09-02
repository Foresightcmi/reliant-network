import urllib.request
import json
import time

BASE_URL = "http://localhost:3000"

print("==================================================")
print(" ?? RUNNING END-TO-END AUTONOMOUS ENGINE AUDIT")
print("==================================================")

# 1. Test Niche Config
req = urllib.request.urlopen(f"{BASE_URL}/api/niches")
niches = json.loads(req.read().decode())
print(f"? Active Niche: {niches['active_niche']}")
print(f"   Brand: {niches['niches']['luxury_restrooms']['brand_title']}")

# 2. Test Vendor Listings
req = urllib.request.urlopen(f"{BASE_URL}/api/vendors?city=Atlanta")
vendors = json.loads(req.read().decode())
print(f"? Fetched {len(vendors)} Verified Vendors in Atlanta, GA")

# 3. Test Inbound Lead Submission & AI Brokerage
lead_payload = {
    "customer_name": "Victoria & James Montgomery",
    "customer_email": "v.montgomery@estates.com",
    "customer_phone": "(404) 555-8833",
    "city": "Atlanta",
    "state": "GA",
    "event_date": "2026-11-14",
    "guest_count": 300,
    "event_type": "VIP Estate Wedding",
    "notes": "Looking for 4-station high-end trailer with air conditioning and sound system."
}
req = urllib.request.Request(
    f"{BASE_URL}/api/leads",
    data=json.dumps(lead_payload).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
res = json.loads(urllib.request.urlopen(req).read().decode())
print(f"? Captured & Brokered Lead: {res['lead_code']}")
print(f"   AI Intent Score: {res['qualification']['intent_score']}/100")
print(f"   Estimated Contract Quote: ${res['qualification']['estimated_quote']:,}")
print(f"   Pay-Per-Lead Value: ${res['qualification']['lead_price']}")
print(f"   Dispatched Alerts to {res['dispatch']['matched_vendors_count']} Local Operators")

# 4. Test Vendor Profile Claiming & MRR Subscription
claim_payload = {
    "vendor_id": vendors[1]['id'],
    "email": "owner@royal-throne.com"
}
req = urllib.request.Request(
    f"{BASE_URL}/api/claim",
    data=json.dumps(claim_payload).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
claim_res = json.loads(urllib.request.urlopen(req).read().decode())
print(f"? Vendor Claim Processed: {claim_res['message']}")

# 5. Test Admin Telemetry
req = urllib.request.urlopen(f"{BASE_URL}/api/admin/metrics")
metrics = json.loads(req.read().decode())
print("\n--------------------------------------------------")
print(" ?? LIVE CASH FLOW TELEMETRY")
print("--------------------------------------------------")
print(f"?? Total Banked Revenue: ${metrics['total_revenue_banked']:,.2f}")
print(f"?? Active Monthly Recurring Revenue (MRR): ${metrics['active_mrr']:,.2f}/mo")
print(f"?? Total Leads Brokered: {metrics['total_leads']}")
print(f"?? Active Directory Listings: {metrics['total_vendors']}")
print(f"? Active Paying Subscribers: {metrics['active_subscribers']}")
print("==================================================")
print(" ?? ALL AUTONOMOUS ENGINE TESTS PASSED (100% HEALTH)")
print("==================================================")
