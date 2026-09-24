import json
import csv
import os

VENDORS_FILE = os.path.join(os.path.dirname(__file__), 'services', 'data', 'vendors.json')
OUTPUT_FILE = os.path.join(os.path.expanduser('~'), 'Desktop', 'reliant_outbound_campaign.csv')

def generate_campaign():
    with open(VENDORS_FILE, 'r', encoding='utf-8') as f:
        vendors = json.load(f)

    headers = ['Email', 'Company', 'City', 'Niche', 'Subject', 'Body']
    rows = []

    for v in vendors:
        email = v.get('email')
        if not email or email == 'N/A' or '@' not in email:
            continue
            
        company = v.get('name', 'your company')
        city = v.get('city', 'your area')
        niche_raw = v.get('niche_id', 'commercial service')
        
        # Format the niche beautifully
        niche_map = {
            'luxury_restrooms': 'luxury restroom trailers',
            'temporary_power': 'commercial temporary power',
            'machinery_moving': 'heavy machinery moving',
            'senior_downsizing': 'senior facility downsizing',
            'wheelchair_vans': 'commercial wheelchair vans',
            'cold_storage': 'commercial cold storage',
            'crane_rigging': 'crane and rigging',
            'aging_in_place': 'commercial accessibility modifications',
            'commercial_dumpsters': 'commercial roll-off dumpsters',
            'private_security': 'private event security',
            'hazmat_remediation': 'hazmat and biohazard remediation',
            'senior_care': 'senior care logistics'
        }
        niche = niche_map.get(niche_raw, niche_raw.replace('_', ' '))

        subject = f"Corporate {niche.title()} leads in {city}"
        
        body = f"""Hey team,

I was reviewing the services for {company} in {city}.

We recently launched The Reliant Network, a closed B2B commercial directory. Right now, we are routing all the incoming corporate quote requests for {niche} in the {city} metro to a generic national fallback, because we don't have a local partner locked in yet.

We only allow one {niche} contractor per city. It's a flat $299/mo to lock the {city} territory monopoly, and you keep 100% of the leads with zero per-lead fees.

Do you want to lock the {city} territory before we route these to a competitor? 

Best,
Alex
Lead Architect, Reliant Verified
https://www.reliantverified.com
"""
        rows.append([email, company, city, niche, subject, body])

    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"Successfully generated outbound campaign for {len(rows)} highly-targeted B2B contractors.")
    print(f"File saved to Desktop: {OUTPUT_FILE}")

if __name__ == '__main__':
    generate_campaign()
