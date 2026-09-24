import urllib.request
import json
import urllib.error
import time

def run_health_check():
    print("Initializing Reliant Verified Live Production Health Monitor...")
    
    endpoints = [
        {"name": "Frontend Edge HTML", "url": "https://www.reliantverified.com/"},
        {"name": "Local SEO Hub", "url": "https://www.reliantverified.com/cost/atlanta"},
        {"name": "Stripe/DB Backend Engine", "url": "https://www.reliantverified.com/api/stripe/status"}
    ]
    
    all_healthy = True
    
    for ep in endpoints:
        try:
            req = urllib.request.Request(ep['url'], headers={'User-Agent': 'Reliant-Health-Probe/1.0'})
            res = urllib.request.urlopen(req, timeout=10)
            status = res.getcode()
            if status == 200:
                print(f"[OK] {ep['name']} responds 200.")
            else:
                print(f"[ERROR] {ep['name']} responded with status {status}")
                all_healthy = False
        except urllib.error.URLError as e:
            print(f"[FATAL] {ep['name']} failed: {e.reason}")
            all_healthy = False
            
    if all_healthy:
        print("\n[SUCCESS] SYSTEM HEALTHY: The lead-generation engine and Edge API are 100% operational.")
        return True
    else:
        print("\n[FAILURE] SYSTEM DEGRADED: A critical endpoint is failing. Intervention required.")
        return False

if __name__ == "__main__":
    run_health_check()
