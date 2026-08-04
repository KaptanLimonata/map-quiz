# -*- coding: utf-8 -*-
"""Step 1: split Natural Earth 50m into two layers.

  filtered.geojson - the 197 quiz countries (clickable, askable)
  decor.geojson    - dependencies / territories drawn in a muted colour so the
                     map does not have holes in it, but never asked or clicked.

Regions that are de-facto part of a quiz country (Somaliland, Northern Cyprus,
Hong Kong, Macau) are merged into that country instead, otherwise the map would
show an unclickable gap inside it.
"""
import json, io

SRC = 'ne50m.geojson'

# NE types that are non-country but that we still want as quiz answers.
EXTRA_NAMES = {'Israel', 'Kazakhstan', 'Cuba', 'Kosovo', 'Palestine'}

# geometry folded into another country's shape: source name -> target NAME_EN
MERGE_INTO = {
    'Somaliland': 'Somalia',
    'Turkish Republic of Northern Cyprus': 'Cyprus',
    'Hong Kong': "People's Republic of China",
    'Macau': "People's Republic of China",
}

# country-typed features that are not states -> decorative layer
TO_DECOR = {
    'Aruba', 'Curaçao', 'Sint Maarten', 'Greenland', 'Guernsey', 'Jersey',
    'Isle of Man', 'Åland',
}

# never drawn at all (Mercator clips the poles anyway, and it is huge)
SKIP = {'Antarctica', 'French Southern and Antarctic Lands',
        'Heard Island and McDonald Islands', 'Siachen Glacier'}

TR_OVERRIDE = {
    'Belarus': 'Belarus', 'Taiwan': 'Tayvan', "People's Republic of China": 'Çin',
    'Cyprus': 'Kıbrıs', 'Kosovo': 'Kosova', 'Palestine': 'Filistin',
    'Israel': 'İsrail', 'Kazakhstan': 'Kazakistan', 'Cuba': 'Küba',
    'Vatican City': 'Vatikan', 'East Timor': 'Doğu Timor',
    'The Bahamas': 'Bahamalar', 'The Gambia': 'Gambiya',
    'Republic of the Congo': 'Kongo Cumhuriyeti',
    'Democratic Republic of the Congo': 'Demokratik Kongo Cumhuriyeti',
    'United States of America': 'Amerika Birleşik Devletleri',
    'United Kingdom': 'Birleşik Krallık', 'South Africa': 'Güney Afrika',
    'Federated States of Micronesia': 'Mikronezya', 'Ivory Coast': 'Fildişi Sahili',
    'Eswatini': 'Esvatini', 'North Macedonia': 'Kuzey Makedonya',
    'Czech Republic': 'Çekya', 'Cape Verde': 'Yeşil Burun Adaları',
    'São Tomé and Príncipe': 'Sao Tome ve Principe',
    'Bosnia and Herzegovina': 'Bosna-Hersek', 'Saint Kitts and Nevis': 'Saint Kitts ve Nevis',
    'Trinidad and Tobago': 'Trinidad ve Tobago', 'Antigua and Barbuda': 'Antigua ve Barbuda',
    'Saint Vincent and the Grenadines': 'Saint Vincent ve Grenadinler',
    'Solomon Islands': 'Solomon Adaları', 'Marshall Islands': 'Marshall Adaları',
    'Papua New Guinea': 'Papua Yeni Gine', 'Equatorial Guinea': 'Ekvator Ginesi',
    'Central African Republic': 'Orta Afrika Cumhuriyeti',
    'Dominican Republic': 'Dominik Cumhuriyeti', 'New Zealand': 'Yeni Zelanda',
    'Sri Lanka': 'Sri Lanka', 'Burkina Faso': 'Burkina Faso',
}

EN_OVERRIDE = {
    "People's Republic of China": 'China', 'The Bahamas': 'Bahamas',
    'The Gambia': 'Gambia', 'United States of America': 'United States',
    'East Timor': 'Timor-Leste', 'Czech Republic': 'Czechia',
    'Cape Verde': 'Cabo Verde',
}

CONT_TR = {
    'Europe': 'Avrupa', 'Asia': 'Asya', 'Africa': 'Afrika',
    'North America': 'Kuzey Amerika', 'South America': 'Güney Amerika',
    'Oceania': 'Okyanusya', 'Seven seas (open ocean)': 'Okyanusya',
}


def slug(name):
    out = []
    for ch in name.lower():
        if ch.isalnum() and ord(ch) < 128:
            out.append(ch)
        elif ch in " -'’":
            out.append('-')
    s = ''.join(out)
    while '--' in s:
        s = s.replace('--', '-')
    return s.strip('-')


def polys(geom):
    """Normalise any geometry to a list of polygons."""
    if geom['type'] == 'MultiPolygon':
        return [p for p in geom['coordinates']]
    return [geom['coordinates']]


def main():
    data = json.load(io.open(SRC, encoding='utf-8'))
    feats = data['features']
    by_name = {}
    for f in feats:
        n = f['properties'].get('NAME_EN') or f['properties'].get('NAME')
        by_name.setdefault(n, []).append(f)

    countries, decor, seen = [], [], set()

    for f in feats:
        p = f['properties']
        name = p.get('NAME_EN') or p.get('NAME')
        typ = p.get('TYPE')
        if name in SKIP or name in MERGE_INTO:
            continue

        is_country = ((typ in ('Sovereign country', 'Country') or name in EXTRA_NAMES)
                      and name not in TO_DECOR)

        if not is_country:
            decor.append({'type': 'Feature',
                          'properties': {'id': slug(name), 'kind': 'd'},
                          'geometry': f['geometry']})
            continue

        if name in seen:
            continue
        seen.add(name)

        shapes = polys(f['geometry'])
        # fold in any de-facto regions belonging to this country
        for src, dst in MERGE_INTO.items():
            if dst == name:
                for extra in by_name.get(src, []):
                    shapes.extend(polys(extra['geometry']))

        en = EN_OVERRIDE.get(name, name)
        tr = TR_OVERRIDE.get(name) or p.get('NAME_TR') or en
        countries.append({
            'type': 'Feature',
            'properties': {'id': slug(name), 'en': en, 'tr': tr, 'kind': 'c',
                           'c': CONT_TR.get(p.get('CONTINENT'), p.get('CONTINENT'))},
            'geometry': {'type': 'MultiPolygon', 'coordinates': shapes},
        })

    countries.sort(key=lambda f: f['properties']['en'])
    print('quiz countries:', len(countries))
    print('decor features :', len(decor))

    # One file so mapshaper simplifies both layers against a shared topology;
    # simplifying them separately would tear shared borders (e.g. Morocco /
    # Western Sahara) apart.
    json.dump({'type': 'FeatureCollection', 'features': countries + decor},
              io.open('all.geojson', 'w', encoding='utf-8'), ensure_ascii=False)
    print('wrote all.geojson')


main()
