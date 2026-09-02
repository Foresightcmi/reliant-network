import sqlite3
import json
import os
import sys

sys.path.append(os.path.dirname(__file__))
from enrich_with_ai import AIEntityEnricher

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'directory.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendors (
        id TEXT PRIMARY KEY,
        slug TEXT UNIQUE,
        niche_id TEXT,
        name TEXT,
        city TEXT,
        state TEXT,
        address TEXT,
        phone TEXT,
        email TEXT,
        website TEXT,
        rating REAL,
        review_count INTEGER,
        min_price INTEGER,
        max_price INTEGER,
        fleet_types TEXT,
        amenities TEXT,
        description TEXT,
        image_url TEXT,
        service_radius_miles INTEGER,
        verified INTEGER DEFAULT 1,
        claimed INTEGER DEFAULT 0,
        subscription_active INTEGER DEFAULT 0,
        stripe_customer_id TEXT,
        json_ld TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id TEXT PRIMARY KEY,
        lead_code TEXT UNIQUE,
        niche_id TEXT,
        customer_name TEXT,
        customer_email TEXT,
        customer_phone TEXT,
        city TEXT,
        state TEXT,
        event_date TEXT,
        guest_count INTEGER,
        event_type TEXT,
        budget TEXT,
        notes TEXT,
        status TEXT DEFAULT 'QUALIFIED',
        ai_intent_score INTEGER,
        estimated_quote INTEGER,
        lead_price INTEGER,
        matched_vendor_ids TEXT,
        unlocked_by_vendor_id TEXT,
        stripe_payment_link TEXT,
        payout_status TEXT DEFAULT 'PENDING',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payouts (
        id TEXT PRIMARY KEY,
        lead_id TEXT,
        vendor_id TEXT,
        amount INTEGER,
        type TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT,
        message TEXT,
        details TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    return conn

def seed_vendors():
    conn = init_db()
    cursor = conn.cursor()
    enricher = AIEntityEnricher()

    sample_vendors = [
        # Atlanta Metros
        {"name": "Peachtree Luxury Restrooms & Suites", "city": "Atlanta", "state": "GA", "rating": 5.0, "review_count": 56, "min_price": 2200, "max_price": 7500, "image_url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80", "phone": "(404) 890-1289", "claimed": 1, "subscription_active": 1},
        {"name": "Royal Throne Mobile VIP Suites", "city": "Atlanta", "state": "GA", "rating": 4.9, "review_count": 48, "min_price": 1900, "max_price": 6200, "image_url": "https://images.unsplash.com/photo-1507652313519-d4e9174996dd?auto=format&fit=crop&w=800&q=80", "phone": "(404) 555-7312"},
        {"name": "Southern Elegance Restroom Trailers", "city": "Atlanta", "state": "GA", "rating": 4.8, "review_count": 34, "min_price": 1800, "max_price": 5500, "image_url": "https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?auto=format&fit=crop&w=800&q=80", "phone": "(770) 412-9901"},
        {"name": "Buckhead Black-Tie Sanitation", "city": "Atlanta", "state": "GA", "rating": 4.9, "review_count": 62, "min_price": 2500, "max_price": 8900, "image_url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=800&q=80", "phone": "(404) 912-3401", "claimed": 1, "subscription_active": 1},
        
        # Dallas Metros
        {"name": "Lone Star Luxury Restroom Trailers", "city": "Dallas", "state": "TX", "rating": 5.0, "review_count": 72, "min_price": 2400, "max_price": 8200, "image_url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80", "phone": "(214) 778-9921", "claimed": 1, "subscription_active": 1},
        {"name": "Dallas VIP Mobile Restrooms", "city": "Dallas", "state": "TX", "rating": 4.9, "review_count": 51, "min_price": 2100, "max_price": 6800, "image_url": "https://images.unsplash.com/photo-1507652313519-d4e9174996dd?auto=format&fit=crop&w=800&q=80", "phone": "(214) 555-8812"},
        {"name": "Prestige Event Restrooms DFW", "city": "Dallas", "state": "TX", "rating": 4.8, "review_count": 39, "min_price": 1950, "max_price": 5900, "image_url": "https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?auto=format&fit=crop&w=800&q=80", "phone": "(972) 341-8840"},

        # Miami Metros
        {"name": "South Beach Luxury Restroom Suites", "city": "Miami", "state": "FL", "rating": 5.0, "review_count": 89, "min_price": 2900, "max_price": 9500, "image_url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80", "phone": "(305) 991-3421", "claimed": 1, "subscription_active": 1},
        {"name": "Biscayne VIP Portable Restrooms", "city": "Miami", "state": "FL", "rating": 4.9, "review_count": 44, "min_price": 2600, "max_price": 7800, "image_url": "https://images.unsplash.com/photo-1507652313519-d4e9174996dd?auto=format&fit=crop&w=800&q=80", "phone": "(305) 555-1290"},
        {"name": "Miami Gala Restroom Trailers", "city": "Miami", "state": "FL", "rating": 4.8, "review_count": 37, "min_price": 2400, "max_price": 7100, "image_url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=800&q=80", "phone": "(786) 431-7789"},

        # Austin Metros
        {"name": "Hill Country Luxury Restroom Rentals", "city": "Austin", "state": "TX", "rating": 5.0, "review_count": 65, "min_price": 2300, "max_price": 7400, "image_url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80", "phone": "(512) 884-1290", "claimed": 1, "subscription_active": 1},
        {"name": "Austin VIP Event Sanitation", "city": "Austin", "state": "TX", "rating": 4.9, "review_count": 41, "min_price": 1950, "max_price": 6100, "image_url": "https://images.unsplash.com/photo-1507652313519-d4e9174996dd?auto=format&fit=crop&w=800&q=80", "phone": "(512) 555-9012"},

        # Los Angeles Metros
        {"name": "Beverly Hills Luxury Restrooms & Honeywagons", "city": "Los Angeles", "state": "CA", "rating": 5.0, "review_count": 112, "min_price": 3200, "max_price": 12000, "image_url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80", "phone": "(310) 902-8812", "claimed": 1, "subscription_active": 1},
        {"name": "Sunset VIP Trailer Rentals LA", "city": "Los Angeles", "state": "CA", "rating": 4.9, "review_count": 84, "min_price": 2800, "max_price": 9400, "image_url": "https://images.unsplash.com/photo-1507652313519-d4e9174996dd?auto=format&fit=crop&w=800&q=80", "phone": "(323) 555-4491"},

        # Chicago Metros
        {"name": "Windy City Luxury Restroom Suites", "city": "Chicago", "state": "IL", "rating": 4.9, "review_count": 68, "min_price": 2200, "max_price": 7200, "image_url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80", "phone": "(312) 881-2299", "claimed": 1, "subscription_active": 1},
        {"name": "Michigan Avenue Event Sanitation", "city": "Chicago", "state": "IL", "rating": 4.8, "review_count": 47, "min_price": 1900, "max_price": 6000, "image_url": "https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?auto=format&fit=crop&w=800&q=80", "phone": "(312) 555-8831"}
    ]

    for raw in sample_vendors:
        enriched = enricher.enrich_vendor(raw)
        cursor.execute("""
        INSERT OR REPLACE INTO vendors (
            id, slug, niche_id, name, city, state, address, phone, email, website,
            rating, review_count, min_price, max_price, fleet_types, amenities,
            description, image_url, service_radius_miles, verified, claimed,
            subscription_active, json_ld
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?
        )
        """, (
            enriched['id'], enriched['slug'], enriched['niche_id'], enriched['name'],
            enriched['city'], enriched['state'], enriched['address'], enriched['phone'],
            enriched['email'], enriched['website'], enriched['rating'], enriched['review_count'],
            enriched['min_price'], enriched['max_price'], enriched['fleet_types'], enriched['amenities'],
            enriched['description'], enriched['image_url'], enriched['service_radius_miles'],
            enriched['verified'], enriched['claimed'], enriched['subscription_active'], enriched['json_ld']
        ))

    # Seed Sample Active Revenue & Leads to demonstrate live cash flow
    sample_leads = [
        ('lead-001', 'LUX-8912', 'luxury_restrooms', 'Caroline Vance (Atlanta Wedding)', 'caroline.vance@gmail.com', '(404) 555-2311', 'Atlanta', 'GA', '2026-10-15', 250, 'Wedding', '$3,500 - $5,000', 'Requires 4-station trailer with A/C & generator for outdoor vineyard venue.', 'SOLD', 98, 3800, 85, '["Peachtree Luxury Restrooms & Suites"]', 'Peachtree Luxury Restrooms & Suites', 'https://buy.stripe.com/test_luxury_lead_85', 'PAID'),
        ('lead-002', 'LUX-4421', 'luxury_restrooms', 'Marcus Sterling (Tech Gala)', 'm.sterling@summitmedia.com', '(214) 555-9081', 'Dallas', 'TX', '2026-09-20', 400, 'Corporate Event', '$5,000 - $8,000', 'Black-tie VIP luxury suites with on-site attendant for 2-day conference.', 'SOLD', 95, 6200, 125, '["Lone Star Luxury Restroom Trailers"]', 'Lone Star Luxury Restroom Trailers', 'https://buy.stripe.com/test_luxury_lead_125', 'PAID'),
        ('lead-003', 'LUX-7732', 'luxury_restrooms', 'Elena Rostova (Art Basel VIP Lounge)', 'elena@rostovadesigns.com', '(305) 555-8842', 'Miami', 'FL', '2026-11-04', 300, 'VIP Gala', '$4,000 - $6,500', 'High-end design aesthetic trailer with marble vanity and gold fixtures.', 'SOLD', 96, 4900, 110, '["South Beach Luxury Restroom Suites"]', 'South Beach Luxury Restroom Suites', 'https://buy.stripe.com/test_luxury_lead_110', 'PAID')
    ]

    for ld in sample_leads:
        cursor.execute("""
        INSERT OR REPLACE INTO leads (
            id, lead_code, niche_id, customer_name, customer_email, customer_phone,
            city, state, event_date, guest_count, event_type, budget, notes,
            status, ai_intent_score, estimated_quote, lead_price, matched_vendor_ids,
            unlocked_by_vendor_id, stripe_payment_link, payout_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, ld)

    # Record payouts
    cursor.execute("INSERT OR REPLACE INTO payouts (id, lead_id, vendor_id, amount, type, status) VALUES ('pay-001', 'lead-001', 'vendor-1', 85, 'PAY_PER_LEAD', 'COMPLETED')")
    cursor.execute("INSERT OR REPLACE INTO payouts (id, lead_id, vendor_id, amount, type, status) VALUES ('pay-002', 'lead-002', 'vendor-5', 125, 'PAY_PER_LEAD', 'COMPLETED')")
    cursor.execute("INSERT OR REPLACE INTO payouts (id, lead_id, vendor_id, amount, type, status) VALUES ('pay-003', 'lead-003', 'vendor-8', 110, 'PAY_PER_LEAD', 'COMPLETED')")
    cursor.execute("INSERT OR REPLACE INTO payouts (id, lead_id, vendor_id, amount, type, status) VALUES ('sub-001', NULL, 'vendor-1', 99, 'MONTHLY_SUBSCRIPTION', 'COMPLETED')")
    cursor.execute("INSERT OR REPLACE INTO payouts (id, lead_id, vendor_id, amount, type, status) VALUES ('sub-002', NULL, 'vendor-5', 99, 'MONTHLY_SUBSCRIPTION', 'COMPLETED')")
    cursor.execute("INSERT OR REPLACE INTO payouts (id, lead_id, vendor_id, amount, type, status) VALUES ('sub-003', NULL, 'vendor-8', 99, 'MONTHLY_SUBSCRIPTION', 'COMPLETED')")
    cursor.execute("INSERT OR REPLACE INTO payouts (id, lead_id, vendor_id, amount, type, status) VALUES ('sub-004', NULL, 'vendor-4', 99, 'MONTHLY_SUBSCRIPTION', 'COMPLETED')")
    cursor.execute("INSERT OR REPLACE INTO payouts (id, lead_id, vendor_id, amount, type, status) VALUES ('sub-005', NULL, 'vendor-11', 99, 'MONTHLY_SUBSCRIPTION', 'COMPLETED')")
    cursor.execute("INSERT OR REPLACE INTO payouts (id, lead_id, vendor_id, amount, type, status) VALUES ('sub-006', NULL, 'vendor-13', 99, 'MONTHLY_SUBSCRIPTION', 'COMPLETED')")
    cursor.execute("INSERT OR REPLACE INTO payouts (id, lead_id, vendor_id, amount, type, status) VALUES ('sub-007', NULL, 'vendor-15', 99, 'MONTHLY_SUBSCRIPTION', 'COMPLETED')")

    conn.commit()
    conn.close()
    print(f"Successfully seeded database with {len(sample_vendors)} vendors and live revenue streams at: {DB_PATH}")

if __name__ == '__main__':
    seed_vendors()
