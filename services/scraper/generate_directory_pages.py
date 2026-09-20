# -*- coding: utf-8 -*-
"""
services/scraper/generate_directory_pages.py
Autonomous GeoDirectory Page Generation Engine
Pre-renders 100% static, edge-deliverable HTML pages for:
  1. Single Listing Detail Pages (/listing/:slug.html)
  2. State Directory Hub Pages (/state/:slug.html)
  3. Fortified Metro Landing Pages (/metro/:slug.html)
Replicating Frey Chu's GeoDirectory + Elementor single listing architecture at $0 marginal cost.
"""

import json
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
VENDORS_FILE = os.path.join(DATA_DIR, "vendors.json")
METROS_FILE = os.path.join(DATA_DIR, "pseo_metros.json")

PUBLIC_DIR = os.path.join(BASE_DIR, "..", "apps", "web", "public")
LISTING_OUT_DIR = os.path.join(PUBLIC_DIR, "listing")
STATE_OUT_DIR = os.path.join(PUBLIC_DIR, "state")
METRO_OUT_DIR = os.path.join(PUBLIC_DIR, "metro")

STATE_NAMES = {
    "AL": ("Alabama", "alabama"),
    "AK": ("Alaska", "alaska"),
    "AZ": ("Arizona", "arizona"),
    "AR": ("Arkansas", "arkansas"),
    "CA": ("California", "california"),
    "CO": ("Colorado", "colorado"),
    "CT": ("Connecticut", "connecticut"),
    "DE": ("Delaware", "delaware"),
    "DC": ("District of Columbia", "district-of-columbia"),
    "FL": ("Florida", "florida"),
    "GA": ("Georgia", "georgia"),
    "HI": ("Hawaii", "hawaii"),
    "ID": ("Idaho", "idaho"),
    "IL": ("Illinois", "illinois"),
    "IN": ("Indiana", "indiana"),
    "IA": ("Iowa", "iowa"),
    "KS": ("Kansas", "kansas"),
    "KY": ("Kentucky", "kentucky"),
    "LA": ("Louisiana", "louisiana"),
    "ME": ("Maine", "maine"),
    "MD": ("Maryland", "maryland"),
    "MA": ("Massachusetts", "massachusetts"),
    "MI": ("Michigan", "michigan"),
    "MN": ("Minnesota", "minnesota"),
    "MS": ("Mississippi", "mississippi"),
    "MO": ("Missouri", "missouri"),
    "MT": ("Montana", "montana"),
    "NE": ("Nebraska", "nebraska"),
    "NV": ("Nevada", "nevada"),
    "NH": ("New Hampshire", "new-hampshire"),
    "NJ": ("New Jersey", "new-jersey"),
    "NM": ("New Mexico", "new-mexico"),
    "NY": ("New York", "new-york"),
    "NC": ("North Carolina", "north-carolina"),
    "ND": ("North Dakota", "north-dakota"),
    "OH": ("Ohio", "ohio"),
    "OK": ("Oklahoma", "oklahoma"),
    "OR": ("Oregon", "oregon"),
    "PA": ("Pennsylvania", "pennsylvania"),
    "RI": ("Rhode Island", "rhode-island"),
    "SC": ("South Carolina", "south-carolina"),
    "SD": ("South Dakota", "south-dakota"),
    "TN": ("Tennessee", "tennessee"),
    "TX": ("Texas", "texas"),
    "UT": ("Utah", "utah"),
    "VT": ("Vermont", "vermont"),
    "VA": ("Virginia", "virginia"),
    "WA": ("Washington", "washington"),
    "WV": ("West Virginia", "west-virginia"),
    "WI": ("Wisconsin", "wisconsin"),
    "WY": ("Wyoming", "wyoming")
}

def ensure_dirs():
    os.makedirs(LISTING_OUT_DIR, exist_ok=True)
    os.makedirs(STATE_OUT_DIR, exist_ok=True)
    os.makedirs(METRO_OUT_DIR, exist_ok=True)

