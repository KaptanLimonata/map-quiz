# -*- coding: utf-8 -*-
"""Step 2: turn the simplified GeoJSON into the compact payload the HTML embeds.

Output shape (data.json):
  {
    "s": 500,                       # quantisation: value/500 == degrees
    "c": [ {i,tr,en,ct,b:[x0,y0,x1,y1],p:[x,y],r:0|1, g:[[ring,...],...]} ],
    "d": [ [ring,...], ... ]        # decorative territories, not clickable
  }
Each ring is a flat delta-encoded int array: [x0,y0,dx1,dy1,dx2,dy2,...].
"""
import json, io, math

SRC = 'simplified.geojson'
DST = 'data.json'
SCALE = 500                 # 1/500 deg == 0.002 deg, matches mapshaper precision

# A part smaller than this (in square degrees) is dropped, unless it is the
# country's largest part - every country keeps at least its main landmass.
MIN_PART_AREA = 0.020       # ~120 km2 near the equator
MIN_DECOR_AREA = 0.10


def ring_area(ring):
    """Signed shoelace area in square degrees."""
    a = 0.0
    n = len(ring)
    for i in range(n):
        x1, y1 = ring[i]
        x2, y2 = ring[(i + 1) % n]
        a += x1 * y2 - x2 * y1
    return a / 2.0


def poly_area(poly):
    """Outer ring minus holes."""
    if not poly:
        return 0.0
    a = abs(ring_area(poly[0]))
    for hole in poly[1:]:
        a -= abs(ring_area(hole))
    return max(a, 0.0)


def bbox_of(poly):
    xs = [p[0] for p in poly[0]]
    ys = [p[1] for p in poly[0]]
    return [min(xs), min(ys), max(xs), max(ys)]


def point_in_poly(x, y, poly):
    """Ray casting over outer ring and holes (odd-even)."""
    inside = False
    for ring in poly:
        n = len(ring)
        j = n - 1
        for i in range(n):
            xi, yi = ring[i]
            xj, yj = ring[j]
            if (yi > y) != (yj > y):
                xc = (xj - xi) * (y - yi) / (yj - yi) + xi
                if x < xc:
                    inside = not inside
            j = i
    return inside


def dist_to_seg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return math.hypot(px - ax, py - ay)
    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def dist_to_poly(x, y, poly):
    best = 1e9
    for ring in poly:
        n = len(ring)
        for i in range(n):
            ax, ay = ring[i]
            bx, by = ring[(i + 1) % n]
            d = dist_to_seg(x, y, ax, ay, bx, by)
            if d < best:
                best = d
    return best


def inner_point(poly):
    """Pole of inaccessibility, approximated by grid search + refinement.

    A plain centroid lands outside crescent-shaped countries (Croatia, Gambia),
    which would put the answer marker in the wrong country.
    """
    x0, y0, x1, y1 = bbox_of(poly)
    w, h = x1 - x0, y1 - y0
    if w <= 0 or h <= 0:
        return [(x0 + x1) / 2, (y0 + y1) / 2]

    best, best_d = None, -1.0
    step_n = 24
    for gy in range(step_n + 1):
        for gx in range(step_n + 1):
            x = x0 + w * gx / step_n
            y = y0 + h * gy / step_n
            if not point_in_poly(x, y, poly):
                continue
            d = dist_to_poly(x, y, poly)
            if d > best_d:
                best_d, best = d, (x, y)

    if best is None:                      # sliver too thin for the grid
        ring = poly[0]
        return [sum(p[0] for p in ring) / len(ring),
                sum(p[1] for p in ring) / len(ring)]

    # local refinement around the winner
    cx, cy = best
    span = max(w, h) / step_n
    for _ in range(5):
        improved = False
        for ox in (-1, 0, 1):
            for oy in (-1, 0, 1):
                if ox == 0 and oy == 0:
                    continue
                x, y = cx + ox * span, cy + oy * span
                if not point_in_poly(x, y, poly):
                    continue
                d = dist_to_poly(x, y, poly)
                if d > best_d:
                    best_d, cx, cy, improved = d, x, y, True
        if not improved:
            span /= 2.0
    return [cx, cy]


def encode_ring(ring):
    """Quantise, drop repeats, delta-encode. Returns None if degenerate."""
    pts, prev = [], None
    for x, y in ring:
        qx = int(round(x * SCALE))
        qy = int(round(y * SCALE))
        if prev is not None and qx == prev[0] and qy == prev[1]:
            continue
        pts.append((qx, qy))
        prev = (qx, qy)
    # GeoJSON repeats the first point at the end; drop it
    if len(pts) > 1 and pts[0] == pts[-1]:
        pts.pop()
    if len(pts) < 3:
        return None
    out = [pts[0][0], pts[0][1]]
    for i in range(1, len(pts)):
        out.append(pts[i][0] - pts[i - 1][0])
        out.append(pts[i][1] - pts[i - 1][1])
    return out


def as_polys(geom):
    if geom['type'] == 'MultiPolygon':
        return list(geom['coordinates'])
    return [geom['coordinates']]


def encode_parts(geom, min_area, keep_largest):
    """Filter tiny parts, encode the rest. Returns (encoded, largest_poly)."""
    parts = [(poly_area(p), p) for p in as_polys(geom) if p and len(p[0]) >= 3]
    if not parts:
        return [], None
    parts.sort(key=lambda t: -t[0])
    largest = parts[0][1]

    kept = []
    for i, (area, poly) in enumerate(parts):
        if area < min_area and not (i == 0 and keep_largest):
            continue
        rings = []
        for r in poly:
            enc = encode_ring(r)
            if enc:
                rings.append(enc)
        if rings:
            kept.append(rings)
    return kept, largest


def q(v):
    return int(round(v * SCALE))


def main():
    data = json.load(io.open(SRC, encoding='utf-8'))
    countries, decor = [], []
    dropped_small = 0

    for f in data['features']:
        p = f['properties']
        if p.get('kind') == 'd':
            enc, _ = encode_parts(f['geometry'], MIN_DECOR_AREA, keep_largest=False)
            decor.extend(enc)
            continue

        enc, largest = encode_parts(f['geometry'], MIN_PART_AREA, keep_largest=True)
        if not enc or largest is None:
            print('!! no geometry for', p.get('en'))
            continue

        bb = bbox_of(largest)
        ip = inner_point(largest)
        countries.append({
            'i': p['id'], 'tr': p['tr'], 'en': p['en'], 'ct': p.get('c') or '',
            'b': [q(bb[0]), q(bb[1]), q(bb[2]), q(bb[3])],
            'p': [q(ip[0]), q(ip[1])],
            'g': enc,
        })

    out = {'s': SCALE, 'c': countries, 'd': decor}
    txt = json.dumps(out, ensure_ascii=False, separators=(',', ':'))
    io.open(DST, 'w', encoding='utf-8').write(txt)

    npts = sum(len(r) // 2 for c in countries for poly in c['g'] for r in poly)
    npts_d = sum(len(r) // 2 for poly in decor for r in poly)
    print('countries:', len(countries))
    print('country points:', npts, ' decor points:', npts_d)
    print('data.json KB:', round(len(txt.encode('utf-8')) / 1024, 1))

    # sanity: the inner point must sit inside the country's own bbox
    bad = [c['i'] for c in countries
           if not (c['b'][0] <= c['p'][0] <= c['b'][2]
                   and c['b'][1] <= c['p'][1] <= c['b'][3])]
    print('inner point outside bbox:', bad if bad else 'none')


main()
