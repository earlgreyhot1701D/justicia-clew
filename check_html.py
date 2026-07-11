import re
content = open('frontend/index.html', 'r', encoding='utf-8').read()

# Check tabindex on the four headings
for hid in ['title', 'loadingTitle', 'questionTitle', 'asked']:
    pattern = rf'id="{hid}"[^>]*tabindex="-1"'
    match = re.search(pattern, content)
    print(f'  {hid}: tabindex="-1" {"PRESENT" if match else "MISSING"}')

# Check ES button disabled
es_match = re.search(r'id="es"[^>]*disabled[^>]*aria-disabled="true"', content)
print(f'  ES button disabled+aria-disabled: {"PRESENT" if es_match else "MISSING"}')
