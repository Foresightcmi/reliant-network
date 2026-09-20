import json
import os
import re

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
VENDORS_FILE = os.path.join(DATA_DIR, 'vendors.json')

METROS = [
    {"city": "Atlanta", "state": "GA", "lat": 33.7490, "lng": -84.3880, "area": "404", "zip": "30303", "addr": "Peachtree Industrial Blvd"},
    {"city": "Dallas", "state": "TX", "lat": 32.7767, "lng": -96.7970, "area": "214", "zip": "75201", "addr": "Stemmons Freeway Logistics Corridor"},
    {"city": "Miami", "state": "FL", "lat": 25.7617, "lng": -80.1918, "area": "305", "zip": "33101", "addr": "Biscayne Commerce Way"},
    {"city": "Austin", "state": "TX", "lat": 30.2672, "lng": -97.7431, "area": "512", "zip": "78701", "addr": "Research Blvd Tech Logistics Corridor"},
    {"city": "Los Angeles", "state": "CA", "lat": 34.0522, "lng": -118.2437, "area": "213", "zip": "90012", "addr": "Olympic Blvd Industrial Staging Yard"},
    {"city": "Chicago", "state": "IL", "lat": 41.8781, "lng": -87.6298, "area": "312", "zip": "60601", "addr": "Industrial Parkway Logistics Hub"},
    {"city": "Houston", "state": "TX", "lat": 29.7604, "lng": -95.3698, "area": "713", "zip": "77002", "addr": "Port Terminal Way Freight Hub"},
    {"city": "Phoenix", "state": "AZ", "lat": 33.4484, "lng": -112.0740, "area": "602", "zip": "85001", "addr": "Grand Ave Industrial Corridor"},
    {"city": "Denver", "state": "CO", "lat": 39.7392, "lng": -104.9903, "area": "303", "zip": "80202", "addr": "Central Park Logistics Way"},
    {"city": "Seattle", "state": "WA", "lat": 47.6062, "lng": -122.3321, "area": "206", "zip": "98101", "addr": "Pacific Highway South Freight Terminal"},
    {"city": "New York", "state": "NY", "lat": 40.6786, "lng": -73.9842, "area": "212", "zip": "10001", "addr": "Metro Logistics Terminal Pier 40"},
    {"city": "Boston", "state": "MA", "lat": 42.3526, "lng": -71.0202, "area": "617", "zip": "02108", "addr": "Seaport Industrial Corridor"},
    {"city": "Philadelphia", "state": "PA", "lat": 39.9897, "lng": -75.1383, "area": "215", "zip": "19102", "addr": "Delaware Ave Maritime Staging Center"},
    {"city": "Nashville", "state": "TN", "lat": 36.1362, "lng": -86.7572, "area": "615", "zip": "37201", "addr": "Cumberland Logistics Depot Park"},
    {"city": "Las Vegas", "state": "NV", "lat": 36.1421, "lng": -115.1352, "area": "702", "zip": "89101", "addr": "Dean Martin Industrial Way"},
    {"city": "Detroit", "state": "MI", "lat": 42.3000, "lng": -83.0330, "area": "313", "zip": "48201", "addr": "Automotive Logistics Mile Road"},
    {"city": "Minneapolis", "state": "MN", "lat": 44.9736, "lng": -93.2440, "area": "612", "zip": "55401", "addr": "Mississippi Riverfront Industrial Terminal"}
]

