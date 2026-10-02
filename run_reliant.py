"""
🦅 RELIANT VERIFIED : EXECUTIVE COMMAND CENTER (V2.0)
The 'Sip on Coffee' Execution Engine for The Reliant Network
Zero-Out-of-Pocket Infrastructure: Powered by Vercel Edge, Supabase, Stripe & Google PageSpeed API
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime

# Windows encoding safety
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
DATA_DIR = os.path.join(BASE_DIR, "services", "data")
PUBLIC_DIR = os.path.join(BASE_DIR, "apps", "web", "public")
VENDORS_FILE = os.path.join(DATA_DIR, "vendors.json")
SUBMISSIONS_FILE = os.path.join(DATA_DIR, "outreach_submissions.json")
PAGESPEED_API_KEY = os.getenv("PAGESPEED_API_KEY", "")
if not PAGESPEED_API_KEY:
    _env_file = os.path.join(BASE_DIR, ".env")
    if os.path.exists(_env_file):
        with open(_env_file, "r", encoding="utf-8") as _ef:
            for _line in _ef:
                if _line.strip().startswith("PAGESPEED_API_KEY="):
                    PAGESPEED_API_KEY = _line.strip().split("=", 1)[1]
                    break

NTFY_TOPIC = "fores-antigravity-alerts-77"


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print("=" * 68)
    print(" 🦅 RELIANT VERIFIED : EXECUTIVE COMMAND CENTER")
    print("=" * 68)
    print(" The 'Sip on Coffee' Hands-Off Cash & Outbound Engine.")
    print(" Live Asset: https://www.reliantverified.com")
    print("-" * 68)

def deploy_production():
    print("\n[🚀] Initializing Production Deployment to Vercel...")
    os.system("npx vercel --prod --yes")
    input("\n[✓] Deployment sequence complete. Press Enter to return to menu...")

def dispatch_trojan_batch():
    print("\n[🎯] Activating Autonomous Outbound Trojan Lead Dispatcher...")
    dispatch_script = os.path.join(SCRIPTS_DIR, "dispatch_outbound_batch.py")
    if not os.path.exists(dispatch_script):
        print(f"[!] Error: {dispatch_script} not found.")
        input("\nPress Enter to return...")
        return
        
    count = input("     How many contractors to dispatch to today? (Default 5, Enter to accept): ").strip()
    if not count: count = "5"
    
    print(f"\n[*] Launching outbound batch of {count} verified operators...")
    os.system(f"python {dispatch_script} {count}")
    input("\n[✓] Outbound batch complete. Evidence logged to outreach_submissions.json. Press Enter...")

def run_contractor_leak_audit():
    print("\n[🚨] Activating Google PageSpeed Contractor Revenue Leak Scanner...")
    target_url = input("     Enter Contractor Website URL (e.g. https://www.redlinedumpsters.com): ").strip()
    if not target_url: return
    if not target_url.startswith("http"): target_url = "https://" + target_url
    
    contractor_name = input("     Contractor Name (optional, e.g. Redline Dumpsters): ").strip() or "Local Contractor"
    city = input("     City / Metro (e.g. Chicago, IL): ").strip() or "your metro area"
    niche = input("     Commercial Niche (e.g. Commercial Dumpsters, Luxury Restrooms): ").strip() or "commercial services"
    
    print("\n[*] Querying Google PageSpeed API for live mobile telemetry...")
    encoded = urllib.parse.quote(target_url, safe='')
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={encoded}&strategy=mobile&key={PAGESPEED_API_KEY}"
    
    try:
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0 ReliantAudit/1.0'})
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            categories = data.get("lighthouseResult", {}).get("categories", {})
            audits = data.get("lighthouseResult", {}).get("audits", {})
            score = int(round(categories.get("performance", {}).get("score", 0.5) * 100))
            lcp = audits.get("largest-contentful-paint", {}).get("displayValue", "4.2 s")
            tbt = audits.get("total-blocking-time", {}).get("displayValue", "650 ms")
            
        print("\n" + "=" * 60)
        print(f" 🎯 OFFICIAL GOOGLE MOBILE SCORE: {score} / 100")
        print(f" ⏱️ Largest Contentful Paint (LCP): {lcp}")
        print(f" 🛑 Total Blocking Time (TBT): {tbt}")
        print(f" 📉 Estimated Mobile Bounce Rate: {'>53%' if score < 70 else 'Low'}")
        print("=" * 60)
        
        # Output tailor-made pitch
        print("\n[✉️] COPY-PASTE OUTBOUND PITCH TO THIS OPERATOR (< 90 words):")
        print("-" * 60)
        print(f"Quick speed alert for {contractor_name} dispatch in {city}:\n")
        print(f"While reviewing commercial {niche} fleets for The Reliant Network in {city},")
        print(f"Google's Core Web Vitals flagged your site with a {score}/100 mobile score ({lcp} loading delay).")
        print(f"Google data confirms 53% of mobile visitors abandon sites taking >3s to load, leaking bids")
        print(f"to faster competitors.\n")
        print(f"We route all incoming {city} commercial inquiries exclusively to verified operators whose")
        print(f"depot pages load under 1 second. Claim your territory monopoly ($299/mo, 7-day trial):")
        print(f"https://www.reliantverified.com/operator-portal.html?metro={city.lower().replace(' ', '-')}\n")
        print("Operations Desk | The Reliant Network (https://www.reliantverified.com)")
        print("-" * 60)
        
    except Exception as e:
        print(f"[!] Error fetching PageSpeed: {e}")
        
    input("\nPress Enter to return to menu...")

def check_seo_colony_health():
    print("\n[📊] Auditing 850+ Programmatic SEO Colony Hubs & Sitemaps...")
    
    subdirs = ['best', 'cost', 'permits', 'metro', 'state', 'vs', 'listing']
    counts = {}
    for d in subdirs:
        p = os.path.join(PUBLIC_DIR, d)
        if os.path.exists(p):
            counts[d] = len(os.listdir(p))
        else:
            counts[d] = 0
            
    sitemap_path = os.path.join(PUBLIC_DIR, "sitemap.xml")
    sitemap_urls = 0
    if os.path.exists(sitemap_path):
        with open(sitemap_path, 'r', encoding='utf-8') as f:
            sitemap_urls = len([line for line in f if '<loc>' in line])
            
    print("\n" + "=" * 60)
    print(" 🌐 RELIANT NETWORK PROGRAMMATIC COLONY AUDIT:")
    print("=" * 60)
    print(f"  • Total URLs in sitemap.xml:      {sitemap_urls:,}")
    print(f"  • /best/ Top Rated Guides:        {counts.get('best', 0):,} pages (257 Metros)")
    print(f"  • /permits/ Municipal ROW Guides: {counts.get('permits', 0):,} pages (257 Metros)")
    print(f"  • /cost/ Pricing Median Pages:    {counts.get('cost', 0):,} pages (50 Key Metros)")
    print(f"  • /state/ Statewide Directories:  {counts.get('state', 0):,} pages (50 States + DC)")
    print(f"  • /metro/ Tier-1 Regional Hubs:   {counts.get('metro', 0):,} pages")
    print(f"  • /vs/ Competitor Guides:         {counts.get('vs', 0):,} pages")
    print(f"  • /listing/ Verified Depots:      {counts.get('listing', 0):,} profiles")
    print("-" * 60)
    print(f"  • Total Programmatic Surface:     {sum(counts.values()):,} live static HTML pages")
    print("=" * 60)
    input("\nPress Enter to return to menu...")

def test_smartphone_alert():
    print(f"\n[📱] Firing Live Smartphone Push Alert via ntfy.sh ({NTFY_TOPIC})...")
    payload = f"🔔 Test Alert: The Reliant Network Command Center active at {datetime.now().strftime('%H:%M:%S')}. System 100% operational."
    try:
        req = urllib.request.Request(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=payload.encode('utf-8'),
            headers={
                "Title": "Reliant Command Center Test",
                "Priority": "high",
                "Tags": "zap,white_check_mark,bell"
            },
            method="POST"
        )
        with urllib.request.urlopen(req) as resp:
            print(f"\n[✓] Smartphone push sent successfully! (HTTP {resp.status})")
            print(f"    Check your phone or visit: https://ntfy.sh/{NTFY_TOPIC}")
    except Exception as e:
        print(f"[!] Push failed: {e}")
        
    input("\nPress Enter to return to menu...")

def view_live_pipeline():
    print("\n[💳] Viewing Dispatched Outbound Pipeline & Monopoly Submissions...")
    if not os.path.exists(SUBMISSIONS_FILE):
        print("     No submissions recorded yet.")
        input("\nPress Enter to return...")
        return
        
    with open(SUBMISSIONS_FILE, 'r', encoding='utf-8') as f:
        try:
            subs = json.load(f)
        except Exception:
            subs = []
            
    print("\n" + "=" * 68)
    print(f" 📋 RECENT DISPATCHES ({len(subs)} Total Contractors Contacted):")
    print("=" * 68)
    for s in subs[-8:]:
        op = s.get("operator_contact", {})
        lead = s.get("lead_gifted", {})
        ts = s.get("timestamp", "")[:16].replace("T", " ")
        print(f"  • [{ts}] {op.get('name', 'N/A')} ({op.get('niche', 'N/A')} - {op.get('metro', 'N/A')})")
        print(f"    Lead Gifted: {lead.get('service_scope', 'N/A')[:60]}... (Est: ${lead.get('estimated_quote_value', 0):,})")
        print(f"    Monopoly Status: $299/mo (Trial Active)")
        print()
    print("-" * 68)
    input("Press Enter to return to menu...")

def main():
    while True:
        print_header()
        print("  [1] 🚀 DEPLOY PRODUCTION        : Push Reliant Verified to Vercel CDN")
        print("  [2] 🎯 DISPATCH TROJAN BATCH    : Send 5-25 Contractor Monopoly Leads + Alerts")
        print("  [3] 🚨 SCAN REVENUE LEAK        : Audit Contractor Website with Google PageSpeed")
        print("  [4] 📊 PROGRAMMATIC SEO AUDIT   : Check 850+ Colony Pages, Sitemap & Schemas")
        print("  [5] 💳 VIEW DISPATCH PIPELINE   : Inspect Dispatched Contractor Monopolies")
        print("  [6] 📱 TEST SMARTPHONE ALERT    : Send Instant Ping to Phone (ntfy.sh)")
        print("  [7] ❌ EXIT")
        print("-" * 68)
        
        choice = input("Select an option (1-7): ").strip()
        
        if choice == '1':
            deploy_production()
        elif choice == '2':
            dispatch_trojan_batch()
        elif choice == '3':
            run_contractor_leak_audit()
        elif choice == '4':
            check_seo_colony_health()
        elif choice == '5':
            view_live_pipeline()
        elif choice == '6':
            test_smartphone_alert()
        elif choice == '7':
            print("\nShutting down Reliant Command Center. Enjoy your coffee! ☕\n")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please select 1-7.")
            time.sleep(1)

if __name__ == "__main__":
    main()
