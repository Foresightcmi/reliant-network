import json
import os
import re

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
VENDORS_FILE = os.path.join(DATA_DIR, 'vendors.json')

METROS = [
    {"city": "Atlanta", "state": "GA"},
    {"city": "Dallas", "state": "TX"},
    {"city": "Miami", "state": "FL"},
    {"city": "Austin", "state": "TX"},
    {"city": "Los Angeles", "state": "CA"},
    {"city": "Chicago", "state": "IL"},
    {"city": "Houston", "state": "TX"},
    {"city": "Phoenix", "state": "AZ"},
    {"city": "Denver", "state": "CO"},
    {"city": "Seattle", "state": "WA"},
    {"city": "New York", "state": "NY"}
]

NEW_VERTICALS = [
    {
        "niche_id": "commercial_dumpsters",
        "prefix": "vend_dmp_",
        "brand_tpl": "{city} Commercial Roll-Off & Waste Logistics",
        "min_p": 450,
        "max_p": 5000,
        "image": "https://images.unsplash.com/photo-1595085610896-1ab46f90d5df?auto=format&fit=crop&w=800&q=80",
        "fleet": ["10-Yard Heavy Debris", "20-Yard Commercial", "30-Yard Construction", "40-Yard Demolition Roll-Off"],
        "amenities": ["24-Hour Swap Out", "Concrete/Dirt Allowed", "LEED Certified Recycling", "No Hidden Tonnage Fees"],
        "desc_tpl": "{city} Commercial Roll-Off provides heavy-duty jobsite waste logistics. We specialize in 40-yard demolition dumpsters, concrete recycling, and LEED compliance reporting for commercial builders.",
        "badges": {"emergency_dispatch_247": True, "insurance_verified": "$2M Policy on File"},
        "highlights": ["Same-day swaps", "Transparent flat-rate pricing", "LEED documentation provided"]
    },
    {
        "niche_id": "private_security",
        "prefix": "vend_sec_",
        "brand_tpl": "{city} Elite Event & Corporate Security",
        "min_p": 1200,
        "max_p": 15000,
        "image": "https://images.unsplash.com/photo-1557053910-d9eadeed1c58?auto=format&fit=crop&w=800&q=80",
        "fleet": ["Armed Off-Duty Police", "Unarmed Event Staffing", "K9 Explosive Detection", "VIP Close Protection Details"],
        "amenities": ["Licensed & Bonded", "Ex-Military/Law Enforcement", "24/7 Command Center", "Crowd Control Specialists"],
        "desc_tpl": "{city} Elite Security delivers uncompromising protection for high-value corporate events, private estates, and commercial jobsites. Fully licensed and bonded ex-law enforcement personnel.",
        "badges": {"emergency_dispatch_247": True, "insurance_verified": "$5M Liability Policy on File"},
        "highlights": ["Off-duty police officers available", "Discreet VIP protection", "Rapid riot/crowd control deployment"]
    },
    {
        "niche_id": "hazmat_remediation",
        "prefix": "vend_haz_",
        "brand_tpl": "{city} Rapid Hazmat & Biohazard Response",
        "min_p": 2500,
        "max_p": 45000,
        "image": "https://images.unsplash.com/photo-1584467735815-f778f274e296?auto=format&fit=crop&w=800&q=80",
        "fleet": ["Level A Hazmat Response Unit", "Bio-Containment Trailers", "Industrial Decontamination Scrubbers", "Chemical Spill Vacuum Trucks"],
        "amenities": ["OSHA HAZWOPER Certified", "Direct Insurance Billing", "EPA Compliant Disposal", "2-Hour Emergency Response"],
        "desc_tpl": "The premier {city} emergency response contractor for industrial chemical spills, biohazard cleanup, and environmental remediation. OSHA certified with turnkey EPA disposal manifesting.",
        "badges": {"emergency_dispatch_247": True, "insurance_verified": "$10M Environmental Policy"},
        "highlights": ["2-hour dispatch for industrial spills", "Full EPA manifesting", "Direct commercial insurance billing"]
    }
]

def load_vendors():
    if not os.path.exists(VENDORS_FILE): return []
    with open(VENDORS_FILE, 'r', encoding='utf-8') as f: return json.load(f)

def save_vendors(data):
    with open(VENDORS_FILE, 'w', encoding='utf-8') as f: json.dump(data, f, indent=2)

def generate_id(city, prefix):
    return f"{prefix}{city.lower().replace(' ', '_')}_{str(os.urandom(2).hex())}"

def generate_phone(area="555"):
    import random
    return f"({area}) {random.randint(200,999)}-{random.randint(1000,9999)}"

def seed():
    vendors = load_vendors()
    existing_ids = {v['id'] for v in vendors}
    added = 0
    
    for niche in NEW_VERTICALS:
        print(f"Seeding B2B vertical: {niche['niche_id']}...")
        for m in METROS:
            city = m['city']
            vid = generate_id(city, niche['prefix'])
            name = niche['brand_tpl'].replace("{city}", city)
            
            v = {
                "id": vid,
                "niche_id": niche['niche_id'],
                "name": name,
                "city": city,
                "state": m['state'],
                "zip": "00000",
                "phone": generate_phone(),
                "email": f"dispatch@{re.sub(r'[^a-z0-9]', '', name.lower())}.com",
                "website": f"https://www.{re.sub(r'[^a-z0-9]', '', name.lower())}.com",
                "rating": 4.9,
                "review_count": 45,
                "min_price": niche['min_p'],
                "max_price": niche['max_p'],
                "fleet_inventory": niche['fleet'],
                "amenities": niche['amenities'],
                "description": niche['desc_tpl'].replace("{city}", city),
                "badges": niche['badges'],
                "highlights": niche['highlights'],
                "stripe_account_id": "acct_1TESTB2B_PENDING"
            }
            vendors.append(v)
            added += 1

    save_vendors(vendors)
    print(f"Generated {added} new B2B/High-Ticket records.")

if __name__ == '__main__':
    seed()
