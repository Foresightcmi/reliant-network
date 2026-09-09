import sqlite3
import json
import time
import os
from deep_enrichment_crawler import scrape_url_to_markdown
from google import genai

DB_PATH = 'services/data/directory.db'

def ensure_column():
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute('ALTER TABLE vendors ADD COLUMN enriched_content TEXT')
        print('[Enrichment] Added enriched_content column to DB')
    except sqlite3.OperationalError:
        pass
    try:
        conn.execute('ALTER TABLE vendors ADD COLUMN trust_badges TEXT')
        print('[Enrichment] Added trust_badges column to DB')
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()

def generate_seo_profile(company_name, markdown_content):
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print('[Enrichment] Error: GEMINI_API_KEY not found in environment.')
        return None
        
    client = genai.Client(api_key=api_key)
    prompt = f"""You are an elite SEO copywriter. I am providing you with the raw markdown text scraped directly from the official website of '{company_name}'.
    
    RAW WEBSITE DATA:
    {markdown_content[:6000]}
    
    YOUR TASK:
    Write a highly detailed, 500-800 word SEO-optimized company profile for this business. 
    Focus on their specific services, equipment, history, and service area based ONLY on the provided text.
    Format the output in clean Markdown with H2 and H3 tags. Do not include any generic placeholder text."""
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f'[Enrichment] AI Generation failed: {e}')
        return None

def extract_trust_badges(markdown_content):
    content_lower = markdown_content.lower()
    badges = []
    if any(k in content_lower for k in ['insured', 'liability', 'coverage']):
        badges.append('Fully Insured')
    if any(k in content_lower for k in ['license', 'licensed', 'permits']):
        badges.append('State Licensed')
    if any(k in content_lower for k in ['osha', 'safety certified', 'nccco', 'certified']):
        badges.append('Safety Certified')
    if any(k in content_lower for k in ['bonded', 'guarantee']):
        badges.append('Bonded & Vetted')
    if not badges:
        badges = ['Reliant Verified Partner']
    return badges

def run_enrichment():
    ensure_column()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    vendors = conn.execute('SELECT id, name, website FROM vendors WHERE website IS NOT NULL AND website != "" AND (enriched_content IS NULL OR enriched_content = "")').fetchall()
    
    if not vendors:
        print('[Enrichment] No vendors need enrichment at this time.')
        return

    print(f'[Enrichment] Found {len(vendors)} vendors to enrich. Starting Deep Crawl...')
    
    for vendor in vendors:
        print(f"\n[Enrichment] Crawling {vendor['name']} at {vendor['website']}...")
        md_text = scrape_url_to_markdown(vendor['website'])
        
        if not md_text or len(md_text) < 100:
            print(f"[Enrichment] Failed to extract meaningful content from {vendor['website']}")
            continue
            
        print(f"[Enrichment] Extracted {len(md_text)} characters. Detecting Trust Badges...")
        badges = extract_trust_badges(md_text)
        print(f"[Enrichment] Detected Badges: {badges}")
        
        print(f"[Enrichment] Synthesizing SEO Profile via Gemini AI...")
        seo_profile = generate_seo_profile(vendor['name'], md_text)
        
        if seo_profile:
            conn.execute('UPDATE vendors SET enriched_content = ?, trust_badges = ? WHERE id = ?', (seo_profile, json.dumps(badges), vendor['id']))
            conn.commit()
            print(f"[Enrichment] Successfully saved profile & badges for {vendor['name']}!")
            
        time.sleep(2) # Respect rate limits
        
    conn.close()
    print('\n[Enrichment] Deep Enrichment Loop Complete!')

if __name__ == '__main__':
    run_enrichment()
