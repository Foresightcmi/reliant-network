import csv
import json
import os
import sys
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone

# Autonomous B2B Outbound Dispatch Engine
# Reliant Verified Network

CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'reliant_outbound_campaign_expanded_v2.csv')
LOG_PATH = os.path.join(os.path.dirname(__file__), '..', 'services', 'data', 'outbound_transmission_log.json')
RESEND_API_KEY = os.environ.get('RESEND_API_KEY', '')

def load_logs():
    if os.path.exists(LOG_PATH):
        try:
            with open(LOG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_logs(logs):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=2)

def send_via_resend(to_email, subject, body_text):
    if not RESEND_API_KEY:
        return False, "NO_API_KEY"

    payload = json.dumps({
        "from": "Reliant Network Operations <dispatch@reliantverified.com>",
        "to": [to_email],
        "subject": subject,
        "text": body_text
    }).encode('utf-8')

    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=payload,
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "ReliantOutboundEngine/1.0"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp_body = resp.read().decode('utf-8')
            return True, resp_body
    except Exception as e:
        return False, str(e)

def run_dispatcher(batch_size=10, dry_run=True, campaign_type='initial'):
    print("=" * 60)
    print("RELIANT VERIFIED AUTONOMOUS OUTBOUND DISPATCH ENGINE")
    print(f"Mode: {'DRY RUN (Simulation)' if dry_run else 'LIVE TRANSMISSION'}")
    print(f"Campaign Type: {campaign_type.upper()}")
    print(f"Target Batch Size: {batch_size}")
    print("=" * 60)

    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found.")
        return

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))

    logs = load_logs()
    already_sent = set([f"{item['email']}_{item.get('campaign', 'initial')}" for item in logs if item.get('status') == 'SENT'])

    pending = [r for r in reader if r['Email'] and f"{r['Email']}_{campaign_type}" not in already_sent]
    print(f"Total Campaign Prospects: {len(reader)}")
    print(f"Previously Dispatched: {len(already_sent)}")
    print(f"Available Uncontacted for {campaign_type}: {len(pending)}")

    to_process = pending[:batch_size]
    dispatched_count = 0

    for i, row in enumerate(to_process, start=1):
        company = row['Company Name']
        email = row['Email']
        city = row['City']
        
        if campaign_type == 'badge':
            encoded_company = urllib.parse.quote(company)
            city_slug = city.lower().replace(' ', '-')
            subject = f"{company} 2026 commercial verification badge ({city})"
            body = (
                f"Hi {company} team,\n\n"
                f"Following our 2026 commercial equipment verification audit for {city}, "
                f"{company} cleared preliminary OSHA and commercial compliance standards.\n\n"
                f"We have generated your official verified partner trust seal here:\n"
                f"https://www.reliantverified.com/badge-generator.html?metro={city_slug}&company={encoded_company}\n\n"
                f"Embedding this badge on your website footer automatically activates 30 days of complimentary "
                f"Featured priority and first-call RFQ routing in {city} at zero cost.\n\n"
                f"Best regards,\n"
                f"Verification Desk | The Reliant Network\n"
                f"https://www.reliantverified.com\n"
            )
        elif campaign_type == 'followup':
            subject = row.get('Follow Up Subject', f"follow up re: commercial quotes in {city}")
            body = row.get('Follow Up Body', f"Hi {company} team,\n\nQuick follow up regarding commercial quote routing in {city}.\n\nBest,\nCommercial Operations Desk")
        else:
            subject = row['Subject Line']
            body = row['Email Body']

        print(f"\n[{i}/{len(to_process)}] Processing: {company} ({city}) -> {email}")
        print(f"Subject: {subject}")

        if dry_run or not RESEND_API_KEY:
            status = "SIMULATED_SENT" if dry_run else "QUEUED_PENDING_KEY"
            logs.append({
                "company": company,
                "email": email,
                "city": city,
                "subject": subject,
                "campaign": campaign_type,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "status": status,
                "mode": "simulation"
            })
            dispatched_count += 1
            print(f"  [OK] Simulated delivery to {email}")
        else:
            success, msg = send_via_resend(email, subject, body)
            status = "SENT" if success else "FAILED"
            logs.append({
                "company": company,
                "email": email,
                "city": city,
                "subject": subject,
                "campaign": campaign_type,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "status": status,
                "response": msg
            })
            if success:
                dispatched_count += 1
                print(f"  [SENT] Live email delivered via Resend API")
            else:
                print(f"  [ERROR] {msg}")

            time.sleep(0.6) # Resend rate limit safety

    save_logs(logs)
    print("\n" + "=" * 60)
    print(f"DISPATCH BATCH COMPLETE: {dispatched_count} emails processed.")
    print(f"Telemetry Log Updated: {LOG_PATH}")
    print("=" * 60)

if __name__ == "__main__":
    is_dry = "--live" not in sys.argv
    limit = 15
    camp = 'initial'
    for arg in sys.argv:
        if arg.startswith("--limit="):
            try:
                limit = int(arg.split("=")[1])
            except:
                pass
        if arg.startswith("--campaign="):
            camp = arg.split("=")[1]
    run_dispatcher(batch_size=limit, dry_run=is_dry, campaign_type=camp)
