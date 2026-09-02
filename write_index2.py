import os

target = os.path.join("apps", "web", "public", "index.html")

part2 = """
  <!-- DIRECTORY SECTION -->
  <section id="directory" class="py-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex flex-col md:flex-row md:items-end justify-between mb-10 gap-4">
      <div>
        <span class="text-xs font-bold text-amber-400 uppercase tracking-widest block mb-1">Verified Fleet Directory</span>
        <h2 class="text-3xl font-serif-title font-bold text-white">Luxury Restroom Operators</h2>
      </div>
      <div class="flex items-center gap-3">
        <span id="vendor-count-badge" class="bg-slate-800 text-slate-300 text-xs px-3 py-1.5 rounded-lg border border-slate-700 font-semibold">16 Listings</span>
        <button onclick="openQuoteModal()" class="bg-amber-500/10 text-amber-400 border border-amber-500/30 text-xs font-bold px-4 py-1.5 rounded-lg hover:bg-amber-500/20 transition-colors flex items-center gap-1.5">
          <i data-lucide="send" class="w-3.5 h-3.5"></i>
          <span>Multi-Operator Broadcast Quote</span>
        </button>
      </div>
    </div>

    <!-- VENDORS GRID -->
    <div id="vendors-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Injected via JS -->
    </div>
  </section>

  <!-- POPULAR METROS & PSEO HUBS -->
  <section id="metros" class="py-16 bg-slate-900/50 border-t border-slate-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center max-w-2xl mx-auto mb-12">
        <span class="text-xs font-bold text-amber-400 uppercase tracking-widest block mb-1">Programmatic SEO Coverage</span>
        <h2 class="text-3xl font-serif-title font-bold text-white">Top Destination Metros &amp; Suburbs</h2>
        <p class="text-slate-400 text-sm mt-2">Dynamic localized landing pages with drone ingress evaluations, laser leveling, and climate control standards.</p>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-4">
        <div onclick="selectMetro('Atlanta')" class="cursor-pointer bg-slate-900 border border-slate-800 hover:border-amber-500/60 p-4 rounded-xl text-center transition-all hover:scale-105">
          <span class="text-amber-400 font-bold text-sm block">Atlanta, GA</span>
          <span class="text-[11px] text-slate-400 block mt-1">Buckhead &bull; Alpharetta</span>
        </div>
        <div onclick="selectMetro('Dallas')" class="cursor-pointer bg-slate-900 border border-slate-800 hover:border-amber-500/60 p-4 rounded-xl text-center transition-all hover:scale-105">
          <span class="text-amber-400 font-bold text-sm block">Dallas, TX</span>
          <span class="text-[11px] text-slate-400 block mt-1">Highland Park &bull; Plano</span>
        </div>
        <div onclick="selectMetro('Miami')" class="cursor-pointer bg-slate-900 border border-slate-800 hover:border-amber-500/60 p-4 rounded-xl text-center transition-all hover:scale-105">
          <span class="text-amber-400 font-bold text-sm block">Miami, FL</span>
          <span class="text-[11px] text-slate-400 block mt-1">Coral Gables &bull; Palm Beach</span>
        </div>
        <div onclick="selectMetro('Austin')" class="cursor-pointer bg-slate-900 border border-slate-800 hover:border-amber-500/60 p-4 rounded-xl text-center transition-all hover:scale-105">
          <span class="text-amber-400 font-bold text-sm block">Austin, TX</span>
          <span class="text-[11px] text-slate-400 block mt-1">Hill Country &bull; Westlake</span>
        </div>
        <div onclick="selectMetro('Los Angeles')" class="cursor-pointer bg-slate-900 border border-slate-800 hover:border-amber-500/60 p-4 rounded-xl text-center transition-all hover:scale-105">
          <span class="text-amber-400 font-bold text-sm block">Los Angeles, CA</span>
          <span class="text-[11px] text-slate-400 block mt-1">Malibu &bull; Beverly Hills</span>
        </div>
        <div onclick="selectMetro('Napa Valley')" class="cursor-pointer bg-slate-900 border border-slate-800 hover:border-amber-500/60 p-4 rounded-xl text-center transition-all hover:scale-105">
          <span class="text-amber-400 font-bold text-sm block">Napa Valley, CA</span>
          <span class="text-[11px] text-slate-400 block mt-1">St. Helena &bull; Yountville</span>
        </div>
      </div>
    </div>
  </section>

  <!-- PROTOCOL STANDARDS SECTION -->
  <section id="how-it-works" class="py-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="text-center max-w-2xl mx-auto mb-12">
      <span class="text-xs font-bold text-amber-400 uppercase tracking-widest block mb-1">Operational Standards</span>
      <h2 class="text-3xl font-serif-title font-bold text-white">The The Reliant Network Technical Standard</h2>
      <p class="text-slate-400 text-sm mt-2">Every listing on our directory complies with strict engineering protocols.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl">
        <div class="w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 mb-4 font-bold">1</div>
        <h3 class="text-base font-bold text-white">Drone Aerial Ingress</h3>
        <p class="text-xs text-slate-400 mt-2">High-resolution drone surveys verify 14ft overhead branch clearance and tight motor court turning radiuses.</p>
      </div>

      <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl">
        <div class="w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 mb-4 font-bold">2</div>
        <h3 class="text-base font-bold text-white">Laser-Leveling</h3>
        <p class="text-xs text-slate-400 mt-2">Laser-calibrated hydraulic stabilizers deployed to ensure +/- 0.5 degree grade tolerance on rolling lawn terrain.</p>
      </div>

      <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl">
        <div class="w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 mb-4 font-bold">3</div>
        <h3 class="text-base font-bold text-white">Acoustic &lt;52 dBA</h3>
        <p class="text-xs text-slate-400 mt-2">Whisper-pack sound baffles ensure zero noise interference during outdoor vows and strict evening residential curfews.</p>
      </div>

      <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl">
        <div class="w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 mb-4 font-bold">4</div>
        <h3 class="text-base font-bold text-white">ADA 1:12 Slope Ramps</h3>
        <p class="text-xs text-slate-400 mt-2">Continuous aluminum handrails, zero-threshold doors, and low-angle illuminated ramps ensure 100% universal access.</p>
      </div>
    </div>
  </section>
"""

with open(target, "a", encoding="utf-8") as f:
    f.write(part2)
print("Part 2 written")
