const fs = require('fs');
const path = require('path');
const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY);
const vendorsFile = path.join(__dirname, 'services', 'data', 'vendors.json');

async function seed() {
  const data = JSON.parse(fs.readFileSync(vendorsFile, 'utf8'));
  const payload = data.map(v => ({
    id: v.id,
    niche_id: v.niche_id || 'luxury_restrooms',
    name: v.name,
    city: v.city || 'Metro',
    state: v.state || 'US',
    phone: v.phone || '',
    email: v.email || '',
    website: v.website || '',
    min_price: v.min_price || 0,
    max_price: v.max_price || 0,
    stripe_account_id: v.stripe_account_id || '',
    monopoly_active: false
  }));

  console.log(`Uploading ${payload.length} vendors to Supabase...`);
  
  const batchSize = 50;
  for (let i = 0; i < payload.length; i += batchSize) {
    const batch = payload.slice(i, i + batchSize);
    const { error } = await supabase.from('vendors').upsert(batch);
    if (error) {
      console.error('Error inserting batch:', error);
    } else {
      console.log(`Inserted batch ${Math.floor(i / batchSize) + 1}`);
    }
  }
  
  console.log('Supabase Data Migration Complete!');
}

seed();
