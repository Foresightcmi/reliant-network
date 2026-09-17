# -*- coding: utf-8 -*-
import os
import re

sitemap_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "apps", "web", "public", "sitemap.xml"))

with open(sitemap_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace escaped \n with actual newlines
content = content.replace("\\n", "\n")

# Replace old domain with canonical Vercel production domain
content = content.replace("https://reliantverified.com", "https://reliant-network.vercel.app")

# Ensure high-ticket pages are present
key_pages = [
    '<url>\n    <loc>https://reliant-network.vercel.app/operator-portal.html</loc>\n    <changefreq>daily</changefreq>\n    <priority>0.95</priority>\n  </url>',
    '<url>\n    <loc>https://reliant-network.vercel.app/financing.html</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.90</priority>\n  </url>',
    '<url>\n    <loc>https://reliant-network.vercel.app/badge-generator.html</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.85</priority>\n  </url>'
]

for kp in key_pages:
    loc_match = re.search(r'<loc>(.*?)</loc>', kp)
    if loc_match and loc_match.group(1) not in content:
        content = content.replace("</urlset>", f"  {kp}\n</urlset>")

# Clean trailing whitespace and blank lines
lines = [l for l in content.split("\n") if l.strip()]
cleaned = "\n".join(lines) + "\n"

with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write(cleaned)

print(f"[OK] Sitemap cleaned and formatted. Total lines: {len(lines)}")
