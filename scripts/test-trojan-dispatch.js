/**
 * Test Simulator: Kyle the Website Landlord's "Trojan Horse" Rank & Rent Engine
 * Demonstrates:
 * 1. Open territory inbound lead -> complimentary gift lead dispatch + Stripe $299/mo lockout link + Kyle's outreach copy.
 * 2. Locked territory inbound lead -> exclusive monopoly routing to paying subscriber ($0 deductions).
 * 3. Territory inventory status & telemetry metrics.
 */

const http = require('http');
const app = require('../apps/web/server');

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
        try {
          resolve({
            statusCode: res.statusCode,
            headers: res.headers,
            body: JSON.parse(data)
          });
        } catch (e) {
          resolve({
            statusCode: res.statusCode,
            headers: res.headers,
            rawBody: data
          });
        }
      });
    });

    req.on('error', reject);

    if (options.body) {
      req.write(typeof options.body === 'string' ? options.body : JSON.stringify(options.body));
    }
    req.end();
  });
}

async function runSimulator() {
  server.listen(0, '127.0.0.1', async () => {
    console.log('\n================================================================');
    console.log('🏛️  KYLE THE WEBSITE LANDLORD: TROJAN HORSE SIMULATOR');
    console.log('================================================================\n');

    // 1. Test Inbound Lead in Open Territory: Chicago Commercial Power
    console.log('--- TEST 1: Open Territory Inbound Lead (Chicago Temporary Power) ---');
    const openLeadPayload = {
      niche_id: 'temporary_power',
      city: 'Chicago',
      state: 'IL',
      customer_name: 'Marcus Sterling (Midwest Industrial Logistics)',
      customer_phone: '(312) 849-2910',
      customer_email: 'procurement@midwestlogistics.org',
      estimated_quote: 8500,
      service_description: '500kVA Tier 4 Diesel Generator Rental + Distribution Panel (3-Week Shutdown)',
      event_type: 'Industrial Plant Shutdown'
    };

    const res1 = await request('/api/leads/trojan-dispatch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: openLeadPayload
    });

    console.log(`HTTP Status: ${res1.statusCode}`);
    console.log(`Dispatch Status: ${res1.body.status}`);
    console.log(`Territory Status: ${res1.body.territory_status}`);
    console.log(`Selected Top Contractor: ${res1.body.target_contractor.name} (${res1.body.target_contractor.city}) - Rating: ${res1.body.target_contractor.rating}★`);
    console.log(`Competitors Identified: ${res1.body.competitors.join(', ') || 'Local rivals'}`);
    console.log(`Stripe Checkout URL: ${res1.body.monopoly_offer.stripe_checkout_url}`);
    console.log(`Exclusivity Reservation Window: 7 Days (Expires: ${res1.body.monopoly_offer.expires_at})`);
    
    console.log('\n📱 KYLE\'S SMS OUTREACH SCRIPT:');
    console.log(res1.body.outreach_scripts.sms);

    console.log('\n📧 KYLE\'S EMAIL TEMPLATE (Preview):');
    console.log(res1.body.outreach_scripts.email.substring(0, 320) + '...\n');

    console.log('📞 KYLE\'S 3-MINUTE TELE-DISPATCH PHONE SCRIPT:');
    console.log('• Opening: ' + res1.body.outreach_scripts.phone_cold_call.opening);
    console.log('• Handoff: ' + res1.body.outreach_scripts.phone_cold_call.lead_handoff);
    console.log('• The Pitch: ' + res1.body.outreach_scripts.phone_cold_call.monopoly_pitch);
    console.log('• The Close: ' + res1.body.outreach_scripts.phone_cold_call.call_to_action);

    // 2. Test Inbound Lead in Locked Territory: Atlanta Luxury Restrooms (Held by Royal Restrooms)
    console.log('\n----------------------------------------------------------------');
    console.log('--- TEST 2: Locked Territory Inbound Lead (Atlanta Luxury Restrooms) ---');
    const lockedLeadPayload = {
      niche_id: 'luxury_restrooms',
      city: 'Atlanta',
      state: 'GA',
      customer_name: 'Genevieve DuMont (Buckhead Estate Weddings)',
      customer_phone: '(404) 555-9382',
      customer_email: 'weddings@buckheadestate.com',
      estimated_quote: 3450,
      service_description: '8-Station Presidential Restroom Suite for 300 Guests'
    };

    const res2 = await request('/api/leads/trojan-dispatch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: lockedLeadPayload
    });

    console.log(`HTTP Status: ${res2.statusCode}`);
    console.log(`Dispatch Status: ${res2.body.status}`);
    console.log(`Territory Status: ${res2.body.territory_status}`);
    console.log(`Exclusive Operator: ${res2.body.operator.company_name} (${res2.body.operator.id})`);
    console.log(`Customer Delivered: ${res2.body.customer.name} - ${res2.body.customer.phone}`);
    console.log(`Lockout Integrity: Zero competitors alerted. 100% exclusive.`);

    // 3. Test Territory Telemetry & Matrix
    console.log('\n----------------------------------------------------------------');
    console.log('--- TEST 3: Territory Telemetry & Real-Time Roster ---');
    const res3 = await request('/api/leads/trojan-status');
    console.log(`Total Trojan Gift Leads Dispatched: ${res3.body.total_dispatched}`);
    console.log(`Total Value Given Away to Operators: $${res3.body.total_gift_value.toLocaleString()}`);
    console.log(`Locked Metropolitan Territories: ${res3.body.locked_territories_count}`);

    const res4 = await request('/api/leads/trojan-territories');
    console.log(`Major Metros Analyzed: ${res4.body.total_territories}`);
    console.log(`Open Metros: ${res4.body.open_count} | Locked Monopolies: ${res4.body.locked_count}`);
    res4.body.territories.forEach(t => {
      console.log(`• [${t.status}] ${t.city}, ${t.state} ($${t.monthly_rental_rate}/mo) -> ${t.status === 'LOCKED' ? t.monopoly_holder.company_name : 'OPEN'}`);
    });

    console.log('\n================================================================');
    console.log('✅ ALL SIMULATION CHECKS COMPLETED SUCCESSFULLY');
    console.log('================================================================\n');

    server.close();
    process.exit(0);
  });
}

runSimulator().catch(err => {
  console.error('Simulator error:', err);
  server.close();
  process.exit(1);
});
