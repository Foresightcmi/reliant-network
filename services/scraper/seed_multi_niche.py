# -*- coding: utf-8 -*-
import sqlite3
import json
import os
import uuid

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "directory.db")

COLD_STORAGE_VENDORS = [
    {
        "id": "cs-001",
        "niche_id": "commercial_cold_storage",
        "name": "ArcticShield Mobile Reefer & Cold Storage",
        "city": "Atlanta",
        "state": "GA",
        "phone": "(404) 772-9011",
        "email": "dispatch@arcticshieldcold.com",
        "website": "https://arcticshieldcold.com",
        "rating": 4.9,
        "review_count": 52,
        "min_price": 2800,
        "max_price": 14000,
        "fleet_types": ["20ft Electric Walk-In Cooler", "40ft Deep Freeze (-20F) Reefer Trailer", "Emergency Diesel Backup Cooler"],
        "amenities": ["-20F to 50F Temp Range", "24/7 Remote Cellular Telemetry", "Food Grade USDA & FDA Compliant", "Single & 3-Phase Electric Hookup", "Rapid 4-Hour Emergency Dispatch"],
        "image_url": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=800&q=80",
        "description": "Emergency mobile refrigeration and cold storage containers for commercial restaurants, pharmaceutical storage, food distribution, and seasonal agricultural harvests.",
        "claimed": 1,
        "subscription_active": 1,
        "ad_budget_tier": "TIER_1_ENTERPRISE",
        "estimated_monthly_ad_spend": 3800
    },
    {
        "id": "cs-002",
        "niche_id": "commercial_cold_storage",
        "name": "Lone Star Industrial Portable Freezers",
        "city": "Dallas",
        "state": "TX",
        "phone": "(214) 883-4120",
        "email": "rentals@lonestarcold.com",
        "website": "https://lonestarcold.com",
        "rating": 4.8,
        "review_count": 41,
        "min_price": 3200,
        "max_price": 16500,
        "fleet_types": ["53ft Highway Reefer Trailers", "Modular Ground-Level Freezer Pods", "Catering & Banquet Chiller Units"],
        "amenities": ["Dual Redundant Compressors", "Digital Temperature Data Logging", "Hydraulic Liftgate Equipped", "GPS Fleet Tracking"],
        "image_url": "https://images.unsplash.com/photo-1587293852726-70cdb56c2866?auto=format&fit=crop&w=800&q=80",
        "description": "Heavy-duty portable cold storage solutions for DFW corporate events, meat processing facilities, and hospital backup refrigeration.",
        "claimed": 1,
        "subscription_active": 1,
        "ad_budget_tier": "TIER_1_ENTERPRISE",
        "estimated_monthly_ad_spend": 4200
    },
    {
        "id": "cs-003",
        "niche_id": "commercial_cold_storage",
        "name": "Biscayne Bay Mobile Refrigeration Solutions",
        "city": "Miami",
        "state": "FL",
        "phone": "(305) 902-6611",
        "email": "info@biscaynecold.com",
        "website": "https://biscaynecold.com",
        "rating": 4.9,
        "review_count": 38,
        "min_price": 3500,
        "max_price": 18000,
        "fleet_types": ["20ft High-Cube Walk-In Freezer", "Florist & Seafood Chiller Trailers", "Superyacht Provisioning Coolers"],
        "amenities": ["Marine Salt-Air Corrosion Coating", "Microprocessor Temp Controller", "Whisper-Quiet Sound Baffles", "Solar Supplemental Battery"],
        "image_url": "https://images.unsplash.com/photo-1586528116493-a029325540fa?auto=format&fit=crop&w=800&q=80",
        "description": "South Florida premier cold storage rentals for Art Basel catering, luxury yacht provisioning, and commercial seafood distributors.",
        "claimed": 0,
        "subscription_active": 0,
        "ad_budget_tier": "TIER_2_GROWTH",
        "estimated_monthly_ad_spend": 2600
    }
]

CRANE_VENDORS = [
    {
        "id": "cr-001",
        "niche_id": "heavy_crane_rigging",
        "name": "Titan Heavy Crane & Rigging Services",
        "city": "Atlanta",
        "state": "GA",
        "phone": "(404) 662-8819",
        "email": "dispatch@titancranerigging.com",
        "website": "https://titancranerigging.com",
        "rating": 5.0,
        "review_count": 67,
        "min_price": 4500,
        "max_price": 32000,
        "fleet_types": ["50-Ton Hydraulic Truck Crane", "120-Ton All-Terrain Crane", "250-Ton Crawler Crane", "Industrial Rigging Forklifts"],
        "amenities": ["NCCCO Certified Master Operators", "PE Stamped Lift Plans", "$10M Commercial Liability Insurance", "Rooftop HVAC Unit Pick & Drop", "24/7 Industrial Emergency Response"],
        "image_url": "https://images.unsplash.com/photo-1541888946425-d0fbb186156a?auto=format&fit=crop&w=800&q=80",
        "description": "Premier heavy mobile crane rental, certified lift planning, and machinery moving for commercial general contractors, HVAC installers, and civil infrastructure.",
        "claimed": 1,
        "subscription_active": 1,
        "ad_budget_tier": "TIER_1_ENTERPRISE",
        "estimated_monthly_ad_spend": 5500
    },
    {
        "id": "cr-002",
        "niche_id": "heavy_crane_rigging",
        "name": "Lone Star Industrial Rigging & Crane Hire",
        "city": "Dallas",
        "state": "TX",
        "phone": "(214) 791-3304",
        "email": "projects@lonestarcranes.com",
        "website": "https://lonestarcranes.com",
        "rating": 4.9,
        "review_count": 58,
        "min_price": 5200,
        "max_price": 38000,
        "fleet_types": ["70-Ton Rough Terrain Crane", "160-Ton Telescopic Boom Crane", "Heavy Transport Multi-Axle Trailers"],
        "amenities": ["3D CAD Lift Simulation Modeling", "DOT Heavy Haul Transport Permits", "OSHA 1926.1400 Certified", "Modular Steel Erection Rigging"],
        "image_url": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=800&q=80",
        "description": "Turnkey crane rental and heavy industrial rigging services for telecommunication tower erection, steel structural placement, and industrial plant maintenance.",
        "claimed": 1,
        "subscription_active": 1,
        "ad_budget_tier": "TIER_1_ENTERPRISE",
        "estimated_monthly_ad_spend": 6200
    }
]