NEW_VERTICALS = [
    {
        "niche_id": "temporary_power",
        "prefix": "vend_pwr_",
        "brand_tpl": "{city} Mega-Watt Emergency Power Fleets",
        "min_p": 3500,
        "max_p": 48000,
        "image": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=80",
        "fleet": [
            "500 kW Sound-Attenuated Diesel Generator",
            "1,000 kW Tier 4 Final Mobile Genset",
            "2,000 kW Containerized Prime Power Unit",
            "Step-Up 480V/4160V Transformer & Distribution Switchgear"
        ],
        "amenities": [
            "24/7 Rapid Emergency Dispatch",
            "Onsite Fuel Management & Scheduled Delivery",
            "Automatic Transfer Switches (ATS) Included",
            "Certified Power Engineering Crew",
            "Sound-Attenuated Whisper-Quiet Enclosures"
        ],
        "desc_tpl": "{city} Mega-Watt Emergency Power Fleets provides utility-grade, sound-attenuated diesel generators and high-voltage distribution switchgear. Delivering 500 kW to 2MW prime power for plant turnarounds, hospital emergency backup, cold storage facilities, and mission-critical commercial operations.",
        "badges": {
            "emergency_dispatch_247": True,
            "insurance_verified": "$5,000,000 Commercial General Liability Policy on File",
            "power_hookup": "High-Voltage Cam-Lock & Lug Connections Included",
            "epa_compliant": "EPA Tier 4 Final Certified Low-Emissions Fleet",
            "sound_attenuated": "Whisper-Quiet Sound Enclosures (68 dBA @ 7m)"
        },
        "highlights": [
            "Rapid 2-hour mobilization for emergency power outages",
            "Full distribution switchgear, cam-locks & load banking",
            "Turnkey fuel supply contracts with automated monitoring",
            "Certified power generation technicians on standby"
        ]
    },
    {
        "niche_id": "machinery_moving",
        "prefix": "vend_mch_",
        "brand_tpl": "{city} Precision Millwrights & Heavy Rigging",
        "min_p": 6500,
        "max_p": 85000,
        "image": "https://images.unsplash.com/photo-1504917599217-d4dc5ebe6122?auto=format&fit=crop&w=800&q=80",
        "fleet": [
            "60/80 Versa-Lift Heavy-Duty Forklift",
            "500-Ton Hydraulic Gantry System",
            "Aerogo Heavy Industrial Air-Caster Skates",
            "Multi-Axle Specialized Heavy Haul Lowboy"
        ],
        "amenities": [
            "Precision Optical Leveling & Laser Alignment",
            "Anchor Bolt Coring & Epoxy Grouting",
            "Cleanroom Machinery Rigging Protocols",
            "OSHA 30 & Master Rigging Certified Crew",
            "Turnkey Plant Relocation Project Management"
        ],
        "desc_tpl": "{city} Precision Millwrights & Heavy Rigging is the premier industrial equipment mover in the region. Specializing in factory machine tool rigging, CNC de-installations, stamping press relocations, and precision leveling for aerospace, automotive, and medical manufacturing plants.",
        "badges": {
            "emergency_dispatch_247": True,
            "insurance_verified": "$5,000,000 Riggers Liability & Cargo Insurance on File",
            "master_riggers": "NCCCO & SC&RA Master Riggers on Every Project",
            "specialized_equipment": "Hydraulic Gantries, Air Skates & Versa-Lifts",
            "turnkey_relocation": "Turnkey Disassembly, Transport & Laser Re-anchoring"
        },
        "highlights": [
            "Zero plant downtime methodology with weekend/overnight rigging",
            "Millwright laser precision optical alignment within 0.001 inch",
            "Cleanroom and semiconductor vibration-free air skate transport",
            "Full turnkey equipment disconnect, relocation, and anchoring"
        ]
    },
    {
        "niche_id": "senior_downsizing",
        "prefix": "vend_dwn_",
        "brand_tpl": "Gentle Transitions Senior Move Management of {city}",
        "min_p": 3800,
        "max_p": 26000,
        "image": "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=800&q=80",
        "fleet": [
            "Turnkey 3-Bedroom Senior Estate Clean-Out",
            "High-Value Antique & Fine Art Cataloged Auction",
            "White-Glove Assisted Living Packing & Setup",
            "Heirloom Distribution & Shipping Service"
        ],
        "amenities": [
            "NASMM Certified Senior Move Managers",
            "Cataloged Digital Estate Sale & Auction Hosting",
            "Direct Heirs Video Inventory & Appraisal",
            "Donation Receipt Accounting & Deep Broom-Clean",
            "Same-Day Floorplan Spacing & Bed Setup in New Residence"
        ],
        "desc_tpl": "Gentle Transitions Senior Move Management of {city} provides compassionate, turnkey downsizing and estate liquidation for aging seniors and their families. Certified by NASMM to handle space planning, estate auctions, packing, and white-glove setup in assisted living.",
        "badges": {
            "emergency_dispatch_247": False,
            "insurance_verified": "$2,000,000 Care, Custody & Control Liability Policy on File",
            "nasmm_certified": "National Association of Senior & Specialty Move Managers",
            "bonded_crews": "100% Background-Checked, Drug-Screened & Bonded Staff",
            "turnkey_cleanout": "Complete Broom-Clean Finish for Immediate Real Estate Listing"
        },
        "highlights": [
            "Compassionate, stress-free relocation for older adults",
            "Maximum value recovery via curated online estate auctions",
            "Same-day bed making and familiar room replication in new suite",
            "Complete donation itemization with tax deduction receipts"
        ]
    },
    {
        "niche_id": "wheelchair_vans",
        "prefix": "vend_wav_",
        "brand_tpl": "Apex Mobility Accessible Vans of {city}",
        "min_p": 2400,
        "max_p": 68000,
        "image": "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?auto=format&fit=crop&w=800&q=80",
        "fleet": [
            "BraunAbility Chrysler Pacifica Power Foldout Ramp Van",
            "VMI Toyota Sienna In-Floor Ramp Minivan",
            "Ford Transit High-Roof Commercial Wheelchair Van",
            "Long-Term Monthly Medical Mobility Lease"
        ],
        "amenities": [
            "Crash-Tested ADA Ground-Level Power Ramps",
            "Q'Straint Electronic Wheelchair Tie-Down Systems",
            "Hand Controls & Transfer Seat Base Installation",
            "24/7 Roadside Assistance & Loaner Van Guarantee",
            "Home Delivery & Family Fitting Demonstration"
        ],
        "desc_tpl": "Apex Mobility Accessible Vans of {city} is the certified provider of wheelchair accessible vehicles, power ramp minivans, and commercial mobility fleets. Offering short-term medical rentals, commercial leases, and certified pre-owned BraunAbility and VMI conversions.",
        "badges": {
            "emergency_dispatch_247": True,
            "insurance_verified": "$3,000,000 Commercial Mobility Fleet Liability on File",
            "nmeda_certified": "National Mobility Equipment Dealers Association (NMEDA) QAP Certified",
            "crash_tested": "FMVSS Crash-Tested & ADA Certified Conversions",
            "home_delivery": "Complimentary Home Delivery & Mobility Fitting Service"
        },
        "highlights": [
            "Fully ADA compliant lowered-floor wheelchair vans",
            "Q'Straint electronic auto-locking securement retractor systems",
            "Flexible weekly, monthly, and annual medical rental options",
            "Free home delivery and comprehensive safety training"
        ]
    }
]

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def main():
    with open(VENDORS_FILE, 'r', encoding='utf-8') as f:
        vendors = json.load(f)

    existing_ids = {v['id'] for v in vendors}
    existing_slugs = {v['slug'] for v in vendors}

    print(f"Loaded {len(vendors)} existing vendors.")

    new_vendors = []
    idx_counter = 100

    for vert in NEW_VERTICALS:
        niche_id = vert['niche_id']
        print(f"\nSeeding vertical: {niche_id}...")

        for metro in METROS:
            idx_counter += 1
            city = metro['city']
            state = metro['state']
            city_slug = slugify(f"{city}-{state}")
            brand_name = vert['brand_tpl'].format(city=city)
            slug = slugify(f"{brand_name}-{city}-{state}")

            vid = f"{vert['prefix']}{slugify(city)[:3]}_{idx_counter:02d}"
            
            # Ensure unique ID
            while vid in existing_ids:
                idx_counter += 1
                vid = f"{vert['prefix']}{slugify(city)[:3]}_{idx_counter:02d}"

            phone_num = f"({metro['area']}) {320 + (idx_counter % 500):03d}-{1000 + (idx_counter * 7 % 8999):04d}"
            email_domain = slugify(brand_name)[:15] + ".com"
            website_url = f"https://www.{slugify(brand_name)[:15]}.com"

            full_addr = f"{100 + (idx_counter * 13 % 8900)} {metro['addr']}, {city}, {state} {metro['zip']}"

            vendor_record = {
                "id": vid,
                "slug": slug,
                "niche_id": niche_id,
                "name": brand_name,
                "city": city,
                "state": state,
                "address": full_addr,
                "phone": phone_num,
                "email": f"dispatch@{email_domain}",
                "website": website_url,
                "rating": 5.0 if idx_counter % 3 == 0 else 4.9,
                "review_count": 45 + (idx_counter % 60),
                "min_price": vert['min_p'],
                "max_price": vert['max_p'],
                "fleet_types": json.dumps(vert['fleet']),
                "amenities": json.dumps(vert['amenities']),
                "description": vert['desc_tpl'].format(city=city),
                "image_url": vert['image'],
                "service_radius_miles": 75,
                "verified": 1,
                "claimed": 1 if idx_counter % 2 == 0 else 0,
                "subscription_active": 1 if idx_counter % 2 == 0 else 0,
                "stripe_customer_id": None,
                "json_ld": json.dumps({
                    "@context": "https://schema.org",
                    "@type": "LocalBusiness",
                    "name": brand_name,
                    "image": vert['image'],
                    "telephone": phone_num,
                    "email": f"dispatch@{email_domain}",
                    "address": {
                        "@type": "PostalAddress",
                        "streetAddress": full_addr,
                        "addressLocality": city,
                        "addressRegion": state,
                        "postalCode": metro['zip'],
                        "addressCountry": "US"
                    },
                    "geo": {
                        "@type": "GeoCoordinates",
                        "latitude": metro['lat'],
                        "longitude": metro['lng']
                    },
                    "aggregateRating": {
                        "@type": "AggregateRating",
                        "ratingValue": 4.9,
                        "reviewCount": 45 + (idx_counter % 60)
                    },
                    "priceRange": "$$$$"
                }),
                "created_at": "2026-09-20 12:00:00",
                "ad_budget_tier": "TIER_1_ENTERPRISE",
                "estimated_monthly_ad_spend": 3500 + (idx_counter % 20) * 100,
                "station_specs": json.dumps([{"type": f, "status": "Available", "certified": True} for f in vert['fleet']]),
                "latitude": metro['lat'],
                "longitude": metro['lng'],
                "zip_code": metro['zip'],
                "full_address": full_addr,
                "badges": vert['badges'],
                "sentiment_summary": {
                    "cleanliness_score": 98,
                    "punctuality_score": 99,
                    "recommended_by_percentage": 99,
                    "key_highlights": vert['highlights']
                },
                "capacity_matrix": {
                    "min_guests": 1,
                    "max_guests": 5000,
                    "typical_setup_time_mins": 60,
                    "primary_uses": vert['fleet']
                }
            }

            new_vendors.append(vendor_record)
            existing_ids.add(vid)

    print(f"Generated {len(new_vendors)} new vendor records.")
    all_vendors = vendors + new_vendors

    with open(VENDORS_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_vendors, f, indent=2)

    print(f"Successfully wrote {len(all_vendors)} vendors to {VENDORS_FILE}.")

if __name__ == '__main__':
    main()
