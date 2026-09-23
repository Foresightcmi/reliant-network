import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'pseo_metros.json')

# Massive list of highly lucrative US cities (beyond the top 50)
EXTRA_CITIES = [
    ("San Antonio", "TX"), ("San Diego", "CA"), ("Dallas", "TX"), ("San Jose", "CA"),
    ("Austin", "TX"), ("Jacksonville", "FL"), ("Fort Worth", "TX"), ("Columbus", "OH"),
    ("Indianapolis", "IN"), ("Charlotte", "NC"), ("San Francisco", "CA"), ("Seattle", "WA"),
    ("Denver", "CO"), ("Washington", "DC"), ("Boston", "MA"), ("El Paso", "TX"),
    ("Nashville", "TN"), ("Detroit", "MI"), ("Oklahoma City", "OK"), ("Portland", "OR"),
    ("Las Vegas", "NV"), ("Memphis", "TN"), ("Louisville", "KY"), ("Baltimore", "MD"),
    ("Milwaukee", "WI"), ("Albuquerque", "NM"), ("Tucson", "AZ"), ("Fresno", "CA"),
    ("Mesa", "AZ"), ("Sacramento", "CA"), ("Atlanta", "GA"), ("Kansas City", "MO"),
    ("Colorado Springs", "CO"), ("Omaha", "NE"), ("Raleigh", "NC"), ("Miami", "FL"),
    ("Long Beach", "CA"), ("Virginia Beach", "VA"), ("Oakland", "CA"), ("Minneapolis", "MN"),
    ("Tulsa", "OK"), ("Tampa", "FL"), ("Arlington", "TX"), ("New Orleans", "LA"),
    ("Wichita", "KS"), ("Bakersfield", "CA"), ("Cleveland", "OH"), ("Aurora", "CO"),
    ("Anaheim", "CA"), ("Honolulu", "HI"), ("Santa Ana", "CA"), ("Riverside", "CA"),
    ("Corpus Christi", "TX"), ("Lexington", "KY"), ("Stockton", "CA"), ("Henderson", "NV"),
    ("Saint Paul", "MN"), ("St. Louis", "MO"), ("Cincinnati", "OH"), ("Pittsburgh", "PA"),
    ("Greensboro", "NC"), ("Anchorage", "AK"), ("Plano", "TX"), ("Lincoln", "NE"),
    ("Orlando", "FL"), ("Irvine", "CA"), ("Newark", "NJ"), ("Durham", "NC"),
    ("Chula Vista", "CA"), ("Toledo", "OH"), ("Fort Wayne", "IN"), ("St. Petersburg", "FL"),
    ("Laredo", "TX"), ("Jersey City", "NJ"), ("Chandler", "AZ"), ("Madison", "WI"),
    ("Lubbock", "TX"), ("Scottsdale", "AZ"), ("Reno", "NV"), ("Buffalo", "NY"),
    ("Gilbert", "AZ"), ("Glendale", "AZ"), ("North Las Vegas", "NV"), ("Winston-Salem", "NC"),
    ("Chesapeake", "VA"), ("Norfolk", "VA"), ("Fremont", "CA"), ("Garland", "TX"),
    ("Irving", "TX"), ("Hialeah", "FL"), ("Frisco", "TX"), ("Boise", "ID"),
    ("Richmond", "VA"), ("Baton Rouge", "LA"), ("Spokane", "WA"), ("Des Moines", "IA"),
    ("Tacoma", "WA"), ("San Bernardino", "CA"), ("Modesto", "CA"), ("Fontana", "CA"),
    ("Santa Clarita", "CA"), ("Birmingham", "AL"), ("Oxnard", "CA"), ("Fayetteville", "NC"),
    ("Moreno Valley", "CA"), ("Rochester", "NY"), ("Glendale", "CA"), ("Huntington Beach", "CA"),
    ("Salt Lake City", "UT"), ("Grand Rapids", "MI"), ("Amarillo", "TX"), ("Yonkers", "NY"),
    ("Aurora", "IL"), ("Montgomery", "AL"), ("Akron", "OH"), ("Little Rock", "AR"),
    ("Huntsville", "AL"), ("Augusta", "GA"), ("Port St. Lucie", "FL"), ("Grand Prairie", "TX"),
    ("Columbus", "GA"), ("Tallahassee", "FL"), ("Overland Park", "KS"), ("Tempe", "AZ"),
    ("McKinney", "TX"), ("Mobile", "AL"), ("Cape Coral", "FL"), ("Shreveport", "LA"),
    ("Knoxville", "TN"), ("Worcester", "MA"), ("Ontario", "CA"), ("Vancouver", "WA"),
    ("Sioux Falls", "SD"), ("Chattanooga", "TN"), ("Brownsville", "TX"), ("Fort Lauderdale", "FL"),
    ("Providence", "RI"), ("Newport News", "VA"), ("Rancho Cucamonga", "CA"), ("Santa Rosa", "CA"),
    ("Peoria", "AZ"), ("Oceanside", "CA"), ("Elk Grove", "CA"), ("Salem", "OR"),
    ("Pembroke Pines", "FL"), ("Eugene", "OR"), ("Garden Grove", "CA"), ("Cary", "NC"),
    ("Fort Collins", "CO"), ("Corona", "CA"), ("Springfield", "MO"), ("Jackson", "MS"),
    ("Alexandria", "VA"), ("Hayward", "CA"), ("Clarksville", "TN"), ("Lakewood", "CO"),
    ("Lancaster", "CA"), ("Salinas", "CA"), ("Palmdale", "CA"), ("Hollywood", "FL"),
    ("Springfield", "MA"), ("Macon", "GA"), ("Kansas City", "KS"), ("Sunnyvale", "CA"),
    ("Pomona", "CA"), ("Killeen", "TX"), ("Escondido", "CA"), ("Pasadena", "TX"),
    ("Naperville", "IL"), ("Bellevue", "WA"), ("Joliet", "IL"), ("Murfreesboro", "TN"),
    ("Midland", "TX"), ("Rockford", "IL"), ("Paterson", "NJ"), ("Savannah", "GA"),
    ("Bridgeport", "CT"), ("Torrance", "CA"), ("McAllen", "TX"), ("Syracuse", "NY"),
    ("Surprise", "AZ"), ("Denton", "TX"), ("Roseville", "CA"), ("Thornton", "CO"),
    ("Miramar", "FL"), ("Pasadena", "CA"), ("Mesquite", "TX"), ("Allentown", "PA"),
    ("Olathe", "KS"), ("Dayton", "OH"), ("Waco", "TX"), ("Orange", "CA"),
    ("Fullerton", "CA"), ("Charleston", "SC"), ("West Valley City", "UT"), ("Visalia", "CA"),
    ("Hampton", "VA"), ("Gainesville", "FL"), ("Warren", "MI"), ("Coral Springs", "FL"),
    ("Cedar Rapids", "IA"), ("Round Rock", "TX"), ("Sterling Heights", "MI"), ("Kent", "WA"),
    ("Columbia", "SC"), ("Santa Clara", "CA"), ("New Haven", "CT"), ("Stamford", "CT"),
    ("Concord", "CA"), ("Elizabeth", "NJ"), ("Athens", "GA"), ("Thousand Oaks", "CA"),
    ("Lafayette", "LA"), ("Simi Valley", "CA"), ("Topeka", "KS"), ("Norman", "OK"),
    ("Fargo", "ND"), ("Wilmington", "NC"), ("Abilene", "TX"), ("Odessa", "TX"),
    ("Pearland", "TX"), ("Victorville", "CA"), ("Hartford", "CT"), ("Vallejo", "CA"),
    ("Allentown", "PA"), ("Berkeley", "CA"), ("Richardson", "TX"), ("Arvada", "CO"),
    ("Ann Arbor", "MI"), ("Rochester", "MN"), ("Cambridge", "MA"), ("Sugar Land", "TX"),
    ("Lansing", "MI"), ("Evansville", "IN"), ("College Station", "TX"), ("Fairfield", "CA"),
    ("Clearwater", "FL"), ("Beaumont", "TX"), ("Independence", "MO"), ("Provo", "UT"),
    ("West Jordan", "UT"), ("Murrieta", "CA"), ("El Monte", "CA"), ("Carlsbad", "CA")
]

