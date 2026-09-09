import requests
from bs4 import BeautifulSoup
import markdownify
import sys

def scrape_url_to_markdown(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Remove useless tags
        for tag in soup(['script', 'style', 'nav', 'footer', 'noscript', 'iframe']):
            tag.decompose()
            
        # Try to find main content area
        main_content = soup.find('main') or soup.find('article') or soup.body
        if not main_content:
            return ""
            
        md = markdownify.markdownify(str(main_content), heading_style="ATX")
        
        # Clean up excessive newlines
        lines = [line.strip() for line in md.split('\n')]
        clean_md = '\n'.join([line for line in lines if line])
        return clean_md
        
    except Exception as e:
        print(f"[Error] Crawl failed for {url}: {e}")
        return ""

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(scrape_url_to_markdown(sys.argv[1]))
