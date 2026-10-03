    let activeNiche = 'all';
    let currentVendors = [];

    const NICHE_METADATA = {
      luxury_restrooms: {
        badge: 'Verified VIP Luxury Sanitation Fleets',
        title: 'Rent High-End Restroom Trailers for <span class="gold-text italic">Weddings &amp; VIP Galas</span>',
        desc: 'Don\'t risk your event\'s reputation. Browse our exclusive network of rigorously vetted luxury restroom operators guaranteeing pristine hygiene, climate control, and flawless execution.',
        heading: 'Trusted Sanitation Partners',
        sub: 'Verified VIP Network'
      },
      commercial_cold_storage: {
        badge: 'Emergency Mobile Cold Storage Network',
        title: 'Rent Commercial Mobile Freezers &amp; <span class="gold-text italic">Refrigeration Pods</span>',
        desc: 'When inventory is on the line, seconds matter. Connect instantly with verified emergency cold storage operators providing rapid deployment of deep-freeze (-20°F) reefers.',
        heading: 'Reliable Cold Storage Operators',
        sub: 'Verified 24/7 Deployment Network'
      },
      heavy_crane_rigging: {
        badge: 'Certified Mobile Crane &amp; Industrial Rigging Fleet',
        title: 'Hire Heavy Mobile Cranes &amp; <span class="gold-text italic">Certified Rigging Crews</span>',
        desc: 'Safety and compliance are non-negotiable. Access our elite network of NCCCO-certified crane operators delivering absolute precision for critical HVAC and structural lifts.',
        heading: 'Vetted Hoisting Contractors',
        sub: 'Verified Industrial Safety Network'
      },
      senior_care_placement: {
        badge: 'Verified Assisted Living &amp; Memory Care Advisors',
        title: 'Find Premium 65+ Care Facilities &amp; <span class="gold-text italic">Placement Services</span>',
        desc: 'Making care decisions for a loved one is overwhelming. Let our compassionate, heavily-vetted local advisors guide you to the safest, highest-rated communities with total transparency.',
        heading: 'Trusted Senior Care Advisors',
        sub: 'Verified 65+ Compassion Network'
      },
      aging_in_place: {
        badge: 'Certified Aging-in-Place Specialists (CAPS) &amp; Accessibility',
        title: 'Modify Homes for 65+ Independence &amp; <span class="gold-text italic">Staying in Place Safely</span>',
        desc: 'Over 88% of seniors choose to remain at home. Connect with rigorously vetted, CAPS-certified remodeling specialists for barrier-free roll-in showers, stairlifts, walk-in tubs, wheelchair ramps, and certified home safety audits.',
        heading: 'Verified Aging-in-Place Specialists',
        sub: 'Certified 65+ Home Independence Network',
        aliases: ['aging_in_place', 'staying_in_place']
      },
      temporary_power: {
        badge: 'Verified Industrial Temporary Power &amp; Mobile Generators',
        title: 'Rent High-Capacity Mobile Generators &amp; <span class="gold-text italic">Emergency Power Fleets</span>',
        desc: 'Zero downtime guaranteed. Connect directly with pre-audited industrial temporary power operators providing Tier 4 Final diesel and gas mobile generators (250 kW – 2MW), high-voltage switchgear, and emergency 24/7 refueling.',
        heading: 'Verified Power Generation Fleets',
        sub: 'Industrial Temporary Power Network',
        aliases: ['temporary_power', 'power', 'generators']
      },
      machinery_moving: {
        badge: 'Certified Heavy Machinery Moving &amp; Millwright Rigging Fleets',
        title: 'Contract Precision Millwright Rigging &amp; <span class="gold-text italic">Heavy Machine Relocation</span>',
        desc: 'Millwright precision for critical factory assets. Access SC&amp;RA-certified industrial machinery movers equipped with Versa-Lift mobile cranes, 500-ton hydraulic gantries, and air-skate cleanroom equipment.',
        heading: 'Verified Millwright &amp; Rigging Contractors',
        sub: 'Heavy Industrial Machinery Relocation Network',
        aliases: ['machinery_moving', 'rigging', 'millwright']
      },
      senior_downsizing: {
        badge: 'Certified Senior Relocation &amp; Estate Transition Specialists',
        title: 'Turnkey Estate Downsizing &amp; <span class="gold-text italic">Senior Transition Management</span>',
        desc: 'Compassionate, full-service transitions for older adults. NASMM-accredited specialists managing whole-home decluttering, cataloged online estate liquidation auctions (65-75% net return), packing, and turnkey relocation.',
        heading: 'Verified Senior Downsizing Specialists',
        sub: 'Accredited Senior Transition Network',
        aliases: ['senior_downsizing', 'estate_downsizing', 'downsizing']
      },
      wheelchair_vans: {
        badge: 'Certified Wheelchair Accessible Vehicles (WAV) &amp; Mobility Fleets',
        title: 'Rent &amp; Purchase Wheelchair Accessible Vans &amp; <span class="gold-text italic">Mobility Fleets</span>',
        desc: 'Freedom of movement with institutional safety standards. Connect with NMEDA QAP-certified dealers offering side- and rear-entry wheelchair accessible minivans, commercial ADA shuttles, and short- or long-term rentals.',
        heading: 'Verified WAV &amp; Mobility Fleet Dealers',
        sub: 'Certified Mobility Vehicle Network',
        aliases: ['wheelchair_vans', 'wav', 'mobility_vans']
      }
    };

    // Support aliases in NICHE_METADATA
    NICHE_METADATA.cold_storage = NICHE_METADATA.commercial_cold_storage;
    NICHE_METADATA.crane_rigging = NICHE_METADATA.heavy_crane_rigging;
    NICHE_METADATA.senior_care = NICHE_METADATA.senior_care_placement;
    NICHE_METADATA.staying_in_place = NICHE_METADATA.aging_in_place;
    NICHE_METADATA.power = NICHE_METADATA.temporary_power;
    NICHE_METADATA.generators = NICHE_METADATA.temporary_power;
    NICHE_METADATA.rigging = NICHE_METADATA.machinery_moving;
    NICHE_METADATA.downsizing = NICHE_METADATA.senior_downsizing;
    NICHE_METADATA.wav = NICHE_METADATA.wheelchair_vans;
    NICHE_METADATA.mobility = NICHE_METADATA.wheelchair_vans;

    function switchNiche(nicheId) {
      activeNiche = nicheId || 'all';
      const allNiches = [
        'all', 'luxury_restrooms', 'commercial_cold_storage', 'heavy_crane_rigging', 
        'temporary_power', 'machinery_moving', 'aging_in_place', 'senior_care_placement', 
        'senior_downsizing', 'wheelchair_vans', 'cold_storage', 'crane_rigging', 
        'senior_care', 'staying_in_place', 'power', 'rigging', 'downsizing', 'wav'
      ];
      allNiches.forEach(k => {
        const tab = document.getElementById(`niche-tab-${k}`);
        if (tab) {
          if (k === activeNiche) {
            tab.className = 'px-3.5 py-2 rounded-xl text-xs font-bold transition-all bg-amber-500 text-slate-950 shadow-sm whitespace-nowrap flex items-center gap-1.5';
          } else {
            tab.className = 'px-3.5 py-2 rounded-xl text-xs font-bold transition-all bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 whitespace-nowrap flex items-center gap-1.5';
          }
        }
      });

      const heroSelect = document.getElementById('hero-niche-select');
      if (heroSelect && heroSelect.value !== activeNiche) {
        heroSelect.value = activeNiche;
      }

      const meta = NICHE_METADATA[activeNiche];
      if (meta) {
        const badgeEl = document.getElementById('hero-badge-text');
        if (badgeEl) badgeEl.innerHTML = meta.badge;
        const titleEl = document.getElementById('hero-title');
        if (titleEl) titleEl.innerHTML = meta.title;
        const descEl = document.getElementById('hero-desc');
        if (descEl) descEl.textContent = meta.desc;
        const headEl = document.getElementById('directory-heading');
        if (headEl) headEl.textContent = meta.heading;
        const subEl = document.getElementById('directory-sub');
        if (subEl) subEl.textContent = meta.sub;
        const qNiche = document.getElementById('q-niche');
        if (qNiche) qNiche.value = activeNiche;
      } else {
        const badgeEl = document.getElementById('hero-badge-text');
        if (badgeEl) badgeEl.textContent = 'Nationwide Independent Verification • $2M+ Liability Insurance Audited';
        const titleEl = document.getElementById('hero-title');
        if (titleEl) titleEl.innerHTML = 'Find &amp; Hire Vetted Specialty Contractors &amp; <span class="gold-text italic">High-Capacity Equipment</span>';
        const descEl = document.getElementById('hero-desc');
        if (descEl) descEl.textContent = 'Connect directly with independently audited specialists across 9 core verticals — from commercial mobile generators and precision millwright rigging to certified 65+ aging-in-place remodeling and wheelchair mobility fleets. Zero broker markups, upfront pricing.';
        const headEl = document.getElementById('directory-heading');
        if (headEl) headEl.textContent = 'All Verified Specialty Contractors';
        const subEl = document.getElementById('directory-sub');
        if (subEl) subEl.textContent = 'Nationwide Verified Directory & Equipment Network';
        const qNiche = document.getElementById('q-niche');
        if (qNiche) qNiche.value = 'all';
      }

      loadVendors();
      if (typeof filterDepotMap === 'function') {
        filterDepotMap(activeNiche);
      }
    }

    function onHeroNicheChange(niche) {
      switchNiche(niche);
    }

    function selectNicheCard(niche) {
      switchNiche(niche);
      const dir = document.getElementById('directory');
      if (dir) {
        dir.scrollIntoView({ behavior: 'smooth' });
      }
    }

    function scrollToDirectoryAndSearch() {
      loadVendors();
      const dir = document.getElementById('directory');
      if (dir) {
        dir.scrollIntoView({ behavior: 'smooth' });
      }
    }

    function switchToolTab(tab) {
      const panes = {
        restrooms: document.getElementById('tool-pane-restrooms'),
        staying: document.getElementById('tool-pane-staying'),
        financing: document.getElementById('tool-pane-financing')
      };
      const buttons = {
        restrooms: document.getElementById('tab-btn-restrooms'),
        staying: document.getElementById('tab-btn-staying'),
        financing: document.getElementById('tab-btn-financing')
      };

      Object.keys(panes).forEach(k => {
        if (panes[k]) {
          if (k === tab) panes[k].classList.remove('hidden');
          else panes[k].classList.add('hidden');
        }
        if (buttons[k]) {
          if (k === tab) {
            buttons[k].className = 'px-4 py-2 rounded-xl text-xs font-bold transition-all bg-amber-500 text-slate-950 shadow-sm border border-amber-400 flex items-center gap-1.5';
          } else {
            buttons[k].className = 'px-4 py-2 rounded-xl text-xs font-bold transition-all text-slate-600 hover:text-slate-900 bg-white border border-slate-200 flex items-center gap-1.5';
          }
        }
      });
      try { lucide.createIcons(); } catch(e){}
    }

    function updateAgingInPlaceCalculator() {
      const items = [
        { id: 'aip-shower', min: 8500, max: 14000 },
        { id: 'aip-stairlift', min: 3200, max: 5500 },
        { id: 'aip-ramp', min: 2800, max: 6500 },
        { id: 'aip-tub', min: 7000, max: 12500 },
        { id: 'aip-grabbars', min: 650, max: 1800 },
        { id: 'aip-doors', min: 1200, max: 3000 }
      ];

      let totalMin = 0;
      let totalMax = 0;
      let count = 0;

      items.forEach(item => {
        const el = document.getElementById(item.id);
        if (el && el.checked) {
          totalMin += item.min;
          totalMax += item.max;
          count++;
        }
      });

      const countEl = document.getElementById('aip-items-count');
      if (countEl) {
        countEl.textContent = `${count} Modification${count === 1 ? '' : 's'} Selected`;
      }

      const totalEl = document.getElementById('aip-total-display');
      if (totalEl) {
        totalEl.textContent = count === 0 ? '$0' : `$${totalMin.toLocaleString()} – $${totalMax.toLocaleString()}`;
      }
    }

    function applyAgingCalculatorToQuote() {
      const items = [
        { id: 'aip-shower', name: 'Roll-In Shower' },
        { id: 'aip-stairlift', name: 'Motorized Stairlift' },
        { id: 'aip-ramp', name: 'Modular Wheelchair Ramp' },
        { id: 'aip-tub', name: 'Walk-In Safety Tub' },
        { id: 'aip-grabbars', name: 'ADA Grab Bars' },
        { id: 'aip-doors', name: 'Doorway Widening' }
      ];
      const selected = items.filter(it => document.getElementById(it.id)?.checked).map(it => it.name);
      const totalDisplay = document.getElementById('aip-total-display')?.textContent || '$8,500 – $14,000';

      openQuoteModal();
      const nicheSelect = document.getElementById('q-niche');
      if (nicheSelect) nicheSelect.value = 'aging_in_place';

      const notesEl = document.getElementById('q-notes');
      if (notesEl) {
        notesEl.value = `65+ Home Accessibility Quote Request: ${selected.join(', ')}. Estimated Project Budget: ${totalDisplay}.`;
      }
    }

    let proximityActive = false;
    let proximityZip = '';

    async function searchByProximity() {
      const input = document.getElementById('proximity-input')?.value?.trim();
      const radius = document.getElementById('proximity-radius')?.value || 50;
      if (!input) {
        alert('Please enter a Zip Code or City to search.');
        return;
      }
      proximityActive = true;
      proximityZip = input;
      const clearBtn = document.getElementById('clear-proximity-btn');
      if (clearBtn) clearBtn.classList.remove('hidden');
      loadVendors();
    }

    function clearProximitySearch() {
      proximityActive = false;
      proximityZip = '';
      const pInput = document.getElementById('proximity-input');
      if (pInput) pInput.value = '';
      const clearBtn = document.getElementById('clear-proximity-btn');
      if (clearBtn) clearBtn.classList.add('hidden');
      loadVendors();
    }

    async function loadVendors() {
      const city = document.getElementById('filter-city')?.value || 'All';
      const amenity = document.getElementById('filter-amenity')?.value || '';
      const search = document.getElementById('search-input')?.value || '';

      const grid = document.getElementById('vendors-grid');
      if (!grid) return;

      grid.innerHTML = '<div class="col-span-full py-16 text-center text-slate-400"><i data-lucide="loader-2" class="w-8 h-8 animate-spin mx-auto text-amber-500 mb-2"></i><span>Loading verified operators...</span></div>';
      try { lucide.createIcons(); } catch(e){}

      try {
        let url = proximityActive
          ? `/api/vendors/proximity?zip=${encodeURIComponent(proximityZip)}&radius=${document.getElementById('proximity-radius')?.value || 50}&niche_id=${encodeURIComponent(activeNiche)}`
          : `/api/vendors?niche_id=${encodeURIComponent(activeNiche)}&city=${encodeURIComponent(city)}&amenity=${encodeURIComponent(amenity)}&search=${encodeURIComponent(search)}`;

        const res = await fetch(url);
        const vendors = await res.json();
        currentVendors = Array.isArray(vendors) ? vendors : [];

        const badge = document.getElementById('vendor-count-badge');
        if (badge) {
          badge.textContent = `${currentVendors.length} Listings${proximityActive ? ' (Near You)' : ''}`;
        }

        if (!currentVendors.length) {
          grid.innerHTML = '<div class="col-span-full py-16 text-center text-slate-500 bg-white border border-slate-200 rounded-2xl p-8"><div class="text-3xl mb-2">🔍</div><div class="font-bold text-slate-800 text-sm">No verified operators found matching your criteria.</div><div class="text-xs text-slate-500 mt-1">Try selecting "All Specialties", clearing your keyword search, or choosing a different metro.</div><button onclick="switchNiche(\'all\')" class="mt-4 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold px-4 py-2 rounded-xl text-xs transition-colors">Show All Verified Operators</button></div>';
          return;
        }

        const sortMode = document.getElementById('sort-select')?.value || 'featured';
        if (sortMode === 'rating') {
          currentVendors.sort((a, b) => b.rating - a.rating);
        } else if (sortMode === 'price_asc') {
          currentVendors.sort((a, b) => a.min_price - b.min_price);
        } else if (sortMode === 'price_desc') {
          currentVendors.sort((a, b) => b.max_price - a.max_price);
        } else {
          currentVendors.sort((a, b) => (b.subscription_active || 0) - (a.subscription_active || 0));
        }

        visibleVendorCount = 12;
        renderVendorCards(currentVendors.slice(0, visibleVendorCount));
      } catch (err) {
        grid.innerHTML = `<div class="col-span-full py-16 text-center text-rose-600 bg-rose-50 border border-rose-200 rounded-2xl p-6">Error loading directory: ${err.message}</div>`;
      }
    }

    let visibleVendorCount = 12;

    function renderVendorCards(vendorsToRender, append = false) {
      const grid = document.getElementById('vendors-grid');
      if (!grid) return;

      const html = vendorsToRender.map(v => {
        const fleetList = Array.isArray(v.fleet_types) ? v.fleet_types : (typeof v.fleet_types === 'string' ? JSON.parse(v.fleet_types || '[]') : []);
        const amenityList = Array.isArray(v.amenities) ? v.amenities : (typeof v.amenities === 'string' ? JSON.parse(v.amenities || '[]') : []);

        return `
        <div class="bg-white border ${v.subscription_active ? 'border-amber-400 shadow-lg shadow-amber-500/10' : 'border-slate-200'} rounded-2xl overflow-hidden flex flex-col justify-between hover:border-amber-500 hover:shadow-xl transition-all duration-300">
          <div>
            <div class="relative h-48 overflow-hidden bg-slate-100">
              <img loading="lazy" src="${v.image_url}" alt="${v.name}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" onerror="this.src='https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80'">
              <div class="absolute top-3 left-3 flex gap-1.5 flex-wrap">
                ${v.subscription_active ? '<span class="bg-amber-500 text-slate-950 font-extrabold text-[10px] px-2.5 py-0.5 rounded-full flex items-center gap-1 shadow-md"><i data-lucide="star" class="w-3 h-3 fill-slate-950"></i> Featured Partner</span>' : ''}
                <span class="bg-white/95 backdrop-blur text-amber-700 border border-amber-300 font-bold text-[10px] px-2.5 py-0.5 rounded-full flex items-center gap-1 shadow-xs">
                  <i data-lucide="check-circle-2" class="w-3 h-3 text-amber-600"></i> Verified
                </span>
              </div>
              <div class="absolute bottom-3 right-3 bg-white/95 text-slate-900 font-bold text-xs px-2.5 py-1 rounded-lg border border-slate-200 shadow-xs font-mono">
                $${(v.min_price || 0).toLocaleString()} - $${(v.max_price || 0).toLocaleString()}
              </div>
            </div>

            <div class="p-5">
              <div class="flex items-center justify-between">
                <span class="text-[11px] font-bold text-amber-700 uppercase tracking-wider">
                  ${v.distance_miles !== undefined ? `📍 ${v.distance_miles} mi • ` : ''}${v.city}, ${v.state}
                </span>
                <div onclick="openReviewModal('${v.id}', '${(v.name || '').replace(/'/g, "\\'")}')" class="flex items-center gap-1 text-xs font-bold text-amber-600 cursor-pointer hover:underline" title="Click to Read &amp; Leave Verified Review">
                  <i data-lucide="star" class="w-3.5 h-3.5 fill-amber-500 text-amber-500"></i>
                  <span class="text-slate-800">${v.rating || 5} (${v.review_count || 30} reviews)</span>
                </div>
              </div>

              <h3 class="text-lg font-bold text-slate-900 mt-1 leading-snug">
                <a href="/listing/${v.slug || ''}" class="hover:text-amber-600 transition-colors">${v.name}</a>
              </h3>
              <p class="text-xs text-slate-600 mt-2 line-clamp-2">${v.description || ''}</p>

              ${fleetList.length ? `
                <div class="mt-3 flex flex-wrap gap-1">
                  ${fleetList.slice(0, 2).map(f => `<span class="bg-amber-50 text-amber-900 border border-amber-200 text-[10px] font-semibold px-2 py-0.5 rounded-md flex items-center gap-1"><i data-lucide="check" class="w-2.5 h-2.5"></i>${f.split('(')[0].trim()}</span>`).join('')}
                  ${fleetList.length > 2 ? `<span class="text-[10px] text-amber-700 font-bold px-1 py-0.5">+${fleetList.length - 2} more</span>` : ''}
                </div>
              ` : ''}

              <div class="mt-3 flex flex-wrap gap-1.5">
                ${amenityList.slice(0, 3).map(a => `<span class="bg-slate-100 text-slate-700 text-[10px] px-2 py-0.5 rounded-md border border-slate-200">${a}</span>`).join('')}
                ${amenityList.length > 3 ? `<span class="text-[10px] text-slate-500 font-semibold px-1 py-0.5">+${amenityList.length - 3} more</span>` : ''}
              </div>

              <div class="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between">
                <a href="/listing/${v.slug || ''}" class="text-[11px] font-bold text-amber-700 hover:text-amber-800 flex items-center gap-1">
                  <span>View Verified Profile</span> &rarr;
                </a>
                <span class="text-emerald-700 font-semibold text-[11px] flex items-center gap-1">
                  <i data-lucide="shield-check" class="w-3 h-3"></i> $2M+ Insured
                </span>
              </div>
            </div>
          </div>

          <div class="p-5 pt-0 border-t border-slate-100 bg-slate-50/40 mt-4 flex items-center justify-between gap-1.5 flex-wrap sm:flex-nowrap">
            <button onclick="openQuoteModal('${v.city}')" class="flex-1 bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-bold py-2 rounded-xl flex items-center justify-center gap-1 transition-colors shadow-xs">
              <i data-lucide="calculator" class="w-3.5 h-3.5"></i>
              <span>Request Quote</span>
            </button>

            <button onclick="openMessageModal('${v.id}', '${(v.name || '').replace(/'/g, "\\'")}')" class="bg-white hover:bg-slate-100 text-slate-800 text-[11px] font-semibold px-2.5 py-2 rounded-xl border border-slate-200 shadow-xs transition-colors flex items-center gap-1" title="Direct Message Operator">
              <i data-lucide="message-square" class="w-3 h-3 text-amber-600"></i>
              <span>Message</span>
            </button>

            <button onclick="openClaimModal('${v.id}', '${(v.name || '').replace(/'/g, "\\'")}')" aria-label="Claim Profile" class="bg-white hover:bg-slate-100 text-slate-700 text-[11px] font-semibold px-2 py-2 rounded-xl border border-slate-200 shadow-xs transition-colors" title="Claim Profile">
              <i data-lucide="key" class="w-3.5 h-3.5 text-amber-600"></i>
            </button>

            <button onclick="openBadgeModal('${v.id}')" aria-label="Get Embeddable Verified Badge" class="bg-white hover:bg-slate-100 text-amber-700 text-[11px] font-semibold px-2 py-2 rounded-xl border border-slate-200 shadow-xs transition-colors" title="Get Embeddable Verified Badge">
              <i data-lucide="badge-check" class="w-3.5 h-3.5 text-amber-600"></i>
            </button>
          </div>
        </div>
        `;
      }).join('');

      const existingBtn = document.getElementById('load-more-vendors-container');
      if (existingBtn) existingBtn.remove();

      if (append) {
        grid.insertAdjacentHTML('beforeend', html);
      } else {
        grid.innerHTML = html;
      }

      if (currentVendors.length > visibleVendorCount) {
        const remaining = currentVendors.length - visibleVendorCount;
        const loadMoreHtml = `
          <div id="load-more-vendors-container" class="col-span-full text-center py-8">
            <button onclick="loadMoreVendors()" class="bg-slate-900 hover:bg-amber-600 text-white hover:text-slate-950 font-bold px-8 py-3.5 rounded-xl text-sm transition-all shadow-md inline-flex items-center gap-2 cursor-pointer">
              <span>View More Verified Fleets (+${remaining} Available)</span>
              <i data-lucide="chevron-down" class="w-4 h-4"></i>
            </button>
          </div>
        `;
        grid.insertAdjacentHTML('afterend', loadMoreHtml);
      }

      try { if (window.lucide) lucide.createIcons(); } catch(e){}
    }

    function loadMoreVendors() {
      const nextBatch = currentVendors.slice(visibleVendorCount, visibleVendorCount + 12);
      visibleVendorCount += 12;
      renderVendorCards(nextBatch, true);
    }

    // --- 🗺️ NATIONWIDE SERVICE COVERAGE & DISPATCH DEPOT MAP ---
    let depotMap = null;
    let depotMarkersLayer = null;
    let allDepotsData = [];
    let activeRadiusCircle = null;
    let userLocationMarker = null;
    let activeMapTheme = 'voyager';
    let mapBaseLayers = {};

    const DEPOT_NICHE_CONFIG = {
      'all': { label: 'All Specialties', color: '#d97706', badgeBg: '#fffbeb', badgeText: '#92400e' },
      'aging_in_place': { label: 'Aging-in-Place', color: '#059669', badgeBg: '#ecfdf5', badgeText: '#065f46' },
      'staying_in_place': { label: 'Aging-in-Place', color: '#059669', badgeBg: '#ecfdf5', badgeText: '#065f46' },
      'luxury_restrooms': { label: 'VIP Restrooms', color: '#d97706', badgeBg: '#fffbeb', badgeText: '#92400e' },
      'cold_storage': { label: 'Cold Storage', color: '#0284c7', badgeBg: '#f0f9ff', badgeText: '#075985' },
      'commercial_cold_storage': { label: 'Cold Storage', color: '#0284c7', badgeBg: '#f0f9ff', badgeText: '#075985' },
      'crane_rigging': { label: 'Mobile Cranes', color: '#ea580c', badgeBg: '#fff7ed', badgeText: '#9a3412' },
      'heavy_crane_rigging': { label: 'Mobile Cranes', color: '#ea580c', badgeBg: '#fff7ed', badgeText: '#9a3412' },
      'temporary_power': { label: 'Temporary Power', color: '#eab308', badgeBg: '#fefce8', badgeText: '#854d0e' },
      'power': { label: 'Temporary Power', color: '#eab308', badgeBg: '#fefce8', badgeText: '#854d0e' },
      'machinery_moving': { label: 'Machinery Moving', color: '#ea580c', badgeBg: '#fff7ed', badgeText: '#9a3412' },
      'rigging': { label: 'Machinery Moving', color: '#ea580c', badgeBg: '#fff7ed', badgeText: '#9a3412' },
      'senior_care': { label: 'Senior Placement', color: '#7c3aed', badgeBg: '#f5f3ff', badgeText: '#5b21b6' },
      'senior_care_placement': { label: 'Senior Placement', color: '#7c3aed', badgeBg: '#f5f3ff', badgeText: '#5b21b6' },
      'senior_downsizing': { label: 'Senior Downsizing', color: '#0d9488', badgeBg: '#f0fdfa', badgeText: '#115e59' },
      'wheelchair_vans': { label: 'Wheelchair Vans', color: '#6366f1', badgeBg: '#eef2ff', badgeText: '#3730a3' },
      'wav': { label: 'Wheelchair Vans', color: '#6366f1', badgeBg: '#eef2ff', badgeText: '#3730a3' }
    };

    const METRO_COORDINATES = {
      'atlanta-ga': { name: 'Atlanta, GA', lat: 33.7490, lng: -84.3880 },
      'new-york-ny': { name: 'New York, NY', lat: 40.7128, lng: -74.0060 },
      'los-angeles-ca': { name: 'Los Angeles, CA', lat: 34.0522, lng: -118.2437 },
      'chicago-il': { name: 'Chicago, IL', lat: 41.8781, lng: -87.6298 },
      'dallas-tx': { name: 'Dallas-Fort Worth, TX', lat: 32.7767, lng: -96.7970 },
      'miami-fl': { name: 'Miami, FL', lat: 25.7617, lng: -80.1918 },
      'phoenix-az': { name: 'Phoenix, AZ', lat: 33.4484, lng: -112.0740 },
      'seattle-wa': { name: 'Seattle, WA', lat: 47.6062, lng: -122.3321 },
      'denver-co': { name: 'Denver, CO', lat: 39.7392, lng: -104.9903 },
      'boston-ma': { name: 'Boston, MA', lat: 42.3601, lng: -71.0589 },
      'houston-tx': { name: 'Houston, TX', lat: 29.7604, lng: -95.3698 },
      'philadelphia-pa': { name: 'Philadelphia, PA', lat: 39.9526, lng: -75.1652 },
      'nashville-tn': { name: 'Nashville, TN', lat: 36.1627, lng: -86.7816 },
      'las-vegas-nv': { name: 'Las Vegas, NV', lat: 36.1699, lng: -115.1398 },
      'detroit-mi': { name: 'Detroit, MI', lat: 42.3314, lng: -83.0458 },
      'minneapolis-mn': { name: 'Minneapolis, MN', lat: 44.9778, lng: -93.2650 },
      'san-francisco-ca': { name: 'San Francisco, CA', lat: 37.7749, lng: -122.4194 }
    };

    function createDepotPin(nicheId) {
      const config = DEPOT_NICHE_CONFIG[nicheId] || { color: '#d97706' };
      return L.divIcon({
        className: 'custom-depot-map-pin',
        html: `<div style="position:relative; width:34px; height:34px; display:flex; align-items:center; justify-content:center; cursor:pointer;">
                 <div style="position:absolute; inset:-4px; border-radius:50%; background:${config.color}35; animation:pulse 2s cubic-bezier(0.4,0,0.6,1) infinite;"></div>
                 <div style="position:relative; width:26px; height:26px; background:${config.color}; border:2.5px solid #ffffff; border-radius:50%; display:flex; align-items:center; justify-content:center; box-shadow:0 4px 10px rgba(0,0,0,0.35);">
                   <svg style="width:13px; height:13px; color:#ffffff;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                 </div>
               </div>`,
        iconSize: [34, 34],
        iconAnchor: [17, 17],
        popupAnchor: [0, -18]
      });
    }

    function createDepotPopupHtml(v) {
      const config = DEPOT_NICHE_CONFIG[v.niche_id] || { label: 'Verified Specialty', color: '#d97706', badgeBg: '#fffbeb', badgeText: '#92400e' };
      const safeName = (v.name || 'Commercial Operator').replace(/"/g, '&quot;');
      const cleanPhone = (v.phone || '').replace(/[^0-9]/g, '');
      const priceText = (v.min_price && v.max_price) ? `$${v.min_price.toLocaleString()} – $${v.max_price.toLocaleString()}` : 'Direct Quote';

      return `
        <div style="font-family:'Plus Jakarta Sans',sans-serif; padding:4px; max-width:270px;">
          <div style="display:flex; align-items:center; justify-content:space-between; gap:4px; margin-bottom:5px;">
            <span style="font-size:10px; font-weight:800; background:${config.badgeBg}; color:${config.badgeText}; padding:2px 7px; border-radius:9999px; text-transform:uppercase; letter-spacing:0.3px;">${config.label}</span>
            <span style="font-size:11px; font-weight:700; color:#059669;">★ ${v.rating || 5.0} (${v.review_count || 32})</span>
          </div>
          <div style="font-size:14px; font-weight:800; color:#0f172a; line-height:1.25; margin-bottom:4px;">${safeName}</div>
          <div style="font-size:12px; color:#64748b; margin-bottom:6px;">📍 Staging Yard: <strong>${v.city}, ${v.state}</strong></div>
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:6px 8px; margin-bottom:8px; font-size:11px; color:#334155; line-height:1.3;">
            <div style="font-weight:700; color:#0f172a; display:flex; justify-content:space-between;"><span>75-Mile Primary Radius</span><span style="color:#d97706;">${priceText}</span></div>
            <div style="color:#64748b; font-size:10px; margin-top:2px;">Rapid on-time dispatch &bull; $2M+ Insured</div>
          </div>
          <div style="display:flex; items-center; justify-content:space-between; gap:6px; border-top:1px solid #e2e8f0; padding-top:8px;">
            <a href="tel:${cleanPhone}" style="flex:1; text-align:center; font-size:11px; font-weight:800; color:#0f172a; text-decoration:none; background:#f1f5f9; padding:6px 8px; border-radius:6px; border:1px solid #cbd5e1;">📞 Call Depot</a>
            <a href="/listing/${v.slug}.html" style="flex:1; text-align:center; font-size:11px; font-weight:800; color:#ffffff; text-decoration:none; background:#d97706; padding:6px 8px; border-radius:6px; box-shadow:0 1px 3px rgba(0,0,0,0.15);">View Fleet &rarr;</a>
          </div>
        </div>
      `;
    }

    function showDepotHud(v) {
      const hud = document.getElementById('depot-hud-card');
      if (!hud) return;

      const config = DEPOT_NICHE_CONFIG[v.niche_id] || { label: 'Verified Specialty', color: '#d97706', badgeBg: '#fffbeb', badgeText: '#92400e' };
      const cleanPhone = (v.phone || '').replace(/[^0-9]/g, '');
      const priceText = (v.min_price && v.max_price) ? `$${v.min_price.toLocaleString()} – $${v.max_price.toLocaleString()}` : '$1,850 – $7,200';

      const badgeEl = document.getElementById('hud-depot-badge');
      if (badgeEl) {
        badgeEl.textContent = config.label;
        badgeEl.style.backgroundColor = config.badgeBg;
        badgeEl.style.color = config.badgeText;
        badgeEl.style.borderColor = config.color + '44';
      }

      const nameEl = document.getElementById('hud-depot-name');
      if (nameEl) nameEl.textContent = v.name || 'Verified Fleet Operator';

      const locEl = document.getElementById('hud-depot-location');
      if (locEl) locEl.innerHTML = `📍 ${v.city}, ${v.state} &bull; <strong>75-Mile Primary Radius</strong>`;

      const priceEl = document.getElementById('hud-depot-price');
      if (priceEl) priceEl.textContent = priceText;

      const ratingEl = document.getElementById('hud-depot-rating');
      if (ratingEl) ratingEl.textContent = `★ ${v.rating || 5.0} (${v.review_count || 45} reviews)`;

      const phoneLink = document.getElementById('hud-depot-phone-link');
      if (phoneLink) {
        phoneLink.href = `tel:${cleanPhone}`;
        phoneLink.textContent = v.phone ? `📞 ${v.phone}` : '📞 Call Depot';
      }

      const detailLink = document.getElementById('hud-depot-detail-link');
      if (detailLink) detailLink.href = `/listing/${v.slug}.html`;

      hud.classList.remove('hidden');
    }

    function closeDepotHud() {
      const hud = document.getElementById('depot-hud-card');
      if (hud) hud.classList.add('hidden');
      if (activeRadiusCircle && depotMap) {
        depotMap.removeLayer(activeRadiusCircle);
        activeRadiusCircle = null;
      }
    }

    function loadLeafletDependencies(callback) {
      if (typeof L !== 'undefined' && typeof L.markerClusterGroup !== 'undefined') {
        return callback();
      }
      if (window._loadingLeaflet) {
        const checkInterval = setInterval(() => {
          if (typeof L !== 'undefined' && typeof L.markerClusterGroup !== 'undefined') {
            clearInterval(checkInterval);
            callback();
          }
        }, 80);
        return;
      }
      window._loadingLeaflet = true;

      const link1 = document.createElement('link');
      link1.rel = 'stylesheet';
      link1.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
      document.head.appendChild(link1);

      const link2 = document.createElement('link');
      link2.rel = 'stylesheet';
      link2.href = 'https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css';
      document.head.appendChild(link2);

      const link3 = document.createElement('link');
      link3.rel = 'stylesheet';
      link3.href = 'https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css';
      document.head.appendChild(link3);

      const s1 = document.createElement('script');
      s1.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
      s1.onload = () => {
        const s2 = document.createElement('script');
        s2.src = 'https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js';
        s2.onload = () => {
          window._loadingLeaflet = false;
          callback();
        };
        document.body.appendChild(s2);
      };
      document.body.appendChild(s1);
    }

    async function initNationwideDepotMap() {
      const mapEl = document.getElementById('nationwide-depot-map');
      if (!mapEl) return;
      if (typeof L === 'undefined' || typeof L.markerClusterGroup === 'undefined') {
        loadLeafletDependencies(() => initNationwideDepotMap());
        return;
      }

      if (depotMap) {
        depotMap.invalidateSize();
        return;
      }

      // Initialize map with responsive center & zoom
      const isMobile = window.innerWidth < 768;
      depotMap = L.map('nationwide-depot-map', {
        scrollWheelZoom: false,
        zoomControl: true
      }).setView(isMobile ? [39.0, -96.0] : [38.5, -96.0], isMobile ? 3.5 : 4.2);

      // Setup Enterprise Esri ArcGIS Base Map Layers (Zero API Key, Zero Watermarks, High Performance Fastly CDN)
      mapBaseLayers = {
        voyager: L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
          maxZoom: 19,
          attribution: 'Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, METI, TomTom'
        }),
        positron: L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
          maxZoom: 16,
          attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ'
        }),
        dark: L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
          maxZoom: 16,
          attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ'
        })
      };

      mapBaseLayers.voyager.addTo(depotMap);
      activeMapTheme = 'voyager';

      // Setup Marker Cluster Group with Executive Gold Badging
      if (typeof L.markerClusterGroup !== 'undefined') {
        depotMarkersLayer = L.markerClusterGroup({
          showCoverageOnHover: false,
          maxClusterRadius: 40,
          spiderfyOnMaxZoom: true,
          iconCreateFunction: function(cluster) {
            const count = cluster.getChildCount();
            let size = count > 15 ? 40 : (count > 6 ? 34 : 28);
            return L.divIcon({
              html: `<div class="custom-cluster-badge" style="width:${size}px; height:${size}px;"><span>${count}</span></div>`,
              className: 'custom-cluster-wrapper',
              iconSize: [size, size]
            });
          }
        });
      } else {
        depotMarkersLayer = L.layerGroup();
      }

      depotMap.addLayer(depotMarkersLayer);

      try {
        const res = await fetch('/api/vendors?niche_id=all');
        const data = await res.json();
        allDepotsData = Array.isArray(data) ? data : [];
      } catch (e) {
        console.error('Error loading vendors for map:', e);
        if (typeof currentVendors !== 'undefined' && currentVendors.length) {
          allDepotsData = currentVendors;
        }
      }

      renderDepotMapMarkers('all');

      setTimeout(() => { if (depotMap) depotMap.invalidateSize(); }, 250);
      setTimeout(() => { if (depotMap) depotMap.invalidateSize(); }, 800);
      window.addEventListener('resize', () => { if (depotMap) depotMap.invalidateSize(); });
    }

    function switchMapBaseLayer(theme) {
      if (!depotMap || !mapBaseLayers[theme] || activeMapTheme === theme) return;

      if (mapBaseLayers[activeMapTheme]) {
        depotMap.removeLayer(mapBaseLayers[activeMapTheme]);
      }

      mapBaseLayers[theme].addTo(depotMap);
      activeMapTheme = theme;

      ['voyager', 'positron', 'dark'].forEach(t => {
        const btn = document.getElementById(`theme-btn-${t}`);
        if (btn) {
          if (t === theme) {
            btn.classList.add('bg-white', 'text-slate-900', 'shadow-2xs');
            btn.classList.remove('text-slate-600');
          } else {
            btn.classList.remove('bg-white', 'text-slate-900', 'shadow-2xs');
            btn.classList.add('text-slate-600');
          }
        }
      });
    }

    function renderDepotMapMarkers(filterNiche) {
      if (!depotMap || !depotMarkersLayer) return;

      depotMarkersLayer.clearLayers();
      if (activeRadiusCircle) {
        depotMap.removeLayer(activeRadiusCircle);
        activeRadiusCircle = null;
      }

      const filtered = (filterNiche === 'all')
        ? allDepotsData
        : allDepotsData.filter(v => {
            const aliases = (typeof NICHE_METADATA !== 'undefined' && NICHE_METADATA[filterNiche])
              ? (NICHE_METADATA[filterNiche].aliases || [filterNiche])
              : [filterNiche];
            return aliases.includes(v.niche_id);
          });

      filtered.forEach(v => {
        if (!v.latitude || !v.longitude) return;

        const pin = createDepotPin(v.niche_id);
        const marker = L.marker([v.latitude, v.longitude], { icon: pin });

        marker.bindPopup(createDepotPopupHtml(v));

        marker.on('click', () => {
          if (activeRadiusCircle) depotMap.removeLayer(activeRadiusCircle);
          const config = DEPOT_NICHE_CONFIG[v.niche_id] || { color: '#d97706' };

          activeRadiusCircle = L.circle([v.latitude, v.longitude], {
            color: config.color,
            weight: 2,
            dashArray: '4, 6',
            fillColor: config.color,
            fillOpacity: 0.16,
            radius: 120700 // 75 miles in meters
          }).addTo(depotMap);

          showDepotHud(v);
        });

        depotMarkersLayer.addLayer(marker);
      });

      const statusEl = document.getElementById('depot-map-status');
      if (statusEl) {
        const nicheTitle = (filterNiche === 'all') ? 'all 9 specialties' : (DEPOT_NICHE_CONFIG[filterNiche]?.label || filterNiche);
        statusEl.textContent = `Showing ${filtered.length} verified commercial staging depots (${nicheTitle})`;
      }
    }

    function filterDepotMap(nicheId) {
      document.querySelectorAll('.depot-filter-btn').forEach(btn => {
        btn.classList.remove('active', 'bg-slate-900', 'text-white');
        btn.classList.add('bg-slate-100', 'text-slate-700');
      });
      const targetBtn = document.getElementById(`depot-filter-${nicheId}`);
      if (targetBtn) {
        targetBtn.classList.remove('bg-slate-100', 'text-slate-700');
        targetBtn.classList.add('active', 'bg-slate-900', 'text-white');
      }

      renderDepotMapMarkers(nicheId);
    }

    function resetDepotMapView() {
      if (!depotMap) return;
      const isMobile = window.innerWidth < 768;
      depotMap.setView(isMobile ? [39.0, -96.0] : [38.5, -96.0], isMobile ? 3.5 : 4.2);
      closeDepotHud();
      filterDepotMap('all');

      const metroSelect = document.getElementById('map-metro-select');
      if (metroSelect) metroSelect.value = '';
    }

    function handleMetroSelectJump(metroSlug) {
      if (!metroSlug) {
        resetDepotMapView();
        return;
      }
      const coords = METRO_COORDINATES[metroSlug];
      if (coords) {
        jumpToMetro(coords.name.split(',')[0], coords.lat, coords.lng);
      }
    }

    function jumpToMetro(city, lat, lng) {
      if (depotMap && lat && lng) {
        depotMap.flyTo([lat, lng], 9.5, { duration: 1.4 });

        if (activeRadiusCircle) depotMap.removeLayer(activeRadiusCircle);
        activeRadiusCircle = L.circle([lat, lng], {
          color: '#d97706',
          weight: 2,
          dashArray: '4, 6',
          fillColor: '#f59e0b',
          fillOpacity: 0.16,
          radius: 120700
        }).addTo(depotMap);

        // Find nearest depot in this metro to show HUD
        const localDepot = allDepotsData.find(v => (v.city && v.city.toLowerCase() === city.toLowerCase()));
        if (localDepot) {
          setTimeout(() => showDepotHud(localDepot), 600);
        }

        const statusEl = document.getElementById('depot-map-status');
        if (statusEl) {
          statusEl.textContent = `Focused on Metro ${city} Staging Yard & 75-Mile Primary Service Zone`;
        }
      }

      const filterCity = document.getElementById('filter-city');
      if (filterCity) {
        for (let opt of filterCity.options) {
          if (opt.value.toLowerCase() === city.toLowerCase()) {
            filterCity.value = city;
            loadVendors();
            break;
          }
        }
      }
    }

    function locateUserDepot() {
      if (!navigator.geolocation) {
        alert('Geolocation is not supported by your browser.');
        return;
      }

      const statusEl = document.getElementById('depot-map-status');
      if (statusEl) statusEl.textContent = 'Locating your nearest verified staging depot...';

      navigator.geolocation.getCurrentPosition(
        pos => {
          const userLat = pos.coords.latitude;
          const userLng = pos.coords.longitude;

          // Find nearest depot by Haversine formula
          let nearest = null;
          let minDistance = Infinity;

          allDepotsData.forEach(v => {
            if (!v.latitude || !v.longitude) return;
            const R = 3958.8; // Radius of the Earth in miles
            const dLat = (v.latitude - userLat) * Math.PI / 180;
            const dLng = (v.longitude - userLng) * Math.PI / 180;
            const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                      Math.cos(userLat * Math.PI / 180) * Math.cos(v.latitude * Math.PI / 180) *
                      Math.sin(dLng / 2) * Math.sin(dLng / 2);
            const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
            const dist = R * c;

            if (dist < minDistance) {
              minDistance = dist;
              nearest = v;
            }
          });

          if (userLocationMarker && depotMap) depotMap.removeLayer(userLocationMarker);

          userLocationMarker = L.circleMarker([userLat, userLng], {
            radius: 8,
            fillColor: '#2563eb',
            color: '#ffffff',
            weight: 3,
            opacity: 1,
            fillOpacity: 0.9
          }).addTo(depotMap).bindPopup('<strong>📍 Your Location</strong>').openPopup();

          if (nearest) {
            depotMap.flyTo([nearest.latitude, nearest.longitude], 9, { duration: 1.5 });
            if (activeRadiusCircle) depotMap.removeLayer(activeRadiusCircle);

            activeRadiusCircle = L.circle([nearest.latitude, nearest.longitude], {
              color: '#059669',
              weight: 2,
              dashArray: '4, 6',
              fillColor: '#10b981',
              fillOpacity: 0.16,
              radius: 120700
            }).addTo(depotMap);

            showDepotHud(nearest);

            if (statusEl) {
              statusEl.textContent = `Nearest Staging Depot: ${nearest.name} (${Math.round(minDistance)} miles from your location)`;
            }
          }
        },
        err => {
          if (statusEl) statusEl.textContent = 'Location access denied. Displaying national view.';
          console.warn('Geolocation error:', err);
        },
        { timeout: 8000 }
      );
    }

    function selectMetro(city) {
      const coords = {
        'Atlanta': [33.749, -84.388],
        'Dallas': [32.7767, -96.797],
        'Miami': [25.7617, -80.1918],
        'Austin': [30.2672, -97.7431],
        'Los Angeles': [34.0522, -118.2437],
        'Napa Valley': [38.2975, -122.2869],
        'Chicago': [41.8781, -87.6298]
      };
      if (coords[city]) {
        jumpToMetro(city, coords[city][0], coords[city][1]);
      }
      document.getElementById('filter-city').value = city;
      loadVendors();
      document.getElementById('directory').scrollIntoView({ behavior: 'smooth' });
    }

    function openQuoteModal(city) {
      if (city) document.getElementById('q-city').value = city;
      document.getElementById('q-niche').value = activeNiche;
      document.getElementById('quote-modal').classList.remove('hidden');
      document.getElementById('quote-form').classList.remove('hidden');
      document.getElementById('quote-success-view').classList.add('hidden');
      try { lucide.createIcons(); } catch(e){}
    }
    function closeQuoteModal() {
      document.getElementById('quote-modal').classList.add('hidden');
    }

    async function handleQuoteSubmit(e) {
      e.preventDefault();
      const btn = document.getElementById('quote-submit-btn');
      btn.disabled = true;
      btn.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>Matching Operators...</span>';
      try { lucide.createIcons(); } catch(e){}

      const payload = {
        niche_id: document.getElementById('q-niche').value,
        customer_name: document.getElementById('q-name').value,
        customer_email: document.getElementById('q-email').value,
        customer_phone: document.getElementById('q-phone').value,
        city: document.getElementById('q-city').value,
        state: 'GA',
        event_date: document.getElementById('q-date').value,
        guest_count: parseInt(document.getElementById('q-guests')?.value) || 150,
        duration: document.getElementById('q-duration')?.value || 'Single Day (4-8 hrs)',
        utilities: document.getElementById('q-utilities')?.value || 'Standard On-Site Utilities Available',
        delivery_zip: document.getElementById('q-zip')?.value || '',
        event_type: document.getElementById('q-type').value || 'Commercial Project',
        notes: document.getElementById('q-notes').value
      };

      try {
        const res = await fetch('/api/leads', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        lastQuoteData = data;

        document.getElementById('quote-form').classList.add('hidden');
        document.getElementById('quote-success-view').classList.remove('hidden');
        document.getElementById('deposit-confirmed-view').classList.add('hidden');
        document.getElementById('btn-lock-deposit').classList.remove('hidden');
        document.getElementById('quote-success-msg').textContent = `Matched with top ${data.dispatch.matched_vendors_count} verified operators in ${payload.city} for ${data.qualification.niche_name}. Estimated Quote: $${data.qualification.estimated_quote.toLocaleString()}.`;

        document.getElementById('quote-dispatch-details').innerHTML = `
          <div>&gt; Request Reference Code: <span class="text-slate-900 font-bold">${data.lead_code}</span></div>
          <div>&gt; Verification Status: <span class="text-emerald-700 font-bold">Verified Match with Licensed Local Operators</span></div>
          <div>&gt; Estimated Market Quote: <span class="text-slate-900 font-bold">${data.qualification.estimated_quote ? data.qualification.estimated_quote.toLocaleString() : '2,800.00'}</span></div>
          <div>&gt; 15% Equipment Reservation Deposit: <span class="text-cyan-700 font-bold">${data.qualification.deposit_fee ? data.qualification.deposit_fee.toLocaleString() : '420.00'}</span></div>
        `;

        // Populate 15% Concierge Deposit numbers
        const totalEst = data.qualification.estimated_quote || 2800;
        const depositEst = data.qualification.deposit_fee || Math.round(totalEst * 0.15);
        const balanceDue = totalEst - depositEst;

        document.getElementById('deposit-amount-display').textContent = '$' + depositEst.toLocaleString() + '.00';
        document.getElementById('deposit-total-display').textContent = '$' + totalEst.toLocaleString() + '.00';
        document.getElementById('deposit-balance-display').textContent = '$' + balanceDue.toLocaleString() + '.00';
        document.getElementById('btn-lock-text').textContent = `Lock In Equipment with 15% Escrow Deposit ($${depositEst.toLocaleString()})`;

        try { lucide.createIcons(); } catch(e){}
      } catch (err) {
        alert('Error submitting quote: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i data-lucide="zap" class="w-4 h-4"></i><span>Calculate Estimate &amp; Match Operators</span>';
        try { lucide.createIcons(); } catch(e){}
      }
    }

    let lastQuoteData = null;

    async function executeConciergeDeposit() {
      if (!lastQuoteData) return;
      const btn = document.getElementById('btn-lock-deposit');
      btn.disabled = true;
      btn.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>Securing Escrow Lock...</span>';
      try { lucide.createIcons(); } catch(e){}

      const payload = {
        lead_code: lastQuoteData.lead_code,
        customer_name: document.getElementById('q-name').value,
        customer_email: document.getElementById('q-email').value,
        customer_phone: document.getElementById('q-phone').value,
        city: document.getElementById('q-city').value,
        event_date: document.getElementById('q-date').value,
        guest_count: parseInt(document.getElementById('q-guests')?.value) || 150,
        event_type: document.getElementById('q-type').value || 'Commercial Project',
        estimated_total: lastQuoteData.qualification.estimated_quote,
        deposit_amount: lastQuoteData.qualification.deposit_fee,
        niche_id: document.getElementById('q-niche').value,
        payment_method: 'stripe_escrow_deposit'
      };

      try {
        const res = await fetch('/api/bookings/deposit', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.success) {
          if (data.checkout_url) {
            btn.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>Redirecting to Secure Stripe Checkout...</span>';
            try { lucide.createIcons(); } catch(e){}
            window.location.href = data.checkout_url;
            return;
          }
          document.getElementById('confirmed-booking-id').textContent = data.booking_id;
          document.getElementById('confirmed-deposit-paid').textContent = '$' + data.deposit_paid.toLocaleString() + '.00';
          document.getElementById('confirmed-balance-due').textContent = '$' + data.balance_due_on_site.toLocaleString() + '.00';
          document.getElementById('confirmed-vendor-name').textContent = data.assigned_vendor.name + ' (' + data.assigned_vendor.city + ')';
          document.getElementById('deposit-confirmed-view').classList.remove('hidden');
          document.getElementById('deposit-cta-card').classList.add('hidden');
          try { lucide.createIcons(); } catch(e){}
        } else {
          alert('Deposit error: ' + data.error);
          btn.disabled = false;
          btn.innerHTML = '<i data-lucide="lock" class="w-4 h-4"></i><span>Lock In Equipment with 15% Escrow Deposit</span>';
        }
      } catch (err) {
        alert('Deposit processing error: ' + err.message);
        btn.disabled = false;
        btn.innerHTML = '<i data-lucide="lock" class="w-4 h-4"></i><span>Lock In Equipment with 15% Escrow Deposit</span>';
      }
    }

    async function openBadgeModal(vendorId) {
      try {
        const res = await fetch(`/api/growth/badge-embed/${vendorId}`);
        const data = await res.json();
        document.getElementById('badge-embed-code').value = data.badge_html;
        document.getElementById('badge-preview-container').innerHTML = data.badge_html;
        document.getElementById('badge-modal').classList.remove('hidden');
        try { lucide.createIcons(); } catch(e){}
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
      try { lucide.createIcons(); } catch(e){}
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
            <div class="border-b border-slate-200 pb-1.5 mb-1.5 flex items-start justify-between">
              <div>
                <span class="text-amber-700 font-bold">[${l.event_type}]</span>
                <span class="text-slate-800 ml-1.5">${l.message}</span>
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
          container.innerHTML = '<div class="text-xs text-slate-500 bg-slate-50 p-3 rounded-xl border border-slate-200">No anomalies detected. Directory Engine Operational & Verified.</div>';
          return;
        }

        container.innerHTML = anomalies.map(a => `
          <div class="bg-slate-50 border ${a.status === 'PENDING_REVIEW' ? 'border-rose-300 bg-rose-50/50' : 'border-slate-200'} p-3 rounded-xl flex items-center justify-between text-xs">
            <div>
              <div class="flex items-center gap-2">
                <span class="font-bold text-slate-900">${a.vendor_name}</span>
                <span class="bg-rose-100 text-rose-700 px-1.5 py-0.5 rounded text-[10px] font-bold font-mono">+${a.percentage_delta.toFixed(1)}% Spike</span>
                <span class="text-slate-500 text-[10px] font-mono">($${a.previous_value.toLocaleString()} -> $${a.incoming_value.toLocaleString()})</span>
              </div>
              <div class="text-[10px] text-slate-500 mt-1">Status: ${a.status} &bull; ${a.detected_at}</div>
            </div>

            ${a.status === 'PENDING_REVIEW' ? `
              <div class="flex items-center gap-2">
                <button onclick="resolveAnomaly('${a.id}', 'APPROVED')" class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-2.5 py-1 rounded-lg text-[10px]">Approve</button>
                <button onclick="resolveAnomaly('${a.id}', 'REJECTED')" class="bg-white hover:bg-slate-100 text-rose-600 font-bold px-2.5 py-1 rounded-lg text-[10px] border border-slate-300">Reject</button>
              </div>
            ` : `
              <span class="text-[10px] font-mono text-slate-500">${a.resolution_action || a.status}</span>
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
      try { lucide.createIcons(); } catch(e){}

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
        try { lucide.createIcons(); } catch(e){}
      }
    }

    // --- CAPACITY PLANNER LOGIC ---
    function toggleAlcohol() {
      const chk = document.getElementById('planner-alcohol');
      if (chk) {
        chk.checked = !chk.checked;
        updateCapacityPlanner();
      }
    }

    function toggleOffGrid() {
      const chk = document.getElementById('planner-offgrid');
      if (chk) {
        chk.checked = !chk.checked;
        updateCapacityPlanner();
      }
    }

    function updateCapacityPlanner() {
      const guestsEl = document.getElementById('planner-guests');
      const durationEl = document.getElementById('planner-duration');
      if (!guestsEl || !durationEl) return;

      const guests = parseInt(guestsEl.value);
      const duration = parseInt(durationEl.value);
      const alcohol = document.getElementById('planner-alcohol')?.checked || false;
      const offgrid = document.getElementById('planner-offgrid')?.checked || false;

      document.getElementById('planner-guest-display').textContent = `${guests.toLocaleString()} Guests`;
      document.getElementById('planner-duration-display').textContent = `${duration} Hours`;

      const factor = (alcohol ? 1.25 : 1.0) * (duration / 5.0);
      const effectiveGuests = Math.round(guests * factor);

      let rec = {};
      if (effectiveGuests <= 100) {
        rec = {
          stallsBadge: '2 Private Stalls',
          title: '2-Station Presidential VIP Suite',
          desc: 'Ideal for intimate gatherings, boutique vineyard weddings, and VIP hospitality suites up to 100 guests. Features 1 private women\'s stall and 1 private men\'s stall.',
          power: offgrid ? 'Quiet Onboard Inverter Generator Included' : '1x Dedicated 20-Amp 110V Circuit',
          water: offgrid ? '150-gal Onboard Freshwater Tank Included' : 'Standard 3/4" garden hose hookup',
          footprint: '16ft L x 8ft W (11ft clearance)',
          price: offgrid ? '$1,650 – $2,100' : '$1,150 – $1,600'
        };
      } else if (effectiveGuests <= 220) {
        rec = {
          stallsBadge: '3 Private Stalls',
          title: '3-Station Elegance Restroom Suite',
          desc: 'Optimal balance for upscale gatherings up to 220 guests. Features 2 women\'s private suites, 1 men\'s private suite, porcelain pedal-flush toilets, and Bluetooth audio.',
          power: offgrid ? 'Quiet Commercial Generator Package Included' : '2x Dedicated 20-Amp 110V Circuits',
          water: offgrid ? '250-gal Onboard Freshwater Tank Included' : 'Standard 3/4" garden hose hookup',
          footprint: '18ft L x 8.5ft W (12ft clearance)',
          price: offgrid ? '$2,100 – $2,650' : '$1,450 – $1,950'
        };
      } else if (effectiveGuests <= 450) {
        rec = {
          stallsBadge: '4 Private Stalls',
          title: '4-Station Luxury Elegance Trailer',
          desc: 'Engineered for events up to 450 guests. Includes 2 private women\'s suites, 2 private men\'s suites, flushing porcelain toilets, dual vanity sinks, climate A/C, and integrated stereo audio.',
          power: offgrid ? 'Dual Onboard Whisper Generators (+$950)' : '2x Dedicated 20-Amp 110V Circuits',
          water: offgrid ? '300-gal Onboard Freshwater Tank Delivery' : 'Standard 3/4" garden hose hookup',
          footprint: '22ft L x 8.5ft W (12ft clearance)',
          price: offgrid ? '$2,600 – $3,350' : '$1,650 – $2,400'
        };
      } else if (effectiveGuests <= 800) {
        rec = {
          stallsBadge: '8 Private Stalls',
          title: '8-Station Black-Tie Gala Master Suite',
          desc: 'High-throughput luxury solution for large galas, corporate summits, and multi-tent weddings. Features 4 women\'s private stalls, 4 men\'s private stalls, dual vanity banks, and rapid circulation.',
          power: offgrid ? 'Commercial Mobile Diesel Generator Package' : '3x Dedicated 20-Amp 110V Circuits or 50A Shore Power',
          water: offgrid ? '500-gal Continuous Freshwater Delivery Tank' : 'Pressurized dual garden hose connections (50 PSI)',
          footprint: '28ft L x 8.5ft W (12.5ft clearance)',
          price: offgrid ? '$3,750 – $4,850' : '$2,800 – $3,900'
        };
      } else {
        rec = {
          stallsBadge: '10+ Station Festival Fleet',
          title: '10-Station Festival & State Fair Master Fleet',
          desc: 'Enterprise high-capacity sanitation for state fairs, multi-day music festivals, and major public exhibitions. Includes ADA hydraulic lowering suite, dedicated VIP attendant lounge, and 800-gallon waste capacity.',
          power: 'Commercial 50-Amp Shore Power or 15kW Super-Quiet Industrial Generator',
          water: 'High-volume municipal connection or continuous auxiliary freshwater tanker delivery',
          footprint: '34ft L x 8.5ft W + Auxiliary Fleet Staging',
          price: offgrid ? '$6,500 – $12,500+' : '$4,500 – $8,500+'
        };
      }

      const stallBadge = document.getElementById('planner-stall-badge');
      const recTitle = document.getElementById('planner-rec-title');
      const recDesc = document.getElementById('planner-rec-desc');
      const recPower = document.getElementById('planner-rec-power');
      const recWater = document.getElementById('planner-rec-water');
      const recFootprint = document.getElementById('planner-rec-footprint');
      const recPrice = document.getElementById('planner-rec-price');

      if (stallBadge) stallBadge.textContent = rec.stallsBadge;
      if (recTitle) recTitle.textContent = rec.title;
      if (recDesc) recDesc.textContent = rec.desc;
      if (recPower) recPower.textContent = rec.power;
      if (recWater) recWater.textContent = rec.water;
      if (recFootprint) recFootprint.textContent = rec.footprint;
      if (recPrice) recPrice.textContent = rec.price;
      try { lucide.createIcons(); } catch(e){}
    }

    function applyPlannerToQuote() {
      const guests = document.getElementById('planner-guests')?.value || 175;
      const durationHrs = document.getElementById('planner-duration')?.value || 5;
      const isAlcohol = document.getElementById('planner-alcohol')?.checked || false;
      const isOffGrid = document.getElementById('planner-offgrid')?.checked || false;
      const recTitle = document.getElementById('planner-rec-title')?.textContent?.trim() || 'Luxury Restroom Trailer';

      openQuoteModal();
      document.getElementById('q-niche').value = 'luxury_restrooms';
      if (document.getElementById('q-guests')) document.getElementById('q-guests').value = guests;
      if (document.getElementById('q-utilities')) {
        document.getElementById('q-utilities').value = isOffGrid ? 'Off-Grid Remote (Generator & Freshwater Needed)' : 'Standard On-Site Utilities Available';
      }
      if (document.getElementById('q-type')) {
        document.getElementById('q-type').value = isAlcohol ? 'VIP Gala / Wedding (Alcohol Served)' : 'Private / Corporate Event';
      }
      if (document.getElementById('q-notes')) {
        document.getElementById('q-notes').value = `Capacity Planner Matched: ${recTitle} for ${guests} guests (${durationHrs} hrs). Utility: ${isOffGrid ? 'Off-Grid Generator & Tanks Required' : 'Standard 110V & Hose Available'}.`;
      }
    }

    function openRfpBlueprintModal() {
      const guests = parseInt(document.getElementById('planner-guests')?.value || 175);
      const duration = parseInt(document.getElementById('planner-duration')?.value || 5);
      const isAlcohol = document.getElementById('planner-alcohol')?.checked || false;
      const isOffGrid = document.getElementById('planner-offgrid')?.checked || false;

      const docCode = 'REL-2026-RFP-' + Math.floor(100000 + Math.random() * 900000);
      const docIdEl = document.getElementById('rfp-doc-id');
      if (docIdEl) docIdEl.textContent = `DOC #${docCode}`;

      const dateEl = document.getElementById('rfp-generated-date');
      if (dateEl) {
        const d = new Date();
        dateEl.textContent = `Date: ${d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`;
      }

      document.getElementById('rfp-p-guests').textContent = `${guests.toLocaleString()} Guests`;
      document.getElementById('rfp-p-duration').textContent = `${duration} Hours`;
      document.getElementById('rfp-p-alcohol').textContent = isAlcohol ? 'Alcohol Served (+25% Factor)' : 'No Alcohol (Standard Factor)';
      document.getElementById('rfp-p-utility').textContent = isOffGrid ? 'Off-Grid (Generator & Tanks)' : 'Standard Utilities Hookup';

      document.getElementById('rfp-spec-badge').textContent = document.getElementById('planner-stall-badge')?.textContent || '4 Private Stalls';
      document.getElementById('rfp-spec-title').textContent = document.getElementById('planner-rec-title')?.textContent || 'Luxury Restroom Suite';
      document.getElementById('rfp-spec-desc').textContent = document.getElementById('planner-rec-desc')?.textContent || '';
      document.getElementById('rfp-spec-power').textContent = document.getElementById('planner-rec-power')?.textContent || '2x 20A Dedicated 110V';
      document.getElementById('rfp-spec-water').textContent = document.getElementById('planner-rec-water')?.textContent || 'Standard 3/4" Hose';
      document.getElementById('rfp-spec-footprint').textContent = document.getElementById('planner-rec-footprint')?.textContent || '22ft L x 8.5ft W';
      document.getElementById('rfp-spec-price').textContent = document.getElementById('planner-rec-price')?.textContent || '$1,650 – $2,400';

      document.getElementById('rfp-modal').classList.remove('hidden');
      try { lucide.createIcons(); } catch(e){}
    }

    function closeRfpModal() {
      document.getElementById('rfp-modal').classList.add('hidden');
    }

    // --- CLAIM PROFILE LOGIC (John Rush Blueprint) ---
    function openClaimModal(vendorId, vendorName) {
      document.getElementById('claim-vendor-id').value = vendorId;
      document.getElementById('claim-vendor-name').textContent = vendorName;
      document.getElementById('claim-modal').classList.remove('hidden');
      document.getElementById('claim-form').classList.remove('hidden');
      document.getElementById('claim-success-view').classList.add('hidden');
      try { lucide.createIcons(); } catch(e){}
    }
    function closeClaimModal() {
      document.getElementById('claim-modal').classList.add('hidden');
    }

    async function handleClaimSubmit(e) {
      e.preventDefault();
      const btn = document.getElementById('claim-submit-btn');
      btn.disabled = true;
      btn.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>Verifying Profile...</span>';
      try { lucide.createIcons(); } catch(e){}

      const vendorId = document.getElementById('claim-vendor-id').value;
      const ownerName = document.getElementById('claim-owner-name').value;
      const ownerEmail = document.getElementById('claim-owner-email').value;
      const ownerPhone = document.getElementById('claim-owner-phone').value;
      const tier = document.querySelector('input[name="claim-tier"]:checked')?.value || 'featured';

      try {
        const res = await fetch('/api/vendors/claim', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            vendor_id: vendorId,
            owner_name: ownerName,
            owner_email: ownerEmail,
            owner_phone: ownerPhone,
            plan_tier: tier
          })
        });
        const data = await res.json();

        document.getElementById('claim-form').classList.add('hidden');
        document.getElementById('claim-success-view').classList.remove('hidden');
        document.getElementById('claim-success-msg').textContent = data.message;

        const cta = document.getElementById('claim-checkout-cta');
        if (data.checkout_url) {
          cta.classList.remove('hidden');
          document.getElementById('claim-stripe-link').href = data.checkout_url;
        } else {
          cta.classList.add('hidden');
        }
        loadVendors();
      } catch (err) {
        alert('Claim error: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i data-lucide="check-circle" class="w-4 h-4"></i><span>Verify &amp; Confirm Ownership</span>';
        try { lucide.createIcons(); } catch(e){}
      }
    }

    // --- SUBMIT LISTING LOGIC (John Rush Blueprint) ---
    function openSubmitModal() {
      document.getElementById('submit-modal').classList.remove('hidden');
      document.getElementById('submit-form').classList.remove('hidden');
      document.getElementById('sub-success-view').classList.add('hidden');
      try { lucide.createIcons(); } catch(e){}
    }
    function closeSubmitModal() {
      document.getElementById('submit-modal').classList.add('hidden');
    }

    async function handleSubmitListing(e) {
      e.preventDefault();
      const btn = document.getElementById('sub-submit-btn');
      btn.disabled = true;
      btn.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>Publishing Fleet...</span>';
      try { lucide.createIcons(); } catch(e){}

      const name = document.getElementById('sub-name').value;
      const niche = document.getElementById('sub-niche').value;
      const city = document.getElementById('sub-city').value;
      const state = document.getElementById('sub-state').value;
      const phone = document.getElementById('sub-phone').value;
      const email = document.getElementById('sub-email').value;
      const website = document.getElementById('sub-website').value;
      const fleet = document.getElementById('sub-fleet').value.split(',').map(s => s.trim()).filter(Boolean);
      const amenities = document.getElementById('sub-amenities').value.split(',').map(s => s.trim()).filter(Boolean);
      const tier = document.querySelector('input[name="sub-tier"]:checked')?.value || 'featured';

      try {
        const res = await fetch('/api/vendors/submit', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name,
            niche_id: niche,
            city,
            state,
            phone,
            email,
            website,
            fleet_types: fleet,
            amenities,
            plan_tier: tier
          })
        });
        const data = await res.json();

        document.getElementById('submit-form').classList.add('hidden');
        document.getElementById('sub-success-view').classList.remove('hidden');
        document.getElementById('sub-success-msg').textContent = data.message;

        const cta = document.getElementById('sub-checkout-cta');
        if (data.checkout_url) {
          cta.classList.remove('hidden');
          document.getElementById('sub-stripe-link').href = data.checkout_url;
        } else {
          cta.classList.add('hidden');
        }
        loadVendors();
      } catch (err) {
        alert('Submission error: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i data-lucide="upload-cloud" class="w-4 h-4"></i><span>Submit &amp; Publish Listing</span>';
        try { lucide.createIcons(); } catch(e){}
      }
    }

    // --- PRICING & MEMBERSHIP MODAL LOGIC (Mr. Web Blueprint) ---
    function openPricingModal() {
      document.getElementById('pricing-modal').classList.remove('hidden');
      try { lucide.createIcons(); } catch(e){}
    }
    function closePricingModal() {
      document.getElementById('pricing-modal').classList.add('hidden');
    }

    // --- DIRECT OPERATOR MESSAGING LOGIC (Mr. Web Blueprint) ---
    function openMessageModal(vendorId, vendorName) {
      document.getElementById('msg-vendor-id').value = vendorId;
      document.getElementById('msg-vendor-name').textContent = vendorName;
      document.getElementById('message-modal').classList.remove('hidden');
      document.getElementById('message-form').classList.remove('hidden');
      document.getElementById('msg-success-view').classList.add('hidden');
      try { lucide.createIcons(); } catch(e){}
    }
    function closeMessageModal() {
      document.getElementById('message-modal').classList.add('hidden');
    }

    async function handleMessageSubmit(e) {
      e.preventDefault();
      const btn = document.getElementById('msg-submit-btn');
      btn.disabled = true;
      btn.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>Transmitting Inquiry...</span>';
      try { lucide.createIcons(); } catch(e){}

      const vendorId = document.getElementById('msg-vendor-id').value;
      const payload = {
        sender_name: document.getElementById('msg-name').value,
        sender_email: document.getElementById('msg-email').value,
        sender_phone: document.getElementById('msg-phone').value,
        event_date: document.getElementById('msg-date').value,
        message: document.getElementById('msg-text').value
      };

      try {
        const res = await fetch(`/api/vendors/${vendorId}/message`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        document.getElementById('message-form').classList.add('hidden');
        document.getElementById('msg-success-view').classList.remove('hidden');
        document.getElementById('msg-success-text').textContent = data.message || `Inquiry reference ${data.lead_code} sent to ${data.vendor_name}.`;
        try { lucide.createIcons(); } catch(e){}
      } catch (err) {
        alert('Error sending message: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i data-lucide="send" class="w-4 h-4"></i><span>Send Direct Inquiry</span>';
        try { lucide.createIcons(); } catch(e){}
      }
    }

    // --- VERIFIED REVIEW SUBMISSION LOGIC (Mr. Web Blueprint) ---
    function openReviewModal(vendorId, vendorName) {
      document.getElementById('rev-vendor-id').value = vendorId;
      document.getElementById('rev-vendor-name').textContent = vendorName;
      document.getElementById('review-modal').classList.remove('hidden');
      document.getElementById('review-form').classList.remove('hidden');
      document.getElementById('rev-success-view').classList.add('hidden');
      try { lucide.createIcons(); } catch(e){}
    }
    function closeReviewModal() {
      document.getElementById('review-modal').classList.add('hidden');
    }

    async function handleReviewSubmit(e) {
      e.preventDefault();
      const btn = document.getElementById('rev-submit-btn');
      btn.disabled = true;
      btn.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>Verifying &amp; Publishing...</span>';
      try { lucide.createIcons(); } catch(e){}

      const vendorId = document.getElementById('rev-vendor-id').value;
      const payload = {
        vendor_id: vendorId,
        reviewer_name: document.getElementById('rev-name').value,
        rating: document.getElementById('rev-rating').value,
        event_type: document.getElementById('rev-type').value,
        comment: document.getElementById('rev-comment').value
      };

      try {
        const res = await fetch('/api/vendors/review', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        document.getElementById('review-form').classList.add('hidden');
        document.getElementById('rev-success-view').classList.remove('hidden');
        document.getElementById('rev-success-text').textContent = data.message || `Your verified review for ${data.vendor_name} has been published with a rating of ${data.new_rating}★!`;
        try { lucide.createIcons(); } catch(e){}
        loadVendors();
      } catch (err) {
        alert('Error submitting review: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i data-lucide="check-circle" class="w-4 h-4"></i><span>Post Verified Review</span>';
        try { lucide.createIcons(); } catch(e){}
      }
    }

    // --- AI LISTING CONTENT GENERATOR (Mr. Web Blueprint - Zero Marginal Cost) ---
    async function enhanceListingWithAI() {
      const btn = document.getElementById('ai-enhance-btn');
      const originalHtml = btn.innerHTML;
      btn.disabled = true;
      btn.innerHTML = '<i data-lucide="loader-2" class="w-3 h-3 animate-spin"></i><span>Generating...</span>';
      try { lucide.createIcons(); } catch(e){}

      const name = document.getElementById('sub-name').value || 'Executive Restrooms & Sanitation';
      const niche = document.getElementById('sub-niche').value;
      const city = document.getElementById('sub-city').value || 'Atlanta';
      const state = document.getElementById('sub-state').value || 'GA';
      const fleet = document.getElementById('sub-fleet').value;

      try {
        const res = await fetch('/api/ai/generate-description', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name, niche_id: niche, city, state, fleet_types: fleet })
        });
        const data = await res.json();
        if (data.description) {
          document.getElementById('sub-description').value = data.description;
        }
      } catch (err) {
        alert('Error generating description: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = originalHtml;
        try { lucide.createIcons(); } catch(e){}
      }
    }

    // Zero-Regressive Hydration & Idle Scheduling (Autonomy Partners High-Performance Standard)
    const deferNonCriticalInit = () => {
      const idleRunner = window.requestIdleCallback || ((cb) => setTimeout(cb, 250));
      idleRunner(() => {
        try { if (window.lucide) lucide.createIcons(); } catch(e){}
        updateCapacityPlanner();
        loadVendors();

        // Lazy-load Leaflet map only when depot section approaches viewport
        const mapEl = document.getElementById('nationwide-depot-map');
        if (mapEl && 'IntersectionObserver' in window) {
          const obs = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
              initNationwideDepotMap();
              obs.disconnect();
            }
          }, { rootMargin: '400px' });
          obs.observe(mapEl);
        } else {
          window.addEventListener('scroll', () => initNationwideDepotMap(), { once: true, passive: true });
        }
      });
    };

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', deferNonCriticalInit);
    } else {
      deferNonCriticalInit();
    }


