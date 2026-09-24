import os
import re

SERVER_JS_PATH = os.path.join(os.path.dirname(__file__), 'apps', 'web', 'server.js')

with open(SERVER_JS_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the problematic supabase init
old_init = "const supabase = createClient(process.env.SUPABASE_URL || '', process.env.SUPABASE_ANON_KEY || '');"

new_init = """
const SUPABASE_URL = process.env.SUPABASE_URL || 'https://wimgimqgkgluwewictyq.supabase.co';
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpbWdpbXFna2dsdXdld2ljdHlxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTAxMjQ2ODcsImV4cCI6MjEwNTcwMDY4N30._3FJQd1AvhsrrfAfzATrkdLUSbvWRAFQxrf0p-IUKc0';
const supabase = (SUPABASE_URL && SUPABASE_ANON_KEY) ? createClient(SUPABASE_URL, SUPABASE_ANON_KEY) : null;
"""

content = content.replace(old_init, new_init)

# Fix the condition inside /api/bookings/deposit
content = content.replace("if (process.env.SUPABASE_URL) {", "if (supabase) {")

with open(SERVER_JS_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("Server.js patched for Vercel boot failure.")
