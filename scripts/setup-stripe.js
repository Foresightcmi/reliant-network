/**
 * Reliant Verified - Automated Stripe Setup & Diagnostic Assistant
 * 
 * Run with: node scripts/setup-stripe.js
 * 
 * This tool:
 * 1. Reads your .env file
 * 2. Connects to Stripe to verify your API credentials
 * 3. Shows account status, business name, and mode (Test vs Live)
 * 4. Generates a live test checkout link to verify payment flow
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const ENV_PATH = path.join(__dirname, '..', '.env');

function loadEnv() {
  const env = {};
  if (fs.existsSync(ENV_PATH)) {
    const raw = fs.readFileSync(ENV_PATH, 'utf8');
    raw.split(/\r?\n/).forEach(line => {
      line = line.trim();
      if (line && !line.startsWith('#')) {
        const idx = line.indexOf('=');
        if (idx > 0) {
          const k = line.slice(0, idx).trim();
          const v = line.slice(idx + 1).trim().replace(/^['"]|['"]$/g, '');
          env[k] = v;
          process.env[k] = v;
        }
      }
    });
  }
  return env;
}

function saveEnv(updates) {
  let existingContent = fs.existsSync(ENV_PATH) ? fs.readFileSync(ENV_PATH, 'utf8') : '';
  const lines = existingContent.split(/\r?\n/);
  const keysUpdated = new Set();

  const newLines = lines.map(line => {
    const trimmed = line.trim();
    if (trimmed && !trimmed.startsWith('#')) {
      const idx = trimmed.indexOf('=');
      if (idx > 0) {
        const k = trimmed.slice(0, idx).trim();
        if (updates[k] !== undefined) {
          keysUpdated.add(k);
          return `${k}=${updates[k]}`;
        }
      }
    }
    return line;
  });

  for (const [k, v] of Object.entries(updates)) {
    if (!keysUpdated.has(k)) {
      newLines.push(`${k}=${v}`);
    }
  }

  fs.writeFileSync(ENV_PATH, newLines.join('\n').trim() + '\n', 'utf8');
}

async function run() {
  console.log('\n======================================================');
  console.log('💳 RELIANT VERIFIED - STRIPE EASY SETUP ASSISTANT');
  console.log('======================================================\n');

  let env = loadEnv();
  let secretKey = process.env.STRIPE_SECRET_KEY;
  let publishableKey = process.env.STRIPE_PUBLISHABLE_KEY;

  if (!secretKey) {
    console.log('⚠️  No STRIPE_SECRET_KEY found in .env\n');
    console.log('👉 To get your keys in 10 seconds:');
    console.log('   1. Open: https://dashboard.stripe.com/test/apikeys');
    console.log('   2. Reveal and copy your "Secret key" (starts with sk_test_... or sk_live_...)');
    console.log('   3. Copy your "Publishable key" (starts with pk_test_... or pk_live_...)\n');

    if (!process.stdin.isTTY || process.argv.includes('--check')) {
      console.log('ℹ️  Setup instructions:');
      console.log('   Add the following to your .env file:');
      console.log('   STRIPE_SECRET_KEY=sk_test_your_key_here');
      console.log('   STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here\n');
      console.log('   Or add them in Vercel: Project Settings -> Environment Variables');
      console.log('======================================================\n');
      return;
    }

    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

    const askKey = () => new Promise(resolve => {
      rl.question('Paste your STRIPE_SECRET_KEY (or press Enter to skip): ', answer => {
        resolve(answer.trim());
      });
    });

    const askPubKey = () => new Promise(resolve => {
      rl.question('Paste your STRIPE_PUBLISHABLE_KEY (optional, press Enter to skip): ', answer => {
        resolve(answer.trim());
      });
    });

    secretKey = await askKey();
    if (secretKey) {
      publishableKey = await askPubKey();
      const updates = { STRIPE_SECRET_KEY: secretKey };
      if (publishableKey) updates.STRIPE_PUBLISHABLE_KEY = publishableKey;
      saveEnv(updates);
      console.log('\n✅ Successfully saved keys to .env!');
      process.env.STRIPE_SECRET_KEY = secretKey;
      if (publishableKey) process.env.STRIPE_PUBLISHABLE_KEY = publishableKey;
    }
    rl.close();
  }

  if (!secretKey) {
    console.log('\nℹ️  Setup skipped for now.');
    console.log('   When you are ready, you can simply add these two lines to your .env file:');
    console.log('   STRIPE_SECRET_KEY=sk_test_your_secret_key_here');
    console.log('   STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here');
    console.log('\n   Or add them in your Vercel Project Dashboard:');
    console.log('   Settings -> Environment Variables -> Add STRIPE_SECRET_KEY');
    console.log('======================================================\n');
    return;
  }

  // Verify key with Stripe API
  console.log('🔍 Testing connection to Stripe API...');
  try {
    const Stripe = require('stripe');
    const stripe = new Stripe(secretKey);

    const account = await stripe.accounts.retrieve();
    const mode = secretKey.startsWith('sk_live_') ? '🟢 LIVE PRODUCTION' : '🟡 TEST / SANDBOX';

    console.log('\n🎉 STRIPE CONNECTION SUCCESSFUL!');
    console.log('------------------------------------------------------');
    console.log(` Mode:              ${mode}`);
    console.log(` Account ID:        ${account.id}`);
    console.log(` Business Name:     ${account.business_profile?.name || account.settings?.dashboard?.display_name || 'Reliant Verified Network'}`);
    console.log(` Country:           ${account.country || 'US'}`);
    console.log(` Default Currency:  ${(account.default_currency || 'usd').toUpperCase()}`);
    console.log(` Charges Enabled:   ${account.charges_enabled ? 'YES' : 'NO'}`);
    console.log('------------------------------------------------------');

    // Create a live test checkout session
    console.log('\n🧪 Generating a test 15% Escrow Deposit Checkout Session...');
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      mode: 'payment',
      line_items: [{
        price_data: {
          currency: 'usd',
          unit_amount: 52500, // $525.00
          product_data: {
            name: '15% Escrow Reservation Deposit (Test Simulation)',
            description: 'Reliant Verified Escrow Guarantee Test Session'
          }
        },
        quantity: 1
      }],
      success_url: 'https://www.reliantverified.com/receipt/BK-REL-2026-TEST?session_id={CHECKOUT_SESSION_ID}',
      cancel_url: 'https://www.reliantverified.com/'
    });

    console.log('✅ Test Checkout URL created:');
    console.log(`\n🔗 ${session.url}\n`);
    console.log('👉 You can Ctrl+Click this link to test your checkout experience in your browser!');
    console.log('======================================================\n');

  } catch (err) {
    console.error('\n❌ Stripe Connection Failed:');
    console.error(`   ${err.message}`);
    console.log('\n👉 Check that your STRIPE_SECRET_KEY in .env is correct and starts with sk_test_ or sk_live_');
    console.log('======================================================\n');
  }
}

if (require.main === module) {
  run();
}

module.exports = { loadEnv, saveEnv };
