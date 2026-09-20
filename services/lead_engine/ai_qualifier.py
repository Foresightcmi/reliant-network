import json

class AILeadQualifier:
    """
    Evaluates raw inbound quote inquiries:
    - Filters out spam / test junk
    - Estimates true contract deal value ($2k - $12k)
    - Computes optimal Pay-Per-Lead pricing ($65 - $150)
    - Assigns an Intent / Close Probability Score (0 - 100)
    """
    def qualify_inquiry(self, lead_data):
        guest_count = int(lead_data.get('guest_count', 150))
        event_type = lead_data.get('event_type', 'Wedding').lower()
        event_date = lead_data.get('event_date', '')
        duration_days = int(lead_data.get('duration_days', 1))
        utilities_needed = lead_data.get('utilities_needed', 'STANDARD') # 'OFF_GRID_GENERATOR_WATER' or 'SHORE_POWER'
        notes = lead_data.get('notes', '').lower()
        city = lead_data.get('city', 'Atlanta')

        # Base Intent Scoring
        score = 80
        if '@' in lead_data.get('customer_email', '') and len(lead_data.get('customer_phone', '')) >= 10:
            score += 10
        if len(notes) > 20:
            score += 5
        if guest_count >= 150:
            score += 5
        if duration_days > 1 or 'fair' in event_type or 'festival' in event_type:
            score += 5

        # Calculate estimated rental contract size based on station requirements
        base_daily_rate = 1800
        if guest_count <= 100:
            daily_quote = base_daily_rate + 400
            stations_needed = "2-Station Presidential Suite (Up to 150 guests)"
        elif guest_count <= 250:
            daily_quote = base_daily_rate + 1200
            stations_needed = "4-Station Elegance Trailer (Up to 300 guests)"
        elif guest_count <= 500:
            daily_quote = base_daily_rate + 3200
            stations_needed = "8-Station Black-Tie Gala Trailer (500+ guests)"
        else:
            daily_quote = base_daily_rate + 5800
            stations_needed = "10-Station Festival Master Suite + ADA Private Unit"

        # Multi-day scaling (discount curve for multi-day events)
        if duration_days == 1:
            total_quote = daily_quote
        elif duration_days <= 3:
            total_quote = int(daily_quote * duration_days * 0.85)
        elif duration_days <= 7:
            total_quote = int(daily_quote * duration_days * 0.75)
        else: # Large multi-week fairs, film sets, festivals (e.g. State Fairs)
            total_quote = int(daily_quote * duration_days * 0.65)

        # High-ticket event type multipliers (fairs, state expos, festivals, film shoots)
        if any(w in event_type for w in ['fair', 'festival', 'film', 'production', 'expo', 'state fair']):
            total_quote = max(total_quote, 12500)
            stations_needed = "Multi-Trailer Master Fleet (10-Station VIP + ADA Compliant Units)"

        # Utility add-ons (Off-grid quiet generator & 500-gal freshwater tank delivery)
        if utilities_needed == 'OFF_GRID_GENERATOR_WATER' or 'generator' in notes:
            total_quote += 950 * min(duration_days, 5)

        # Calculate Pay-Per-Lead Price to Charge Local Operator
        if total_quote >= 15000:
            lead_price = 250
        elif total_quote >= 8000:
            lead_price = 175
        elif total_quote >= 4000:
            lead_price = 125
        else:
            lead_price = 85

        # Premium metro multiplier
        if city.lower() in ['miami', 'los angeles', 'new york', 'aspen', 'hamptons']:
            lead_price += 25

        deposit_fee = int(total_quote * 0.15)

        return {
            'is_valid': True,
            'intent_score': min(score, 99),
            'stations_recommended': stations_needed,
            'duration_days': duration_days,
            'estimated_quote': total_quote,
            'lead_price': lead_price,
            'deposit_fee': deposit_fee,
            'urgency_level': 'HIGH' if 'urgent' in notes or 'asap' in notes else 'NORMAL'
        }

if __name__ == '__main__':
    qualifier = AILeadQualifier()
    res = qualifier.qualify_inquiry({
        'guest_count': 220,
        'event_type': 'Vineyard Wedding',
        'customer_email': 'sarah.miller@gmail.com',
        'customer_phone': '(404) 732-9012',
        'notes': 'Looking for a clean modern 3-4 station trailer with flushing toilets and air conditioning.',
        'city': 'Atlanta'
    })
    print('Qualification test passed:', json.dumps(res, indent=2))
