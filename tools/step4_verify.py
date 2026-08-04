# -*- coding: utf-8 -*-
"""Step 4: independent check of the packed data.

  a) known city coordinates must land in the expected country
  b) every country's stored inner point must be inside its own polygon
  c) country count / name sanity
"""
import json, io, sys

d = json.load(io.open('data.json', encoding='utf-8'))
Q = d['s']

# rebuild absolute rings from the delta encoding, same as the browser does
def rings_of(country):
    out = []
    for poly in country['g']:
        rr = []
        for enc in poly:
            n = len(enc) // 2
            x, y = enc[0], enc[1]
            pts = [(x / Q, y / Q)]
            for i in range(1, n):
                x += enc[i * 2]; y += enc[i * 2 + 1]
                pts.append((x / Q, y / Q))
            rr.append(pts)
        out.append(rr)
    return out

def in_poly(px, py, poly):
    inside = False
    for ring in poly:
        n = len(ring); j = n - 1
        for i in range(n):
            xi, yi = ring[i]; xj, yj = ring[j]
            if (yi > py) != (yj > py):
                xc = (xj - xi) * (py - yi) / (yj - yi) + xi
                if px < xc:
                    inside = not inside
            j = i
    return inside

geo = {c['i']: rings_of(c) for c in d['c']}
byid = {c['i']: c for c in d['c']}

def locate(lon, lat):
    hits = []
    for cid, parts in geo.items():
        for poly in parts:
            if in_poly(lon, lat, poly):
                hits.append(cid)
                break
    return hits

CITIES = [
    ('Ankara',        32.85,  39.93, 'turkey'),
    ('Istanbul',      28.98,  41.01, 'turkey'),
    ('Paris',          2.35,  48.86, 'france'),
    ('Berlin',        13.40,  52.52, 'germany'),
    ('Madrid',        -3.70,  40.42, 'spain'),
    ('Rome',          12.50,  41.90, 'italy'),
    ('Warsaw',        21.01,  52.23, 'poland'),
    ('Moscow',        37.62,  55.75, 'russia'),
    ('Cairo',         31.24,  30.04, 'egypt'),
    ('Nairobi',       36.82,  -1.29, 'kenya'),
    ('Pretoria',      28.19, -25.75, 'south-africa'),
    ('Lagos',          3.38,   6.52, 'nigeria'),
    ('Brasilia',     -47.88, -15.79, 'brazil'),
    ('Buenos Aires',  -58.38, -34.60, 'argentina'),
    ('Santiago',      -70.65, -33.45, 'chile'),
    ('Bogota',        -74.07,   4.71, 'colombia'),
    ('Mexico City',   -99.13,  19.43, 'mexico'),
    ('Denver',       -104.99,  39.74, 'united-states-of-america'),
    ('Ottawa',        -75.70,  45.42, 'canada'),
    ('Beijing',       116.41,  39.90, 'people-s-republic-of-china'),
    ('Tokyo',         139.69,  35.69, 'japan'),
    ('New Delhi',      77.21,  28.61, 'india'),
    ('Jakarta',       106.85,  -6.21, 'indonesia'),
    ('Canberra',      149.13, -35.28, 'australia'),
    ('Wellington',    174.78, -41.29, 'new-zealand'),
    ('Riyadh',         46.72,  24.69, 'saudi-arabia'),
    ('Tehran',         51.39,  35.69, 'iran'),
    ('Astana',         71.43,  51.13, 'kazakhstan'),
    ('Kyiv',           30.52,  50.45, 'ukraine'),
    ('Oslo',           10.75,  59.91, 'norway'),
    ('Ulaanbaatar',   106.92,  47.89, 'mongolia'),
    ('Kinshasa',       15.31,  -4.32, 'democratic-republic-of-the-congo'),
    ('Havana',        -82.38,  23.13, 'cuba'),
    ('Tel Aviv',       34.78,  32.08, 'israel'),
    ('Reykjavik',     -21.94,  64.15, 'iceland'),
]

print('--- a) city -> country')
fails = 0
for name, lon, lat, expect in CITIES:
    hits = locate(lon, lat)
    ok = expect in hits
    if not ok:
        fails += 1
        got = ', '.join(byid[h]['en'] for h in hits) or '(none)'
        print('  FAIL %-14s expected %-34s got: %s' % (name, expect, got))
print('  %d/%d cities correct' % (len(CITIES) - fails, len(CITIES)))

print('--- b) inner point inside own shape')
bad_inner = []
for c in d['c']:
    px, py = c['p'][0] / Q, c['p'][1] / Q
    if not any(in_poly(px, py, poly) for poly in geo[c['i']]):
        bad_inner.append(c['en'])
print('  outside own polygon: %d %s' % (len(bad_inner), bad_inner[:15]))

print('--- c) sanity')
print('  countries        :', len(d['c']))
ids = [c['i'] for c in d['c']]
print('  duplicate ids    :', len(ids) - len(set(ids)))
names_tr = [c['tr'] for c in d['c']]
print('  duplicate tr name:', len(names_tr) - len(set(names_tr)))
print('  empty geometry   :', sum(1 for c in d['c'] if not c['g']))

sys.exit(1 if (fails or bad_inner) else 0)
