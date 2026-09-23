import os
import re

SERVER_JS_PATH = os.path.join(os.path.dirname(__file__), 'apps', 'web', 'server.js')

with open(SERVER_JS_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Supabase Client Initialization
supabase_init = """
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL || '', process.env.SUPABASE_ANON_KEY || '');
"""
content = re.sub(r"(const express = require\('express'\);)", r"\1\n" + supabase_init, content)

# 2. Rewrite /api/bookings/deposit to remove escrow and insert to Supabase
new_deposit_logic = """
app.post('/api/bookings/deposit', async (req, res) => {
  try {
    const {
      lead_code, customer_name, customer_email, customer_phone,
      city, state, event_date, guest_count, event_type, estimated_total, niche_id
    } = req.body;

    const totalEst = parseFloat(estimated_total) || 2800;
    const targetNiche = niche_id || 'luxury_restrooms';
    const bookingId = 'BK-REL-2026-' + Math.floor(100000 + Math.random() * 900000);

    // Get a local vendor to assign the lead to
    const vendors = readDataFile('vendors.json', []);
    const local = vendors.filter(v => (!city || v.city.toLowerCase() === (city || '').toLowerCase()) && v.niche_id === targetNiche);
    let assignedVendor = local.length > 0 ? local[Math.floor(Math.random() * local.length)] : { id: 'sys_fallback', name: "National Affiliate Network" };

    // Insert Lead into Supabase
    if (process.env.SUPABASE_URL) {
      await supabase.from('leads').insert([{
        id: bookingId,
        lead_code: lead_code || 'L-2026',
        niche_id: targetNiche,
        city: city || 'Metro',
        state: state || 'US',
        customer_name,
        customer_phone,
        customer_email,
        estimated_total: totalEst,
        assigned_vendor_id: assignedVendor.id !== 'sys_fallback' ? assignedVendor.id : null,
        expires_at: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString()
      }]);
    }

    // Success response - NO 15% ESCROW REQUIRED
    return res.json({
      success: true,
      booking_id: bookingId,
      lead_code: lead_code || 'L-2026',
      total_contract: totalEst,
      assigned_vendor: assignedVendor,
      message: 'Lead successfully captured and dispatched. 100% Free for the customer.'
    });

  } catch (error) {
    console.error('Lead capture error:', error);
    res.status(500).json({ error: error.message });
  }
});
"""

# Find the start of the deposit route and replace it
# Use regex to find app.post('/api/bookings/deposit' ... until the next app.post or app.get
content = re.sub(r"app\.post\('/api/bookings/deposit'.*?(?=app\.(get|post|delete))", new_deposit_logic, content, flags=re.DOTALL)

with open(SERVER_JS_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("Server.js successfully patched to remove escrow and integrate Supabase.")
