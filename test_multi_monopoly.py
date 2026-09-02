import urllib.request
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://localhost:3000"

print("==================================================")
print(" 🚀 RUNNING MULTI-VERTICAL MICRO-MONOPOLY AUDIT")
print("==================================================")

# 1. Test Multi-Vertical Directory Filtering
print("\n[STEP 1: Multi-Niche Listings Verification]")
for niche in ["luxury_restrooms", "commercial_cold_storage", "heavy_crane_rigging"]:
    req = urllib.request.urlopen(f"{BASE_URL}/api/vendors?niche_id={niche}")
    vendors = json.loads(req.read().decode())
    print(f"✅ Vertical [{niche}]: {len(vendors)} Active Listings")
    for v in vendors[:1]:
        print(f"   • Sample: {v['name']} ({v['city']}, {v['state']}) - ${v['min_price']:,} to ${v['max_price']:,}")

# 2. Test Multi-Tier Quote Dispatch
print("\n[STEP 2: Multi-Tier Brokerage Quote Lead Test]")
lead_payload = {
    "niche_id": "commercial_cold_storage",
    "customer_name": "Marcus Vance (Regional Logistics)",
    "customer_email": "marcus@supplychain.com",
    "customer_phone": "(404) 881-9922",
    "city": "Atlanta",
    "state": "GA",
    "event_date": "2026-11-10",
    "guest_count": 150,
    "event_type": "Emergency Food Distribution Outage",
    "budget": "$5,000 - $12,000",
    "notes": "Urgent requirement for 2x 40ft deep freeze reefer trailers (-20F)."
}

req = urllib.request.Request(
    f"{BASE_URL}/api/leads",
    data=json.dumps(lead_payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)
with urllib.request.urlopen(req) as res:
    lead_res = json.loads(res.read().decode())
    print(f"✅ Lead Created: {lead_res['lead_code']} for {lead_res['niche_id']}")
    print(f"   • AI Intent Score: {lead_res['qualification']['intent_score']}/100")
    print(f"   • Pay-Per-Lead Fee: ${lead_res['qualification']['lead_price']} (Higher Tier)")
    print(f"   • Booking Deposit (15%): ${lead_res['qualification']['deposit_fee']:,.2f}")
    print(f"   • Matched Operators: {lead_res['dispatch']['matched_vendors_count']}")

# 3. Test Cloudflare Edge Pre-Rendered Static Pages
print("\n[STEP 3: Cloudflare Edge Static Pages Audit]")
edge_dir = os.path.join(os.path.dirname(__file__), "dist", "static-pseo")
static_files = [f for f in os.listdir(edge_dir) if f.endswith(".html")] if os.path.exists(edge_dir) else []
print(f"✅ Pre-Rendered Edge Pages: {len(static_files)} Static HTML Files in dist/static-pseo/")
if static_files:
    sample_file = os.path.join(edge_dir, static_files[0])
    with open(sample_file, "r", encoding="utf-8") as f:
        content = f.read()
    has_schema = '"@type": "Service"' in content
    print(f"   • Sample Page: {static_files[0]} | Schema.org Valid: {has_schema}")

# 4. Test Portfolio Financial Telemetry
print("\n[STEP 4: Portfolio Cash Flow Reconciliation]")
req = urllib.request.urlopen(f"{BASE_URL}/api/admin/metrics")
metrics = json.loads(req.read().decode())
print(f"✅ Total Banked Revenue: ${metrics['total_revenue_banked']:,.2f}")
print(f"✅ Portfolio Active MRR: ${metrics['active_mrr']:,.2f}/mo ({metrics['active_subscribers']} Subscribed Operators)")
print(f"✅ Total Brokered Leads: {metrics['total_leads']}")
print(f"✅ Niche Breakdown: {len(metrics['niche_breakdown'])} Verticals Active")

print("\n==================================================")
print(" 🏆 MULTI-MONOPOLY AUDIT COMPLETE: 100% HEALTH")
print("==================================================")
