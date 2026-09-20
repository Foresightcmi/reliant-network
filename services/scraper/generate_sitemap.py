# -*- coding: utf-8 -*-
"""
services/scraper/generate_sitemap.py
Generates an exhaustive, canonical sitemap.xml covering:
- Core home & multi-vertical hubs
- All 51 statewide hubs (/state/:slug)
- All 71 metro landing pages (/metro/:slug)
- All 146 verified single listing pages (/listing/:slug)
- Institutional legal, receipt, and portal surfaces
"""

import json
import os
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PUBLIC_DIR = os.path.join(BASE_DIR, "..", "apps", "web", "public")
SITEMAP_FILE = os.path.join(PUBLIC_DIR, "sitemap.xml")

def run():
    with open(os.path.join(DATA_DIR, "vendors.json"), "r", encoding="utf-8") as f:
        vendors = json.load(f)

    with open(os.path.join(DATA_DIR, "pseo_metros.json"), "r", encoding="utf-8") as f:
        metros = json.load(f)

    state_files = glob.glob(os.path.join(PUBLIC_DIR, "state", "*.html"))
    state_slugs = sorted([os.path.basename(f).replace(".html", "") for f in state_files])

    core_urls = [
        "https://www.reliantverified.com/",
        "https://www.reliantverified.com/cold-storage",
        "https://www.reliantverified.com/cranes",
        "https://www.reliantverified.com/senior-care",
        "https://www.reliantverified.com/staying-in-place",
        "https://www.reliantverified.com/financing",
        "https://www.reliantverified.com/operator-portal.html",
        "https://www.reliantverified.com/badge-generator.html",
        "https://www.reliantverified.com/terms",
        "https://www.reliantverified.com/privacy",
        "https://www.reliantverified.com/refund-policy"
    ]

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    for u in core_urls:
        lines.append('  <url>')
        lines.append(f'    <loc>{u}</loc>')
        lines.append('    <changefreq>weekly</changefreq>')
        lines.append('    <priority>0.9</priority>')
        lines.append('  </url>')

    # 51 State Hubs
    for st in state_slugs:
        lines.append('  <url>')
        lines.append(f'    <loc>https://www.reliantverified.com/state/{st}</loc>')
        lines.append('    <changefreq>weekly</changefreq>')
        lines.append('    <priority>0.85</priority>')
        lines.append('  </url>')

    # 71 Metros
    for m in metros:
        m_slug = m.get("slug")
        if m_slug:
            lines.append('  <url>')
            lines.append(f'    <loc>https://www.reliantverified.com/metro/{m_slug}</loc>')
            lines.append('    <changefreq>weekly</changefreq>')
            lines.append('    <priority>0.8</priority>')
            lines.append('  </url>')

    # 146 Single Listings
    for v in vendors:
        v_slug = v.get("slug")
        if v_slug:
            lines.append('  <url>')
            lines.append(f'    <loc>https://www.reliantverified.com/listing/{v_slug}</loc>')
            lines.append('    <changefreq>monthly</changefreq>')
            lines.append('    <priority>0.75</priority>')
            lines.append('  </url>')

    lines.append('</urlset>')
    xml_content = "\n".join(lines)

    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write(xml_content)

    total_urls = len(core_urls) + len(state_slugs) + len(metros) + len(vendors)
    print(f"Generated comprehensive sitemap.xml with {total_urls} indexed URLs.")

if __name__ == "__main__":
    run()
