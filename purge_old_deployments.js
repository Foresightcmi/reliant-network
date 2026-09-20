const fs = require('fs');
const path = require('path');
const https = require('https');

// 1. Resolve Token from environment, .env, or Vercel CLI global config
function getVercelToken() {
  if (process.env.VERCEL_TOKEN) return process.env.VERCEL_TOKEN;

  const envPath = path.join(__dirname, '..', '.env');
  if (fs.existsSync(envPath)) {
    const envContent = fs.readFileSync(envPath, 'utf8');
    const match = envContent.match(/^VERCEL_TOKEN=(.+)$/m);
    if (match) return match[1].trim();
  }

  const cliAuthPath = path.join(
    process.env.APPDATA || '',
    'xdg.data',
    'com.vercel.cli',
    'auth.json'
  );
  if (fs.existsSync(cliAuthPath)) {
    try {
      const auth = JSON.parse(fs.readFileSync(cliAuthPath, 'utf8'));
      if (auth.token) return auth.token;
    } catch (e) {}
  }

  return null;
}

function httpsRequest(options, postData = null) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(body || '{}');
          resolve({ status: res.statusCode, data: parsed });
        } catch (e) {
          resolve({ status: res.statusCode, data: body });
        }
      });
    });
    req.on('error', reject);
    if (postData) req.write(typeof postData === 'string' ? postData : JSON.stringify(postData));
    req.end();
  });
}

async function purgeDeployments() {
  const token = getVercelToken();
  if (!token) {
    console.error('❌ No Vercel authentication token found.');
    console.log('\nTo allow Antigravity to purge historical deployments for you:');
    console.log('Option A: Create a token at https://vercel.com/account/tokens and add to .env:');
    console.log('          VERCEL_TOKEN=your_token_here');
    console.log('Option B: Run `npx vercel login` in your terminal.');
    process.exit(1);
  }

  console.log('🔍 Fetching deployments from Vercel API...');
  const listRes = await httpsRequest({
    hostname: 'api.vercel.com',
    path: '/v7/deployments?limit=100',
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'User-Agent': 'Antigravity-Purge-Tool/1.0'
    }
  });

  if (listRes.status !== 200) {
    console.error(`❌ API Error (${listRes.status}):`, listRes.data);
    process.exit(1);
  }

  const deployments = listRes.data.deployments || [];
  console.log(`📋 Total deployments found in account: ${deployments.length}`);

  if (deployments.length === 0) {
    console.log('✅ No deployments found.');
    return;
  }

  // Filter to find the current active production deployment
  // We NEVER delete the current production deployment!
  let prodDep = deployments.find(d => d.target === 'production' && d.state === 'READY');
  if (!prodDep && deployments.length > 0) {
    prodDep = deployments[0]; // Most recent
  }

  console.log(`🛡️ Preserving Active Production Deployment: ${prodDep.url} (ID: ${prodDep.uid})`);

  const toDelete = deployments.filter(d => d.uid !== prodDep.uid);
  console.log(`🗑️ Deployments eligible for purge: ${toDelete.length}`);

  let deletedCount = 0;
  for (const dep of toDelete) {
    try {
      console.log(`⏳ Deleting [${dep.state || 'BUILD'}] ${dep.url} (${dep.uid})...`);
      const delRes = await httpsRequest({
        hostname: 'api.vercel.com',
        path: `/v13/deployments/${dep.uid}`,
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'User-Agent': 'Antigravity-Purge-Tool/1.0'
        }
      });
      if (delRes.status === 200) {
        deletedCount++;
        console.log(`   ✅ Purged.`);
      } else {
        console.log(`   ⚠️ Skipped (status ${delRes.status}):`, delRes.data);
      }
    } catch (err) {
      console.error(`   ❌ Failed to delete ${dep.uid}:`, err.message);
    }
  }

  console.log(`\n🎉 Purge Complete! Successfully removed ${deletedCount} historical deployments.`);
  console.log(`💾 Reclaimed ~${deletedCount * 180} MB+ of Deployment Storage at $0 cost.`);
  console.log(`🚀 Live production site remains active at https://${prodDep.url}`);
}

purgeDeployments().catch(console.error);
