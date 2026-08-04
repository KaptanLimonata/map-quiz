# World Map Quiz

A single-file world map quiz. It names a country, you tap it on the map.
Works on desktop, mobile and iOS Safari. No network, no dependencies: the map
data is embedded in the HTML, so the file runs straight from disk.

**Play:** https://kaptanlimonata.github.io/map-quiz/

Or open [`world-map-quiz.html`](world-map-quiz.html) from disk in any browser.

> On a phone, use the link. Sending the file through a messaging app does not
> work: WhatsApp and the iOS Files app render the HTML in a preview that never
> executes JavaScript, so the page just sits on its placeholder text.

## What it does

- 197 countries (193 UN members + Vatican, Taiwan, Kosovo, Palestine), asked in
  random order, never repeating within a run
- The country to find stays pinned in the overlay at the top
- Two wrong taps reveal the answer: the map flies to it and marks it
- **Geç** (Skip) at the bottom reveals the answer and moves on
- A country you get right flashes green, then turns white and stays white for
  the rest of the run, so the map fills in as you go
- Pinch, wheel, double-tap and +/− all zoom; drag to pan
- TR / EN country names, toggled bottom-left

Countries too small to tap at world zoom (Malta, Singapore, Monaco, ...) are
drawn as small circles that stay tappable, and turn back into real outlines as
you zoom in.

## Layout

```
world-map-quiz.html   the whole game - this is the deliverable
tools/                pipeline that regenerates the embedded map data
INDEX.md              current state of the work
environment.md        toolchain and data-source notes
history.md            root causes worth remembering
```

## Rebuilding the map data

Only needed if you want to change the country list, detail level or styling.
`tools/template.html` is the real source of the game; the shipped HTML is that
template with the map data injected into it.

Requires Python 3 and [mapshaper](https://github.com/mbloch/mapshaper)
(`npm install -g mapshaper`).

```bash
cd tools
curl -Lo ne50m.geojson https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson
python step1_filter.py                                              # pick the 197 countries -> all.geojson
mapshaper all.geojson -simplify 18% keep-shapes -o precision=0.002 simplified.geojson
python step2_pack.py                                                # quantise + delta-encode -> data.json
python step4_verify.py                                              # geographic sanity checks
python step3_build.py                                               # inject into template -> world-map-quiz.html
```

`step3_build.py` writes to `C:\Users\Burak\Documents\MapHTML\world-map-quiz.html`;
change `OUT` in that file if you move the project.

### Detail vs. speed

`-simplify 18%` is a deliberate trade-off, measured on this data:

| detail | points | HTML size | pan at world zoom |
|--------|--------|-----------|-------------------|
| 15%    | 15.1k  | 182 KB    | fast              |
| 18%    | 17.7k  | 205 KB    | 69 fps (shipped)  |
| 30%    | 28.4k  | 281 KB    | noticeably slower |

## Map data

Natural Earth 1:50m Admin 0 countries (public domain). Turkish names come from
the dataset's own `NAME_TR` field, with a handful corrected by hand.

Borders and names follow the source dataset and are not a political statement.
Somaliland and Northern Cyprus are merged into Somalia and Cyprus so the map has
no unclickable gaps; dependencies such as Greenland are drawn in a muted colour
and are never asked or clickable.
