# -*- coding: utf-8 -*-
"""Step 3: inline data.json into template.html -> world-map-quiz.html"""
import io, os

TPL = 'template.html'
DATA = 'data.json'
OUT = r'C:\Users\Burak\Documents\MapHTML\world-map-quiz.html'

tpl = io.open(TPL, encoding='utf-8').read()
data = io.open(DATA, encoding='utf-8').read()

if '__MAP_DATA__' not in tpl:
    raise SystemExit('placeholder __MAP_DATA__ missing from template')

# JSON cannot contain "</script>", but be explicit about it anyway
assert '</script' not in data.lower(), 'data would break out of the script tag'

html = tpl.replace('__MAP_DATA__', data)
io.open(OUT, 'w', encoding='utf-8').write(html)
print('wrote', OUT)
print('size KB:', round(os.path.getsize(OUT) / 1024, 1))
