# -*- coding: utf-8 -*-
import urllib.request
import json
import os
import subprocess
import time
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:3000"

print("=" * 60)
print("🚀 VERIFYING ZERO-LIMIT PROFIT MAXIMIZATION ENGINE")
print("=" * 60)

# Helper function for JSON requests
def post_json(endpoint, data):
    req = urllib.request.Request(
        f"{BASE_URL}{endpoint}",
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    res = urllib.request.urlopen(req)
    return json.loads(res.read().decode())

def get_json(endpoint):
    req = urllib.request.Request(f"{BASE_URL}{endpoint}")
    res = urllib.request.urlopen(req)
    return json.loads(res.read().decode())

try:
    # 1. Health check
    health = get_json("/api/health")
    print(f"[OK] Health Status: {health['status']} | Engine: {health['engine']}")

    # 2. Test 15% Concierge Booking Deposit Lock-In
    deposit_payload = {
        "lead_code": "REL-2026-TEST",
        "customer_name": "Eleanor Vance (Gala Director)",
        "customer_email": "eleanor.vance@society.org",
        "customer_phone": "(404) 555-7799",
        "city": "Atlanta",
        "state": "GA",
        "event_date": "2026-10-18",
        "guest_count": 350,
        "event_type": "VIP Symphony Gala",
        "estimated_total": 3200,
        "deposit_amount": 480,
        "niche_id": "luxury_restrooms"
    }
    dep_res = post_json("/api/bookings/deposit", deposit_payload)
    print(f"[OK] Concierge Booking Deposit Locked:")
    print(f"     Booking ID: {dep_res['booking_id']}")
    print(f"     15% Escrow Deposit Paid: ${dep_res['deposit_paid']:,}")
    print(f"     Balance Due On-Site: ${dep_res['balance_due_on_site']:,}")
    print(f"     Assigned Fleet Partner: {dep_res['assigned_vendor']['name']} ({dep_res['assigned_vendor']['city']})")

    # 3. Test Operator Wallet & Feed
    wallet_res = get_json("/api/operator/wallet?operator_id=vend_atl_01")
    print(f"[OK] Operator Wallet Retrieved:")
    print(f"     Company: {wallet_res['wallet']['company_name']}")
    print(f"     Current Balance: ${wallet_res['wallet']['balance']:.2f}")
    print(f"     Live Territory Leads: {len(wallet_res['feed'])} available in feed")

    # 4. Test Operator Wallet Top-Up ($500 + $50 Bonus)
    topup_res = post_json("/api/operator/wallet/topup", {"operator_id": "vend_atl_01", "amount": 500})
    print(f"[OK] Wallet Reloaded:")
    print(f"     Amount Loaded: ${topup_res['amount_loaded']:,}")
    print(f"     Bonus Awarded: ${topup_res['bonus_awarded']:,}")
    print(f"     New Balance: ${topup_res['new_balance']:.2f}")

    # 5. Test Instant 1-Click Lead Unlock ($85 deduction)
    unlock_res = post_json("/api/operator/leads/unlock", {"operator_id": "vend_atl_01", "lead_id": "lead-1"})
    print(f"[OK] Lead Unlocked:")
    print(f"     Lead ID: {unlock_res['lead_id']}")
    print(f"     Remaining Balance: ${unlock_res['new_balance']:.2f}")

    # 6. Test Exclusive Metro Monopoly Subscription ($299/mo)
    monopoly_res = post_json("/api/operator/monopoly/subscribe", {
        "operator_id": "vend_atl_01",
        "metro_slug": "atlanta-ga",
        "tier": "metro_monopoly"
    })
    print(f"[OK] Metro Monopoly Activated:")
    print(f"     Tier: {monopoly_res['tier']} (${monopoly_res['monthly_cost']}/mo)")
    print(f"     Message: {monopoly_res['message']}")

    # 7. Test Fleet Equipment Financing Rates & Section 179
    rates_res = get_json("/api/financing/rates")
    print(f"[OK] Financing Rates & Section 179:")
    print(f"     Prime APR: {rates_res['base_apr_ranges']['tier_1_prime']['min_apr']}% - {rates_res['base_apr_ranges']['tier_1_prime']['max_apr']}%")
    print(f"     IRS 179 Max Deduction: ${rates_res['section_179']['max_deduction_limit']:,} (100% Bonus Expensing)")

    # 8. Test Commercial Fleet Pre-Qualification & Broker Referral Bounty
    finance_payload = {
        "business_name": "Apex Mobile Sanitation & Cold Storage LLC",
        "contact_name": "Marcus Vance",
        "email": "marcus@apexfleets.com",
        "phone": "(404) 555-8822",
        "years_in_business": "4",
        "equipment_type": "2026 Presidential 5-Station Luxury Restroom Trailer",
        "purchase_amount": 85000,
        "term_months": 60,
        "credit_tier": "tier_1_prime"
    }
    fin_app_res = post_json("/api/financing/apply", finance_payload)
    print(f"[OK] Commercial Fleet Financing Application Processed:")
    print(f"     Application ID: {fin_app_res['application_id']}")
    print(f"     Purchase Amount: ${fin_app_res['purchase_amount']:,}")
    print(f"     Estimated Monthly Payment: ${fin_app_res['monthly_payment']:,}/mo")
    print(f"     Section 179 Tax Savings: -${fin_app_res['section_179_savings']:,}")
    print(f"     Net Cost After Tax: ${fin_app_res['net_cost_after_tax']:,}")
    print(f"     Platform Referral Bounty (3.5%): ${fin_app_res['estimated_broker_bounty']:,}")

    # 9. Verify Static Pages Exist
    public_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "apps", "web", "public"))
    pages_to_check = [
        "operator-portal.html",
        "financing.html",
        "badge-generator.html",
        "cost/atlanta.html",
        "cost/salt-lake-city.html"
    ]
    for p in pages_to_check:
        full_p = os.path.join(public_dir, p)
        assert os.path.exists(full_p), f"Missing page: {p}"
        print(f"[OK] Verified Static File: {p} ({os.path.getsize(full_p):,} bytes)")

    print("\n" + "=" * 60)
    print("✅ ALL ZERO-LIMIT MONETIZATION ENGINES VERIFIED SUCCESSFULLY!")
    print("=" * 60)

except Exception as e:
    print(f"\n[ERROR] Test failed: {e}")
    sys.exit(1)
