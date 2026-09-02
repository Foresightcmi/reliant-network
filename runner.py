import base64
with open('payload.b64', 'r') as f:
    code = base64.b64decode(f.read().strip()).decode('utf-8')
exec(code)