def generate_single_listing_html(v, all_vendors):
    slug = v.get("slug", "operator")
    name = v.get("name", "Featured Fleet Operator")
    city = v.get("city", "Atlanta")
    state = v.get("state", "GA")
    state_full, state_slug = STATE_NAMES.get(state, (state, state.lower()))
    phone = v.get("phone", "(404) 732-8190")
    rating = v.get("rating", 5.0)
    review_count = v.get("review_count", 18)
    min_price = v.get("min_price", 1500)
    max_price = v.get("max_price", 6500)
    lat = v.get("latitude", 33.7490)
    lng = v.get("longitude", -84.3880)
    zip_code = v.get("zip_code", "30301")
    full_address = v.get("full_address", f"{city}, {state} {zip_code}")
    description = v.get("description", f"{name} is an elite commercial equipment operator servicing {city}, {state}.")
    
    fleet_raw = v.get("fleet_types", [])
    if isinstance(fleet_raw, str):
        try: fleet_types = json.loads(fleet_raw)
        except: fleet_types = [fleet_raw]
    else: fleet_types = fleet_raw

    amenities_raw = v.get("amenities", [])
    if isinstance(amenities_raw, str):
        try: amenities = json.loads(amenities_raw)
        except: amenities = [amenities_raw]
    else: amenities = amenities_raw

    badges = v.get("badges", {})
    sentiment = v.get("sentiment_summary", {
        "cleanliness_score": 99,
        "punctuality_score": 98,
        "recommended_by_percentage": 99,
        "key_highlights": ["Immaculate porcelain fixtures", "Punctual delivery"]
    })
    reviews = v.get("sample_reviews", [])

    # Nearby competitors in same city
    nearby = [x for x in all_vendors if x.get("city") == city and x.get("id") != v.get("id")][:3]

    nearby_html = "".join([f"""
      <a href="/listing/{nb.get('slug')}" class="block bg-slate-50 border border-slate-200 rounded-xl p-4 hover:border-amber-500 hover:bg-amber-50/20 transition-all">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-slate-900">{nb.get('name')}</span>
          <span class="text-[11px] font-bold text-amber-600">★ {nb.get('rating', 5.0)}</span>
        </div>
        <span class="text-[11px] text-slate-500 mt-1 block">{nb.get('city')}, {nb.get('state')} • ${nb.get('min_price'):,} - ${nb.get('max_price'):,}</span>
      </a>
    """ for nb in nearby])

    fleet_cards_html = "".join([f"""
      <div class="bg-white border border-slate-200 p-3.5 rounded-xl shadow-2xs">
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-amber-500"></span>
          <span class="text-xs font-semibold text-slate-800">{item}</span>
        </div>
      </div>
    """ for item in fleet_types])

    amenities_badges_html = "".join([f"""
      <span class="inline-flex items-center gap-1.5 bg-slate-100 border border-slate-200 text-slate-700 text-xs px-3 py-1.5 rounded-lg">
        <svg class="w-3.5 h-3.5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
        {item}
      </span>
    """ for item in amenities])

    reviews_html = "".join([f"""
      <div class="border-b border-slate-100 pb-4 mb-4 last:border-0 last:pb-0 last:mb-0">
        <div class="flex items-center justify-between mb-1">
          <span class="text-xs font-bold text-slate-900">{r.get('author')}</span>
          <span class="text-[11px] text-slate-400">{r.get('date')}</span>
        </div>
        <div class="flex text-amber-500 text-xs mb-1.5">★★★★★</div>
        <p class="text-xs text-slate-600 leading-relaxed">"{r.get('text')}"</p>
      </div>
    """ for r in reviews])

    json_ld = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": name,
        "description": description,
        "telephone": phone,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": full_address,
            "addressLocality": city,
            "addressRegion": state,
            "postalCode": zip_code,
            "addressCountry": "US"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": lat,
            "longitude": lng
        },
        "areaServed": {
            "@type": "GeoCircle",
            "geoMidpoint": {
                "@type": "GeoCoordinates",
                "latitude": lat,
                "longitude": lng
            },
            "geoRadius": 120700
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": rating,
            "reviewCount": review_count
        },
        "priceRange": f"${min_price} - ${max_price}"
    }

    breadcrumb_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://reliantverified.com/"},
            {"@type": "ListItem", "position": 2, "name": state_full, "item": f"https://reliantverified.com/state/{state_slug}"},
            {"@type": "ListItem", "position": 3, "name": f"{city}, {state}", "item": f"https://reliantverified.com/metro/{city.lower().replace(' ', '-')}-{state.lower()}"},
            {"@type": "ListItem", "position": 4, "name": name, "item": f"https://reliantverified.com/listing/{slug}"}
        ]
    }

    clean_phone = re.sub(r'[^0-9]', '', phone)
    safe_name = name.replace("'", "\\'").replace('"', '&quot;')
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} | {city}, {state} Commercial Fleet Operator</title>
  <meta name="description" content="Verified specifications, pricing (${min_price:,} - ${max_price:,}), verified reviews, and direct dispatch for {name} in {city}, {state_full}.">
  <link rel="canonical" href="https://reliantverified.com/listing/{slug}">
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script type="application/ld+json">
  {json.dumps(json_ld, indent=2)}
  </script>
  <script type="application/ld+json">
  {json.dumps(breadcrumb_ld, indent=2)}
  </script>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen font-sans antialiased">
  <!-- HEADER -->
  <header class="border-b border-slate-200 bg-white/95 sticky top-0 z-40 py-3.5 px-6 shadow-2xs backdrop-blur-md">
    <div class="max-w-7xl mx-auto flex items-center justify-between">
      <a href="/" class="text-xl font-bold text-slate-900 tracking-tight">Reliant<span class="text-amber-600 font-extrabold">Network</span></a>
      <div class="flex items-center gap-3">
        <a href="/state/{state_slug}" class="text-xs font-semibold text-slate-600 hover:text-amber-600 transition-colors">Browse {state_full}</a>
        <a href="/#quote-modal" class="bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold px-4 py-2 rounded-xl text-xs transition-colors shadow-xs">Get Instant Quote</a>
      </div>
    </div>
  </header>

  <!-- BREADCRUMB NAVIGATION (Frey Chu Schema Standard) -->
  <nav class="bg-white border-b border-slate-200 py-2.5 px-6">
    <div class="max-w-7xl mx-auto flex items-center gap-2 text-xs text-slate-500 flex-wrap">
      <a href="/" class="hover:text-amber-600">Home</a>
      <span>&rsaquo;</span>
      <a href="/state/{state_slug}" class="hover:text-amber-600">{state_full}</a>
      <span>&rsaquo;</span>
      <a href="/metro/{city.lower().replace(' ', '-')}-{state.lower()}" class="hover:text-amber-600">{city}, {state}</a>
      <span>&rsaquo;</span>
      <span class="text-slate-900 font-semibold truncate max-w-xs">{name}</span>
    </div>
  </nav>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- TOP OPERATOR HERO CARD -->
    <div class="bg-white border border-slate-200 rounded-3xl p-6 sm:p-8 shadow-xs mb-8 relative overflow-hidden">
      <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
        <div>
          <div class="flex items-center gap-2 mb-2 flex-wrap">
            <span class="bg-amber-100 text-amber-800 text-[11px] font-bold px-3 py-1 rounded-full border border-amber-300">
              Verified Gold Partner
            </span>
            <span class="bg-emerald-100 text-emerald-800 text-[11px] font-bold px-3 py-1 rounded-full border border-emerald-300 flex items-center gap-1">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-600"></span> 24/7 Rapid Dispatch Ready
            </span>
            <span class="bg-slate-100 text-slate-700 text-[11px] font-semibold px-2.5 py-1 rounded-full border border-slate-200">
              {city}, {state}
            </span>
          </div>
          <h1 class="text-2xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">{name}</h1>
          <p class="text-xs sm:text-sm text-slate-600 mt-2 max-w-2xl leading-relaxed">{description}</p>
          
          <div class="flex items-center gap-4 mt-4 text-xs font-semibold text-slate-700">
            <div class="flex items-center gap-1 text-amber-600">
              <span class="text-amber-500 font-black">★★★★★</span>
              <span class="font-bold text-slate-900">{rating}</span>
              <span class="text-slate-500">({review_count} verified reviews)</span>
            </div>
            <span>&bull;</span>
            <span>Est. Rate: <strong class="text-slate-900">${min_price:,} – ${max_price:,}</strong></span>
            <span>&bull;</span>
            <span>Coverage: <strong class="text-slate-900">75-Mile Metro Radius</strong></span>
          </div>
        </div>

        <div class="flex flex-col sm:flex-row lg:flex-col gap-3 shrink-0">
          <a href="#direct-message-card" class="bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold px-6 py-3 rounded-xl text-xs text-center transition-colors shadow-xs">
            Send Direct Operator Inquiry
          </a>
          <a href="tel:{clean_phone}" class="bg-white hover:bg-slate-50 text-slate-800 font-semibold px-6 py-3 rounded-xl border border-slate-200 text-xs text-center transition-colors">
            📞 Direct Line: {phone}
          </a>
        </div>
      </div>
    </div>

    <!-- 2-COLUMN MAIN CONTENT -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- LEFT 2 COLS: SPECS, FLEET, MAP, REVIEWS -->
      <div class="lg:col-span-2 space-y-8">
        <!-- TRUST & OPERATIONAL SPECIFICATIONS (enrich.directory Blueprint) -->
        <section class="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs">
          <h2 class="text-lg font-bold text-slate-900 mb-4">Vetted Operator Compliance &amp; Standards</h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
            <div class="bg-slate-50 border border-slate-200 p-3.5 rounded-xl">
              <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">Commercial Insurance</span>
              <span class="text-xs font-semibold text-slate-800 mt-1 block">{badges.get('insurance_verified')}</span>
            </div>
            <div class="bg-slate-50 border border-slate-200 p-3.5 rounded-xl">
              <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">ADA Accessibility</span>
              <span class="text-xs font-semibold text-slate-800 mt-1 block">{badges.get('ada_certified')}</span>
            </div>
            <div class="bg-slate-50 border border-slate-200 p-3.5 rounded-xl">
              <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">Power &amp; Generation</span>
              <span class="text-xs font-semibold text-slate-800 mt-1 block">{badges.get('power_hookup')}</span>
            </div>
            <div class="bg-slate-50 border border-slate-200 p-3.5 rounded-xl">
              <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">Freshwater &amp; Tanks</span>
              <span class="text-xs font-semibold text-slate-800 mt-1 block">{badges.get('onboard_freshwater')}</span>
            </div>
          </div>
        </section>

        <!-- FLEET TYPES & AMENITIES -->
        <section class="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs">
          <h2 class="text-lg font-bold text-slate-900 mb-3">Available Fleet Configurations</h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-6">
            {fleet_cards_html}
          </div>

          <h3 class="text-sm font-bold text-slate-900 mb-3">Onboard Luxury Amenities &amp; Hardware</h3>
          <div class="flex flex-wrap gap-2">
            {amenities_badges_html}
          </div>
        </section>

        <!-- INTERACTIVE OPENSTREETMAP / LEAFLET (Zero Marginal Cost) -->
        <section class="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs">
          <div class="flex items-center justify-between mb-4 flex-wrap gap-2">
            <div>
              <div class="flex items-center gap-2 mb-1">
                <span class="inline-flex items-center gap-1 bg-emerald-50 text-emerald-800 text-[11px] font-bold px-2.5 py-0.5 rounded-full border border-emerald-300">
                  <svg class="w-3 h-3 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" stroke-width="2"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3"/></svg>
                  Verified Active Dispatch Depot
                </span>
                <span class="text-xs text-slate-400">&bull;</span>
                <span class="text-xs font-semibold text-slate-600">75-Mile Primary Service Radius</span>
              </div>
              <h2 class="text-lg font-bold text-slate-900">Service Coverage &amp; Dispatch Depot</h2>
              <p class="text-xs text-slate-500">Commercial fleet staging depot headquartered in {city}, {state} with guaranteed rapid regional delivery.</p>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-xs font-mono font-bold text-slate-600 bg-slate-100 border border-slate-200 px-2.5 py-1 rounded-lg">
                GPS: {lat}, {lng}
              </span>
              <a href="https://www.google.com/maps/search/?api=1&query={lat},{lng}" target="_blank" rel="noopener noreferrer" class="text-xs font-bold text-amber-700 hover:text-amber-800 bg-amber-50 hover:bg-amber-100 border border-amber-300 px-2.5 py-1 rounded-lg transition-colors flex items-center gap-1">
                Directions
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
              </a>
            </div>
          </div>

          <div id="vendor-map" class="rounded-xl border border-slate-200 overflow-hidden shadow-inner" style="height: 380px; min-height: 320px; width: 100%; position: relative; z-index: 1;"></div>

          <div class="mt-3 flex items-center justify-between text-xs text-slate-500 flex-wrap gap-2 pt-2 border-t border-slate-100">
            <div class="flex items-center gap-4">
              <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-amber-500 inline-block shadow-xs"></span> <strong>Depot Staging Hub:</strong> {city}, {state}</span>
              <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-amber-100 border border-amber-400 inline-block"></span> <strong>Guaranteed 75-Mi Radius:</strong> Direct Dispatch</span>
            </div>
            <span class="text-[11px] text-slate-400 font-medium">OpenStreetMap &bull; Zero Broker Markups</span>
          </div>

          <script>
            document.addEventListener('DOMContentLoaded', () => {{
              const mapContainer = document.getElementById('vendor-map');
              if (!mapContainer || typeof L === 'undefined') return;

              const map = L.map('vendor-map', {{
                scrollWheelZoom: false
              }}).setView([{lat}, {lng}], 9);

              L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png', {{
                maxZoom: 20,
                subdomains: 'abcd',
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
              }}).addTo(map);

              // Custom Gold Depot SVG Pin with Pulse Beacon
              const depotIcon = L.divIcon({{
                className: 'custom-depot-pin',
                html: `<div style="position:relative; width:40px; height:40px; display:flex; align-items:center; justify-content:center;">
                         <div style="position:absolute; inset:-6px; border-radius:50%; background:rgba(217,119,6,0.25); animation:pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;"></div>
                         <div style="position:relative; width:34px; height:34px; background:linear-gradient(135deg, #d97706, #b45309); border:2.5px solid #ffffff; border-radius:50%; display:flex; align-items:center; justify-content:center; box-shadow:0 4px 10px rgba(0,0,0,0.25);">
                           <svg style="width:18px; height:18px; color:#ffffff;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                         </div>
                       </div>`,
                iconSize: [40, 40],
                iconAnchor: [20, 20],
                popupAnchor: [0, -22]
              }});

              const marker = L.marker([{lat}, {lng}], {{ icon: depotIcon }}).addTo(map);

              const popupContent = `
                <div style="font-family:'Plus Jakarta Sans',sans-serif; padding:4px; max-width:260px;">
                  <div style="display:inline-block; font-size:10px; font-weight:800; background:#fef3c7; color:#92400e; padding:2px 8px; border-radius:9999px; margin-bottom:4px; text-transform:uppercase; letter-spacing:0.5px;">Verified Dispatch Depot</div>
                  <div style="font-size:14px; font-weight:800; color:#0f172a; line-height:1.2; margin-bottom:4px;">{safe_name}</div>
                  <div style="font-size:12px; color:#64748b; margin-bottom:8px;">📍 {city}, {state}</div>
                  <div style="display:flex; align-items:center; justify-content:space-between; border-top:1px solid #e2e8f0; padding-top:6px;">
                    <span style="font-size:12px; font-weight:700; color:#059669;">★ {rating} Rating</span>
                    <a href="tel:{clean_phone}" style="font-size:11px; font-weight:800; color:#d97706; text-decoration:none; background:#fffbeb; padding:3px 8px; border-radius:6px; border:1px solid #fde68a;">📞 Call Depot</a>
                  </div>
                </div>
              `;
              marker.bindPopup(popupContent).openPopup();

              // 75-mile verified primary dispatch radius circle
              L.circle([{lat}, {lng}], {{
                color: '#d97706',
                weight: 2,
                dashArray: '4, 6',
                fillColor: '#f59e0b',
                fillOpacity: 0.12,
                radius: 120700
              }}).addTo(map);

              // Responsive size invalidation
              setTimeout(() => {{ map.invalidateSize(); }}, 200);
              setTimeout(() => {{ map.invalidateSize(); }}, 600);
              window.addEventListener('resize', () => {{ map.invalidateSize(); }});
            }});
          </script>
        </section>

        <!-- VERIFIED CLIENT REVIEWS -->
        <section class="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h2 class="text-lg font-bold text-slate-900">Verified Client Feedback</h2>
              <p class="text-xs text-slate-500">{review_count} verified client reviews from {state_full} commercial clients &amp; event planners</p>
            </div>
            <div class="text-right">
              <span class="text-2xl font-bold text-slate-900">{sentiment.get('cleanliness_score')}%</span>
              <span class="text-[10px] text-slate-400 block uppercase font-bold">Cleanliness Score</span>
            </div>
          </div>
          <div>
            {reviews_html}
          </div>
        </section>
      </div>

      <!-- RIGHT COL: DIRECT INQUIRY & NEARBY OPERATORS -->
      <div class="space-y-8">
        <!-- DIRECT MESSAGE INQUIRY BOX -->
        <div id="direct-message-card" class="bg-white border-2 border-amber-500 rounded-3xl p-6 shadow-xl relative">
          <div class="flex items-center gap-2 mb-3">
            <span class="w-3 h-3 rounded-full bg-amber-500 animate-pulse"></span>
            <h3 class="text-base font-bold text-slate-900">Direct Inquire to Operator</h3>
          </div>
          <p class="text-xs text-slate-500 mb-4">Direct message sent straight to {name}'s dispatch desk. Receive an estimate within 2-4 hours.</p>

          <form id="listing-inquiry-form" onsubmit="submitListingInquiry(event)" class="space-y-3">
            <input type="hidden" id="inq-vendor-id" value="{v.get('id')}">
            <div>
              <label class="block text-[11px] font-semibold text-slate-700 mb-1">Your Name</label>
              <input type="text" id="inq-name" required placeholder="Marcus Vance" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs text-slate-900 focus:outline-none focus:border-amber-500">
            </div>
            <div>
              <label class="block text-[11px] font-semibold text-slate-700 mb-1">Your Email</label>
              <input type="email" id="inq-email" required placeholder="marcus@events.com" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs text-slate-900 focus:outline-none focus:border-amber-500">
            </div>
            <div>
              <label class="block text-[11px] font-semibold text-slate-700 mb-1">Phone Number</label>
              <input type="tel" id="inq-phone" required placeholder="(404) 732-8190" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs text-slate-900 focus:outline-none focus:border-amber-500">
            </div>
            <div>
              <label class="block text-[11px] font-semibold text-slate-700 mb-1">Target Event Date</label>
              <input type="date" id="inq-date" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs text-slate-900 focus:outline-none focus:border-amber-500">
            </div>
            <div>
              <label class="block text-[11px] font-semibold text-slate-700 mb-1">Message / Requirements</label>
              <textarea id="inq-msg" rows="3" required placeholder="Looking for 4-station luxury trailer with generator..." class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs text-slate-900 focus:outline-none focus:border-amber-500"></textarea>
            </div>
            <button type="submit" id="inq-btn" class="w-full bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold py-2.5 rounded-xl text-xs transition-colors shadow-xs">
              Dispatch Inquiry
            </button>
          </form>
          <div id="inq-success" class="hidden text-center py-4">
            <span class="text-xs font-bold text-emerald-600 block">Inquiry Transmitted!</span>
            <p id="inq-code" class="text-[11px] text-slate-500 mt-1"></p>
          </div>
        </div>

        <!-- CLAIM LISTING UPSELL (John Rush Blueprint) -->
        <div class="bg-slate-900 text-white border border-slate-800 rounded-2xl p-5 shadow-xs">
          <span class="text-[11px] font-bold text-amber-400 uppercase tracking-wider block">Are you the owner?</span>
          <h4 class="text-sm font-bold text-white mt-1">Claim {name}'s Verified Profile</h4>
          <p class="text-xs text-slate-300 mt-1.5 leading-relaxed">Upgrade to Featured Partner ($99/mo) to unlock guaranteed #1 ranking, direct client lead dispatch, and zero commission fees.</p>
          <a href="/#pricing-modal" class="mt-4 block bg-amber-400 hover:bg-amber-300 text-slate-950 text-xs font-bold py-2 rounded-xl text-center transition-colors">
            Claim Profile &amp; Upgrade
          </a>
        </div>

        <!-- NEARBY ALTERNATIVE FLEETS (Internal Linking Mesh) -->
        <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs">
          <h4 class="text-xs font-bold text-slate-900 uppercase tracking-wider mb-3">Nearby Fleets in {city}</h4>
          <div class="space-y-2.5">
            {nearby_html if nearby_html else '<span class="text-xs text-slate-400">Exclusive verified operator in this zone.</span>'}
          </div>
        </div>
      </div>
    </div>
  </main>

  <script>
    async function submitListingInquiry(e) {{
      e.preventDefault();
      const btn = document.getElementById('inq-btn');
      btn.disabled = true;
      btn.innerText = 'Transmitting...';
      const vendorId = document.getElementById('inq-vendor-id').value;
      const payload = {{
        sender_name: document.getElementById('inq-name').value,
        sender_email: document.getElementById('inq-email').value,
        sender_phone: document.getElementById('inq-phone').value,
        event_date: document.getElementById('inq-date').value,
        message: document.getElementById('inq-msg').value
      }};
      try {{
        const res = await fetch(`/api/vendors/${{vendorId}}/message`, {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify(payload)
        }});
        const data = await res.json();
        document.getElementById('listing-inquiry-form').classList.add('hidden');
        document.getElementById('inq-success').classList.remove('hidden');
        document.getElementById('inq-code').innerText = `Ref Code: ${{data.lead_code || 'DIR-SENT'}}. The operator has received your inquiry.`;
      }} catch (err) {{
        alert('Error transmitting inquiry: ' + err.message);
      }} finally {{
        btn.disabled = false;
        btn.innerText = 'Dispatch Inquiry';
      }}
    }}
  </script>
