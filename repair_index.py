import sys

html_file = 'C:\\Users\\fores\\.gemini\\antigravity\\scratch\\autonomous-directory-engine\\apps\\web\\public\\index.html'

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

correct_header = """<body class="bg-slate-950 text-slate-100 min-h-screen selection:bg-amber-500 selection:text-slate-950">

  <!-- TOP ANNOUNCEMENT BAR -->
  <div class="bg-gradient-to-r from-amber-600 via-amber-500 to-amber-700 text-slate-950 px-4 py-2 text-xs font-bold tracking-wide text-center flex items-center justify-center gap-2">
    <i data-lucide="shield-check" class="w-4 h-4"></i>
    <span>Autonomous Multi-Vertical B2B Portfolio: Restrooms &bull; Cold Storage &bull; Heavy Cranes &bull; Senior Care</span>
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
        <button onclick="switchNiche('senior_care_placement')" id="niche-btn-senior" class="px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all text-slate-400 hover:text-white">
          65+ Senior Care ($250/lead)
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
    
    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">"""

import re
new_content = re.sub(
    r'<body class="bg-slate-950 text-slate-100 min-h-screen selection:bg-amber-500 selection:text-slate-950">.*?<div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">', 
    correct_header, 
    content, 
    flags=re.DOTALL
)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Repaired index.html")
