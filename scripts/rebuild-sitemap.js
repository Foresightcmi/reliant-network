const fs = require('fs');
const path = require('path');

const sitemapPath = path.join(__dirname, '..', 'apps', 'web', 'public', 'sitemap.xml');
const content = fs.readFileSync(sitemapPath, 'utf8');

// Extract all existing locs
const locRegex = /<loc>(.*?)<\/loc>/g;
let match;
const existingLocs = new Set();
while ((match = locRegex.exec(content)) !== null) {
  existingLocs.add(match[1].trim());
}
console.log('Existing loc count:', existingLocs.size);

const stateFiles = fs.readdirSync(path.join(__dirname, '..', 'apps', 'web', 'public', 'state')).filter(f => f.endsWith('.html'));
const stateSlugs = stateFiles.map(f => f.replace('.html', '')).sort();

const verticalHubs = [
  'cold-storage',
  'commercial-hvac',
  'chillers',
  'cranes',
  'senior-care',
  'staying-in-place',
  'power',
  'machinery-moving',
  'senior-downsizing',
  'wheelchair-vans',
  'terms',
  'privacy',
  'refund-policy'
];

const priorityUrls = [
  'https://www.reliantverified.com/',
  'https://www.reliantverified.com/#directory',
  'https://www.reliantverified.com/#metros',
  ...verticalHubs.map(h => 'https://www.reliantverified.com/' + h),
  ...stateSlugs.map(s => 'https://www.reliantverified.com/state/' + s)
];

const allUrls = new Set([...priorityUrls, ...existingLocs]);
console.log('Total unique URLs after adding all states and hubs:', allUrls.size);

let xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
for (const u of allUrls) {
  let changefreq = 'weekly';
  let prio = '0.8';
  if (u === 'https://www.reliantverified.com/' || u.endsWith('#directory')) {
    changefreq = 'daily';
    prio = '1.0';
  } else if (u.includes('/state/') || verticalHubs.some(h => u.endsWith('/' + h))) {
    changefreq = 'weekly';
    prio = '0.9';
  }
  xml += '  <url>\n    <loc>' + u + '</loc>\n    <changefreq>' + changefreq + '</changefreq>\n    <priority>' + prio + '</priority>\n  </url>\n';
}
xml += '</urlset>\n';

fs.writeFileSync(sitemapPath, xml, 'utf8');
console.log('Successfully wrote updated sitemap.xml with', allUrls.size, 'URLs!');
