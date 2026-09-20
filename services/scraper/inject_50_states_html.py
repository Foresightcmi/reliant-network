# -*- coding: utf-8 -*-
"""
services/scraper/inject_50_states_html.py
Injects all 50 US States + DC organized into 5 regional directory grids
into apps/web/public/index.html.
"""

import os
import re

INDEX_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "apps", "web", "public", "index.html")

REGIONS = {
    'South & Southeast': [
        ('Georgia', 'georgia', 'Atlanta &bull; Savannah'),
        ('Florida', 'florida', 'Miami &bull; Tampa &bull; Orlando'),
        ('North Carolina', 'north-carolina', 'Charlotte &bull; Raleigh'),
        ('South Carolina', 'south-carolina', 'Charleston &bull; Columbia'),
        ('Tennessee', 'tennessee', 'Nashville &bull; Memphis'),
        ('Alabama', 'alabama', 'Birmingham &bull; Huntsville'),
        ('Mississippi', 'mississippi', 'Jackson &bull; Gulfport'),
        ('Louisiana', 'louisiana', 'New Orleans &bull; Baton Rouge'),
        ('Arkansas', 'arkansas', 'Little Rock &bull; Fayetteville'),
        ('Virginia', 'virginia', 'Richmond &bull; Virginia Beach'),
        ('West Virginia', 'west-virginia', 'Charleston &bull; Morgantown'),
        ('Kentucky', 'kentucky', 'Louisville &bull; Lexington')
    ],
    'Texas & Southwest': [
        ('Texas', 'texas', 'Dallas &bull; Austin &bull; Houston'),
        ('Arizona', 'arizona', 'Phoenix &bull; Scottsdale &bull; Tucson'),
        ('Nevada', 'nevada', 'Las Vegas &bull; Reno &bull; Tahoe'),
        ('New Mexico', 'new-mexico', 'Albuquerque &bull; Santa Fe'),
        ('Oklahoma', 'oklahoma', 'Oklahoma City &bull; Tulsa'),
        ('Utah', 'utah', 'Salt Lake City &bull; Park City')
    ],
    'West & Pacific': [
        ('California', 'california', 'Los Angeles &bull; SF &bull; San Diego'),
        ('Washington', 'washington', 'Seattle &bull; Bellevue &bull; Tacoma'),
        ('Oregon', 'oregon', 'Portland &bull; Eugene &bull; Bend'),
        ('Colorado', 'colorado', 'Denver &bull; Boulder &bull; Aspen'),
        ('Idaho', 'idaho', 'Boise &bull; Sun Valley'),
        ('Montana', 'montana', 'Billings &bull; Bozeman &bull; Missoula'),
        ('Wyoming', 'wyoming', 'Cheyenne &bull; Jackson Hole'),
        ('Alaska', 'alaska', 'Anchorage &bull; Fairbanks'),
        ('Hawaii', 'hawaii', 'Honolulu &bull; Maui &bull; Kauai')
    ],
    'Midwest & Great Lakes': [
        ('Illinois', 'illinois', 'Chicago &bull; Naperville'),
        ('Ohio', 'ohio', 'Columbus &bull; Cleveland &bull; Cincinnati'),
        ('Michigan', 'michigan', 'Detroit &bull; Grand Rapids &bull; Ann Arbor'),
        ('Indiana', 'indiana', 'Indianapolis &bull; Fort Wayne'),
        ('Wisconsin', 'wisconsin', 'Milwaukee &bull; Madison &bull; Green Bay'),
        ('Minnesota', 'minnesota', 'Minneapolis &bull; St. Paul'),
        ('Missouri', 'missouri', 'St. Louis &bull; Kansas City'),
        ('Iowa', 'iowa', 'Des Moines &bull; Cedar Rapids'),
        ('Kansas', 'kansas', 'Wichita &bull; Overland Park'),
        ('Nebraska', 'nebraska', 'Omaha &bull; Lincoln'),
        ('North Dakota', 'north-dakota', 'Fargo &bull; Bismarck'),
        ('South Dakota', 'south-dakota', 'Sioux Falls &bull; Rapid City')
    ],
    'Northeast & Mid-Atlantic': [
        ('New York', 'new-york', 'NYC &bull; Hamptons &bull; Buffalo'),
        ('Pennsylvania', 'pennsylvania', 'Philadelphia &bull; Pittsburgh'),
        ('New Jersey', 'new-jersey', 'Newark &bull; Jersey Shore'),
        ('Massachusetts', 'massachusetts', 'Boston &bull; Cape Cod &bull; Worcester'),
        ('Connecticut', 'connecticut', 'Hartford &bull; Greenwich &bull; Stamford'),
        ('Maryland', 'maryland', 'Baltimore &bull; Bethesda &bull; Annapolis'),
        ('District of Columbia', 'district-of-columbia', 'Washington DC Capital Hub'),
        ('Delaware', 'delaware', 'Wilmington &bull; Rehoboth Beach'),
        ('Rhode Island', 'rhode-island', 'Providence &bull; Newport'),
        ('New Hampshire', 'new-hampshire', 'Manchester &bull; Portsmouth'),
        ('Maine', 'maine', 'Portland &bull; Bar Harbor'),
        ('Vermont', 'vermont', 'Burlington &bull; Stowe')
    ]
}

