# -*- coding: utf-8 -*-
import os

target = os.path.join("apps", "web", "public", "index.html")

p1 = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Reliant Network | Multi-Vertical High-Ticket B2B Rental Directory</title>
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
    <span>Autonomous Multi-Vertical B2B Portfolio: Restrooms &bull; Cold Storage &bull; Heavy Cranes</span>
    <span class="hidden md:inline bg-slate-950 text-amber-400 px-2 py-0.5 rounded-full text-[10px] ml-2">Edge Pre-Rendered (0ms)</span>
  </div>

  <!-- NAVBAR -->
  <header class="sticky top-0 z-40 bg-slate-950/90 backdrop-blur-md border-b border-slate-800/80">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-amber-400">
          <i data-lucide="layers" class="w-6 h-6"></i>
        </div>
        <div>
          <span class="text-2xl font-bold font-serif-title tracking-tight text-white flex items-center gap-1.5">
            Privy<span class="text-amber-400 font-sans font-extrabold">Luxe</span>
          </span>
          <span class="text-[10px] text-slate-400 tracking-wider block font-semibold uppercase">High-Ticket B2B Directory Network</span>
        </div>
      </div>

      <!-- NICHE SELECTOR PILLS IN NAVBAR -->
      <div class="hidden lg:flex items-center gap-1 bg-slate-900 border border-slate-800 p-1.5 rounded-2xl">
        <button onclick="switchNiche('luxury_restrooms')" id="niche-btn-restrooms" class="px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all bg-amber-500 text-slate-950 shadow-md">
          VIP Restrooms ($85/lead)
        </button>
        <button onclick="switchNiche('commercial_cold_storage')" id="niche-btn-cold" class="px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all text-slate-400 hover:text-white">
          Cold Storage ($125/lead)
        </button>
        <button onclick="switchNiche('heavy_crane_rigging')" id="niche-btn-crane" class="px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all text-slate-400 hover:text-white">
          Heavy Cranes ($175/lead)
        </button>
      </div>

      <div class="flex items-center gap-3">
        <button onclick="openAdminModal()" class="flex items-center gap-1.5 text-amber-400 hover:text-amber-300 font-semibold bg-amber-500/10 px-3 py-1.5 rounded-lg border border-amber-500/30 text-xs">
          <i data-lucide="line-chart" class="w-4 h-4"></i>
          <span class="hidden sm:inline">Cash Flow Command</span>
        </button>
        <button onclick="openQuoteModal()" class="bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-bold text-xs px-4 py-2 rounded-xl shadow-lg shadow-amber-500/20 flex items-center gap-2 transition-all">
          <i data-lucide="calculator" class="w-4 h-4"></i>
          <span>Instant Quote</span>
        </button>
      </div>
    </div>
  </header>

  <!-- HERO SECTION -->
  <section class="relative pt-16 pb-20 overflow-hidden border-b border-slate-800">
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-amber-500/10 via-slate-950/0 to-slate-950"></div>
    
    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <div id="hero-badge" class="inline-flex items-center gap-2 bg-slate-900/80 border border-slate-700/60 px-4 py-1.5 rounded-full text-xs font-semibold text-amber-400 mb-6 shadow-inner">
        <i data-lucide="shield-check" class="w-4 h-4"></i>
        <span>Verified High-Ticket Commercial &amp; VIP Fleets</span>
      </div>

      <h1 id="hero-title" class="text-4xl sm:text-6xl font-serif-title font-bold text-white tracking-tight leading-tight max-w-4xl mx-auto">
        Rent High-End Restroom Trailers for <span class="gold-text italic">Weddings, VIP Galas &amp; Productions</span>
      </h1>
      
      <p id="hero-desc" class="mt-6 text-lg text-slate-400 max-w-2xl mx-auto">
        Browse top-rated luxury restroom trailers with flushing porcelain toilets, climate control, running hot water, and granite vanities. Get instant quotes matched to verified operators.
      </p>

      <!-- SEARCH & FILTER BAR -->
      <div class="mt-10 max-w-4xl mx-auto bg-slate-900/90 border border-slate-700/80 p-4 rounded-2xl shadow-2xl backdrop-blur-xl grid grid-cols-1 sm:grid-cols-4 gap-3 text-left">
        <div>
          <label class="block text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1">Target Metro</label>
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
          <label class="block text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1">Feature / Spec</label>
          <select id="filter-amenity" onchange="loadVendors()" class="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:border-amber-500">
            <option value="">All Features</option>
            <option value="ADA Compliant">ADA Compliant</option>
            <option value="Climate Controlled A/C">Climate Controlled A/C</option>
            <option value="-20F to 50F Temp Range">-20F Deep Freeze</option>
            <option value="NCCCO Certified">NCCCO Certified Crane</option>
            <option value="Granite Countertops">Granite Countertops</option>
          </select>
        </div>

        <div class="sm:col-span-2 flex items-end gap-2">
          <div class="flex-1">
            <label class="block text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1">Search Fleet / Equipment</label>
            <input type="text" id="search-input" onkeyup="loadVendors()" placeholder="e.g. trailer, reefer container, all-terrain crane..." class="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:border-amber-500">
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
    f.write(p1)
print("Multi-Niche Part 1 written")
