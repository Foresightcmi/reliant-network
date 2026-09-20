# -*- coding: utf-8 -*-
"""
services/scraper/update_sitemap.py
Regenerate and synchronize apps/web/public/sitemap.xml with:
1. All 9 vertical hubs
2. Utility and legal pages
3. 51 Statewide directory hubs
4. 71 Metro hubs
5. Programmatic permits, best, cost, vs pages
6. All 214 single listing permalinks
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
SITEMAP_FILE = os.path.join(BASE_DIR, "..", "apps", "web", "public", "sitemap.xml")

with open(VENDORS_FILE, "r", encoding="utf-8") as f:
    vendors = json.load(f)

with open(SITEMAP_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Read all existing URLs that are NOT /listing/
non_listing_urls = []
for block in re.findall(r'<url>.*?</url>', content, re.DOTALL):
    loc_match = re.search(r'<loc>(.*?)</loc>', block)
    if loc_match:
        loc = loc_match.group(1)
        if '/listing/' not in loc:
            non_listing_urls.append(block)

# Category hubs that must be present
category_hubs = [
    "https://www.reliantverified.com/cold-storage",
    "https://www.reliantverified.com/cranes",
    "https://www.reliantverified.com/senior-care",
    "https://www.reliantverified.com/staying-in-place",
    "https://www.reliantverified.com/power",
    "https://www.reliantverified.com/machinery-moving",
    "https://www.reliantverified.com/senior-downsizing",
    "https://www.reliantverified.com/wheelchair-vans"
]

existing_locs = set()
for b in non_listing_urls:
    m = re.search(r'<loc>(.*?)</loc>', b)
    if m: existing_locs.add(m.group(1))

# Insert missing category hubs
for hub in category_hubs:
    if hub not in existing_locs:
        block = f"""  <url>
    <loc>{hub}</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>"""
        # insert after root /
        non_listing_urls.insert(1, block)
        existing_locs.add(hub)

# Generate listing url blocks for all 214 vendors
listing_blocks = []
seen_slugs = set()
for v in vendors:
    slug = v.get("slug")
    if not slug or slug in seen_slugs:
        continue
    seen_slugs.add(slug)
    block = f"""  <url>
    <loc>https://www.reliantverified.com/listing/{slug}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.75</priority>
  </url>"""
    listing_blocks.append(block)

all_blocks = non_listing_urls + listing_blocks

new_sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
new_sitemap += "\n".join(all_blocks) + "\n</urlset>\n"

with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
    f.write(new_sitemap)

print(f"✅ Successfully updated {SITEMAP_FILE} with {len(all_blocks)} total URLs ({len(listing_blocks)} listings, {len(non_listing_urls)} hubs & pages)!")