SENIOR_CARE_VENDORS = [
    {
        "id": "sc-001",
        "niche_id": "senior_care_placement",
        "name": "Oasis Senior Advisors Atlanta",
        "city": "Atlanta",
        "state": "GA",
        "phone": "(404) 555-9281",
        "email": "contact@oasisatlanta.com",
        "website": "https://oasisatlanta.com",
        "rating": 4.9,
        "review_count": 82,
        "min_price": 2500,
        "max_price": 7500,
        "fleet_types": ["Assisted Living Placement", "Memory Care Specialists", "In-Home Care Coordination"],
        "amenities": ["Free Concierge Placement Service", "Dementia & Alzheimer's Specialized", "Local Facility Tours Arranged", "Veterans Aid & Attendance Assistance"],
        "image_url": "https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?auto=format&fit=crop&w=800&q=80",
        "description": "Compassionate, free, and localized senior care placement services matching families with the perfect assisted living or memory care facilities.",
        "claimed": 1,
        "subscription_active": 1,
        "ad_budget_tier": "TIER_1_ENTERPRISE",
        "estimated_monthly_ad_spend": 5000
    },
    {
        "id": "sc-002",
        "niche_id": "senior_care_placement",
        "name": "Dallas Eldercare Consultants",
        "city": "Dallas",
        "state": "TX",
        "phone": "(214) 555-3104",
        "email": "help@dallaseldercare.com",
        "website": "https://dallaseldercare.com",
        "rating": 4.8,
        "review_count": 64,
        "min_price": 3000,
        "max_price": 8500,
        "fleet_types": ["Independent Living", "Assisted Living", "Respite Care Transitions"],
        "amenities": ["RN On-Staff Assessment", "Financial & Medicaid Planning", "24/7 Helpline", "Post-Rehab Placement"],
        "image_url": "https://images.unsplash.com/photo-1516307365426-bea591f05011?auto=format&fit=crop&w=800&q=80",
        "description": "Expert guidance for Dallas families navigating the complexities of elder care, facility selection, and financial planning for long-term care.",
        "claimed": 1,
        "subscription_active": 1,
        "ad_budget_tier": "TIER_2_GROWTH",
        "estimated_monthly_ad_spend": 3000
    }
]

def seed_multi_verticals():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    all_new_vendors = COLD_STORAGE_VENDORS + CRANE_VENDORS + SENIOR_CARE_VENDORS
    for v in all_new_vendors:
        cursor.execute("""
        INSERT INTO vendors (
            id, niche_id, name, city, state, phone, email, website,
            rating, review_count, min_price, max_price, fleet_types,
            amenities, image_url, description, claimed, subscription_active,
            ad_budget_tier, estimated_monthly_ad_spend
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            niche_id = excluded.niche_id,
            name = excluded.name,
            min_price = excluded.min_price,
            max_price = excluded.max_price,
            fleet_types = excluded.fleet_types,
            amenities = excluded.amenities,
            description = excluded.description,
            claimed = excluded.claimed,
            subscription_active = excluded.subscription_active,
            ad_budget_tier = excluded.ad_budget_tier,
            estimated_monthly_ad_spend = excluded.estimated_monthly_ad_spend
        """, (
            v["id"], v["niche_id"], v["name"], v["city"], v["state"], v["phone"], v["email"], v["website"],
            v["rating"], v["review_count"], v["min_price"], v["max_price"], json.dumps(v["fleet_types"]),
            json.dumps(v["amenities"]), v["image_url"], v["description"], v["claimed"], v["subscription_active"],
            v["ad_budget_tier"], v["estimated_monthly_ad_spend"]
        ))

        if v["subscription_active"]:
            payout_id = f"sub-{v['id']}-init"
            cursor.execute("""
            INSERT OR IGNORE INTO payouts (id, vendor_id, amount, type, status)
            VALUES (?, ?, 99, 'MONTHLY_SUBSCRIPTION', 'COMPLETED')
            """, (payout_id, v["id"]))

    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM vendors")
    total_v = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM vendors WHERE subscription_active = 1")
    total_subs = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(amount) FROM payouts WHERE status = 'COMPLETED'")
    total_rev = cursor.fetchone()[0]

    conn.close()

    print(f"Multi-Vertical Seed Complete! Total Directory Listings: {total_v} across 3 high-ticket niches.")
    print(f"Active Subscribed Operators: {total_subs} (${total_subs * 99}/mo MRR). Total Banked: ${total_rev:.2f}")

if __name__ == "__main__":
    seed_multi_verticals()
