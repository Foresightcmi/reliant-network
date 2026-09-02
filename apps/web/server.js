const express = require('express');
const cors = require('cors');
const path = require('path');
const { spawnSync } = require('child_process');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const BRIDGE_PATH = path.join(__dirname, '..', '..', 'services', 'data', 'db_bridge.py');
const PSEO_DATA_PATH = path.join(__dirname, '..', '..', 'services', 'data', 'pseo_metros.json');

// --- ⚡ IN-MEMORY CACHE LAYER FOR DATA PIPELINE ---
class PseoMemoryCache {
  constructor(ttlMs = 10 * 60 * 1000) {
    this.cache = new Map();
    this.ttlMs = ttlMs;
    this.stats = { hits: 0, misses: 0 };
  }

  get(key) {
    const item = this.cache.get(key);
    if (!item) {
      this.stats.misses++;
      return null;
    }
    if (Date.now() > item.expiresAt) {
      this.cache.delete(key);
      this.stats.misses++;
      return null;
    }
    this.stats.hits++;
    return item.value;
  }

  set(key, value) {
    this.cache.set(key, {
      value,
      expiresAt: Date.now() + this.ttlMs
    });
  }

  invalidate(keyPrefix = '') {
    if (!keyPrefix) {
      this.cache.clear();
    } else {
      for (const k of this.cache.keys()) {
        if (k.startsWith(keyPrefix)) this.cache.delete(k);
      }
    }
  }

  getStats() {
    const total = this.stats.hits + this.stats.misses;
    const hitRate = total > 0 ? ((this.stats.hits / total) * 100).toFixed(1) + '%' : '0%';
    return { ...this.stats, total, hitRate, cachedKeys: this.cache.size };
  }
}

const pseoCache = new PseoMemoryCache();

function queryDb(sql, params = []) {
  try {
    if (sql.trim().toUpperCase().startsWith('SELECT')) {
      const vendorsFile = path.join(__dirname, '..', '..', 'services', 'data', 'vendors.json');
      if (fs.existsSync(vendorsFile)) {
        let allVendors = JSON.parse(fs.readFileSync(vendorsFile, 'utf8'));
        
        let pIndex = 0;
        if (sql.includes('niche_id = ?')) {
           const n = params[pIndex++];
           allVendors = allVendors.filter(v => v.niche_id === n);
        }
        if (sql.includes('city = ?')) {
           const c = params[pIndex++];
           allVendors = allVendors.filter(v => v.city === c);
        }
        if (sql.includes('amenities LIKE ?')) {
           const term = params[pIndex++].replace(/%/g, '');
           allVendors = allVendors.filter(v => v.amenities && v.amenities.includes(term));
        }
        
        return allVendors;
      }
      return [];
    } else {
      return { lastInsertRowid: 1, changes: 1 };
    }
  } catch (err) {
    console.error('JSON Mock DB error:', err.message);
    return [];
  }
}

// 1. Robots.txt
app.get('/robots.txt', (req, res) => {
  res.type('text/plain');
  res.send("User-agent: *\nAllow: /\nSitemap: http://localhost:3000/sitemap.xml\n");
});

// 2. Dynamic XML Sitemap
app.get('/sitemap.xml', (req, res) => {
  const sitemapPath = path.join(__dirname, 'public', 'sitemap.xml');
  if (fs.existsSync(sitemapPath)) {
    res.type('application/xml');
    res.sendFile(sitemapPath);
  } else {
    res.status(404).send('Sitemap not found');
  }
});

// 3. Programmatic SEO Metros API (Cached)
app.get('/api/pseo/metros', (req, res) => {
  const cacheKey = 'all_metros';
  const cached = pseoCache.get(cacheKey);
  if (cached) {
    res.setHeader('X-Cache', 'HIT');
    return res.json(cached);
  }

  if (fs.existsSync(PSEO_DATA_PATH)) {
    const data = JSON.parse(fs.readFileSync(PSEO_DATA_PATH, 'utf-8'));
    pseoCache.set(cacheKey, data);
    res.setHeader('X-Cache', 'MISS');
    res.json(data);
  } else {
    res.json([]);
  }
});

