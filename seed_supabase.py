import os
import json
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

VENDORS_FILE = os.path.join(os.path.dirname(__file__), 'services', 'data', 'vendors.json')

def seed_vendors():
    with open(VENDORS_FILE, 'r', encoding='utf-8') as f:
        vendors = json.load(f)
    
    # We only insert the required fields according to the schema
    payload = []
    for v in vendors:
        payload.append({
            "id": v.get("id"),
            "niche_id": v.get("niche_id", "luxury_restrooms"),
            "name": v.get("name"),
            "city": v.get("city", "Metro"),
            "state": v.get("state", "US"),
            "phone": v.get("phone", ""),
            "email": v.get("email", ""),
            "website": v.get("website", ""),
            "min_price": v.get("min_price", 0),
            "max_price": v.get("max_price", 0),
            "stripe_account_id": v.get("stripe_account_id", ""),
            "monopoly_active": False
        })
    
    print(f"Uploading {len(payload)} vendors to Supabase...")
    # Insert in batches of 50 to avoid any Supabase anon limits
    batch_size = 50
    for i in range(0, len(payload), batch_size):
        batch = payload[i:i + batch_size]
        response = supabase.table("vendors").upsert(batch).execute()
        print(f"Inserted batch {i//batch_size + 1}")
    
    print("Supabase Data Migration Complete!")

if __name__ == '__main__':
    seed_vendors()
