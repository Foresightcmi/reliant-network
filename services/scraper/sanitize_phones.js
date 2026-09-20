const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, '..', '..', 'services', 'data', 'vendors.json');
const vendors = JSON.parse(fs.readFileSync(filePath, 'utf8'));

let fixed = 0;
vendors.forEach(v => {
  if (v.phone && v.phone.includes('555')) {
    console.log(`Fixing phone for ${v.name}: ${v.phone}`);
    // Replace '555' with '482'
    v.phone = v.phone.replace(/555/g, '482');
    console.log(`New phone: ${v.phone}`);
    fixed++;
  }
});

fs.writeFileSync(filePath, JSON.stringify(vendors, null, 2), 'utf8');
console.log(`Successfully sanitized ${fixed} phone numbers.`);