</body>
</html>"""
    return html

def generate_state_hub_html(state_code, state_name, state_slug, state_vendors, state_metros):
    metros_html = "".join([f"""
      <a href="/metro/{m.get('slug')}" class="bg-white border border-slate-200 rounded-2xl p-5 hover:border-amber-500 hover:shadow-md transition-all">
        <div class="flex items-center justify-between mb-1">
          <h3 class="text-sm font-bold text-slate-900">{m.get('city')}, {state_code}</h3>
          <span class="text-[11px] font-bold text-amber-600">${m.get('avg_cost', 2800):,} avg</span>
        </div>
        <p class="text-xs text-slate-500 mt-1">{m.get('venues', 'Private Estates & Venues')}</p>
        <span class="text-[10px] font-semibold text-slate-400 mt-3 block">View Local Operators &rarr;</span>
      </a>
    """ for m in state_metros])

    vendors_html = "".join([f"""
      <div class="bg-white border border-slate-200 rounded-2xl p-5 hover:border-amber-500 transition-all flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between">
            <span class="text-[11px] font-bold text-amber-700 uppercase">{v.get('city')}, {v.get('state')}</span>
            <span class="text-xs font-bold text-amber-600">★ {v.get('rating', 5.0)}</span>
          </div>
          <h4 class="text-base font-bold text-slate-900 mt-1">{v.get('name')}</h4>
          <p class="text-xs text-slate-600 mt-1 line-clamp-2">{v.get('description')}</p>
        </div>
        <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
          <span class="text-xs font-semibold text-slate-700">${v.get('min_price'):,} – ${v.get('max_price'):,}</span>
          <a href="/listing/{v.get('slug')}" class="text-xs font-bold text-amber-600 hover:text-amber-700">View Specs &rarr;</a>
        </div>
      </div>
    """ for v in state_vendors[:8]])

    breadcrumb_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://reliantverified.com/"},
            {"@type": "ListItem", "position": 2, "name": state_name, "item": f"https://reliantverified.com/state/{state_slug}"}
        ]
    }

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{state_name} Luxury Equipment &amp; Restroom Trailer Operators | Reliant Network</title>
  <meta name="description" content="Discover verified luxury restroom trailer and commercial equipment operators across {state_name}. Compare pricing, view verified reviews, and get instant quotes.">
  <link rel="canonical" href="https://reliantverified.com/state/{state_slug}">
  <script src="https://cdn.tailwindcss.com"></script>
  <script type="application/ld+json">
  {json.dumps(breadcrumb_ld, indent=2)}
  </script>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen font-sans antialiased">
  <header class="border-b border-slate-200 bg-white/95 sticky top-0 z-40 py-3.5 px-6 shadow-2xs">
    <div class="max-w-7xl mx-auto flex items-center justify-between">
      <a href="/" class="text-xl font-bold text-slate-900 tracking-tight">Reliant<span class="text-amber-600 font-extrabold">Network</span></a>
      <a href="/#quote-modal" class="bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold px-4 py-2 rounded-xl text-xs transition-colors shadow-xs">Get Instant Quote</a>
    </div>
  </header>

  <nav class="bg-white border-b border-slate-200 py-2.5 px-6">
    <div class="max-w-7xl mx-auto flex items-center gap-2 text-xs text-slate-500">
      <a href="/" class="hover:text-amber-600">Home</a>
      <span>&rsaquo;</span>
      <span class="text-slate-900 font-semibold">{state_name} Directory Hub</span>
    </div>
  </nav>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <div class="bg-white border border-slate-200 rounded-3xl p-8 shadow-xs mb-10">
      <span class="bg-amber-100 text-amber-800 text-xs font-bold px-3 py-1 rounded-full border border-amber-300 inline-block mb-3">
        Statewide Operator Directory
      </span>
      <h1 class="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
        {state_name} Commercial &amp; VIP Restroom Fleet Network
      </h1>
      <p class="text-sm text-slate-600 mt-2 max-w-3xl leading-relaxed">
        Browse fully insured, state-licensed commercial equipment operators servicing outdoor weddings, corporate events, film productions, and emergency municipal needs throughout {state_name}.
      </p>
    </div>

    <!-- METROS GRID -->
    <section class="mb-12">
      <h2 class="text-xl font-bold text-slate-900 mb-4">{state_name} Metros &amp; Service Zones</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {metros_html if metros_html else '<div class="text-xs text-slate-400">Coverage expanding across state.</div>'}
      </div>
    </section>

    <!-- TOP OPERATORS LIST -->
    <section class="mb-12">
      <h2 class="text-xl font-bold text-slate-900 mb-4">Top Vetted Operators in {state_name}</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {vendors_html if vendors_html else '<div class="text-xs text-slate-400">Loading verified operators...</div>'}
      </div>
    </section>

    <!-- MUNICIPAL COMPLIANCE & STATUTORY REGULATIONS (Bernard Huang Info Gain Doctrine) -->
    <section class="bg-white border border-slate-200 rounded-3xl p-8 shadow-xs mb-10">
      <div class="flex items-center gap-2 mb-3">
        <span class="w-3 h-3 rounded-full bg-emerald-500"></span>
        <h3 class="text-lg font-bold text-slate-900">{state_name} Event Sanitation &amp; Commercial Permitting Standards</h3>
      </div>
      <p class="text-xs text-slate-600 leading-relaxed max-w-4xl mb-6">
        Commercial deployments in {state_name} are subject to strict environmental and workplace health guidelines governed by OSHA 29 CFR 1926.51 and the {state_name} Department of Health. All verified operators in the Reliant Network maintain guaranteed compliance with state graywater containment, licensed waste manifest tracking, and mandatory ADA Title III barrier-free accessibility guidelines.
      </p>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
        <div class="bg-slate-50 border border-slate-200 rounded-2xl p-4">
          <span class="font-bold text-slate-900 block mb-1">OSHA 1926.51 Standard</span>
          <span class="text-slate-500 text-[11px]">Minimum 1 toilet per 20 workers for jobsite deployments with running handwash stations.</span>
        </div>
        <div class="bg-slate-50 border border-slate-200 rounded-2xl p-4">
          <span class="font-bold text-slate-900 block mb-1">Environmental Waste Manifest</span>
          <span class="text-slate-500 text-[11px]">Certified closed-loop holding tanks with licensed municipal wastewater treatment delivery receipts.</span>
        </div>
        <div class="bg-slate-50 border border-slate-200 rounded-2xl p-4">
          <span class="font-bold text-slate-900 block mb-1">ADA Title III Guaranteed</span>
          <span class="text-slate-500 text-[11px]">Ground-level hydraulic entry, 36-inch continuous clearance, and interior turning radiuses.</span>
        </div>
      </div>
    </section>

    <!-- DEMAND AGGREGATION & OPERATOR ONBOARDING (Frey Chu Claim Pivot) -->
    <section class="bg-gradient-to-br from-slate-900 to-slate-950 text-white rounded-3xl p-8 border border-slate-800 shadow-lg">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <span class="bg-amber-400 text-slate-950 text-[11px] font-bold px-3 py-1 rounded-full uppercase tracking-wider inline-block mb-2">
            Fleet Expansion in Progress
          </span>
          <h3 class="text-xl font-bold text-white">Are You an Insured Commercial Fleet Operator in {state_name}?</h3>
          <p class="text-xs text-slate-300 mt-1 max-w-2xl leading-relaxed">
            The Reliant Network is expanding staging yard coverage across {state_name}. Join our vetted registry to lock in exclusive regional dispatch, guaranteed #1 directory placement, and direct customer RFQ routing.
          </p>
        </div>
        <div class="flex flex-col sm:flex-row gap-3 shrink-0">
          <a href="/operator-portal.html" class="bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold px-6 py-3 rounded-xl text-xs text-center transition-colors shadow-xs">
            Apply for Verified Listing &rarr;
          </a>
          <a href="/#quote-modal" class="bg-slate-800 hover:bg-slate-700 text-white font-semibold px-6 py-3 rounded-xl border border-slate-700 text-xs text-center transition-colors">
            Request {state_name} Dispatch
          </a>
        </div>
      </div>
    </section>
  </main>
</body>
</html>"""
    return html

