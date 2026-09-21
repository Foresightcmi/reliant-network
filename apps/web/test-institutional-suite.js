const http = require('http');
const app = require('./server');

const server = http.createServer(app);

function request(path, options = {}) {
  return new Promise((resolve, reject) => {
    const address = server.address();
    const port = address.port;
    const reqOptions = {
      hostname: '127.0.0.1',
      port: port,
      path: path,
      method: options.method || 'GET',
      headers: options.headers || {}
    };

    const req = http.request(reqOptions, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        resolve({
          statusCode: res.statusCode,
          headers: res.headers,
          body: data
        });
      });
    });

    req.on('error', reject);

    if (options.body) {
      req.write(typeof options.body === 'string' ? options.body : JSON.stringify(options.body));
    }
    req.end();
  });
}

async function runTests() {
  server.listen(0, '127.0.0.1', async () => {
    console.log('--- INSTITUTIONAL ZERO-OMISSION TEST SUITE RUNNING ---');
    let passed = 0;
    let failed = 0;

    async function assert(name, fn) {
      try {
        await fn();
        console.log(`[PASS] ${name}`);
        passed++;
      } catch (err) {
        console.error(`[FAIL] ${name}:`, err.message);
        failed++;
      }
    }

    // 1. Legal Suite
    await assert('GET /terms serves terms.html', async () => {
      const res = await request('/terms');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      if (!res.body.includes('Platform Role &amp; Brokerage Disclaimer')) throw new Error('Missing disclaimer text');
    });

    await assert('GET /privacy serves privacy.html', async () => {
      const res = await request('/privacy');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      if (!res.body.includes('Privacy Policy')) throw new Error('Missing privacy text');
    });

    await assert('GET /refund-policy serves refund-policy.html', async () => {
      const res = await request('/refund-policy');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      if (!res.body.includes('Escrow Refund &amp; Lead Replacement Policy')) throw new Error('Missing refund text');
    });

    // 2. Static Multi-Vertical Hubs
    await assert('GET /cold-storage serves cold-storage.html', async () => {
      const res = await request('/cold-storage');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      if (!res.body.includes('Commercial Mobile Cold Storage')) throw new Error('Missing cold storage header');
      if (!res.body.includes('id="calculator"')) throw new Error('Missing calculator');
    });

    await assert('GET /cranes serves cranes.html', async () => {
      const res = await request('/cranes');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      if (!res.body.includes('Heavy Mobile Crane Rental')) throw new Error('Missing crane header');
      if (!res.body.includes('val-weight-display')) throw new Error('Missing tonnage calculator');
    });

    await assert('GET /senior-care serves senior-care.html', async () => {
      const res = await request('/senior-care');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      if (!res.body.includes('Senior Living &amp; Assisted Memory Care')) throw new Error('Missing senior care header');
      if (!res.body.includes('adl-meds')) throw new Error('Missing ADL assessment');
    });

    await assert('GET /staying-in-place serves staying-in-place.html', async () => {
      const res = await request('/staying-in-place');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      if (!res.body.includes('65+ Staying in Place')) throw new Error('Missing staying in place header');
      if (!res.body.includes('calc-total-range')) throw new Error('Missing modification calculator');
    });

    await assert('GET /power serves power.html with Tier 4 generator specs and calculator', async () => {
      const res = await request('/power');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      if (!res.body.includes('Industrial Temporary Power')) throw new Error('Missing power header');
      if (!res.body.includes('Tier 4 Final')) throw new Error('Missing Tier 4 Final compliance');
      if (!res.body.includes('id="quote-calculator"')) throw new Error('Missing quote calculator');
    });

    await assert('GET /machinery-moving serves machinery-moving.html with SC&RA millwright specs and calculator', async () => {
      const res = await request('/machinery-moving');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      if (!res.body.includes('Industrial Machinery Moving')) throw new Error('Missing machinery moving header');
      if (!res.body.includes('SC&RA')) throw new Error('Missing SC&RA certification');
      if (!res.body.includes('id="rigging-estimator"')) throw new Error('Missing rigging estimator');
    });

    await assert('GET /senior-downsizing serves senior-downsizing.html with NASMM standards and transition calculator', async () => {
      const res = await request('/senior-downsizing');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      if (!res.body.includes('Senior Downsizing')) throw new Error('Missing senior downsizing header');
      if (!res.body.includes('NASMM')) throw new Error('Missing NASMM accreditation');
      if (!res.body.includes('id="downsizing-calculator"')) throw new Error('Missing downsizing calculator');
    });

    await assert('GET /wheelchair-vans serves wheelchair-vans.html with NMEDA QAP standards and lease estimator', async () => {
      const res = await request('/wheelchair-vans');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      if (!res.body.includes('Wheelchair Accessible Vans')) throw new Error('Missing wheelchair vans header');
      if (!res.body.includes('NMEDA QAP Certified')) throw new Error('Missing NMEDA QAP certification');
      if (!res.body.includes('id="van-calculator"')) throw new Error('Missing van calculator');
    });

    // 3. GEO Standards
    await assert('GET /llms.txt serves Kevin Indig / Princeton KDD standard', async () => {
      const res = await request('/llms.txt');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      if (!res.body.includes('# The Reliant Network')) throw new Error('Missing llms title');
    });

    await assert('GET /llms-full.txt serves full semantic context graph', async () => {
      const res = await request('/llms-full.txt');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      if (!res.body.includes('## 1. Metropolitan Cost & Regulatory Benchmark Index')) throw new Error('Missing llms-full header');
    });

    // 4. Custom 404 Shield
    await assert('GET /random-nonexistent-route-1234 returns 404 with custom branded shield', async () => {
      const res = await request('/random-nonexistent-route-1234');
      if (res.statusCode !== 404) throw new Error(`Expected 404, got ${res.statusCode}`);
      if (!res.body.includes('Commercial Resource Not Found')) throw new Error('Missing 404 shield content');
    });

    // 5. Escrow Booking & Receipt Retrieval Flow
    let testBookingId = null;
    const testIdempKey = 'IDEMP-TEST-INST-' + Date.now();
    await assert('POST /api/bookings/deposit creates escrow booking & receipt URL', async () => {
      const res = await request('/api/bookings/deposit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'idempotency-key': testIdempKey },
        body: JSON.stringify({
          lead_code: 'TEST-LEAD-999',
          customer_name: 'Institutional Test Client',
          customer_email: 'test@reliant-network.com',
          customer_phone: '(404) 732-9876',
          city: 'Atlanta',
          state: 'GA',
          event_date: 'December 12, 2026',
          guest_count: 300,
          event_type: 'High-Ticket Corporate Event',
          estimated_total: 3500,
          deposit_amount: 525,
          niche_id: 'luxury_restrooms'
        })
      });
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      const data = JSON.parse(res.body);
      if (!data.success) throw new Error('Failed to create booking');
      if (!data.booking_id) throw new Error('Missing booking_id');
      testBookingId = data.booking_id;
      if (data.deposit_paid !== 525) throw new Error(`Expected 525 deposit, got ${data.deposit_paid}`);
    });

    await assert('POST /api/bookings/deposit replaying same idempotency-key returns existing booking', async () => {
      const res = await request('/api/bookings/deposit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'idempotency-key': testIdempKey },
        body: JSON.stringify({
          lead_code: 'TEST-LEAD-999-DUPE',
          customer_name: 'Duplicate Accidental Submit',
          deposit_amount: 525
        })
      });
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      const data = JSON.parse(res.body);
      if (!data.idempotent_replay) throw new Error('Expected idempotent_replay: true');
      if (data.booking_id !== testBookingId) throw new Error('Replay booking_id mismatch');
    });

    await assert(`GET /api/bookings/${testBookingId} retrieves stored escrow booking`, async () => {
      const res = await request(`/api/bookings/${testBookingId}`);
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      const data = JSON.parse(res.body);
      if (!data.success || !data.booking) throw new Error('Failed to retrieve booking');
      if (data.booking.booking_id !== testBookingId) throw new Error('Booking ID mismatch');
      if (data.booking.deposit_amount !== 525) throw new Error('Deposit amount mismatch');
    });

    await assert(`GET /receipt/${testBookingId} serves receipt.html certificate`, async () => {
      const res = await request(`/receipt/${testBookingId}`);
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      if (!res.body.includes('Equipment Reservation &amp; Dispatch Voucher')) throw new Error('Missing receipt voucher title');
      if (!res.body.includes('Official Escrow Certificate of Reservation')) throw new Error('Missing certificate title');
    });

    // 6. Push Notifications Log
    await assert('GET /api/notifications contains logged dispatch events', async () => {
      const res = await request('/api/notifications');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      const data = JSON.parse(res.body);
      if (!Array.isArray(data)) throw new Error('Expected array of notifications');
      const found = data.find(n => n.reference === testBookingId);
      if (!found) throw new Error('Notification for test booking not found');
    });

    // 7. Operator Self-Serve Wallet, Top-Up & Lead Unlock
    await assert('GET /api/operator/wallet retrieves operator wallet & lead feed', async () => {
      const res = await request('/api/operator/wallet?operator_id=vend_atl_01');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      const data = JSON.parse(res.body);
      if (!data.success || !data.wallet) throw new Error('Failed to retrieve wallet');
    });

    await assert('POST /api/operator/wallet/topup adds $500 balance with $50 bonus', async () => {
      const res = await request('/api/operator/wallet/topup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ operator_id: 'vend_atl_01', amount: 500 })
      });
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      const data = JSON.parse(res.body);
      if (!data.success || data.bonus_awarded !== 50) throw new Error('Bonus mismatch');
    });

    await assert('POST /api/operator/monopoly/subscribe activates $299/mo metro takeover', async () => {
      const res = await request('/api/operator/monopoly/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ operator_id: 'vend_atl_01', metro_slug: 'atlanta-ga', tier: 'metro_monopoly' })
      });
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      const data = JSON.parse(res.body);
      if (!data.success || data.monthly_cost !== 299) throw new Error('Monopoly cost mismatch');
    });

    await assert('POST /api/operator/monopoly/subscribe rejects rival operator for locked metro with 409', async () => {
      const res = await request('/api/operator/monopoly/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ operator_id: 'vend_bhm_01', metro_slug: 'atlanta-ga', tier: 'metro_monopoly' })
      });
      if (res.statusCode !== 409) throw new Error(`Expected 409 Conflict, got ${res.statusCode}`);
      const data = JSON.parse(res.body);
      if (data.error !== 'METRO_MONOPOLY_LOCKED') throw new Error(`Expected METRO_MONOPOLY_LOCKED, got ${data.error}`);
    });

    // 8. Section 179 Equipment Financing
    await assert('POST /api/financing/apply pre-qualifies $75,000 commercial equipment', async () => {
      const res = await request('/api/financing/apply', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          business_name: 'Georgia Mobile Fleets LLC',
          contact_name: 'David Vance',
          email: 'dvance@gafleets.com',
          phone: '(404) 732-4321',
          purchase_amount: 75000,
          term_months: 60,
          credit_tier: 'tier_1_prime',
          equipment_type: 'Luxury Restroom Trailer'
        })
      });
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      const data = JSON.parse(res.body);
      if (!data.success || data.section_179_savings !== 18750) throw new Error('Section 179 savings mismatch');
      if (data.estimated_broker_bounty !== 2625) throw new Error('Broker referral kickback mismatch');
    });

    // 9. Reciprocal Trust Badge API
    await assert('GET /api/growth/badge-embed/vend_atl_01 serves valid HTML embed snippet', async () => {
      const res = await request('/api/growth/badge-embed/vend_atl_01');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      const data = JSON.parse(res.body);
      if (!data.badge_html || !data.badge_html.includes('The Reliant Network')) throw new Error('Invalid badge HTML');
    });

    // 10. Vector Trust Badge SVG Delivery
    await assert('GET /badges/verified-2026.svg serves vector badge with correct MIME type', async () => {
      const res = await request('/badges/verified-2026.svg');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      const contentType = res.headers['content-type'] || '';
      if (!contentType.includes('image/svg+xml')) throw new Error(`Expected image/svg+xml, got ${contentType}`);
      if (!res.body.includes('<svg') || !res.body.includes('RELIANT NETWORK') || !res.body.includes('VERIFIED 2026')) throw new Error('Invalid SVG content');
    });

    // 11. Programmatic Municipal Compliance Hubs
    await assert('GET /permits/atlanta-ga serves municipal compliance guide with calculator', async () => {
      const res = await request('/permits/atlanta-ga');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      if (!res.body.includes('OSHA 29 CFR 1926.51')) throw new Error('Missing OSHA 1926.51 compliance citation');
      if (!res.body.includes('Atlanta, GA Event Sanitation & Restroom Trailer Permit Guide')) throw new Error('Missing permit title');
      if (!res.body.includes('updateCompliance')) throw new Error('Missing interactive calculator script');
    });

    // 12. Programmatic Best-in-City Leaderboards
    await assert('GET /best/atlanta-ga serves leaderboard with ItemList schema and comparison matrix', async () => {
      const res = await request('/best/atlanta-ga');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      if (!res.body.includes('"@type": "ItemList"')) throw new Error('Missing ItemList JSON-LD schema');
      if (!res.body.includes('Best Luxury Restroom Trailers in Atlanta, GA')) throw new Error('Missing leaderboard title');
      if (!res.body.includes('Trust Score')) throw new Error('Missing Trust Score comparison column');
    });

    // 13. National vs Local Alternative Comparison Hubs
    await assert('GET /vs/united-rentals-alternative serves direct-to-operator comparison', async () => {
      const res = await request('/vs/united-rentals-alternative');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      if (!res.body.includes('United Rentals Alternative for Luxury Restroom Trailers')) throw new Error('Missing alternative comparison title');
      if (!res.body.includes('Reliant Verified Local Fleets') || !res.body.includes('United Rentals')) throw new Error('Missing comparison columns');
    });

    // 14. Reciprocal Backlink Verification Engine
    await assert('GET /api/growth/verify-badge-backlink/vend_atl_01 unlocks 15% discount', async () => {
      const res = await request('/api/growth/verify-badge-backlink/vend_atl_01');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      const data = JSON.parse(res.body);
      if (!data.success || !data.backlink_verified) throw new Error('Backlink verification failed');
      if (!data.reward_unlocked.includes('15% Discount')) throw new Error('Missing discount reward in response');
    });

    // 15. Standalone Fleet Verification Standard Banner
    await assert('GET / index.html displays Standalone Fleet Verification Standard banner', async () => {
      const res = await request('/');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      if (!res.body.includes('Institutional Asset &amp; Fleet Verification Standard')) throw new Error('Missing Fleet Verification Standard banner');
      if (!res.body.includes('Vetted Commercial Equipment &amp; High-Capacity Fleets Nationwide')) throw new Error('Missing fleet assurance headline');
    });

    // 16. 50-State Scaling & Statewide Hub Availability
    await assert('GET /state/alabama and /state/alaska serve valid state directory hubs with 200 OK', async () => {
      const resAl = await request('/state/alabama');
      if (resAl.statusCode !== 200) throw new Error(`Expected 200 for Alabama, got ${resAl.statusCode}`);
      if (!resAl.body.includes('Alabama Commercial &amp; VIP Restroom Fleet Network')) throw new Error('Missing Alabama title');

      const resAk = await request('/state/alaska');
      if (resAk.statusCode !== 200) throw new Error(`Expected 200 for Alaska, got ${resAk.statusCode}`);
      if (!resAk.body.includes('Alaska Commercial &amp; VIP Restroom Fleet Network')) throw new Error('Missing Alaska title');
    });

    // 17. 50-State Directory API & Zero Placeholder Data Integrity (214 Verified Vendors)
    await assert('GET /api/vendors?niche_id=all returns 214 verified vendors across all 50 states with zero 555-numbers', async () => {
      const res = await request('/api/vendors?niche_id=all');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      const vendors = JSON.parse(res.body);
      if (vendors.length !== 214) throw new Error(`Expected exactly 214 vendors, got ${vendors.length}`);
      
      const states = new Set(vendors.map(v => v.state));
      if (states.size < 50) throw new Error(`Expected at least 50 states covered, got ${states.size}`);

      const has555 = vendors.some(v => v.phone && v.phone.includes('555'));
      if (has555) throw new Error('Detected forbidden 555 placeholder phone number in vendor database');
    });

    // 18. New Vertical API Endpoints (17 Verified Depots Each)
    await assert('GET /api/vendors?niche_id=temporary_power returns 17 verified power fleets', async () => {
      const res = await request('/api/vendors?niche_id=temporary_power');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      const vendors = JSON.parse(res.body);
      if (vendors.length !== 17) throw new Error(`Expected 17 temporary power vendors, got ${vendors.length}`);
      if (vendors.some(v => !v.phone || v.phone.includes('555'))) throw new Error('Invalid vendor data in power fleet');
    });

    await assert('GET /api/vendors?niche_id=machinery_moving returns 17 verified millwright contractors', async () => {
      const res = await request('/api/vendors?niche_id=machinery_moving');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      const vendors = JSON.parse(res.body);
      if (vendors.length !== 17) throw new Error(`Expected 17 machinery moving vendors, got ${vendors.length}`);
    });

    await assert('GET /api/vendors?niche_id=senior_downsizing returns 17 verified downsizing specialists', async () => {
      const res = await request('/api/vendors?niche_id=senior_downsizing');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      const vendors = JSON.parse(res.body);
      if (vendors.length !== 17) throw new Error(`Expected 17 senior downsizing vendors, got ${vendors.length}`);
    });

    await assert('GET /api/vendors?niche_id=wheelchair_vans returns 17 verified mobility vehicle dealers', async () => {
      const res = await request('/api/vendors?niche_id=wheelchair_vans');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      const vendors = JSON.parse(res.body);
      if (vendors.length !== 17) throw new Error(`Expected 17 wheelchair van vendors, got ${vendors.length}`);
    });

    // 19. Comprehensive 50-State Canonical Sitemap
    await assert('GET /sitemap.xml contains 350+ URLs including 50 state hubs and all 9 vertical hubs', async () => {
      const res = await request('/sitemap.xml');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      if (!res.body.includes('https://www.reliantverified.com/state/alabama')) throw new Error('Missing Alabama in sitemap');
      if (!res.body.includes('https://www.reliantverified.com/state/wyoming')) throw new Error('Missing Wyoming in sitemap');
      if (!res.body.includes('https://www.reliantverified.com/power')) throw new Error('Missing power hub in sitemap');
      if (!res.body.includes('https://www.reliantverified.com/machinery-moving')) throw new Error('Missing machinery moving hub in sitemap');
      if (!res.body.includes('https://www.reliantverified.com/senior-downsizing')) throw new Error('Missing senior downsizing hub in sitemap');
      if (!res.body.includes('https://www.reliantverified.com/wheelchair-vans')) throw new Error('Missing wheelchair vans hub in sitemap');
      const urlCount = (res.body.match(/<loc>/g) || []).length;
      if (urlCount < 350) throw new Error(`Expected at least 350 URLs in sitemap, got ${urlCount}`);
    });

    // 20. Stripe Frictionless Checkout & Verification Suite
    await assert('GET /api/stripe/status returns valid Stripe engine telemetry', async () => {
      const res = await request('/api/stripe/status');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      const data = JSON.parse(res.body);
      if (typeof data.configured !== 'boolean') throw new Error('Missing configured boolean');
      if (!Array.isArray(data.supported_checkout_types)) throw new Error('Missing supported_checkout_types');
      if (data.supported_checkout_types.length !== 4) throw new Error('Expected 4 supported checkout types');
    });

    await assert('POST /api/stripe/create-checkout-session creates dynamic session or demo fallback', async () => {
      const res = await request('/api/stripe/create-checkout-session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          type: 'escrow_deposit',
          amount: 525,
          niche_id: 'temporary_power',
          city: 'Atlanta',
          state: 'GA',
          customer_name: 'Stripe Test Corp'
        })
      });
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      const data = JSON.parse(res.body);
      if (!data.success) throw new Error('Failed to create session');
      if (!data.checkout_url) throw new Error('Missing checkout_url');
    });

    await assert('GET /api/stripe/verify-session validates payment verification flow', async () => {
      const res = await request('/api/stripe/verify-session?session_id=demo_session_test_999');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      const data = JSON.parse(res.body);
      if (!data.verified) throw new Error('Expected verified: true for demo verification');
    });

    await assert('GET /stripe-setup serves graphical setup assistant with 200 OK', async () => {
      const res = await request('/stripe-setup');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      if (!res.body.includes('Stripe Checkout Integration')) throw new Error('Missing Stripe setup title');
      if (!res.body.includes('Live Checkout Sandbox')) throw new Error('Missing sandbox title');
    });

    // 21. Kyle's "Trojan Horse" Rank & Rent Engine Suite
    await assert('POST /api/leads/trojan-dispatch initiates free gift lead and Kyle\'s outreach kit for open territory', async () => {
      const res = await request('/api/leads/trojan-dispatch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          niche_id: 'machinery_moving',
          city: 'Houston',
          state: 'TX',
          customer_name: 'David Vance (Gulf Coast Heavy Haul)',
          customer_phone: '(713) 902-8812',
          customer_email: 'procurement@gulfhaul.com',
          estimated_quote: 12500,
          service_description: '80-Ton Stamping Press Machine Moving & Millwright Leveling'
        })
      });
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      const data = JSON.parse(res.body);
      if (data.status !== 'TROJAN_HORSE_GIFT_DISPATCHED') throw new Error(`Expected TROJAN_HORSE_GIFT_DISPATCHED, got ${data.status}`);
      if (data.territory_status !== 'OPEN') throw new Error(`Expected OPEN territory, got ${data.territory_status}`);
      if (!data.target_contractor || !data.target_contractor.name) throw new Error('Missing target_contractor');
      if (!data.monopoly_offer || !data.monopoly_offer.stripe_checkout_url) throw new Error('Missing stripe_checkout_url');
      if (!data.outreach_scripts || !data.outreach_scripts.sms || !data.outreach_scripts.email || !data.outreach_scripts.phone_cold_call) {
        throw new Error('Missing Kyle\'s multi-channel outreach scripts');
      }
    });

    await assert('POST /api/leads/trojan-dispatch routes exclusively to active monopoly partner for locked territory', async () => {
      const res = await request('/api/leads/trojan-dispatch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          niche_id: 'luxury_restrooms',
          city: 'Atlanta',
          state: 'GA',
          customer_name: 'Margaret Holloway',
          customer_phone: '(404) 555-1234',
          customer_email: 'margaret@atlantaevent.com',
          estimated_quote: 3100,
          service_description: 'Luxury VIP Restroom Suite for Corporate Gala'
        })
      });
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      const data = JSON.parse(res.body);
      if (data.status !== 'EXCLUSIVE_MONOPOLY_ROUTED') throw new Error(`Expected EXCLUSIVE_MONOPOLY_ROUTED, got ${data.status}`);
      if (data.territory_status !== 'LOCKED') throw new Error(`Expected LOCKED territory, got ${data.territory_status}`);
      if (data.operator.id !== 'vend_atl_01') throw new Error(`Expected vend_atl_01, got ${data.operator.id}`);
    });

    await assert('GET /api/leads/trojan-status returns valid telemetry on dispatched gift leads', async () => {
      const res = await request('/api/leads/trojan-status');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      const data = JSON.parse(res.body);
      if (typeof data.total_dispatched !== 'number') throw new Error('Missing total_dispatched count');
      if (typeof data.total_gift_value !== 'number') throw new Error('Missing total_gift_value');
      if (!Array.isArray(data.locked_territories)) throw new Error('Missing locked_territories array');
    });

    await assert('GET /api/leads/trojan-territories returns metropolitan roster and lockout telemetry', async () => {
      const res = await request('/api/leads/trojan-territories');
      if (res.statusCode !== 200) throw new Error(`Expected 200, got ${res.statusCode}`);
      const data = JSON.parse(res.body);
      if (data.total_territories < 5) throw new Error(`Expected at least 5 territories, got ${data.total_territories}`);
      if (typeof data.open_count !== 'number' || typeof data.locked_count !== 'number') throw new Error('Missing open/locked counts');
      const atlanta = data.territories.find(t => t.city === 'Atlanta');
      if (!atlanta || atlanta.status !== 'LOCKED') throw new Error('Expected Atlanta to be LOCKED');
    });

    console.log(`\nTEST RESULTS: ${passed} PASSED, ${failed} FAILED.`);
    server.close();
    process.exit(failed > 0 ? 1 : 0);
  });
}

runTests().catch(err => {
  console.error('Fatal test error:', err);
  server.close();
  process.exit(1);
});