def build_section_html():
    region_blocks = []
    for reg_title, states in REGIONS.items():
        cards = "".join([
            f"""        <a href="/state/{slug}" class="p-3 bg-slate-50 hover:bg-amber-50/60 border border-slate-200 hover:border-amber-400 rounded-xl transition-all block shadow-2xs hover:shadow-xs group">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-slate-900 group-hover:text-amber-700">{name}</span>
            <span class="text-[10px] text-amber-600 font-bold opacity-0 group-hover:opacity-100 transition-opacity">&rarr;</span>
          </div>
          <span class="text-[10px] text-slate-500 block mt-0.5 truncate">{metros}</span>
        </a>\n"""
            for name, slug, metros in states
        ])
        
        block = f"""      <!-- {reg_title} -->
      <div class="mb-8 last:mb-0">
        <h4 class="text-xs font-extrabold text-slate-700 uppercase tracking-wider mb-3 flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-amber-500"></span>
          <span>{reg_title} ({len(states)} States)</span>
        </h4>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2.5">
{cards}        </div>
      </div>"""
        region_blocks.append(block)

    all_regions_html = "\n\n".join(region_blocks)

    full_section = f"""  <!-- STATE DIRECTORY EXPLORER (ALL 50 US STATES + DC) -->
  <section class="py-14 bg-white border-t border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between mb-8 flex-wrap gap-3">
        <div>
          <span class="text-xs font-bold text-amber-700 uppercase tracking-widest block">Nationwide Directory Network</span>
          <h3 class="text-2xl font-bold text-slate-900 mt-1">Statewide Commercial Fleet &amp; Restroom Networks</h3>
          <p class="text-xs text-slate-500 mt-1">Direct access to state-licensed commercial operators and staging depots across all 50 US states and the District of Columbia.</p>
        </div>
        <span class="text-xs text-emerald-700 font-bold bg-emerald-50 border border-emerald-300 px-3.5 py-1.5 rounded-full flex items-center gap-1.5 shadow-2xs">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          50 States &amp; DC Active (146 Depots)
        </span>
      </div>

{all_regions_html}
    </div>
  </section>"""
    return full_section

def run():
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the STATE DIRECTORY EXPLORER section
    pattern = r"<!-- STATE DIRECTORY EXPLORER -->.*?</section>"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print("❌ Could not find STATE DIRECTORY EXPLORER section in index.html")
        return

    new_section = build_section_html()
    new_content = content[:match.start()] + new_section + content[match.end():]

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("✅ Successfully replaced Statewide Directories in index.html with all 50 states + DC across 5 regions!")

if __name__ == "__main__":
    run()