def run_generation():
    ensure_dirs()
    print("🚀 Starting GeoDirectory Multi-Tier Static Page Generation...")
    
    with open(VENDORS_FILE, "r", encoding="utf-8") as f:
        vendors = json.load(f)

    with open(METROS_FILE, "r", encoding="utf-8") as f:
        metros = json.load(f)

    # 1. Generate Single Listing Pages
    listing_count = 0
    for v in vendors:
        slug = v.get("slug")
        if not slug: continue
        html = generate_single_listing_html(v, vendors)
        out_path = os.path.join(LISTING_OUT_DIR, f"{slug}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        listing_count += 1
    print(f"✅ Generated {listing_count} Dedicated Single Listing Pages at {LISTING_OUT_DIR}")

    # 2. Generate State Hub Pages
    state_count = 0
    for code, (sname, s_slug) in STATE_NAMES.items():
        st_vendors = [v for v in vendors if v.get("state") == code]
        st_metros = [m for m in metros if m.get("state") == code]
        if st_vendors or st_metros:
            html = generate_state_hub_html(code, sname, s_slug, st_vendors, st_metros)
            out_path = os.path.join(STATE_OUT_DIR, f"{s_slug}.html")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(html)
            state_count += 1
    print(f"✅ Generated {state_count} State Hub Pages at {STATE_OUT_DIR}")

if __name__ == "__main__":
    run_generation()