// 4. Fortified Programmatic Metro Landing Page API (With In-Memory Caching & Protocol Schema)
app.get('/api/pseo/metro/:slug', (req, res) => {
  const start = process.hrtime.bigint();
  const cacheKey = 'metro_' + req.params.slug;
  const cached = pseoCache.get(cacheKey);
  if (cached) {
    const end = process.hrtime.bigint();
    const latencyMs = (Number(end - start) / 1e6).toFixed(3);
    res.setHeader('X-Cache', 'HIT');
    res.setHeader('X-Latency-Ms', latencyMs);
    return res.json(cached);
  }

  if (!fs.existsSync(PSEO_DATA_PATH)) return res.status(404).json({ error: 'pSEO data missing' });
  const metros = JSON.parse(fs.readFileSync(PSEO_DATA_PATH, 'utf-8'));
  const metro = metros.find(m => m.slug === req.params.slug);
  if (!metro) return res.status(404).json({ error: 'Metro not found' });

  const vendors = queryDb("SELECT * FROM vendors WHERE city = ? ORDER BY rating DESC", [metro.city]);
  const parsedVendors = vendors.map(v => ({
    ...v,
    fleet_types: JSON.parse(v.fleet_types || '[]'),
    amenities: JSON.parse(v.amenities || '[]')
  }));

  const faqs = (metro.localized_faqs || []).map(f => ({
    "@type": "Question",
    "name": f.q,
    "acceptedAnswer": {
      "@type": "Answer",
      "text": f.a
    }
  }));

  const responsePayload = {
    metro,
    vendors: parsedVendors,
    geo_schema: {
      "@context": "https://schema.org",
      "@type": "Service",
      "serviceType": "Luxury Restroom Trailer Rental",
      "areaServed": {
        "@type": "City",
        "name": metro.city,
        "containedInPlace": metro.state_full
      },
      "offers": {
        "@type": "AggregateOffer",
        "lowPrice": metro.min_cost,
        "highPrice": metro.max_cost,
        "priceCurrency": "USD"
      }
    },
    faq_schema: {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": faqs
    }
  };

  pseoCache.set(cacheKey, responsePayload);
  const end = process.hrtime.bigint();
  const latencyMs = (Number(end - start) / 1e6).toFixed(3);
  res.setHeader('X-Cache', 'MISS');
  res.setHeader('X-Latency-Ms', latencyMs);
  res.json(responsePayload);
});

// 5. Niche Configuration
app.get('/api/niches', (req, res) => {
  const configPath = path.join(__dirname, '..', '..', 'config', 'niches.json');
  if (fs.existsSync(configPath)) {
    res.json(JSON.parse(fs.readFileSync(configPath, 'utf-8')));
  } else {
    res.status(404).json({ error: 'Config not found' });
  }
});

