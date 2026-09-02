import os

target = os.path.join("apps", "web", "public", "index.html")

part3 = """
  <!-- INSTANT QUOTE MODAL -->
  <div id="quote-modal" class="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md hidden flex items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-700 rounded-3xl max-w-xl w-full p-6 sm:p-8 shadow-2xl relative">
      <button onclick="closeQuoteModal()" class="absolute top-5 right-5 text-slate-400 hover:text-white"><i data-lucide="x" class="w-6 h-6"></i></button>

      <div class="flex items-center gap-3 mb-6">
        <div class="w-10 h-10 rounded-xl bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-amber-400">
          <i data-lucide="calculator" class="w-5 h-5"></i>
        </div>
        <div>
          <h3 class="text-xl font-serif-title font-bold text-white">Instant AI Quote Calculator</h3>
          <p class="text-xs text-slate-400">Instant contract sizing &amp; broadcast quote to verified operators</p>
        </div>
      </div>

      <form id="quote-form" onsubmit="handleQuoteSubmit(event)" class="space-y-4">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1">Your Full Name</label>
            <input type="text" id="q-name" required placeholder="e.g. Jessica Sterling" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-amber-500">
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1">Email Address</label>
            <input type="email" id="q-email" required placeholder="jessica@events.com" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-amber-500">
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1">Phone (SMS Alerts)</label>
            <input type="tel" id="q-phone" required placeholder="(404) 555-0199" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-amber-500">
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1">Event City</label>
            <select id="q-city" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-amber-500">
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
            <label class="block text-xs font-semibold text-slate-300 mb-1">Event Date</label>
            <input type="date" id="q-date" required class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-amber-500">
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1">Estimated Guest Count</label>
            <input type="number" id="q-guests" required value="200" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-amber-500">
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1">Event Type</label>
            <select id="q-type" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-amber-500">
              <option value="Luxury Wedding">Luxury Wedding</option>
              <option value="VIP Gala / Fundraiser">VIP Gala / Fundraiser</option>
              <option value="Film & TV Production">Film &amp; TV Production</option>
              <option value="Corporate Retreat">Corporate Retreat</option>
              <option value="Private Estate Party">Private Estate Party</option>
            </select>
          </div>
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-300 mb-1">Venue Details &amp; Special Requirements</label>
          <textarea id="q-notes" rows="2" placeholder="e.g. Need heated suites, ADA ramp required, private lawn access..." class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-amber-500"></textarea>
        </div>

        <button type="submit" id="quote-submit-btn" class="w-full bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-extrabold text-sm py-3 rounded-xl shadow-xl shadow-amber-500/20 flex items-center justify-center gap-2 transition-all">
          <i data-lucide="zap" class="w-4 h-4"></i>
          <span>Calculate AI Estimate &amp; Dispatch to Operators</span>
        </button>
      </form>

      <!-- SUCCESS DISPATCH VIEW -->
      <div id="quote-success-view" class="hidden text-center py-6">
        <div class="w-16 h-16 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center mx-auto mb-4 border border-emerald-500/40">
          <i data-lucide="check" class="w-8 h-8"></i>
        </div>
        <h4 class="text-xl font-bold text-white">Quote Request Broadcasted!</h4>
        <p id="quote-success-msg" class="text-sm text-slate-300 mt-2 max-w-md mx-auto"></p>
        <div id="quote-dispatch-details" class="mt-4 bg-slate-950 border border-slate-800 rounded-xl p-4 text-xs font-mono text-left space-y-1 text-slate-300"></div>
        <button onclick="closeQuoteModal()" class="mt-6 bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs px-6 py-2.5 rounded-xl border border-slate-700">Done</button>
      </div>
    </div>
  </div>

  <!-- EMBED TRUST BADGE MODAL -->
  <div id="badge-modal" class="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md hidden flex items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-700 rounded-3xl max-w-lg w-full p-6 shadow-2xl relative">
      <button onclick="closeBadgeModal()" class="absolute top-5 right-5 text-slate-400 hover:text-white"><i data-lucide="x" class="w-6 h-6"></i></button>

      <div class="flex items-center gap-3 mb-4">
        <div class="w-10 h-10 rounded-xl bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-amber-400">
          <i data-lucide="badge-check" class="w-5 h-5"></i>
        </div>
        <div>
          <h3 class="text-lg font-serif-title font-bold text-white">The Reliant Network Verified 2026 Partner Badge</h3>
          <p class="text-xs text-slate-400">Embed this verified badge on your website for instant SEO authority.</p>
        </div>
      </div>

      <div id="badge-preview-container" class="bg-slate-950 border border-slate-800 p-4 rounded-xl text-center my-4">
        <!-- Live preview -->
      </div>

      <div>
        <label class="block text-xs font-semibold text-slate-300 mb-1">HTML Embed Code (Paste into your website footer/header):</label>
        <textarea id="badge-embed-code" readonly rows="4" class="w-full bg-slate-950 border border-slate-800 font-mono text-xs text-amber-300 p-3 rounded-xl focus:outline-none"></textarea>
      </div>

      <button onclick="copyBadgeCode()" class="mt-4 w-full bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold py-2.5 rounded-xl text-xs flex items-center justify-center gap-2">
        <i data-lucide="copy" class="w-4 h-4"></i>
        <span id="copy-btn-text">Copy HTML Embed Code</span>
      </button>
    </div>
  </div>

  <!-- ADMIN CASH FLOW COMMAND CENTER -->
  <div id="admin-modal" class="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md hidden flex items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-700 rounded-3xl max-w-4xl w-full p-6 sm:p-8 shadow-2xl relative max-h-[90vh] overflow-y-auto">
      <button onclick="closeAdminModal()" class="absolute top-5 right-5 text-slate-400 hover:text-white"><i data-lucide="x" class="w-6 h-6"></i></button>

      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-6 mb-6">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 rounded-2xl bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-amber-400">
            <i data-lucide="wallet" class="w-6 h-6"></i>
          </div>
          <div>
            <h3 class="text-2xl font-serif-title font-bold text-white">Passive Cash Flow Command Center</h3>
            <p class="text-xs text-slate-400">Real-Time Revenue, Subscriptions &amp; Autonomous Guardrails</p>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <button onclick="runAutonomousCron()" id="cron-trigger-btn" class="bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-bold text-xs px-4 py-2 rounded-xl flex items-center gap-1.5 transition-all">
            <i data-lucide="play" class="w-3.5 h-3.5"></i>
            <span>Trigger 24h Cadence Cycle</span>
          </button>
        </div>
      </div>

      <!-- METRIC CARDS -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
        <div class="bg-slate-950 border border-slate-800/80 p-4 rounded-2xl">
          <span class="text-xs text-slate-400 block">Total Banked Revenue</span>
          <span id="metric-revenue" class="text-2xl sm:text-3xl font-extrabold text-emerald-400 mt-1 block">$1,211.00</span>
          <span class="text-[10px] text-emerald-500/80 mt-1 block flex items-center gap-1"><i data-lucide="arrow-up-right" class="w-3 h-3"></i> 100% Passive</span>
        </div>

        <div class="bg-slate-950 border border-slate-800/80 p-4 rounded-2xl">
          <span class="text-xs text-slate-400 block">Active MRR (Vendors)</span>
          <span id="metric-mrr" class="text-2xl sm:text-3xl font-extrabold text-amber-400 mt-1 block">$693.00/mo</span>
          <span class="text-[10px] text-amber-500/80 mt-1 block">7 Subscribed Operators</span>
        </div>

        <div class="bg-slate-950 border border-slate-800/80 p-4 rounded-2xl">
          <span class="text-xs text-slate-400 block">Brokered Quotes</span>
          <span id="metric-leads" class="text-2xl sm:text-3xl font-extrabold text-white mt-1 block">6</span>
          <span class="text-[10px] text-slate-500 mt-1 block">Avg $85 - $125 / lead</span>
        </div>

        <div class="bg-slate-950 border border-slate-800/80 p-4 rounded-2xl">
          <span class="text-xs text-slate-400 block">Cache &amp; Latency</span>
          <span id="metric-cache-hit" class="text-2xl sm:text-3xl font-extrabold text-cyan-400 mt-1 block">100%</span>
          <span class="text-[10px] text-cyan-500/80 mt-1 block">&lt; 1.5ms response time</span>
        </div>
      </div>

      <!-- DELIVERABILITY SHIELD GAUGE -->
      <div class="bg-slate-950 border border-slate-800 rounded-2xl p-4 mb-6">
        <div class="flex items-center justify-between mb-2">
          <div class="flex items-center gap-2">
            <i data-lucide="shield" class="w-4 h-4 text-emerald-400"></i>
            <span class="text-xs font-bold text-white uppercase tracking-wider">Outbound Deliverability Shield</span>
            <span class="text-[10px] text-emerald-400 bg-emerald-500/10 border border-emerald-500/30 px-2 py-0.5 rounded-full font-mono">alerts-reliantverified.com</span>
          </div>
          <span id="deliv-quota-text" class="text-xs text-slate-400 font-mono">2 / 15 Daily Quota Used</span>
        </div>
        <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
          <div id="deliv-progress-bar" class="bg-emerald-500 h-full rounded-full transition-all" style="width: 13%;"></div>
        </div>
      </div>

      <!-- ANOMALY REVIEW QUEUE -->
      <div class="mb-6">
        <h4 class="text-sm font-bold text-white mb-3 flex items-center justify-between">
          <span class="flex items-center gap-2">
            <i data-lucide="alert-triangle" class="w-4 h-4 text-rose-400"></i>
            <span>Data Anomaly Review Queue (Circuit Breaker)</span>
          </span>
          <span id="anomaly-badge" class="bg-rose-500/20 text-rose-400 border border-rose-500/30 text-[10px] font-bold px-2 py-0.5 rounded-full">0 Pending</span>
        </h4>
        <div id="anomaly-container" class="space-y-2">
          <!-- Injected via JS -->
        </div>
      </div>

      <!-- LOGS & REAL-TIME DISPATCH FEED -->
      <div>
        <h4 class="text-sm font-bold text-white mb-3 flex items-center gap-2">
          <i data-lucide="activity" class="w-4 h-4 text-amber-400"></i>
          <span>Live Autonomous Engine Activity Logs</span>
        </h4>
        <div id="admin-logs-container" class="bg-slate-950 border border-slate-800 rounded-2xl p-4 font-mono text-xs text-slate-300 space-y-2 max-h-48 overflow-y-auto">
        </div>
      </div>
    </div>
  </div>
"""

with open(target, "a", encoding="utf-8") as f:
    f.write(part3)
print("Part 3 written")
