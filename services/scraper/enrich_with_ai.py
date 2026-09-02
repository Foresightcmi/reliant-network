import json
import uuid

class AIEntityEnricher:
    """
    Simulates / integrates LLM extraction for raw directory data.
    Adds deep schema entity attributes, SEO tags, JSON-LD, and amenity scoring.
    """
    def __init__(self, niche="luxury_restrooms"):
        self.niche = niche

    def enrich_vendor(self, raw_data):
        name = raw_data.get("name", "Luxury Restroom Co")
        city = raw_data.get("city", "Atlanta")
        state = raw_data.get("state", "GA")
        
        clean_name = name.lower().replace(" ", "-").replace("&", "and")
        slug = f"{clean_name}-{city.lower()}-{state.lower()}"
        slug = "".join(e for e in slug if e.isalnum() or e == "-")

        fleet = raw_data.get("fleet_types", [
            "2-Station Presidential Suite (Up to 150 guests)",
            "4-Station Elegance Trailer (Up to 300 guests)",
            "8-Station Black-Tie Gala Trailer (500+ guests)",
            "ADA Single Private Suite"
        ])

        amenities = raw_data.get("amenities", [
            "Flushing Porcelain Toilets",
            "Full Climate Control (A/C & Heat)",
            "Granite Countertops & Vessel Sinks",
            "LED Vanity Mirrors",
            "Integrated Bluetooth Sound",
            "Hardwood Style Flooring"
        ])

        json_ld = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": name,
            "image": raw_data.get("image_url", "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80"),
            "telephone": raw_data.get("phone", "(404) 555-0199"),
            "email": raw_data.get("email", f"rentals@{slug[:15]}.com"),
            "address": {
                "@type": "PostalAddress",
                "addressLocality": city,
                "addressRegion": state,
                "addressCountry": "US"
            },
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": raw_data.get("rating", 4.9),
                "reviewCount": raw_data.get("review_count", 42)
            },
            "priceRange": raw_data.get("price_range", "$$$ - $$$$")
        }

        return {
            "id": raw_data.get("id", str(uuid.uuid4())[:8]),
            "slug": slug,
            "niche_id": self.niche,
            "name": name,
            "city": city,
            "state": state,
            "address": raw_data.get("address", f"{city}, {state}"),
            "phone": raw_data.get("phone", "(555) 019-2834"),
            "email": raw_data.get("email", f"info@{slug[:12]}.com"),
            "website": raw_data.get("website", f"https://www.{slug[:15]}.com"),
            "rating": raw_data.get("rating", 4.9),
            "review_count": raw_data.get("review_count", 38),
            "min_price": raw_data.get("min_price", 1800),
            "max_price": raw_data.get("max_price", 6500),
            "fleet_types": json.dumps(fleet),
            "amenities": json.dumps(amenities),
            "description": raw_data.get("description", f"{name} is a premier luxury mobile restroom trailer provider serving {city}, {state} and surrounding event venues. Specializing in high-end weddings, VIP corporate retreats, film productions, and private galas."),
            "image_url": raw_data.get("image_url", "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80"),
            "service_radius_miles": raw_data.get("service_radius_miles", 75),
            "verified": 1,
            "claimed": raw_data.get("claimed", 0),
            "subscription_active": raw_data.get("subscription_active", 0),
            "json_ld": json.dumps(json_ld)
        }
