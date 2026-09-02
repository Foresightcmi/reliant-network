import os

target = os.path.join("apps", "web", "public", "index.html")

part4 = """
  <!-- JAVASCRIPT APP LOGIC -->
  <script>
    let currentVendors = [];
    let selectedClaimVendorId = null;

    async function loadVendors() {
      const city = document.getElementById('filter-city').value;
      const amenity = document.getElementById('filter-amenity').value;
      const search = document.getElementById('search-input')?.value || '';

      const grid = document.getElementById('vendors-grid');
      grid.innerHTML = '<div class="col-span-full py-16 text-center text-slate-500"><i data-lucide="loader-2" class="w-8 h-8 animate-spin mx-auto text-amber-500 mb-2"></i><span>Filtering luxury operators...</span></div>';
      lucide.createIcons();

      try {
        let url = `/api/vendors?city=${encodeURIComponent(city)}&amenity=${encodeURIComponent(amenity)}&search=${encodeURIComponent(search)}`;
        const res = await fetch(url);
        const vendors = await res.json();
        currentVendors = vendors;

        document.getElementById('vendor-count-badge').textContent = `${vendors.length} Listings`;

        if (!vendors.length) {
          grid.innerHTML = '<div class="col-span-full py-16 text-center text-slate-400">No operators found matching your criteria. Try switching the metro or amenity filter.</div>';
          return;
        }

        grid.innerHTML = vendors.map(v => `
          <div class="bg-slate-900 border ${v.subscription_active ? 'border-amber-500/60 shadow-xl shadow-amber-500/5' : 'border-slate-800'} rounded-2xl overflow-hidden flex flex-col justify-between hover:border-amber-500/80 transition-all duration-300">
            <div>
              <div class="relative h-48 overflow-hidden">
                <img src="${v.image_url}" alt="${v.name}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                <div class="absolute top-3 left-3 flex gap-1.5 flex-wrap">
                  ${v.subscription_active ? '<span class="bg-amber-500 text-slate-950 font-extrabold text-[10px] px-2.5 py-0.5 rounded-full flex items-center gap-1 shadow-md"><i data-lucide="star" class="w-3 h-3 fill-slate-950"></i> Featured Partner</span>' : ''}
                  <span class="bg-slate-950/80 backdrop-blur text-amber-400 border border-amber-500/30 font-bold text-[10px] px-2 py-0.5 rounded-full flex items-center gap-1">
                    <i data-lucide="check-circle-2" class="w-3 h-3"></i> Verified
                  </span>
                </div>
                <div class="absolute bottom-3 right-3 bg-slate-950/90 text-white font-bold text-xs px-2.5 py-1 rounded-lg border border-slate-800">
                  $${v.min_price.toLocaleString()} - $${v.max_price.toLocaleString()}
                </div>
              </div>

              <div class="p-5">
                <div class="flex items-center justify-between">
                  <span class="text-[11px] font-bold text-amber-400 uppercase tracking-wider">${v.city}, ${v.state}</span>
                  <div class="flex items-center gap-1 text-xs font-bold text-amber-400">
                    <i data-lucide="star" class="w-3.5 h-3.5 fill-amber-400"></i>
                    <span>${v.rating} (${v.review_count})</span>
                  </div>
                </div>

                <h3 class="text-lg font-bold text-white mt-1 leading-snug">${v.name}</h3>
                <p class="text-xs text-slate-400 mt-2 line-clamp-2">${v.description}</p>

                <div class="mt-4 flex flex-wrap gap-1.5">
                  ${v.amenities.slice(0, 3).map(a => `<span class="bg-slate-800/80 text-slate-300 text-[10px] px-2 py-0.5 rounded-md border border-slate-700/60">${a}</span>`).join('')}
                  ${v.amenities.length > 3 ? `<span class="text-[10px] text-slate-400 font-semibold px-1 py-0.5">+${v.amenities.length - 3} more</span>` : ''}
                </div>
              </div>
            </div>

            <div class="p-5 pt-0 border-t border-slate-800/80 mt-4 flex items-center justify-between gap-2">
              <button onclick="openQuoteModal('${v.city}')" class="flex-1 bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-bold py-2 rounded-xl flex items-center justify-center gap-1.5 transition-colors">
                <i data-lucide="send" class="w-3.5 h-3.5"></i>
                <span>Quote</span>
              </button>

              <button onclick="openBadgeModal('${v.id}')" class="bg-slate-800 hover:bg-slate-700 text-amber-400 text-[11px] font-semibold px-2.5 py-2 rounded-xl border border-slate-700" title="Get Embeddable Verified Badge">
                <i data-lucide="badge-check" class="w-3.5 h-3.5"></i>
              </button>
            </div>
          </div>
        `).join('');

        lucide.createIcons();
      } catch (err) {
        grid.innerHTML = `<div class="col-span-full py-16 text-center text-rose-400">Error loading directory: ${err.message}</div>`;
      }
    }

    function selectMetro(city) {
      document.getElementById('filter-city').value = city;
      loadVendors();
      document.getElementById('directory').scrollIntoView({ behavior: 'smooth' });
    }

    function openQuoteModal(city) {
      if (city) document.getElementById('q-city').value = city;
      document.getElementById('quote-modal').classList.remove('hidden');
      document.getElementById('quote-form').classList.remove('hidden');
      document.getElementById('quote-success-view').classList.add('hidden');
      lucide.createIcons();
    }
    function closeQuoteModal() {
      document.getElementById('quote-modal').classList.add('hidden');
    }

    async function handleQuoteSubmit(e) {
      e.preventDefault();
      const btn = document.getElementById('quote-submit-btn');
      btn.disabled = true;
      btn.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>AI Grading &amp; Dispatched...</span>';
      lucide.createIcons();

      const payload = {
        customer_name: document.getElementById('q-name').value,
        customer_email: document.getElementById('q-email').value,
        customer_phone: document.getElementById('q-phone').value,
        city: document.getElementById('q-city').value,
        state: 'GA',
        event_date: document.getElementById('q-date').value,
        guest_count: parseInt(document.getElementById('q-guests').value),
        event_type: document.getElementById('q-type').value,
        notes: document.getElementById('q-notes').value
      };

      try {
        const res = await fetch('/api/leads', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();

        document.getElementById('quote-form').classList.add('hidden');
        document.getElementById('quote-success-view').classList.remove('hidden');
        document.getElementById('quote-success-msg').textContent = `Matched with top ${data.dispatch.matched_vendors_count} verified operators in ${payload.city}. Estimated Quote Range: $${data.qualification.estimated_quote.toLocaleString()} (${data.qualification.stations_recommended}).`;

        document.getElementById('quote-dispatch-details').innerHTML = `
          <div>&gt; Lead Reference Code: <span class="text-white font-bold">${data.lead_code}</span></div>
          <div>&gt; AI Intent Quality Score: <span class="text-emerald-400 font-bold">${data.qualification.intent_score}/100</span></div>
          <div>&gt; Pay-Per-Lead Value: <span class="text-emerald-400 font-bold">$${data.qualification.lead_price}</span></div>
          <div class="mt-2 text-slate-400">&gt; Automated Deliverability-Safe Alert sent from alerts-reliantverified.com.</div>
        `;
        lucide.createIcons();
      } catch (err) {
        alert('Error submitting quote: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i data-lucide="zap" class="w-4 h-4"></i><span>Calculate AI Estimate &amp; Dispatch to Operators</span>';
        lucide.createIcons();
      }
    }

    async function openBadgeModal(vendorId) {
      try {
        const res = await fetch(`/api/growth/badge-embed/${vendorId}`);
        const data = await res.json();
        document.getElementById('badge-embed-code').value = data.badge_html;
        document.getElementById('badge-preview-container').innerHTML = data.badge_html;
        document.getElementById('badge-modal').classList.remove('hidden');
        lucide.createIcons();
      } catch (err) {
        alert('Error fetching badge: ' + err.message);
      }
    }
    function closeBadgeModal() {
      document.getElementById('badge-modal').classList.add('hidden');
    }

    function copyBadgeCode() {
      const code = document.getElementById('badge-embed-code').value;
      navigator.clipboard.writeText(code);
      document.getElementById('copy-btn-text').textContent = 'Copied to Clipboard!';
      setTimeout(() => {
        document.getElementById('copy-btn-text').textContent = 'Copy HTML Embed Code';
      }, 2000);
    }

    async function openAdminModal() {
      document.getElementById('admin-modal').classList.remove('hidden');
      lucide.createIcons();
      await fetchAdminMetrics();
      await fetchAnomalies();
      await fetchDeliverabilityStats();
    }
    function closeAdminModal() {
      document.getElementById('admin-modal').classList.add('hidden');
    }

    async function fetchAdminMetrics() {
      try {
        const res = await fetch('/api/admin/metrics');
        const data = await res.json();

        document.getElementById('metric-revenue').textContent = `$${data.total_revenue_banked.toLocaleString('en-US', { minimumFractionDigits: 2 })}`;
        document.getElementById('metric-mrr').textContent = `$${data.active_mrr.toLocaleString('en-US', { minimumFractionDigits: 2 })}/mo`;
        document.getElementById('metric-leads').textContent = data.total_leads;
        if (data.cache_telemetry) {
          document.getElementById('metric-cache-hit').textContent = data.cache_telemetry.hitRate || '100%';
        }

        const logsContainer = document.getElementById('admin-logs-container');
        if (data.recent_logs && data.recent_logs.length) {
          logsContainer.innerHTML = data.recent_logs.map(l => `
            <div class="border-b border-slate-800/60 pb-1.5 mb-1.5 flex items-start justify-between">
              <div>
                <span class="text-amber-400 font-bold">[${l.event_type}]</span>
                <span class="text-slate-200 ml-1.5">${l.message}</span>
              </div>
              <span class="text-slate-500 text-[10px] whitespace-nowrap ml-4">${l.created_at}</span>
            </div>
          `).join('');
        }
      } catch (err) {
        console.error('Error fetching admin metrics:', err);
      }
    }

    async function fetchDeliverabilityStats() {
      try {
        const res = await fetch('/api/admin/deliverability-stats');
        const data = await res.json();
        const usage = data.usage;
        document.getElementById('deliv-quota-text').textContent = `${usage.sent_today} / ${usage.daily_limit} Daily Quota Used (${usage.remaining} Remaining)`;
        const pct = Math.min(100, Math.round((usage.sent_today / usage.daily_limit) * 100));
        document.getElementById('deliv-progress-bar').style.width = pct + '%';
      } catch (err) {
        console.error('Error fetching deliverability stats:', err);
      }
    }

    async function fetchAnomalies() {
      try {
        const res = await fetch('/api/admin/anomalies');
        const anomalies = await res.json();
        const container = document.getElementById('anomaly-container');
        const pending = anomalies.filter(a => a.status === 'PENDING_REVIEW');
        document.getElementById('anomaly-badge').textContent = `${pending.length} Pending`;

        if (!anomalies.length) {
          container.innerHTML = '<div class="text-xs text-slate-500 bg-slate-950 p-3 rounded-xl border border-slate-800">No anomalies detected. Circuit breaker healthy.</div>';
          return;
        }

        container.innerHTML = anomalies.map(a => `
          <div class="bg-slate-950 border ${a.status === 'PENDING_REVIEW' ? 'border-rose-500/40 bg-rose-500/5' : 'border-slate-800'} p-3 rounded-xl flex items-center justify-between text-xs">
            <div>
              <div class="flex items-center gap-2">
                <span class="font-bold text-white">${a.vendor_name}</span>
                <span class="bg-rose-500/20 text-rose-400 px-1.5 py-0.5 rounded text-[10px] font-bold font-mono">+${a.percentage_delta.toFixed(1)}% Spike</span>
                <span class="text-slate-400 text-[10px] font-mono">($${a.previous_value.toLocaleString()} -> $${a.incoming_value.toLocaleString()})</span>
              </div>
              <div class="text-[10px] text-slate-500 mt-1">Status: ${a.status} &bull; ${a.detected_at}</div>
            </div>

            ${a.status === 'PENDING_REVIEW' ? `
              <div class="flex items-center gap-2">
                <button onclick="resolveAnomaly('${a.id}', 'APPROVED')" class="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold px-2.5 py-1 rounded-lg text-[10px]">Approve</button>
                <button onclick="resolveAnomaly('${a.id}', 'REJECTED')" class="bg-slate-800 hover:bg-slate-700 text-rose-400 font-bold px-2.5 py-1 rounded-lg text-[10px] border border-slate-700">Reject</button>
              </div>
            ` : `
              <span class="text-[10px] font-mono text-slate-400">${a.resolution_action || a.status}</span>
            `}
          </div>
        `).join('');
      } catch (err) {
        console.error('Error fetching anomalies:', err);
      }
    }

    async function resolveAnomaly(anomalyId, action) {
      try {
        const res = await fetch('/api/admin/resolve-anomaly', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ anomaly_id: anomalyId, action })
        });
        await fetchAnomalies();
        await fetchAdminMetrics();
      } catch (err) {
        alert('Resolution failed: ' + err.message);
      }
    }

    async function runAutonomousCron() {
      const btn = document.getElementById('cron-trigger-btn');
      btn.disabled = true;
      btn.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>Executing Cycle...</span>';
      lucide.createIcons();

      try {
        const res = await fetch('/api/admin/run-cron', { method: 'POST' });
        const data = await res.json();
        await fetchAdminMetrics();
        await fetchAnomalies();
        await fetchDeliverabilityStats();
        alert(`Autonomous Broker Cycle Executed!\nBanked Revenue: $${data.telemetry.total_revenue_banked.toLocaleString()}\nMRR: $${data.telemetry.active_mrr}/mo`);
      } catch (err) {
        alert('Cron execution failed: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i data-lucide="play" class="w-4 h-4"></i><span>Trigger 24h Cadence Cycle</span>';
        lucide.createIcons();
      }
    }

    document.addEventListener('DOMContentLoaded', () => {
      loadVendors();
      lucide.createIcons();
    });
  </script>
</body>
</html>
"""

with open(target, "a", encoding="utf-8") as f:
    f.write(part4)
print("Part 4 written. apps/web/public/index.html is complete!")
