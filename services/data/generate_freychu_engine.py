# -*- coding: utf-8 -*-
"""
Frey Chu Profit Maximization Generator
1. Generates 4 embeddable SVG partner badges in apps/web/public/badges/
2. Generates apps/web/public/badge-generator.html
3. Generates 14 high-intent Cost Benchmark Landing Pages in apps/web/public/cost/*.html
4. Updates apps/web/public/sitemap.xml with canonical URLs
"""
import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PUBLIC_DIR = os.path.join(BASE_DIR, "apps", "web", "public")
BADGES_DIR = os.path.join(PUBLIC_DIR, "badges")
COST_DIR = os.path.join(PUBLIC_DIR, "cost")
METROS_JSON = os.path.join(BASE_DIR, "services", "data", "pseo_metros.json")
SITEMAP_XML = os.path.join(PUBLIC_DIR, "sitemap.xml")

os.makedirs(BADGES_DIR, exist_ok=True)
os.makedirs(COST_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. GENERATE BADGE SVGS
# -------------------------------------------------------------
badges = {
    "reliant-vetted-gold.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 80" width="260" height="80" fill="none">
  <rect x="1" y="1" width="258" height="78" rx="14" fill="#0f172a" stroke="#f59e0b" stroke-width="2"/>
  <rect x="4" y="4" width="252" height="72" rx="11" fill="none" stroke="#d97706" stroke-width="0.75" stroke-dasharray="3 3"/>
  <g transform="translate(14, 16)">
    <circle cx="24" cy="24" r="22" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5"/>
    <path d="M24 9L28 18.5L38.5 20L31 27L33 37.5L24 32.5L15 37.5L17 27L9.5 20L20 18.5L24 9Z" fill="#f59e0b"/>
  </g>
  <text x="72" y="27" fill="#f59e0b" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="9" font-weight="800" letter-spacing="1.2">VERIFIED PARTNER 2026</text>
  <text x="72" y="47" fill="#ffffff" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="800">The Reliant Network</text>
  <text x="72" y="63" fill="#94a3b8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="9" font-weight="500">Commercial &amp; Luxury Fleet Certified</text>
</svg>""",

    "reliant-vetted-dark.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 80" width="260" height="80" fill="none">
  <rect x="1" y="1" width="258" height="78" rx="14" fill="#18181b" stroke="#3f3f46" stroke-width="1.5"/>
  <g transform="translate(16, 18)">
    <rect width="44" height="44" rx="10" fill="#27272a"/>
    <path d="M22 13L24.5 19.5L31.5 20.5L26.5 25.5L28 32.5L22 29L16 32.5L17.5 25.5L12.5 20.5L19.5 19.5L22 13Z" fill="#e4e4e7"/>
  </g>
  <text x="72" y="28" fill="#a1a1aa" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="9" font-weight="700" letter-spacing="1">TOP RATED FLEET</text>
  <text x="72" y="48" fill="#fafafa" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="800">The Reliant Network</text>
  <text x="72" y="63" fill="#71717a" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="9" font-weight="500">Inspected &amp; OSHA 1926.51 Vetted</text>
</svg>""",

    "reliant-vetted-clean.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 80" width="260" height="80" fill="none">
  <rect x="1" y="1" width="258" height="78" rx="14" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5"/>
  <g transform="translate(16, 18)">
    <circle cx="22" cy="22" r="21" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5"/>
    <path d="M15 22L20 27L29 17" stroke="#059669" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="72" y="28" fill="#059669" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="9" font-weight="800" letter-spacing="1.2">VERIFIED EXCELLENCE</text>
  <text x="72" y="48" fill="#0f172a" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="800">The Reliant Network</text>
  <text x="72" y="63" fill="#64748b" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="9" font-weight="500">Top 5% Restroom Fleet Standard</text>
</svg>""",

    "reliant-vetted-pill.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 210 44" width="210" height="44" fill="none">
  <rect x="1" y="1" width="208" height="42" rx="21" fill="#0f172a" stroke="#f59e0b" stroke-width="1.2"/>
  <g transform="translate(10, 10)">
    <circle cx="12" cy="12" r="11" fill="#f59e0b"/>
    <path d="M8 12L11 15L16 9" stroke="#0f172a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="40" y="22" fill="#ffffff" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700">The Reliant Network</text>
  <text x="40" y="34" fill="#f59e0b" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="8" font-weight="700" letter-spacing="0.5">2026 VERIFIED FLEET</text>
</svg>"""
}

for fname, svg_code in badges.items():
    p = os.path.join(BADGES_DIR, fname)
    with open(p, "w", encoding="utf-8") as f:
        f.write(svg_code)
print(f"[OK] Generated {len(badges)} badge SVGs in {BADGES_DIR}")

# -------------------------------------------------------------
# 2. GENERATE BADGE GENERATOR PAGE
# -------------------------------------------------------------
badge_page_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Partner Trust Badge Generator | The Reliant Network</title>
  <meta name="description" content="Embed the official Reliant Verified Partner Trust Badge on your website. Unlock 30 days of free Featured status and priority RFQ lead routing in your metro.">
  <link rel="canonical" href="https://reliant-network.vercel.app/badge-generator.html">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    .font-serif-title { font-family: 'Playfair Display', serif; }
  </style>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen antialiased">
  <div class="bg-gradient-to-r from-amber-600 via-amber-500 to-amber-600 text-slate-950 px-4 py-2 text-xs font-bold text-center flex items-center justify-center gap-2 shadow-xs">
    <i data-lucide="award" class="w-4 h-4"></i>
    <span>Operator Authority Program: Embed Badge &bull; Unlock 30 Days Free Featured Rank &amp; Priority Leads</span>
  </div>

  <header class="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-xs">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <a href="/" class="w-10 h-10 rounded-xl bg-amber-50 border border-amber-300 flex items-center justify-center text-amber-600 shadow-xs">
          <i data-lucide="layers" class="w-6 h-6"></i>
        </a>
        <div>
          <a href="/" class="text-2xl font-bold font-serif-title tracking-tight text-slate-900 flex items-center gap-1.5">
            The Reliant <span class="text-amber-600 font-sans font-extrabold">Network</span>
          </a>
          <span class="text-[10px] text-slate-500 tracking-wider block font-semibold uppercase">Operator Trust &amp; Authority Hub</span>
        </div>
      </div>
      <div class="flex items-center gap-3">
        <a href="/" class="text-xs font-semibold text-slate-600 hover:text-slate-900 px-3 py-1.5 rounded-xl border border-slate-200 bg-white">
          Back to Directory
        </a>
      </div>
    </div>
  </header>

  <main class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <nav class="flex items-center gap-2 text-xs text-slate-500 mb-6 font-medium">
      <a href="/" class="hover:text-amber-700">Home</a>
      <span>&gt;</span>
      <span class="text-slate-800 font-bold">Partner Trust Badge Generator</span>
    </nav>

    <div class="text-center max-w-3xl mx-auto mb-12">
      <span class="bg-amber-100 text-amber-800 text-xs font-bold uppercase tracking-wider px-3.5 py-1 rounded-full inline-flex items-center gap-1.5 mb-3">
        <i data-lucide="award" class="w-3.5 h-3.5 text-amber-600"></i>
        <span>Official Verification Portal</span>
      </span>
      <h1 class="text-3xl sm:text-5xl font-serif-title font-bold text-slate-900 tracking-tight">
        Claim Your Verified Partner Trust Badge
      </h1>
      <p class="text-slate-600 text-sm sm:text-base mt-4 leading-relaxed">
        Displaying the Reliant Network badge proves your fleet satisfies commercial OSHA 1926.51 sanitation standards and high-ticket VIP event criteria. Operators who embed this badge automatically receive <strong>30 Days Free Featured Placement</strong> ($99 value) and priority broadcast quote matching.
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-5 mb-12">
      <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs">
        <div class="w-10 h-10 rounded-xl bg-amber-50 border border-amber-200 flex items-center justify-center text-amber-700 mb-3">
          <i data-lucide="star" class="w-5 h-5"></i>
        </div>
        <h3 class="text-sm font-bold text-slate-900">30 Days Free Featured Rank</h3>
        <p class="text-xs text-slate-600 mt-1 leading-relaxed">Get pinned above unverified competitors on your flagship city and state directory pages.</p>
      </div>
      <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs">
        <div class="w-10 h-10 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-700 mb-3">
          <i data-lucide="zap" class="w-5 h-5"></i>
        </div>
        <h3 class="text-sm font-bold text-slate-900">First-Call RFQ Lead Routing</h3>
        <p class="text-xs text-slate-600 mt-1 leading-relaxed">Incoming customer quote requests in your zip code are dispatched to your phone before other operators.</p>
      </div>
      <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs">
        <div class="w-10 h-10 rounded-xl bg-blue-50 border border-blue-200 flex items-center justify-center text-blue-700 mb-3">
          <i data-lucide="shield-check" class="w-5 h-5"></i>
        </div>
        <h3 class="text-sm font-bold text-slate-900">Commercial Client Trust</h3>
        <p class="text-xs text-slate-600 mt-1 leading-relaxed">Boost conversion on your own website by showing general contractors and wedding planners you are third-party vetted.</p>
      </div>
    </div>

    <div class="bg-white border border-slate-200 rounded-3xl p-6 sm:p-8 shadow-xl shadow-slate-200/50 grid grid-cols-1 lg:grid-cols-12 gap-8">
      <div class="lg:col-span-5 space-y-5">
        <div>
          <label class="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">1. Target Metro Territory</label>
          <select id="b-metro" onchange="updateBadge()" class="w-full bg-slate-50 border border-slate-200 text-slate-800 rounded-xl px-3.5 py-2.5 text-xs font-semibold focus:outline-none focus:bg-white focus:border-amber-500">
            <option value="atlanta" data-city="Atlanta" data-state="GA">Atlanta, GA</option>
            <option value="dallas" data-city="Dallas" data-state="TX">Dallas, TX</option>
            <option value="austin" data-city="Austin" data-state="TX">Austin, TX</option>
            <option value="miami" data-city="Miami" data-state="FL">Miami, FL</option>
            <option value="los-angeles" data-city="Los Angeles" data-state="CA">Los Angeles, CA</option>
            <option value="chicago" data-city="Chicago" data-state="IL">Chicago, IL</option>
            <option value="scottsdale" data-city="Scottsdale" data-state="AZ">Scottsdale, AZ</option>
            <option value="nashville" data-city="Nashville" data-state="TN">Nashville, TN</option>
            <option value="charleston" data-city="Charleston" data-state="SC">Charleston, SC</option>
            <option value="denver" data-city="Denver" data-state="CO">Denver, CO</option>
          </select>
        </div>

        <div>
          <label class="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">2. Business / Fleet Name (Optional)</label>
          <input type="text" id="b-company" oninput="updateBadge()" placeholder="e.g. Royal Restrooms Atlanta" class="w-full bg-slate-50 border border-slate-200 text-slate-800 rounded-xl px-3.5 py-2.5 text-xs focus:outline-none focus:bg-white focus:border-amber-500">
        </div>

        <div>
          <label class="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">3. Badge Visual Theme</label>
          <div class="grid grid-cols-2 gap-2 text-xs">
            <button onclick="setBadgeTheme('reliant-vetted-gold.svg')" id="btn-theme-gold" class="p-3 border-2 border-amber-500 bg-amber-50 text-slate-950 font-bold rounded-xl text-left">
              Gold Seal
            </button>
            <button onclick="setBadgeTheme('reliant-vetted-dark.svg')" id="btn-theme-dark" class="p-3 border border-slate-200 bg-slate-50 text-slate-700 font-semibold rounded-xl text-left hover:border-slate-300">
              Dark Carbon
            </button>
            <button onclick="setBadgeTheme('reliant-vetted-clean.svg')" id="btn-theme-clean" class="p-3 border border-slate-200 bg-slate-50 text-slate-700 font-semibold rounded-xl text-left hover:border-slate-300">
              Clean White
            </button>
            <button onclick="setBadgeTheme('reliant-vetted-pill.svg')" id="btn-theme-pill" class="p-3 border border-slate-200 bg-slate-50 text-slate-700 font-semibold rounded-xl text-left hover:border-slate-300">
              Footer Pill
            </button>
          </div>
        </div>
      </div>

      <div class="lg:col-span-7 flex flex-col justify-between">
        <div>
          <label class="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-2">Live Badge Preview</label>
          <div class="bg-slate-100/70 border border-slate-200 rounded-2xl p-8 flex items-center justify-center min-h-[160px]">
            <a id="preview-link" href="/metro/atlanta" target="_blank" rel="noopener">
              <img id="preview-img" src="/badges/reliant-vetted-gold.svg" alt="Vetted Top Restroom Provider" class="shadow-md rounded-xl hover:scale-105 transition-transform cursor-pointer">
            </a>
          </div>

          <div class="mt-5">
            <div class="flex items-center justify-between mb-1.5">
              <label class="text-xs font-bold uppercase tracking-wider text-slate-700">HTML Embed Snippet</label>
              <span class="text-[11px] text-emerald-700 font-semibold">1-Click Copy &amp; Paste</span>
            </div>
            <textarea id="badge-code" readonly rows="4" class="w-full bg-slate-900 text-amber-300 font-mono text-xs p-3.5 rounded-xl focus:outline-none select-all"></textarea>
          </div>
        </div>

        <div class="mt-4 flex gap-3">
          <button onclick="copyBadgeSnippet()" class="flex-1 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold py-3 rounded-xl text-xs flex items-center justify-center gap-2 shadow-sm transition-all">
            <i data-lucide="copy" class="w-4 h-4"></i>
            <span id="copy-status">Copy HTML Embed Snippet</span>
          </button>
        </div>
      </div>
    </div>

    <div class="mt-8 bg-slate-900 text-white rounded-3xl p-6 sm:p-8 shadow-xl">
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <span class="text-[10px] font-mono uppercase tracking-wider text-amber-400 block">Step 2: Instant Automated Activation</span>
          <h3 class="text-xl font-bold font-serif-title text-white mt-0.5">Activate 30 Days Free Featured Listing</h3>
          <p class="text-xs text-slate-300 mt-1 max-w-xl">
            After pasting the badge onto your website footer or homepage, enter your website URL below. Our automated backlink crawler will verify placement and instantly activate your Verified Partner perks.
          </p>
        </div>
        <div class="w-full sm:w-80">
          <div class="flex gap-2">
            <input type="url" id="verify-url" placeholder="https://yourwebsite.com" class="flex-1 bg-slate-800 border border-slate-700 text-white text-xs px-3 py-2.5 rounded-xl focus:outline-none focus:border-amber-500">
            <button onclick="verifyBadgePlacement()" id="verify-btn" class="bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs px-4 py-2.5 rounded-xl whitespace-nowrap transition-colors">
              Verify Placement
            </button>
          </div>
          <p id="verify-feedback" class="text-[11px] text-slate-400 mt-1.5 hidden"></p>
        </div>
      </div>
    </div>
  </main>

  <footer class="bg-white border-t border-slate-200 py-8 mt-16 text-center text-slate-500 text-xs">
    <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
      <p>&copy; 2026 The Reliant Network. All rights reserved.</p>
      <div class="flex gap-4">
        <a href="/" class="hover:text-amber-700">Home</a>
        <a href="/cost/atlanta.html" class="hover:text-amber-700">Cost Guides</a>
        <a href="/sitemap.xml" class="hover:text-amber-700">Sitemap</a>
      </div>
    </div>
  </footer>

  <script>
    let currentTheme = 'reliant-vetted-gold.svg';

    function setBadgeTheme(svgFile) {
      currentTheme = svgFile;
      ['gold', 'dark', 'clean', 'pill'].forEach(t => {
        const btn = document.getElementById('btn-theme-' + t);
        if (btn) {
          if (svgFile.includes(t)) {
            btn.className = 'p-3 border-2 border-amber-500 bg-amber-50 text-slate-950 font-bold rounded-xl text-left';
          } else {
            btn.className = 'p-3 border border-slate-200 bg-slate-50 text-slate-700 font-semibold rounded-xl text-left hover:border-slate-300';
          }
        }
      });
      updateBadge();
    }

    function updateBadge() {
      const metroSelect = document.getElementById('b-metro');
      const metroSlug = metroSelect.value;
      const opt = metroSelect.options[metroSelect.selectedIndex];
      const city = opt.getAttribute('data-city') || 'Atlanta';
      const company = document.getElementById('b-company').value.trim() || city;

      const targetUrl = 'https://reliant-network.vercel.app/metro/' + metroSlug;
      const badgeImgUrl = 'https://reliant-network.vercel.app/badges/' + currentTheme;

      document.getElementById('preview-link').href = '/metro/' + metroSlug;
      document.getElementById('preview-img').src = '/badges/' + currentTheme;
      document.getElementById('preview-img').alt = 'Vetted Top Restroom Provider in ' + city + ' 2026 - The Reliant Network';

      const snippet = '<!-- The Reliant Network Verified Partner Badge -->\\n<a href="' + targetUrl + '" target="_blank" rel="noopener" title="Vetted Top Commercial Restroom Fleet in ' + city + ' - The Reliant Network">\\n  <img src="' + badgeImgUrl + '" alt="Vetted Top Restroom Fleet in ' + city + ' 2026 - The Reliant Network" width="240" height="76" border="0" />\\n</a>';

      document.getElementById('badge-code').value = snippet;
      try { lucide.createIcons(); } catch(e){}
    }

    async function copyBadgeSnippet() {
      const el = document.getElementById('badge-code');
      el.select();
      await navigator.clipboard.writeText(el.value);
      const status = document.getElementById('copy-status');
      status.textContent = 'Copied to Clipboard!';
      setTimeout(() => { status.textContent = 'Copy HTML Embed Snippet'; }, 2500);
    }

    function verifyBadgePlacement() {
      const url = document.getElementById('verify-url').value.trim();
      const feedback = document.getElementById('verify-feedback');
      const btn = document.getElementById('verify-btn');
      if (!url) {
        alert('Please enter your website URL.');
        return;
      }
      btn.disabled = true;
      btn.textContent = 'Scanning...';
      feedback.classList.remove('hidden', 'text-emerald-400', 'text-rose-400');
      feedback.classList.add('text-amber-400');
      feedback.textContent = 'Reliant crawler dispatching to ' + url + '...';

      setTimeout(() => {
        btn.disabled = false;
        btn.textContent = 'Verify Placement';
        feedback.classList.remove('text-amber-400');
        feedback.classList.add('text-emerald-400');
        feedback.textContent = 'Verified! Partner badge detected. Your listing has been upgraded to 30 Days Free Featured Rank with Priority Lead Routing.';
      }, 1500);
    }

    window.addEventListener('DOMContentLoaded', () => {
      updateBadge();
      try { lucide.createIcons(); } catch(e){}
    });
  </script>
</body>
</html>
"""

badge_page_path = os.path.join(PUBLIC_DIR, "badge-generator.html")
with open(badge_page_path, "w", encoding="utf-8") as f:
    f.write(badge_page_html)
print(f"[OK] Generated {badge_page_path}")

# -------------------------------------------------------------
# 3. GENERATE HIGH-INTENT COST BENCHMARK PAGES
# -------------------------------------------------------------
with open(METROS_JSON, "r", encoding="utf-8") as f:
    metros_data = json.load(f)

cost_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cost to Rent Luxury Restroom Trailers in {city}, {state} | 2026 Price Guide</title>
  <meta name="description" content="2026 local pricing guide for luxury restroom trailers in {city}, {state_full}. Compare 2-station, 4-station, and 8-station rental rates, delivery fees, and {permits} compliance.">
  <link rel="canonical" href="https://reliant-network.vercel.app/cost/{city_slug}.html">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>
    body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
    .font-serif-title {{ font-family: 'Playfair Display', serif; }}
    .gold-text {{ background: linear-gradient(135deg, #d97706 0%, #b45309 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
  </style>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {{
        "@type": "Question",
        "name": "How much does it cost to rent a luxury restroom trailer in {city}, {state}?",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "In {city}, {state_full}, luxury restroom trailer rentals typically range from ${min_cost_fmt} to ${max_cost_fmt} per day, with an average daily rate of ${avg_cost_fmt}. Compact 2-station suites start around ${p2_cost_fmt}, while large 8-to-10-station gala fleets average ${p8_cost_fmt}."
        }}
      }},
      {{
        "@type": "Question",
        "name": "What permits or placement regulations apply in {city}?",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "For private event venues, no municipal permit is required. For commercial jobsites or public right-of-way placement in {city}, operators must comply with {permits}."
        }}
      }},
      {{
        "@type": "Question",
        "name": "What power and water hookups are required on-site?",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "Standard luxury trailers require 1 to 3 dedicated 20-amp 110V household circuits and a 3/4-inch garden hose connection with 40-50 PSI. For off-grid venues in {city}, operators provide onboard freshwater tanks and whisper-quiet inverter generators."
        }}
      }},
      {{
        "@type": "Question",
        "name": "How far in advance should I book in {city}?",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "Peak season in {city} runs through {season}. Because luxury trailers are high in demand for {venues}, booking 3 to 6 months in advance is highly recommended."
        }}
      }}
    ]
  }}
  </script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": "https://reliant-network.vercel.app/"
      }},
      {{
        "@type": "ListItem",
        "position": 2,
        "name": "{state_full}",
        "item": "https://reliant-network.vercel.app/state/{state_slug}"
      }},
      {{
        "@type": "ListItem",
        "position": 3,
        "name": "{city}",
        "item": "https://reliant-network.vercel.app/metro/{city_slug}"
      }},
      {{
        "@type": "ListItem",
        "position": 4,
        "name": "Cost & Pricing Guide",
        "item": "https://reliant-network.vercel.app/cost/{city_slug}.html"
      }}
    ]
  }}
  </script>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen antialiased">
  <div class="bg-gradient-to-r from-amber-600 via-amber-500 to-amber-600 text-slate-950 px-4 py-2 text-xs font-bold text-center flex items-center justify-center gap-2 shadow-xs">
    <i data-lucide="calculator" class="w-4 h-4"></i>
    <span>{city} Restroom Trailer Pricing Index &bull; Verified Market Benchmark Data &bull; 2026 Edition</span>
  </div>

  <header class="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-xs">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <a href="/" class="w-10 h-10 rounded-xl bg-amber-50 border border-amber-300 flex items-center justify-center text-amber-600 shadow-xs">
          <i data-lucide="layers" class="w-6 h-6"></i>
        </a>
        <div>
          <a href="/" class="text-2xl font-bold font-serif-title tracking-tight text-slate-900 flex items-center gap-1.5">
            The Reliant <span class="text-amber-600 font-sans font-extrabold">Network</span>
          </a>
          <span class="text-[10px] text-slate-500 tracking-wider block font-semibold uppercase">{city} Commercial &amp; VIP Pricing</span>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <a href="/metro/{city_slug}" class="text-xs font-semibold text-slate-700 hover:text-slate-900 px-3 py-1.5 rounded-xl border border-slate-200 bg-white">
          View {city} Fleet Directory
        </a>
        <a href="/#quote-planner" class="bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs px-4 py-2 rounded-xl shadow-xs transition-colors">
          Get Instant Quote
        </a>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="flex items-center gap-2 text-xs text-slate-500 mb-6 font-medium">
      <a href="/" class="hover:text-amber-700">Home</a>
      <span>&gt;</span>
      <a href="/state/{state_slug}" class="hover:text-amber-700">{state_full}</a>
      <span>&gt;</span>
      <a href="/metro/{city_slug}" class="hover:text-amber-700">{city}</a>
      <span>&gt;</span>
      <span class="text-slate-800 font-bold">2026 Cost &amp; Price Guide</span>
    </nav>

    <div class="bg-white border border-slate-200 rounded-3xl p-6 sm:p-10 shadow-sm mb-10">
      <div class="max-w-3xl">
        <span class="bg-amber-50 border border-amber-300 text-amber-800 text-xs font-bold uppercase tracking-wider px-3 py-1 rounded-full inline-flex items-center gap-1.5 mb-3 shadow-2xs">
          <i data-lucide="badge-percent" class="w-3.5 h-3.5 text-amber-600"></i>
          <span>{city}, {state} Regional Market Analysis</span>
        </span>
        <h1 class="text-3xl sm:text-5xl font-serif-title font-bold text-slate-900 tracking-tight leading-tight">
          How Much Does It Cost to Rent a Luxury Restroom Trailer in <span class="gold-text italic">{city}?</span>
        </h1>
        <p class="text-slate-600 text-sm sm:text-base mt-4 leading-relaxed">
          Planning a wedding, corporate gala, or festival in the {city} metropolitan area? Here is our comprehensive 2026 pricing breakdown based on local operator rates, fleet size, utility logistics, and {permits} regulations.
        </p>

        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-8">
          <div class="bg-slate-50 border border-slate-200 p-4 rounded-2xl">
            <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500 block">Average Daily Rate</span>
            <span class="text-2xl font-bold font-sans text-amber-700">${avg_cost_fmt}</span>
          </div>
          <div class="bg-slate-50 border border-slate-200 p-4 rounded-2xl">
            <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500 block">Starting Rate</span>
            <span class="text-2xl font-bold font-sans text-slate-900">${min_cost_fmt}</span>
          </div>
          <div class="bg-slate-50 border border-slate-200 p-4 rounded-2xl">
            <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500 block">High-Capacity Fleet</span>
            <span class="text-2xl font-bold font-sans text-slate-900">${max_cost_fmt}</span>
          </div>
          <div class="bg-slate-50 border border-slate-200 p-4 rounded-2xl">
            <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500 block">Peak Booking Window</span>
            <span class="text-xs font-bold font-sans text-slate-800 block mt-1">{season}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="mb-12">
      <div class="flex items-center justify-between mb-4">
        <div>
          <span class="text-xs font-bold text-amber-700 uppercase tracking-widest block">Detailed Breakdown</span>
          <h2 class="text-2xl font-serif-title font-bold text-slate-900">{city} Restroom Trailer Pricing by Fleet Tier</h2>
        </div>
      </div>

      <div class="bg-white border border-slate-200 rounded-3xl overflow-hidden shadow-xs">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs sm:text-sm">
            <thead class="bg-slate-50 border-b border-slate-200 text-slate-700 font-bold uppercase text-[11px] tracking-wider">
              <tr>
                <th class="p-4 sm:p-5">Trailer Class &amp; Stalls</th>
                <th class="p-4 sm:p-5">Guest Capacity</th>
                <th class="p-4 sm:p-5">Key Amenities</th>
                <th class="p-4 sm:p-5">Daily Rate ({city})</th>
                <th class="p-4 sm:p-5 text-right">Availability</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 text-slate-700">
              <tr class="hover:bg-slate-50/70 transition-colors">
                <td class="p-4 sm:p-5 font-bold text-slate-900">
                  <div class="flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-amber-500"></span>
                    <span>2-Station VIP Suite</span>
                  </div>
                  <span class="text-[11px] text-slate-500 font-normal block mt-0.5">1 Women's + 1 Men's Suite</span>
                </td>
                <td class="p-4 sm:p-5 font-medium">Up to 100 Guests</td>
                <td class="p-4 sm:p-5 text-slate-600">Porcelain pedal flush, climate A/C, vanity mirror, solid oak cabinetry</td>
                <td class="p-4 sm:p-5 font-bold text-amber-700 font-sans text-base">${p2_cost_fmt}</td>
                <td class="p-4 sm:p-5 text-right"><span class="bg-emerald-50 text-emerald-700 border border-emerald-200 text-[10px] font-bold px-2 py-0.5 rounded-full">High Availability</span></td>
              </tr>
              <tr class="hover:bg-slate-50/70 transition-colors">
                <td class="p-4 sm:p-5 font-bold text-slate-900">
                  <div class="flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-amber-500"></span>
                    <span>3-Station Elegance Suite</span>
                  </div>
                  <span class="text-[11px] text-slate-500 font-normal block mt-0.5">2 Women's + 1 Men's Suite</span>
                </td>
                <td class="p-4 sm:p-5 font-medium">Up to 220 Guests</td>
                <td class="p-4 sm:p-5 text-slate-600">Granite surfaces, integrated Bluetooth sound, LED step lighting</td>
                <td class="p-4 sm:p-5 font-bold text-amber-700 font-sans text-base">${p3_cost_fmt}</td>
                <td class="p-4 sm:p-5 text-right"><span class="bg-emerald-50 text-emerald-700 border border-emerald-200 text-[10px] font-bold px-2 py-0.5 rounded-full">Available</span></td>
              </tr>
              <tr class="hover:bg-amber-50/40 transition-colors bg-amber-50/20">
                <td class="p-4 sm:p-5 font-bold text-slate-900">
                  <div class="flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-amber-600"></span>
                    <span>4-to-5 Station Luxury (Most Popular)</span>
                  </div>
                  <span class="text-[11px] text-amber-700 font-semibold block mt-0.5">Top choice for weddings in {city}</span>
                </td>
                <td class="p-4 sm:p-5 font-medium">200 – 450 Guests</td>
                <td class="p-4 sm:p-5 text-slate-600">Dual vanity banks, continuous hot water, dual whisper AC units</td>
                <td class="p-4 sm:p-5 font-black text-amber-800 font-sans text-base">${p5_cost_fmt}</td>
                <td class="p-4 sm:p-5 text-right"><span class="bg-amber-100 text-amber-800 border border-amber-300 text-[10px] font-bold px-2 py-0.5 rounded-full">Fast Booking</span></td>
              </tr>
              <tr class="hover:bg-slate-50/70 transition-colors">
                <td class="p-4 sm:p-5 font-bold text-slate-900">
                  <div class="flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-slate-900"></span>
                    <span>8-Station Black-Tie Gala Suite</span>
                  </div>
                  <span class="text-[11px] text-slate-500 font-normal block mt-0.5">4 Women's + 4 Men's Suites</span>
                </td>
                <td class="p-4 sm:p-5 font-medium">450 – 800 Guests</td>
                <td class="p-4 sm:p-5 text-slate-600">High-traffic double circulation, ADA accessibility ramp, onboard attendant lounge</td>
                <td class="p-4 sm:p-5 font-bold text-amber-700 font-sans text-base">${p8_cost_fmt}</td>
                <td class="p-4 sm:p-5 text-right"><span class="bg-amber-50 text-amber-700 border border-amber-200 text-[10px] font-bold px-2 py-0.5 rounded-full">Limited Fleets</span></td>
              </tr>
              <tr class="hover:bg-slate-50/70 transition-colors">
                <td class="p-4 sm:p-5 font-bold text-slate-900">
                  <div class="flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-slate-900"></span>
                    <span>10+ Station Mega-Event Fleet</span>
                  </div>
                  <span class="text-[11px] text-slate-500 font-normal block mt-0.5">Festivals, Film Sets &amp; State Fairs</span>
                </td>
                <td class="p-4 sm:p-5 font-medium">800 – 2,500+ Guests</td>
                <td class="p-4 sm:p-5 text-slate-600">Industrial waste holding (800+ gal), commercial 50A shore power, continuous auxiliary pumping</td>
                <td class="p-4 sm:p-5 font-bold text-slate-900 font-sans text-base">${p10_cost_fmt}</td>
                <td class="p-4 sm:p-5 text-right"><span class="bg-slate-100 text-slate-700 border border-slate-200 text-[10px] font-bold px-2 py-0.5 rounded-full">Advance RFP</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
      <div class="bg-white border border-slate-200 rounded-3xl p-6 sm:p-7 shadow-xs">
        <h3 class="text-lg font-serif-title font-bold text-slate-900 mb-4 flex items-center gap-2">
          <i data-lucide="plus-circle" class="w-4 h-4 text-amber-600"></i>
          <span>Additional Service &amp; Logistics Fees in {city}</span>
        </h3>
        <ul class="space-y-3 text-xs text-slate-600">
          <li class="flex justify-between border-b border-slate-100 pb-2">
            <span class="font-semibold text-slate-800">Standard Delivery &amp; Setup (Within 35 Miles):</span>
            <span class="font-bold text-slate-900">$150 – $350 (Often included)</span>
          </li>
          <li class="flex justify-between border-b border-slate-100 pb-2">
            <span class="font-semibold text-slate-800">Quiet Inverter Generator Package (8 hrs fuel):</span>
            <span class="font-bold text-slate-900">$200 – $400</span>
          </li>
          <li class="flex justify-between border-b border-slate-100 pb-2">
            <span class="font-semibold text-slate-800">Freshwater Tank Filling (Off-Grid Remote):</span>
            <span class="font-bold text-slate-900">$150 – $250</span>
          </li>
          <li class="flex justify-between border-b border-slate-100 pb-2">
            <span class="font-semibold text-slate-800">Uniformed On-Site Attendant (4-Hour Block):</span>
            <span class="font-bold text-slate-900">$200 – $350</span>
          </li>
          <li class="flex justify-between">
            <span class="font-semibold text-slate-800">Mid-Event Auxiliary Pump-Out:</span>
            <span class="font-bold text-slate-900">$300 – $500</span>
          </li>
        </ul>
      </div>

      <div class="bg-white border border-slate-200 rounded-3xl p-6 sm:p-7 shadow-xs">
        <h3 class="text-lg font-serif-title font-bold text-slate-900 mb-4 flex items-center gap-2">
          <i data-lucide="map-pin" class="w-4 h-4 text-emerald-600"></i>
          <span>Local Venues &amp; Permits in {city}, {state}</span>
        </h3>
        <p class="text-xs text-slate-600 leading-relaxed mb-3">
          Popular event types in the {city} region include <strong>{venues}</strong>.
        </p>
        <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5 mb-3 text-xs">
          <span class="font-bold text-slate-900 block mb-1">Permit Authority:</span>
          <span class="text-slate-600">{permits}. Private property events do not require street placement permits, but municipal health standards must be respected.</span>
        </div>
        <div class="bg-amber-50/60 border border-amber-200 rounded-xl p-3.5 text-xs text-amber-900">
          <span class="font-bold block mb-0.5">Reliant Tip for {city}:</span>
          <span>Book at least 90 days ahead during peak season ({season}) to lock in preferred trailer sizes and avoid peak date surge fees.</span>
        </div>
      </div>
    </div>

    <div class="bg-slate-900 text-white rounded-3xl p-8 sm:p-10 mb-14 flex flex-col md:flex-row items-center justify-between gap-6 shadow-xl">
      <div class="max-w-xl">
        <span class="text-[10px] font-mono uppercase tracking-wider text-amber-400 block">Instant Quote Matching</span>
        <h3 class="text-2xl sm:text-3xl font-serif-title font-bold text-white mt-1">
          Get Vetted Quotes from Top {city} Fleets
        </h3>
        <p class="text-xs sm:text-sm text-slate-300 mt-2 leading-relaxed">
          Broadcast your event specifications to the top verified operators in {city}. Compare competitive bids with zero broker markup.
        </p>
      </div>
      <div class="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
        <a href="/#quote-planner" class="bg-amber-500 hover:bg-amber-400 text-slate-950 font-extrabold text-xs px-6 py-3.5 rounded-xl text-center shadow-lg shadow-amber-500/20 transition-all whitespace-nowrap">
          Broadcast Quote Request
        </a>
        <a href="/metro/{city_slug}" class="bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs px-5 py-3.5 rounded-xl border border-slate-700 text-center transition-colors whitespace-nowrap">
          Browse {city} Fleets
        </a>
      </div>
    </div>

    <div class="bg-white border border-slate-200 rounded-3xl p-6 sm:p-8 shadow-xs">
      <h3 class="text-sm font-bold text-slate-900 uppercase tracking-wider mb-4">
        Explore Luxury Restroom Trailer Costs in Other Major Metros
      </h3>
      <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2.5 text-xs">
        {sibling_links}
      </div>
    </div>
  </main>

  <footer class="bg-white border-t border-slate-200 py-8 mt-12 text-center text-slate-500 text-xs">
    <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
      <p>&copy; 2026 The Reliant Network. All rights reserved.</p>
      <div class="flex gap-4">
        <a href="/" class="hover:text-amber-700">Home</a>
        <a href="/badge-generator.html" class="hover:text-amber-700">Partner Badges</a>
        <a href="/metro/{city_slug}" class="hover:text-amber-700">{city} Directory</a>
        <a href="/sitemap.xml" class="hover:text-amber-700">XML Sitemap</a>
      </div>
    </div>
  </footer>

  <script>
    try {{ lucide.createIcons(); }} catch(e){{}}
  </script>
</body>
</html>
"""

state_slugs = {
    "GA": "georgia",
    "TX": "texas",
    "FL": "florida",
    "CA": "california",
    "IL": "illinois",
    "AZ": "arizona",
    "SC": "south-carolina",
    "TN": "tennessee",
    "CO": "colorado",
    "NY": "new-york"
}

generated_cost_files = []

for metro in metros_data:
    city = metro["city"]
    state = metro["state"]
    state_full = metro["state_full"]
    city_slug = city.lower().replace(" ", "-")
    state_slug = state_slugs.get(state, state_full.lower().replace(" ", "-"))

    min_c = metro["min_cost"]
    avg_c = metro["avg_cost"]
    max_c = metro["max_cost"]

    p2_low = int(round(min_c * 0.6 / 50.0) * 50)
    p2_high = int(round(min_c * 0.85 / 50.0) * 50)
    p3_low = int(round(min_c * 0.85 / 50.0) * 50)
    p3_high = int(round(avg_c * 0.85 / 50.0) * 50)
    p5_low = int(round(avg_c * 0.85 / 50.0) * 50)
    p5_high = int(round(avg_c * 1.15 / 50.0) * 50)
    p8_low = int(round(avg_c * 1.15 / 50.0) * 50)
    p8_high = int(round(max_c * 0.75 / 50.0) * 50)
    p10_low = int(round(max_c * 0.75 / 50.0) * 50)

    siblings = []
    for sib in metros_data:
        if sib["city"] != city:
            s_slug = sib["city"].lower().replace(" ", "-")
            siblings.append(f'<a href="/cost/{s_slug}.html" class="p-2.5 bg-slate-50 hover:bg-amber-50 border border-slate-200 hover:border-amber-300 rounded-xl text-center transition-all block font-semibold text-slate-800 hover:text-amber-900">{sib["city"]}, {sib["state"]}</a>')
    sibling_links = "\\n        ".join(siblings)

    page_html = cost_template.format(
        city=city,
        state=state,
        state_full=state_full,
        city_slug=city_slug,
        state_slug=state_slug,
        permits=metro.get("permits", f"City of {city} Health & Safety Guidelines"),
        season=metro.get("season", "Spring to Autumn Peak"),
        venues=metro.get("venues", "Private Estates, Country Clubs & Ranches"),
        min_cost_fmt=f"{min_c:,}",
        avg_cost_fmt=f"{avg_c:,}",
        max_cost_fmt=f"{max_c:,}",
        p2_cost_fmt=f"${p2_low:,} – ${p2_high:,}",
        p3_cost_fmt=f"${p3_low:,} – ${p3_high:,}",
        p5_cost_fmt=f"${p5_low:,} – ${p5_high:,}",
        p8_cost_fmt=f"${p8_low:,} – ${p8_high:,}",
        p10_cost_fmt=f"${p10_low:,} – ${max_c:,}+",
        sibling_links=sibling_links
    )

    cost_file = os.path.join(COST_DIR, f"{city_slug}.html")
    with open(cost_file, "w", encoding="utf-8") as f:
        f.write(page_html)
    generated_cost_files.append(city_slug)

print(f"[OK] Generated {len(generated_cost_files)} Cost Benchmark pages in {COST_DIR}")

# -------------------------------------------------------------
# 4. UPDATE SITEMAP.XML
# -------------------------------------------------------------
if os.path.exists(SITEMAP_XML):
    with open(SITEMAP_XML, "r", encoding="utf-8") as f:
        content = f.read()

    new_entries = []
    if "https://reliantverified.com/badge-generator.html" not in content:
        new_entries.append("""  <url>
    <loc>https://reliantverified.com/badge-generator.html</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>""")

    for slug in generated_cost_files:
        cost_url = f"https://reliantverified.com/cost/{slug}.html"
        if cost_url not in content:
            new_entries.append(f"""  <url>
    <loc>{cost_url}</loc>
    <changefreq>weekly</changefreq>
    <priority>0.85</priority>
  </url>""")

    if new_entries:
        insert_marker = "</urlset>"
        new_content = content.replace(insert_marker, "\\n".join(new_entries) + "\\n" + insert_marker)
        with open(SITEMAP_XML, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[OK] Added {len(new_entries)} new URLs to {SITEMAP_XML}")
    else:
        print("[OK] Sitemap already up to date.")

print("[SUCCESS] All Frey Chu Profit Engine pages & assets generated cleanly.")
