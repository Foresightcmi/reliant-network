import os

target = os.path.join("apps", "web", "public", "index.html")

part1 = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Reliant Network | Premier Luxury Restroom Trailers & VIP Sanitation Directory</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    .font-serif-title { font-family: 'Playfair Display', serif; }
    .gold-text { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen selection:bg-amber-500 selection:text-slate-950">

  <!-- TOP ANNOUNCEMENT BAR -->
  <div class="bg-gradient-to-r from-amber-600 via-amber-500 to-amber-700 text-slate-950 px-4 py-2 text-xs font-bold tracking-wide text-center flex items-center justify-center gap-2">
    <i data-lucide="shield-check" class="w-4 h-4"></i>
    <span>Autonomous AI Lead Engine v3.2 Active: In-Memory Caching (&lt;1.5ms) &amp; Enterprise Anomaly Guardrails</span>
    <span class="hidden md:inline bg-slate-950 text-amber-400 px-2 py-0.5 rounded-full text-[10px] ml-2">99.4% Lead Accuracy</span>
  </div>

  <!-- NAVBAR -->
  <header class="sticky top-0 z-40 bg-slate-950/90 backdrop-blur-md border-b border-slate-800/80">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-amber-400">
          <i data-lucide="crown" class="w-6 h-6"></i>
        </div>
        <div>
          <span class="text-2xl font-bold font-serif-title tracking-tight text-white flex items-center gap-1.5">
            Privy<span class="text-amber-400 font-sans font-extrabold">Luxe</span>
          </span>
          <span class="text-[10px] text-slate-400 tracking-wider block font-semibold uppercase">Luxury Restroom Directory</span>
        </div>
      </div>

      <nav class="hidden md:flex items-center gap-8 text-sm font-medium text-slate-300">
        <a href="#directory" class="hover:text-amber-400 transition-colors">Directory</a>
        <a href="#metros" class="hover:text-amber-400 transition-colors">Top Metros</a>
        <a href="#how-it-works" class="hover:text-amber-400 transition-colors">Protocol Standards</a>
        <button onclick="openAdminModal()" class="flex items-center gap-1.5 text-amber-400 hover:text-amber-300 font-semibold bg-amber-500/10 px-3 py-1.5 rounded-lg border border-amber-500/30">
          <i data-lucide="line-chart" class="w-4 h-4"></i>
          <span>Cash Flow Command</span>
        </button>
      </nav>

      <div class="flex items-center gap-3">
        <button onclick="openQuoteModal()" class="bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-bold text-sm px-5 py-2.5 rounded-xl shadow-lg shadow-amber-500/20 flex items-center gap-2 transition-all hover:scale-105 active:scale-95">
          <i data-lucide="calculator" class="w-4 h-4"></i>
          <span>Instant AI Quote</span>
        </button>
      </div>
    </div>
  </header>

  <!-- HERO SECTION -->
  <section class="relative pt-16 pb-20 overflow-hidden border-b border-slate-800">
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-amber-500/10 via-slate-950/0 to-slate-950"></div>
    
    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <div class="inline-flex items-center gap-2 bg-slate-900/80 border border-slate-700/60 px-4 py-1.5 rounded-full text-xs font-semibold text-amber-400 mb-6 shadow-inner">
        <i data-lucide="shield-check" class="w-4 h-4"></i>
        <span>Laser-Leveling &amp; Drone Aerial Ingress Certified VIP Operators</span>
      </div>

      <h1 class="text-4xl sm:text-6xl font-serif-title font-bold text-white tracking-tight leading-tight max-w-4xl mx-auto">
        Rent High-End Restroom Trailers for <span class="gold-text italic">Weddings, VIP Galas &amp; Productions</span>
      </h1>
      
      <p class="mt-6 text-lg text-slate-400 max-w-2xl mx-auto">
        Browse top-rated luxury restroom trailers with flushing porcelain toilets, climate control, running hot water, and granite vanities. Get instant quotes matched to verified operators.
      </p>

      <!-- SEARCH & FILTER BAR -->
      <div class="mt-10 max-w-4xl mx-auto bg-slate-900/90 border border-slate-700/80 p-4 rounded-2xl shadow-2xl backdrop-blur-xl grid grid-cols-1 sm:grid-cols-4 gap-3 text-left">
        <div>
          <label class="block text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1">Target Metro / Suburb</label>
          <select id="filter-city" onchange="loadVendors()" class="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:border-amber-500">
            <option value="All">All Major Metros</option>
            <option value="Atlanta">Atlanta, GA</option>
            <option value="Dallas">Dallas, TX</option>
            <option value="Miami">Miami, FL</option>
            <option value="Austin">Austin, TX</option>
            <option value="Los Angeles">Los Angeles, CA</option>
            <option value="Chicago">Chicago, IL</option>
            <option value="Napa Valley">Napa Valley, CA</option>
          </select>
        </div>

        <div>
          <label class="block text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1">Feature / Amenity</label>
          <select id="filter-amenity" onchange="loadVendors()" class="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:border-amber-500">
            <option value="">All Features</option>
            <option value="ADA Compliant">ADA Compliant</option>
            <option value="Climate Controlled A/C">Climate Controlled A/C</option>
            <option value="Granite Countertops">Granite Countertops</option>
            <option value="Bluetooth Sound System">Bluetooth Sound</option>
            <option value="Porcelain Flushing Toilets">Flushing Porcelain</option>
          </select>
        </div>

        <div class="sm:col-span-2 flex items-end gap-2">
          <div class="flex-1">
            <label class="block text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1">Keyword Search</label>
            <input type="text" id="search-input" onkeyup="loadVendors()" placeholder="e.g. wedding suite, honeywagon, 4-station..." class="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:border-amber-500">
          </div>
          <button onclick="loadVendors()" class="bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold px-4 py-2.5 rounded-xl text-sm flex items-center gap-1.5 transition-colors">
            <i data-lucide="search" class="w-4 h-4"></i>
            <span>Search</span>
          </button>
        </div>
      </div>
    </div>
  </section>
"""

with open(target, "w", encoding="utf-8") as f:
    f.write(part1)
print("Part 1 written")
