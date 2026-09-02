# -*- coding: utf-8 -*-
import json
import os
from spintax_engine import generate_spintax, generate_faq_schema

PSEO_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "pseo_metros.json")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "dist", "static-pseo")

def prerender_all_edge_pages():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not os.path.exists(PSEO_DATA_PATH):
        print("PSEO Data path does not exist.")
        return

    with open(PSEO_DATA_PATH, "r", encoding="utf-8") as f:
        metros = json.load(f)

    rendered_count = 0
    for m in metros:
        slug = m["slug"]
        city = m["city"]
        state = m["state"]
        state_full = m.get("state_full", state)
        avg_cost = m.get("avg_cost", 3000)
        min_cost = m.get("min_cost", 2000)
        max_cost = m.get("max_cost", 8000)
        season = m.get("season", "Peak Event Season")
        venues = m.get("venues", "Private Estates & Event Venues")
        permits = m.get("permits", "Local Municipal Health Guidelines")
        tech = m.get("technical_protocols", {})

        spintax = generate_spintax({"city": city, "state": state, "service": "Luxury Restroom Trailers"})
        faq_schema, faq_html = generate_faq_schema(city, state, "Luxury Restroom Trailers", avg_cost)
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{spintax['h1']} | The Reliant Network</title>
  <meta name="description" content="{spintax['intro']}">
  <link rel="canonical" href="https://reliantverified.com/metro/{slug}">
  <script src="https://cdn.tailwindcss.com"></script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Service",
    "name": "{spintax['h1']}",
    "serviceType": "Luxury Restroom Trailer Rental",
    "areaServed": {{
      "@type": "City",
      "name": "{city}",
      "containedInPlace": "{state_full}"
    }},
    "offers": {{
      "@type": "AggregateOffer",
      "lowPrice": {min_cost},
      "highPrice": {max_cost},
      "priceCurrency": "USD"
    }}
  }}
  </script>
  <script type="application/ld+json">
  {faq_schema}
  </script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans">
  <header class="border-b border-slate-800 bg-slate-950/90 py-4 px-6 max-w-7xl mx-auto flex items-center justify-between">
    <a href="/" class="text-xl font-bold text-white tracking-tight">Reliant<span class="text-amber-400">Network</span></a>
    <a href="/" class="bg-amber-500 text-slate-950 px-4 py-2 rounded-xl text-xs font-bold">Browse All Metros</a>
  </header>

  <main class="max-w-5xl mx-auto px-6 py-12">
    <div class="inline-block bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-semibold px-3 py-1 rounded-full mb-4">
      {city}, {state_full} VIP Sanitation Hub
    </div>

    <h1 class="text-4xl sm:text-5xl font-extrabold text-white tracking-tight leading-tight">
      {spintax['h1']}
    </h1>

    <p class="mt-4 text-slate-400 text-base leading-relaxed">
      {spintax['intro']}
    </p>

    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 my-8">
      <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
        <span class="text-xs text-slate-400 block">Average Rental Cost</span>
        <span class="text-2xl font-bold text-amber-400 mt-1 block">${avg_cost:,}</span>
        <span class="text-[11px] text-slate-500 mt-1 block">${min_cost:,} - ${max_cost:,} typical range</span>
      </div>
      <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
        <span class="text-xs text-slate-400 block">Peak Event Season</span>
        <span class="text-sm font-bold text-white mt-1 block">{season}</span>
      </div>
      <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
        <span class="text-xs text-slate-400 block">Unique Value Proposition</span>
        <span class="text-xs text-slate-300 mt-1 block">{spintax['valueProp']}</span>
      </div>
    </div>

    <section class="bg-slate-900 border border-slate-800 rounded-2xl p-6 my-8">
      <h2 class="text-lg font-bold text-white mb-3">Local Technical & Guidelines ({city})</h2>
      <ul class="text-xs text-slate-300 space-y-2 font-mono">
        <li>&bull; Permit Requirement: {permits}</li>
        <li>&bull; Ingress Standard: {tech.get("site_ingress_protocol", "Standard 14ft overhead clearance")}</li>
        <li>&bull; Leveling Protocol: {tech.get("leveling_standard", "Laser-guided hydraulic leveling to +/- 0.5 degrees")}</li>
      </ul>
    </section>

    {faq_html}

    <div class="text-center py-8">
      <a href="/#quote-modal" class="bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-sm px-8 py-3.5 rounded-xl shadow-lg transition-all inline-block">
        Get Direct Instant Quotes in {city}
      </a>
    </div>
  </main>
</body>
</html>"""

        file_name = f"{slug}.html"
        out_file = os.path.join(OUTPUT_DIR, file_name)
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        rendered_count += 1

    print(f"Edge Pre-Renderer Complete! Generated {rendered_count} static pSEO HTML pages at {OUTPUT_DIR}")

if __name__ == "__main__":
    prerender_all_edge_pages()