def expand():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        metros = json.load(f)
    
    existing = {m['city'].lower() for m in metros}
    
    added = 0
    for city, state in EXTRA_CITIES:
        if city.lower() not in existing:
            metros.append({
                "city": city,
                "state": state,
                "state_full": state,
                "slug": f"{city.lower().replace(' ', '-')}-{state.lower()}",
                "avg_cost": 2800,
                "permits": f"{city} Special Event & Construction Sanitation Permit",
                "venues": "Private Estates, Commercial Job Sites & Public Parks",
                "season": "Year-Round (Peak: March-October)",
                "technical_protocols": {
                    "site_ingress_protocol": "Standard flatbed and heavy hauler ingress clearances enforced.",
                    "leveling_standard": "Hydraulic or block-and-tackle leveling to handle local gradients.",
                    "acoustic_noise_curfew": f"Must comply with {city} evening noise ordinances.",
                    "ada_compliance_spec": "Full strict compliance with ADA accessibility ramp standards.",
                    "odor_barrier_spec": "Climate-controlled active venting required during high temperatures."
                },
                "neighborhood_landmarks": [f"Downtown {city}", f"{city} Business Park", f"Central {city} Hub", f"Greater {city} Commercial Area"],
                "power_water_infrastructure": "Dedicated 20A 110V circuit or tier-4 generator. Standard hose spigot connection.",
                "localized_cost_histogram": {"p25": 1800, "median": 2800, "p75": 4200, "p95": 7800},
                "localized_faqs": [
                    {
                        "q": f"What are the commercial sanitation requirements for {city}?",
                        "a": "All commercial operations must maintain a minimum 1:75 ratio of facilities to workers or guests, in compliance with OSHA standards."
                    },
                    {
                        "q": f"How long does it take to deploy a VIP trailer in {city}?",
                        "a": "Emergency dispatches can mobilize within 2-4 hours. Standard bookings require 48 hours notice for guaranteed delivery."
                    }
                ]
            })
            existing.add(city.lower())
            added += 1

    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(metros, f, indent=2)

    print(f"Added {added} new highly populated US cities to pseo_metros.json. Total is now {len(metros)}.")

if __name__ == '__main__':
    expand()
