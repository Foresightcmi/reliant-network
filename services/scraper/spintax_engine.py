# -*- coding: utf-8 -*-
import random
import json

SPINTAX_TEMPLATES = {
    "h1": [
        "Find the Right {service} in {city}, {state} Without the Stress",
        "Trusted {service} Partners in {city} You Can Actually Rely On",
        "We've Vetted the Best {service} Providers in {city} For You",
        "Take the Guesswork Out of Finding {service} in {city}, {state}",
        "Connecting {city} with Premium, Reliable {service}",
        "Your Guide to Navigating {service} Options in {city}",
        "Local {city} Experts in {service}—Ready When You Need Them",
        "Discover Peace of Mind with Verified {service} in {city}"
    ],
    "intro": [
        "Making the right choice for {service} in {city} can feel completely overwhelming. We understand. That's why we've done the heavy lifting for you, hand-picking local partners who truly value your time, respect your budget, and deliver on their promises.",
        "When it comes to {service} in {city}, you shouldn't have to settle for second best. Whether you're managing a complex logistical project or making a highly sensitive decision, our curated network connects you instantly with compassionate, highly qualified professionals.",
        "We know that finding reliable {service} across {state} can be a massive headache. You need a partner who actually answers the phone, respects your timeline, and handles the details flawlessly. Let us introduce you to {city}'s most trusted and responsive operators.",
        "Your peace of mind is our absolute top priority. We built this platform because we saw how difficult it was for people in {city} to find transparent, high-quality {service}. Every single provider in our network has been rigorously evaluated for quality, safety, and reliability."
    ],
    "valueProp": [
        "Because we independently verify our {city} partners, you never have to worry about hidden fees, bait-and-switch tactics, or subpar service. We believe you deserve total transparency.",
        "We believe that navigating {service} shouldn't be a stressful burden. Our intelligent matching process ensures you are paired with professionals who genuinely listen to and understand your specific needs.",
        "By focusing exclusively on top-tier {service} providers in {city}, we protect you from the common pitfalls of unreliable contractors and untrustworthy agencies. You are in safe hands.",
        "Time is your most valuable asset. Stop spending hours reading fake online reviews or leaving unreturned voicemails—our direct network connects you immediately with the absolute best {service} experts in {city}, {state}."
    ]
}

def generate_spintax(data):
    """
    Generates dynamic, humanized SEO content optimized for psychological safety and trust.
    Replaces {service}, {city}, and {state} with actual data.
    """
    h1_tmpl = random.choice(SPINTAX_TEMPLATES["h1"])
    intro_tmpl = random.choice(SPINTAX_TEMPLATES["intro"])
    val_tmpl = random.choice(SPINTAX_TEMPLATES["valueProp"])
    
    for k, v in data.items():
        placeholder = "{" + k + "}"
        h1_tmpl = h1_tmpl.replace(placeholder, str(v))
        intro_tmpl = intro_tmpl.replace(placeholder, str(v))
        val_tmpl = val_tmpl.replace(placeholder, str(v))
        
    return {
        "h1": h1_tmpl,
        "intro": intro_tmpl,
        "valueProp": val_tmpl
    }

def generate_faq_schema(city, state, service, avg_cost):
    """
    Generates highly localized FAQPage JSON-LD schema for rich snippets in Google Search,
    while injecting Frey Chu's high-intent capacity, utility, and logistical search queries.
    """
    faqs = [
        {
            "question": f"How many luxury restroom trailer stalls do I need for my event in {city}?",
            "answer": f"For weddings and private events in {city}, industry standards recommend 1 restroom station per 50-75 guests for events lasting 4 to 6 hours. If alcohol is served, factor in a 20-25% increase in usage. A 2-station trailer comfortably supports up to 150 guests, a 4-station trailer accommodates up to 300 guests, and an 8-station or 10-station master unit handles 500 to 1,500+ attendees."
        },
        {
            "question": f"Do luxury restroom trailers require on-site water and electrical hookups in {city}?",
            "answer": f"Most luxury restroom trailers in {city} require 1 to 3 dedicated 20-amp 110V electrical circuits and a standard 3/4-inch garden hose connection providing 40-50 PSI. For remote venues, ranches, or parks without power or water, verified {city} operators provide onboard whisper-quiet generators and multi-hundred-gallon freshwater holding tanks."
        },
        {
            "question": f"How much does {service} typically cost in {city}, {state}?",
            "answer": f"On average, luxury restroom trailer rentals in {city} range between $1,400 to $4,500 per day depending on trailer size (2-station to 8-station suites) and amenities. Multi-day corporate rentals, film productions, and multi-week fairs receive volume discounts. Our verified {city} network provides instant, transparent quotes with zero hidden fees."
        },
        {
            "question": f"What is the difference between a luxury restroom trailer and a standard portable toilet?",
            "answer": f"Unlike chemical porta-potties, luxury restroom trailers provide private, individual locking suites featuring flushing porcelain toilets, running hot and cold water sinks, marble or granite countertops, LED vanity lighting, climate-controlled A/C and heating, and Bluetooth sound systems—delivering a 5-star hotel restroom experience."
        },
        {
            "question": f"What is the delivery radius and setup protocol for {city} operators?",
            "answer": f"Verified operators typically service a 50 to 100-mile radius around {city}. Setup includes precision laser hydraulic leveling, water line pressurization, electrical testing, and complete stocking with luxury hand soaps, plush paper towels, and mints prior to guest arrival."
        }
    ]
    
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": []
    }
    
    html_out = '<div class="mt-12 mb-8"><h2 class="text-2xl font-serif-title font-bold text-slate-900 mb-6">Frequently Asked Questions &amp; Event Logistics</h2><div class="space-y-4">'
    
    for faq in faqs:
        schema["mainEntity"].append({
            "@type": "Question",
            "name": faq["question"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["answer"]
            }
        })
        html_out += f'<div class="bg-white border border-slate-200 p-6 rounded-2xl shadow-xs"><h3 class="text-base font-bold text-slate-900">{faq["question"]}</h3><p class="text-slate-600 text-sm mt-2 leading-relaxed">{faq["answer"]}</p></div>'
        
    html_out += '</div></div>'
    
    return json.dumps(schema, indent=2), html_out
