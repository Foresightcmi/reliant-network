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
    while injecting LSI keywords to bolster semantic relevance.
    """
    faqs = [
        {
            "question": f"How much does {service} typically cost in {city}, {state}?",
            "answer": f"On average, clients in {city} can expect to pay around ${avg_cost:,} for premium {service}. However, prices can fluctuate depending on availability, specific requirements, and the season. Our verified local network ensures you receive transparent, competitive quotes without hidden fees."
        },
        {
            "question": f"How do you verify the {service} providers in {city}?",
            "answer": f"We rigorously vet every {service} contractor in {city} for proper licensing, up-to-date insurance, and a proven track record of reliable execution. We prioritize operators who specialize in high-end, compliant services so you don't have to risk your project or peace of mind."
        },
        {
            "question": f"Can I get a same-day or emergency {service} quote in {city}?",
            "answer": f"Yes. We understand that emergencies happen. Our network connects you directly to responsive {service} professionals in the {city} area who can provide rapid deployment, 24/7 support, and immediate estimates."
        }
    ]
    
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": []
    }
    
    html_out = '<div class="mt-10 mb-6"><h2 class="text-2xl font-bold text-white mb-4">Frequently Asked Questions</h2><div class="space-y-4">'
    
    for faq in faqs:
        schema["mainEntity"].append({
            "@type": "Question",
            "name": faq["question"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["answer"]
            }
        })
        html_out += f'<div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl"><h3 class="text-lg font-bold text-amber-400">{faq["question"]}</h3><p class="text-slate-300 text-sm mt-2 leading-relaxed">{faq["answer"]}</p></div>'
        
    html_out += '</div></div>'
    
    return json.dumps(schema, indent=2), html_out