// Explicit Global Bindings for HTML Event Handlers
window.applyAgingCalculatorToQuote = applyAgingCalculatorToQuote;window.applyPlannerToQuote = applyPlannerToQuote;window.clearProximitySearch = clearProximitySearch;window.closeAdminModal = closeAdminModal;window.closeBadgeModal = closeBadgeModal;window.closeClaimModal = closeClaimModal;window.closeDepotHud = closeDepotHud;window.closeMessageModal = closeMessageModal;window.closePricingModal = closePricingModal;window.closeQuoteModal = closeQuoteModal;window.closeReviewModal = closeReviewModal;window.closeRfpModal = closeRfpModal;window.closeSubmitModal = closeSubmitModal;window.copyBadgeCode = copyBadgeCode;window.createDepotPin = createDepotPin;window.createDepotPopupHtml = createDepotPopupHtml;window.enhanceListingWithAI = enhanceListingWithAI;window.executeConciergeDeposit = executeConciergeDeposit;window.fetchAdminMetrics = fetchAdminMetrics;window.fetchAnomalies = fetchAnomalies;window.fetchDeliverabilityStats = fetchDeliverabilityStats;window.filterDepotMap = filterDepotMap;window.handleClaimSubmit = handleClaimSubmit;window.handleMessageSubmit = handleMessageSubmit;window.handleMetroSelectJump = handleMetroSelectJump;window.handleQuoteSubmit = handleQuoteSubmit;window.handleReviewSubmit = handleReviewSubmit;window.handleSubmitListing = handleSubmitListing;window.initNationwideDepotMap = initNationwideDepotMap;window.jumpToMetro = jumpToMetro;window.loadLeafletDependencies = loadLeafletDependencies;window.loadMoreVendors = loadMoreVendors;window.loadVendors = loadVendors;window.locateUserDepot = locateUserDepot;window.onHeroNicheChange = onHeroNicheChange;window.openAdminModal = openAdminModal;window.openBadgeModal = openBadgeModal;window.openClaimModal = openClaimModal;window.openMessageModal = openMessageModal;window.openPricingModal = openPricingModal;window.openQuoteModal = openQuoteModal;window.openReviewModal = openReviewModal;window.openRfpBlueprintModal = openRfpBlueprintModal;window.openSubmitModal = openSubmitModal;window.renderDepotMapMarkers = renderDepotMapMarkers;window.renderVendorCards = renderVendorCards;window.resetDepotMapView = resetDepotMapView;window.resolveAnomaly = resolveAnomaly;window.runAutonomousCron = runAutonomousCron;window.scrollToDirectoryAndSearch = scrollToDirectoryAndSearch;window.searchByProximity = searchByProximity;window.selectMetro = selectMetro;window.selectNicheCard = selectNicheCard;window.showDepotHud = showDepotHud;window.switchMapBaseLayer = switchMapBaseLayer;window.switchNiche = switchNiche;window.switchToolTab = switchToolTab;window.toggleAlcohol = toggleAlcohol;window.toggleOffGrid = toggleOffGrid;window.updateAgingInPlaceCalculator = updateAgingInPlaceCalculator;window.updateCapacityPlanner = updateCapacityPlanner;
