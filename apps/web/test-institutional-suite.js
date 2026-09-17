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
    await assert('POST /api/bookings/deposit creates escrow booking & receipt URL', async () => {
      const res = await request('/api/bookings/deposit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          lead_code: 'TEST-LEAD-999',
          customer_name: 'Institutional Test Client',
          customer_email: 'test@reliant-network.com',
          customer_phone: '(404) 555-9876',
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

    // 8. Section 179 Equipment Financing
    await assert('POST /api/financing/apply pre-qualifies $75,000 commercial equipment', async () => {
      const res = await request('/api/financing/apply', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          business_name: 'Georgia Mobile Fleets LLC',
          contact_name: 'David Vance',
          email: 'dvance@gafleets.com',
          phone: '(404) 555-4321',
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
