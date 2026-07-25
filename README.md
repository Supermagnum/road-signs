# Norwegian traffic signs (SVG + open database)

Open catalogue of official Norwegian **fareskilt** (warning signs, 100-series) and **speed-limit-related signs**, published as SVG graphics plus machine-readable JSON databases (bilingual and English-primary).

This repository is a **standalone open resource**. Source data is published by Statens vegvesen / Kartverket under the [Norwegian Licence for Open Government Data (NLOD) 2.0](https://data.norge.no/nlod/en/2.0). It may be used for any purpose, including commercial use, within the licence terms.

## What is in this catalogue?

Two groups of official signs, taken from the full NVDB `Skiltnummer` listing (not a hand-picked subset):

1. **Warning signs (fareskilt)** — triangular signs that alert drivers to a hazard ahead (bends, animals, slippery road, level crossings, etc.). **51** codes.
2. **Speed limit and related signs** — mandatory speed limits (`362`), end of special limits (`364`), speed zones (`366`–`369`), recommended speed (`812`), and related information signs (`560.1`, `560.3`, `856`). **24** codes.

Every NVDB code in those groups appears in the databases. If no graphic file could be found, the entry remains with `"svg": null` and `"status": "no_source_found"`.

| Category | NVDB codes | With SVG | Unresolved |
|----------|------------|----------|------------|
| Warning signs (fareskilt) | 51 | 51 | 0 |
| Speed limit / related | 24 | 19 | 5 |
| **Total** | **75** | **70** | **5** |

Unresolved codes (still listed in the databases): `362.20`, `364.20`, `560.1`, `560.3`, `856`.

## Contents

| Path | Description |
|------|-------------|
| `svg/fareskilt/` | Warning-sign SVGs |
| `svg/speed_limit/` | Speed-limit and related SVGs |
| `database/signs.json` | Bilingual inventory (Norwegian + English fields) |
| `database/signs_en.json` | **English-primary** inventory (`name`, `meaning`, plus `name_nb`) |
| `tool/` | Reproducible download / convert / catalogue pipeline |
| `run.py` | CLI entry point |

## Sign catalogue — what each sign means

In the tables below, the **SVG** column shows a clickable preview that opens the full vector file (relative links work on GitHub).

Official codes follow Norwegian numbering ([Skiltforskriften](https://lovdata.no/dokument/SF/forskrift/2005-10-07-1219) / Skiltnormalen). English names and meanings below are curated glosses for reuse; Norwegian official wording is in `name_nb` in the JSON files.

### Warning signs (fareskilt)

Yellow triangular signs with a red border. They do **not** set a rule by themselves; they warn of a hazard so you can adapt speed and attention. Many are used with an underskilt (supplementary plate) for distance, extent, or extra detail.

| Code | Name (EN) | Meaning | SVG |
|------|-----------|---------|-----|
| `100.1` | Dangerous bend to the right | Warns of a sharp or otherwise dangerous bend ahead to the right. Reduce speed and prepare to steer right. | [![SVG](svg/fareskilt/100_1.svg)](svg/fareskilt/100_1.svg) |
| `100.2` | Dangerous bend to the left | Warns of a sharp or otherwise dangerous bend ahead to the left. Reduce speed and prepare to steer left. | [![SVG](svg/fareskilt/100_2.svg)](svg/fareskilt/100_2.svg) |
| `102.1` | Series of dangerous bends, first to the right | Warns of a series of dangerous bends; the first bend is to the right. | [![SVG](svg/fareskilt/102_1.svg)](svg/fareskilt/102_1.svg) |
| `102.2` | Series of dangerous bends, first to the left | Warns of a series of dangerous bends; the first bend is to the left. | [![SVG](svg/fareskilt/102_2.svg)](svg/fareskilt/102_2.svg) |
| `104.1` | Steep hill upwards | Warns of a steep uphill gradient ahead. Be prepared for reduced speed, especially for heavy vehicles. | [![SVG](svg/fareskilt/104_1.svg)](svg/fareskilt/104_1.svg) |
| `104.2` | Steep hill downwards | Warns of a steep downhill gradient ahead. Control speed; use a lower gear if needed. | [![SVG](svg/fareskilt/104_2.svg)](svg/fareskilt/104_2.svg) |
| `106.1` | Road narrows on both sides | Warns that the carriageway narrows on both sides ahead. | [![SVG](svg/fareskilt/106_1.svg)](svg/fareskilt/106_1.svg) |
| `106.2` | Road narrows on the right | Warns that the carriageway narrows on the right-hand side ahead. | [![SVG](svg/fareskilt/106_2.svg)](svg/fareskilt/106_2.svg) |
| `106.3` | Road narrows on the left | Warns that the carriageway narrows on the left-hand side ahead. | [![SVG](svg/fareskilt/106_3.svg)](svg/fareskilt/106_3.svg) |
| `108` | Uneven road | Warns of an uneven road surface ahead (potholes, ridges, or similar). | [![SVG](svg/fareskilt/108.svg)](svg/fareskilt/108.svg) |
| `109` | Speed hump | Warns of a speed hump (traffic calming bump) ahead. | [![SVG](svg/fareskilt/109.svg)](svg/fareskilt/109.svg) |
| `110` | Road works | Warns of road works ahead. Expect workers, equipment, temporary layouts, and lower speeds. | [![SVG](svg/fareskilt/110.svg)](svg/fareskilt/110.svg) |
| `112` | Loose chippings | Warns of loose chippings / stone spray from the road surface ahead. | [![SVG](svg/fareskilt/112.svg)](svg/fareskilt/112.svg) |
| `114.1` | Falling rocks, right side | Warns of falling rocks or landslide risk from the right-hand side. | [![SVG](svg/fareskilt/114_1.svg)](svg/fareskilt/114_1.svg) |
| `114.2` | Falling rocks, left side | Warns of falling rocks or landslide risk from the left-hand side. | [![SVG](svg/fareskilt/114_2.svg)](svg/fareskilt/114_2.svg) |
| `116` | Slippery road | Warns that the road may be slippery (ice, water, oil, polished surface, etc.). | [![SVG](svg/fareskilt/116.svg)](svg/fareskilt/116.svg) |
| `117` | Soft verges | Warns of a soft, weak, or otherwise dangerous road shoulder / verge. | [![SVG](svg/fareskilt/117.svg)](svg/fareskilt/117.svg) |
| `118` | Opening or swing bridge | Warns of an opening, swing, or otherwise movable bridge ahead. | [![SVG](svg/fareskilt/118.svg)](svg/fareskilt/118.svg) |
| `120` | Quayside or ferry terminal | Warns of a quay, shore, or ferry berth ahead — risk of driving into water. | [![SVG](svg/fareskilt/120.svg)](svg/fareskilt/120.svg) |
| `122` | Tunnel | Warns of a tunnel ahead. Adapt lighting and speed; watch for restrictions. | [![SVG](svg/fareskilt/122.svg)](svg/fareskilt/122.svg) |
| `124` | Dangerous junction | Warns of a dangerous road junction ahead. | [![SVG](svg/fareskilt/124.svg)](svg/fareskilt/124.svg) |
| `126` | Roundabout | Warns of a roundabout ahead. | [![SVG](svg/fareskilt/126.svg)](svg/fareskilt/126.svg) |
| `132` | Traffic signals | Warns of traffic light signals ahead. | [![SVG](svg/fareskilt/132.svg)](svg/fareskilt/132.svg) |
| `134` | Level crossing with barrier | Warns of a railway level crossing with barriers/gates ahead. | [![SVG](svg/fareskilt/134.svg)](svg/fareskilt/134.svg) |
| `135` | Level crossing without barrier | Warns of a railway level crossing without barriers/gates ahead. | [![SVG](svg/fareskilt/135.svg)](svg/fareskilt/135.svg) |
| `136.1h` | Distance to level crossing | Distance marker approaching a level crossing (right-side / countdown panel variant). | [![SVG](svg/fareskilt/136_1h.svg)](svg/fareskilt/136_1h.svg) |
| `136.1v` | Distance to level crossing | Distance marker approaching a level crossing (left-side / countdown panel variant). | [![SVG](svg/fareskilt/136_1v.svg)](svg/fareskilt/136_1v.svg) |
| `136.2h` | Distance to level crossing | Intermediate distance marker approaching a level crossing (right-side variant). | [![SVG](svg/fareskilt/136_2h.svg)](svg/fareskilt/136_2h.svg) |
| `136.2v` | Distance to level crossing | Intermediate distance marker approaching a level crossing (left-side variant). | [![SVG](svg/fareskilt/136_2v.svg)](svg/fareskilt/136_2v.svg) |
| `136.3h` | Distance to level crossing | Closest distance marker approaching a level crossing (right-side variant). | [![SVG](svg/fareskilt/136_3h.svg)](svg/fareskilt/136_3h.svg) |
| `136.3v` | Distance to level crossing | Closest distance marker approaching a level crossing (left-side variant). | [![SVG](svg/fareskilt/136_3v.svg)](svg/fareskilt/136_3v.svg) |
| `138.1` | Single-track railway | Warns of a single-track railway crossing / railway track ahead. | [![SVG](svg/fareskilt/138_1.svg)](svg/fareskilt/138_1.svg) |
| `138.2` | Multi-track railway | Warns of a multi-track railway crossing / railway tracks ahead. | [![SVG](svg/fareskilt/138_2.svg)](svg/fareskilt/138_2.svg) |
| `139` | Tramway | Warns of a tramway / tram tracks ahead. | [![SVG](svg/fareskilt/139.svg)](svg/fareskilt/139.svg) |
| `140` | Distance to pedestrian crossing | Warns of the distance remaining to a pedestrian crossing ahead. | [![SVG](svg/fareskilt/140.svg)](svg/fareskilt/140.svg) |
| `142` | Children | Warns that children may be on or near the road (e.g. near schools or playgrounds). | [![SVG](svg/fareskilt/142.svg)](svg/fareskilt/142.svg) |
| `144` | Cyclists | Warns of cyclists on or crossing the road ahead. | [![SVG](svg/fareskilt/144.svg)](svg/fareskilt/144.svg) |
| `146.1` | Elk / moose | Warns of elk/moose that may cross or be on the road. | [![SVG](svg/fareskilt/146_1.svg)](svg/fareskilt/146_1.svg) |
| `146.2` | Reindeer | Warns of reindeer that may cross or be on the road. | [![SVG](svg/fareskilt/146_2.svg)](svg/fareskilt/146_2.svg) |
| `146.3` | Deer | Warns of deer that may cross or be on the road. | [![SVG](svg/fareskilt/146_3.svg)](svg/fareskilt/146_3.svg) |
| `146.4` | Cattle | Warns of cattle that may be on or crossing the road. | [![SVG](svg/fareskilt/146_4.svg)](svg/fareskilt/146_4.svg) |
| `146.5` | Sheep | Warns of sheep that may be on or crossing the road. | [![SVG](svg/fareskilt/146_5.svg)](svg/fareskilt/146_5.svg) |
| `148` | Two-way traffic | Warns that two-way traffic begins, or oncoming traffic must be expected. | [![SVG](svg/fareskilt/148.svg)](svg/fareskilt/148.svg) |
| `149` | Queue / congestion | Warns of queues / congestion ahead. | [![SVG](svg/fareskilt/149.svg)](svg/fareskilt/149.svg) |
| `150` | Low-flying aircraft | Warns of low-flying aircraft or an area near an aerodrome. | [![SVG](svg/fareskilt/150.svg)](svg/fareskilt/150.svg) |
| `151` | Military activity | Warns of military activity that may affect the road. | [![SVG](svg/fareskilt/151.svg)](svg/fareskilt/151.svg) |
| `152` | Side winds | Warns of strong side winds that may affect vehicle stability. | [![SVG](svg/fareskilt/152.svg)](svg/fareskilt/152.svg) |
| `153` | Accident | Warns of a traffic accident / crash scene ahead. | [![SVG](svg/fareskilt/153.svg)](svg/fareskilt/153.svg) |
| `154` | Skiers crossing | Warns of skiers crossing or using the road area. | [![SVG](svg/fareskilt/154.svg)](svg/fareskilt/154.svg) |
| `155` | Horse riders | Warns of horse riders on or near the road. | [![SVG](svg/fareskilt/155.svg)](svg/fareskilt/155.svg) |
| `156` | Other danger | General warning of another hazard not covered by a more specific warning sign. Often combined with a supplementary plate. | [![SVG](svg/fareskilt/156.svg)](svg/fareskilt/156.svg) |

### Speed limit and related signs

| Code | Name (EN) | Meaning | SVG |
|------|-----------|---------|-----|
| `362.100` | Speed limit 100 km/h | Mandatory maximum speed limit of 100 km/h begins. | [![SVG](svg/speed_limit/362_100.svg)](svg/speed_limit/362_100.svg) |
| `362.110` | Speed limit 110 km/h | Mandatory maximum speed limit of 110 km/h begins. | [![SVG](svg/speed_limit/362_110.svg)](svg/speed_limit/362_110.svg) |
| `362.20` | Speed limit 20 km/h | Mandatory maximum speed limit of 20 km/h begins. | — (no graphic) |
| `362.30` | Speed limit 30 km/h | Mandatory maximum speed limit of 30 km/h begins. | [![SVG](svg/speed_limit/362_30.svg)](svg/speed_limit/362_30.svg) |
| `362.40` | Speed limit 40 km/h | Mandatory maximum speed limit of 40 km/h begins. | [![SVG](svg/speed_limit/362_40.svg)](svg/speed_limit/362_40.svg) |
| `362.50` | Speed limit 50 km/h | Mandatory maximum speed limit of 50 km/h begins. | [![SVG](svg/speed_limit/362_50.svg)](svg/speed_limit/362_50.svg) |
| `362.60` | Speed limit 60 km/h | Mandatory maximum speed limit of 60 km/h begins. | [![SVG](svg/speed_limit/362_60.svg)](svg/speed_limit/362_60.svg) |
| `362.70` | Speed limit 70 km/h | Mandatory maximum speed limit of 70 km/h begins. | [![SVG](svg/speed_limit/362_70.svg)](svg/speed_limit/362_70.svg) |
| `362.80` | Speed limit 80 km/h | Mandatory maximum speed limit of 80 km/h begins. | [![SVG](svg/speed_limit/362_80.svg)](svg/speed_limit/362_80.svg) |
| `362.90` | Speed limit 90 km/h | Mandatory maximum speed limit of 90 km/h begins. | [![SVG](svg/speed_limit/362_90.svg)](svg/speed_limit/362_90.svg) |
| `364.20` | End of special speed limit 20 km/h | Ends the special 20 km/h speed limit; the general limit for the road type applies again. | — (no graphic) |
| `364.30` | End of special speed limit 30 km/h | Ends the special 30 km/h speed limit; the general limit for the road type applies again. | [![SVG](svg/speed_limit/364_30.svg)](svg/speed_limit/364_30.svg) |
| `364.40` | End of special speed limit 40 km/h | Ends the special 40 km/h speed limit; the general limit for the road type applies again. | [![SVG](svg/speed_limit/364_40.svg)](svg/speed_limit/364_40.svg) |
| `364.50` | End of special speed limit 50 km/h | Ends the special 50 km/h speed limit; the general limit for the road type applies again. | [![SVG](svg/speed_limit/364_50.svg)](svg/speed_limit/364_50.svg) |
| `364.60` | End of special speed limit 60 km/h | Ends the special 60 km/h speed limit; the general limit for the road type applies again. | [![SVG](svg/speed_limit/364_60.svg)](svg/speed_limit/364_60.svg) |
| `364.70` | End of special speed limit 70 km/h | Ends the special 70 km/h speed limit; the general limit for the road type applies again. | [![SVG](svg/speed_limit/364_70.svg)](svg/speed_limit/364_70.svg) |
| `366` | Speed limit zone | Marks the start of a speed-limit zone. The zone speed applies until the matching end-of-zone sign. | [![SVG](svg/speed_limit/366.svg)](svg/speed_limit/366.svg) |
| `367` | Speed limit zone for small electric vehicles | Marks the start of a speed-limit zone for small electric vehicles (e.g. e-scooters). | [![SVG](svg/speed_limit/367.svg)](svg/speed_limit/367.svg) |
| `368` | End of speed limit zone | Marks the end of a speed-limit zone. | [![SVG](svg/speed_limit/368.svg)](svg/speed_limit/368.svg) |
| `369` | End of speed limit zone for small electric vehicles | Marks the end of a speed-limit zone for small electric vehicles. | [![SVG](svg/speed_limit/369.svg)](svg/speed_limit/369.svg) |
| `560.1` | General speed limits | Information about the general speed limits that apply (built-up area vs. outside). | — (no graphic) |
| `560.3` | Warning of speed measurement | Warns that speed may be measured ahead (speed camera / enforcement warning). | — (no graphic) |
| `812` | Recommended speed | Indicates a recommended (advisory) speed — not the same as a mandatory speed limit. | [![SVG](svg/speed_limit/812.svg)](svg/speed_limit/812.svg) |
| `856` | General speed limit (miniature) | Miniature version of the general speed-limit information sign. | — (no graphic) |

#### How the speed-limit series relate

- **`362.xx`** — start of a **mandatory** maximum speed (km/h on the sign).
- **`364.xx`** — **end** of that special mandatory limit; the general limit for the road type applies again.
- **`366` / `368`** — start / end of a **speed-limit zone** (zone rules apply until the end sign).
- **`367` / `369`** — same idea for **small electric vehicles** (e.g. e-scooters).
- **`812`** — **recommended** (advisory) speed only; not a mandatory limit.
- **`560.1` / `856`** — information about **general** speed limits (built-up vs elsewhere).
- **`560.3`** — warning that **speed measurement / enforcement** may occur ahead.

## Databases

### `database/signs_en.json` (English-primary)

Best starting point for English-language apps and docs. Each entry includes:

| Field | Meaning |
|-------|---------|
| `code` | Official skiltnummer |
| `category` / `category_label` | `fareskilt` / `speed_limit`, plus English label |
| `name` | English sign name |
| `name_nb` | Official Norwegian NVDB description |
| `meaning` | Plain-English explanation of what the sign means |
| `svg` | Relative path to SVG, or `null` |
| `conversion_method` | `geonorge_native` \| `eps_converted` \| `jpg_traced` \| `no_source_found` |
| `status` | `ok` \| `no_source_found` \| `conversion_failed` |
| `legal_reference` | Skiltforskriften URL with series hint |
| `source_attribution` | NLOD attribution block |
| `color_codes` | Official PMS values used for traffic-sign production |

### `database/signs.json` (bilingual)

Same inventory with Norwegian-first fields (`name_nb`, `name_en`, `meaning_en`) for consumers that want both languages on equal footing.

**Coverage rule:** every in-scope NVDB code is listed. Gaps are explicit — never silently omitted.

## Attribution

Contains data under the Norwegian Licence for Open Government Data (NLOD) made available by:

- **Statens vegvesen** — EPS/JPG sign artwork and PMS colour guidance ([filer og fargekoder](https://www.vegvesen.no/fag/veg-og-gate/trafikkskilt-og-vegoppmerking/filer-og-fargekoder-for-trafikkskilt/))
- **NVDB (Nasjonal vegdatabank)** — authoritative skiltnummer codes, names, and categories via [API Les v4](https://nvdbapiles.atlas.vegvesen.no/)
- **Kartverket / Geonorge** — [Trafikkskilt symbol package](https://register.geonorge.no/symbol/symbolpackages/details/1e2f592a-1d69-45a3-9ce1-e55a64fe1dc3)
- Legal references point at [Skiltforskriften](https://lovdata.no/dokument/SF/forskrift/2005-10-07-1219)

## Conversion methods (fidelity)

1. **`geonorge_native`** — SVG taken from the Geonorge Trafikkskilt package (preferred when present).
2. **`eps_converted`** — official EPS vector artwork converted to SVG. Uses Inkscape when installed (`inkscape input.eps -o output.svg`); otherwise Ghostscript (`EPS`→`PDF`) + Poppler `pdftocairo` (`PDF`→`SVG`). Both paths keep vector data (format conversion, not re-tracing).
3. **`jpg_traced`** — JPG/PNG raster traced with [vtracer](https://github.com/visioncortex/vtracer). Lower fidelity than native vectors; flagged per file.
4. **`no_source_found`** — no Geonorge SVG, EPS, or raster could be matched to the NVDB code.

Every published SVG is checked for basic XML validity before inclusion.

## Regenerate / update

Requirements: Python 3.10+, `pip install -r requirements.txt`. Optional but recommended: `inkscape`. Also used when present: `gs` (Ghostscript) and `pdftocairo` (poppler-utils).

```bash
pip install -r requirements.txt
python run.py                 # download, unpack, convert, write both databases
python run.py --skip-download # reuse work/ caches
python run.py --force-download
```

Working downloads and unpacked archives live under `work/` (gitignored). Published outputs are `svg/`, `database/signs.json`, and `database/signs_en.json`.

## Licence

- **Source data:** [NLOD 2.0](https://data.norge.no/nlod/en/2.0) — Statens vegvesen / Kartverket.
- **Pipeline code in this repository:** available for reuse under the same spirit of open reuse; please retain attribution to Statens vegvesen / NVDB / Geonorge when redistributing the sign graphics or derived database.
