const app = require('./server');
const http = require('http');

async function runTests() {
  const server = http.createServer(app);
  await new Promise(resolve => server.listen(0, resolve));
  const port = server.address().port;
  const baseUrl = `http://127.0.0.1:${port}`;

  console.log(`🧪 Testing WebMCP Gateway on ${baseUrl}...`);
  let passed = 0;
  let failed = 0;

  async function check(name, fn) {
    try {
      await fn();
      console.log(`  ✅ PASS: ${name}`);
      passed++;
    } catch (err) {
      console.error(`  ❌ FAIL: ${name} -> ${err.message}`);
      failed++;
    }
  }

  // 1. Discovery manifests
  await check('GET /.well-known/webmcp.json returns valid manifest', async () => {
    const res = await fetch(`${baseUrl}/.well-known/webmcp.json`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    if (!data.tools || data.tools.length !== 7) throw new Error(`Expected 7 tools, got ${data.tools?.length}`);
  });

  await check('GET /.well-known/mcp.json returns valid manifest', async () => {
    const res = await fetch(`${baseUrl}/.well-known/mcp.json`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    if (!data.tools || data.tools.length !== 7) throw new Error(`Expected 7 tools, got ${data.tools?.length}`);
  });

  await check('GET /api/webmcp/tools returns tools array', async () => {
    const res = await fetch(`${baseUrl}/api/webmcp/tools`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    if (!data.success || !Array.isArray(data.tools)) throw new Error('Invalid tools payload');
  });

  // 2. JSON-RPC 2.0 tools/list
  await check('POST /api/webmcp JSON-RPC tools/list', async () => {
    const res = await fetch(`${baseUrl}/api/webmcp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        method: 'tools/list',
        id: 101
      })
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    if (data.id !== 101 || !data.result?.tools) throw new Error('Invalid JSON-RPC response');
  });

  // 3. JSON-RPC 2.0 tools/call: search_contractors
  await check('POST /api/webmcp tools/call: search_contractors (Atlanta restrooms)', async () => {
    const res = await fetch(`${baseUrl}/api/webmcp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        method: 'tools/call',
        params: {
          name: 'search_contractors',
          arguments: { city: 'Atlanta', niche_id: 'luxury_restrooms' }
        },
        id: 102
      })
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const parsed = JSON.parse(data.result.content[0].text);
    if (!parsed.vendors || parsed.vendors.length === 0) throw new Error('Expected vendors');
  });

  // 4. JSON-RPC 2.0 tools/call: estimate_commercial_project
  await check('POST /api/webmcp tools/call: estimate_commercial_project (crane)', async () => {
    const res = await fetch(`${baseUrl}/api/webmcp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        method: 'tools/call',
        params: {
          name: 'estimate_commercial_project',
          arguments: { vertical: 'heavy_crane_rigging', load_weight_lbs: 25000, lift_radius_ft: 60 }
        },
        id: 103
      })
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const parsed = JSON.parse(data.result.content[0].text);
    if (!parsed.minimum_recommended_tonnage) throw new Error('Expected crane tonnage estimate');
  });

  // 5. JSON-RPC 2.0 tools/call: request_commercial_quote
  await check('POST /api/webmcp tools/call: request_commercial_quote', async () => {
    const res = await fetch(`${baseUrl}/api/webmcp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        method: 'tools/call',
        params: {
          name: 'request_commercial_quote',
          arguments: {
            client_name: 'Alpha Logistics Inc',
            client_email: 'procurement@alphalogistics.com',
            client_phone: '404-555-0199',
            niche_id: 'commercial_cold_storage',
            project_city: 'Atlanta',
            project_state: 'GA',
            project_description: 'Need two 40ft sub-zero reefers for 6 months'
          }
        },
        id: 104
      })
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const parsed = JSON.parse(data.result.content[0].text);
    if (!parsed.lead_id) throw new Error('Expected lead_id generated');
  });

  server.close();
  console.log(`\n🏁 WebMCP Test Suite Complete: ${passed} PASSED, ${failed} FAILED`);
  if (failed > 0) process.exit(1);
}

runTests();