// 6. Get Multi-Vertical Vendors (With Niche Filter Support)
app.get('/api/vendors', (req, res) => {
  try {
    const { city, amenity, search, niche_id } = req.query;
    let sql = "SELECT * FROM vendors WHERE 1=1";
    const params = [];

    if (niche_id && niche_id !== 'All') {
      sql += " AND niche_id = ?";
      params.push(niche_id);
    }
    if (city && city !== 'All') {
      sql += " AND city = ?";
      params.push(city);
    }
    if (amenity) {
      sql += " AND amenities LIKE ?";
      params.push(`%${amenity}%`);
    }
    if (search) {
      sql += " AND (name LIKE ? OR description LIKE ? OR city LIKE ?)";
      params.push(`%${search}%`, `%${search}%`, `%${search}%`);
    }

    sql += " ORDER BY subscription_active DESC, rating DESC";
    const vendors = queryDb(sql, params);
    
    const parsed = vendors.map(v => ({
      ...v,
      fleet_types: JSON.parse(v.fleet_types || '[]'),
      amenities: JSON.parse(v.amenities || '[]')
    }));

    res.json(parsed);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 7. Multi-Vertical Lead Capture, AI Qualification & Dispatch
app.post('/api/leads', (req, res) => {
  try {
    const { customer_name, customer_email, customer_phone, city, state, event_date, guest_count, event_type, budget, notes, niche_id } = req.body;
    const activeNiche = niche_id || 'luxury_restrooms';

    const pyScript = `
import sys, json, os
sys.path.append(r"${path.join(__dirname, '..', '..', 'services', 'lead_engine')}")
from ai_qualifier import AILeadQualifier
from revenue_splitter import MultiNicheRevenueSplitter

data = json.loads(sys.stdin.read())
qualifier = AILeadQualifier()
q_res = qualifier.qualify_inquiry(data)

splitter = MultiNicheRevenueSplitter()
rev_res = splitter.calculate_lead_brokerage(data.get("niche_id", "luxury_restrooms"), q_res["estimated_quote"])

res = {
    "intent_score": q_res["intent_score"],
    "estimated_quote": q_res["estimated_quote"],
    "lead_price": rev_res["pay_per_lead_fee"],
    "deposit_fee": rev_res["estimated_15pct_booking_deposit"],
    "stations_recommended": q_res.get("stations_recommended", "Standard Fleet Unit"),
    "niche_name": rev_res["niche_name"]
}
print(json.dumps(res))
`;
    const qProc = spawnSync('python', ['-c', pyScript], {
      input: JSON.stringify(req.body),
      encoding: 'utf-8'
    });
    const qualResult = JSON.parse(qProc.stdout.trim());

    const leadId = 'lead-' + Date.now();
    const leadCode = activeNiche.substring(0, 3).toUpperCase() + '-' + Math.floor(1000 + Math.random() * 9000);
    const stripeLink = `https://buy.stripe.com/test_${activeNiche}_${qualResult.lead_price}_${leadCode}`;

    queryDb(`
      INSERT INTO leads (
        id, lead_code, niche_id, customer_name, customer_email, customer_phone,
        city, state, event_date, guest_count, event_type, budget, notes,
        status, ai_intent_score, estimated_quote, lead_price, stripe_payment_link
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `, [
      leadId, leadCode, activeNiche, customer_name, customer_email, customer_phone,
      city || 'Atlanta', state || 'GA', event_date, guest_count || 150, event_type || 'Commercial Event',
      budget || '$3,000 - $8,000', notes || '', 'QUALIFIED', qualResult.intent_score,
      qualResult.estimated_quote, qualResult.lead_price, stripeLink
    ]);

    // Dispatch lead alerts
    const dScript = `
import sys, json, os
sys.path.append(r"${path.join(__dirname, '..', '..', 'services', 'lead_engine')}")
from dispatcher import LeadBrokerDispatcher
dispatcher = LeadBrokerDispatcher()
res = dispatcher.dispatch_lead("${leadId}")
print(json.dumps(res))
`;
    const dProc = spawnSync('python', ['-c', dScript], { encoding: 'utf-8' });
    const dispatchResult = JSON.parse(dProc.stdout.trim());

    // Trigger Deliverability-Shielded Outbound Outreach
    const gScript = `
import sys, json, os
sys.path.append(r"${path.join(__dirname, '..', '..', 'services', 'lead_engine')}")
from growth_loops import FortifiedGrowthEngine
growth = FortifiedGrowthEngine()
res = growth.trigger_lead_first_outreach("${leadId}")
print(json.dumps(res))
`;
    const gProc = spawnSync('python', ['-c', gScript], { encoding: 'utf-8' });
    const growthResult = JSON.parse(gProc.stdout.trim());

    res.json({
      success: true,
      lead_id: leadId,
      lead_code: leadCode,
      niche_id: activeNiche,
      qualification: qualResult,
      dispatch: dispatchResult,
      growth_outreach: growthResult
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 8. Claim Profile
app.post('/api/claim', (req, res) => {
  try {
    const { vendor_id, email } = req.body;
    queryDb("UPDATE vendors SET claimed = 1, subscription_active = 1 WHERE id = ?", [vendor_id]);
    
    const payoutId = 'sub-' + Date.now();
    queryDb("INSERT INTO payouts (id, vendor_id, amount, type, status) VALUES (?, ?, 99, 'MONTHLY_SUBSCRIPTION', 'COMPLETED')", [payoutId, vendor_id]);

    queryDb("INSERT INTO logs (event_type, message, details) VALUES (?, ?, ?)", [
      'VENDOR_CLAIMED',
      `Vendor ${vendor_id} claimed profile and activated $99/mo subscription`,
      JSON.stringify({ vendor_id, email, amount: 99 })
    ]);

    pseoCache.invalidate();
    res.json({ success: true, message: 'Profile claimed and priority subscription activated!' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 9. Anomaly Review Queue Endpoints
app.get('/api/admin/anomalies', (req, res) => {
  try {
    const rows = queryDb("SELECT * FROM anomaly_queue ORDER BY detected_at DESC LIMIT 20");
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/admin/resolve-anomaly', (req, res) => {
  try {
    const { anomaly_id, action, override_value } = req.body;
    const aScript = `
import sys, json, os
sys.path.append(r"${path.join(__dirname, '..', '..', 'services', 'lead_engine')}")
from ad_library_ingest import FortifiedAdSpendIngest
ingest = FortifiedAdSpendIngest()
res = ingest.resolve_anomaly("${anomaly_id}", "${action || 'APPROVED'}", ${override_value || 'None'})
print(json.dumps(res))
`;
    const aProc = spawnSync('python', ['-c', aScript], { encoding: 'utf-8' });
    res.json(JSON.parse(aProc.stdout.trim()));
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 10. Deliverability Stats API
app.get('/api/admin/deliverability-stats', (req, res) => {
  try {
    const dScript = `
import sys, json, os
sys.path.append(r"${path.join(__dirname, '..', '..', 'services', 'lead_engine')}")
from growth_loops import FortifiedGrowthEngine
growth = FortifiedGrowthEngine()
print(json.dumps({
    "sender_domain": growth.outbound_domain,
    "usage": growth.get_daily_usage()
}))
`;
    const dProc = spawnSync('python', ['-c', dScript], { encoding: 'utf-8' });
    res.json(JSON.parse(dProc.stdout.trim()));
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 11. Embed Badge Generator API
app.get('/api/growth/badge-embed/:vendorId', (req, res) => {
  try {
    const rows = queryDb("SELECT * FROM vendors WHERE id = ?", [req.params.vendorId]);
    const name = rows.length ? rows[0].name : "High-Ticket Verified Partner";
    
    const gScript = `
import sys, json, os
sys.path.append(r"${path.join(__dirname, '..', '..', 'services', 'lead_engine')}")
from growth_loops import FortifiedGrowthEngine
growth = FortifiedGrowthEngine()
badge_code = growth.generate_embed_badge("${req.params.vendorId}", "${name.replace(/"/g, '\\"')}")
print(json.dumps({"badge_html": badge_code}))
`;
    const gProc = spawnSync('python', ['-c', gScript], { encoding: 'utf-8' });
    res.json(JSON.parse(gProc.stdout.trim()));
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 12. Admin Metrics & Multi-Vertical Portfolio Telemetry
app.get('/api/admin/metrics', (req, res) => {
  try {
    const rev = queryDb("SELECT SUM(amount) as total_rev FROM payouts WHERE status = 'COMPLETED'");
    const totalRevenue = rev[0].total_rev || 0;

    const leadsCount = queryDb("SELECT COUNT(*) as cnt FROM leads");
    const vendorsCount = queryDb("SELECT COUNT(*) as cnt FROM vendors");
    const subsCount = queryDb("SELECT COUNT(*) as cnt FROM vendors WHERE subscription_active = 1");
    const anomalyCount = queryDb("SELECT COUNT(*) as cnt FROM anomaly_queue WHERE status = 'PENDING_REVIEW'");

    const nicheStats = queryDb(`
      SELECT niche_id, COUNT(*) as vendor_count, SUM(subscription_active) as active_subscribers
      FROM vendors GROUP BY niche_id
    `);

    const recentLogs = queryDb("SELECT * FROM logs ORDER BY created_at DESC LIMIT 20");
    const recentLeads = queryDb("SELECT * FROM leads ORDER BY created_at DESC LIMIT 10");
    const recentPayouts = queryDb("SELECT * FROM payouts ORDER BY created_at DESC LIMIT 10");

    res.json({
      total_revenue_banked: totalRevenue,
      active_mrr: (subsCount[0].cnt || 0) * 99,
      total_leads: leadsCount[0].cnt || 0,
      total_vendors: vendorsCount[0].cnt || 0,
      active_subscribers: subsCount[0].cnt || 0,
      pending_anomalies: anomalyCount[0].cnt || 0,
      niche_breakdown: nicheStats,
      cache_telemetry: pseoCache.getStats(),
      recent_logs: recentLogs,
      recent_leads: recentLeads,
      recent_payouts: recentPayouts
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 13. Run Cron Automation Trigger
app.post('/api/admin/run-cron', (req, res) => {
  try {
    const cScript = `
import sys, json, os
sys.path.append(r"${path.join(__dirname, '..', '..', 'services', 'lead_engine')}")
from automation_cron import run_hourly_broker_cycle
res = run_hourly_broker_cycle()
print(json.dumps(res))
`;
    const cProc = spawnSync('python', ['-c', cScript], { encoding: 'utf-8' });
    const cronResult = JSON.parse(cProc.stdout.trim());
    pseoCache.invalidate();
    res.json({ success: true, telemetry: cronResult });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

if (process.env.NODE_ENV !== 'production') {
  app.listen(PORT, () => {
    console.log(`🚀 The Reliant Network Multi-Vertical Autonomous Directory Engine running on http://localhost:${PORT}`);
  });
}
module.exports = app;
