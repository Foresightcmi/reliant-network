import os

root_dir = 'C:/Users/fores/.gemini/antigravity/scratch/autonomous-directory-engine'
replacements = {
    'The Reliant Network': 'The Reliant Network',
    'reliantverified.com': 'reliantverified.com',
    'Reliant<span class="text-amber-400">Network</span>': 'Reliant<span class="text-amber-400">Network</span>',
    'quotes@reliantverified.com': 'quotes@reliantverified.com'
}

for subdir, dirs, files in os.walk(root_dir):
    if 'node_modules' in subdir or 'dist' in subdir or '.git' in subdir:
        continue
    for file in files:
        if file.endswith(('.html', '.py', '.md', '.json', '.js')):
            filepath = os.path.join(subdir, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                changed = False
                for k, v in replacements.items():
                    if k in content:
                        content = content.replace(k, v)
                        changed = True
                
                if changed:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f'Updated {filepath}')
            except Exception as e:
                print(f'Error reading {filepath}: {e}')
