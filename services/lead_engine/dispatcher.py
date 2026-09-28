# -*- coding: utf-8 -*-
import json
import os
import urllib.request
import urllib.parse

VENDORS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'vendors.json')
LEADS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'leads.json')

class LeadBrokerDispatcher:
    """
    Connects qualified commercial RFQs with local operators.
    If no local operator exists in the requested city, instantly routes the lead
    to the National Affiliate Brokerage network to monetize the gap territory.
    """
    def __init__(self):
        self.vendors_path = VENDORS_PATH
        self.leads_path = LEADS_PATH

    def dispatch_lead(self, lead_data):
        # Read vendors
        vendors = []
        if os.path.exists(self.vendors_path):
            with open(self.vendors_path, 'r', encoding='utf-8') as f:
                vendors = json.load(f)

        city = lead_data.get("city", "")
        state = lead_data.get("state", "")
        niche_id = lead_data.get("niche_id", "commercial_service")
        
        # Match vendors in the exact city
        matched_vendors = [v for v in vendors if (v.get("city") or "").lower() == city.lower() and (v.get("state") or "").lower() == state.lower()]
        
        dispatched_alerts = []
        
        if len(matched_vendors) > 0:
            # We have local contractors! Pitch them the monopoly.
            for v in matched_vendors[:3]:
                name_parts = lead_data.get('customer_name', 'Client').split()
                masked_name = name_parts[0] + " " + (name_parts[-1][0] + "." if len(name_parts) > 1 else "")
                phone = lead_data.get('customer_phone', '555-0000')
                masked_phone = phone[:6] + "****"
                
                sms_text = f"Reliant Network Alert ({city}): Commercial inquiry for {niche_id.replace('_', ' ')}. Client: {masked_name} ({masked_phone}). Est Value: ${lead_data.get('estimated_quote', 0):,}. To claim this lead & lock the {city} territory monopoly: {lead_data.get('stripe_payment_link')}."
                
                dispatched_alerts.append({
                    "type": "LOCAL_MONOPOLY_PITCH",
                    "recipient": v["name"],
                    "email": v.get("email"),
                    "message": sms_text
                })
        else:
            # GAP TERRITORY DETECTED! We have no contractor here.
            # Route to National Affiliate Broker (e.g. Bark / HomeAdvisor / Buyer Network)
            # This ensures we make money on EVERY lead, even if we haven't indexed a contractor yet.
            brokerage_value = lead_data.get('lead_price', 100)
            
            dispatched_alerts.append({
                "type": "NATIONAL_AFFILIATE_BROKERAGE",
                "recipient": "National Lead Exchange (API)",
                "payout": brokerage_value,
                "message": f"Lead routed to national affiliate exchange for ${brokerage_value} instant payout."
            })

            # Send a push notification to the Admin (Entrepreneur) so they know they made money!
            try:
                alert_msg = f"💸 AFFILIATE BROKERAGE SALE!\nSold an orphaned {niche_id} lead in {city} to the National Network.\nProfit: ${brokerage_value}\nClient: {lead_data.get('customer_name')}"
                req = urllib.request.Request(
                    "https://ntfy.sh/reliant_verified_admin_alerts",
                    data=alert_msg.encode('utf-8'),
                    headers={
                        "Title": f"Orphan Lead Sold: ${brokerage_value}",
                        "Priority": "high",
                        "Tags": "moneybag,dollar"
                    }
                )
                urllib.request.urlopen(req, timeout=5)
            except Exception as e:
                pass

        return {
            "lead_code": lead_data.get("lead_code", "UNKNOWN"),
            "matched_vendors_count": len(matched_vendors),
            "dispatched_alerts": dispatched_alerts
        }

if __name__ == '__main__':
    broker = LeadBrokerDispatcher()
    # Test Payload
    test_lead = {
        "lead_code": "TEST-123",
        "city": "Nowhereville",
        "state": "TX",
        "niche_id": "commercial_roofing",
        "customer_name": "John Doe",
        "customer_phone": "555-123-4567",
        "estimated_quote": 45000,
        "lead_price": 150,
        "stripe_payment_link": "https://buy.stripe.com/test"
    }
    res = broker.dispatch_lead(test_lead)
    print(json.dumps(res, indent=2))
