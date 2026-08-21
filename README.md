# Norwegian traffic signs (SVG + open database)

Open catalogue of official Norwegian traffic-sign graphics published as SVG plus machine-readable JSON databases (bilingual and English-primary).

This repository is a **standalone open resource**. Source data is published by Statens vegvesen / Kartverket under the [Norwegian Licence for Open Government Data (NLOD) 2.0](https://data.norge.no/nlod/en/2.0). It may be used for any purpose, including commercial use, within the licence terms.

## What is in this catalogue?

Four groups of official signs, taken from the NVDB `Skiltnummer` listing:

1. **Warning signs (fareskilt)** — triangular hazard warnings (100-series). **51** codes.
2. **Speed limit and related signs** — mandatory limits, zone start/end, recommended speed, related info signs. **24** codes.
3. **Service / tourist symbols (serviceskilt)** — 640/650 series (sights, activities). **13** codes.
4. **Direction / route symbols (vegvisning)** — selected 723 / 755–780 / 790 symbols. **33** codes.

Every listed NVDB code in those groups appears in the databases. If no graphic file could be found, the entry remains with `"svg": null` and `"status": "no_source_found"`.

| Category | NVDB codes | With SVG | Unresolved |
|----------|------------|----------|------------|
| Warning signs (fareskilt) | 51 | 51 | 0 |
| Speed limit / related | 24 official + 12 generated | 31 | 5 official unresolved |
| Service / tourist (serviceskilt) | 13 | 13 | 0 |
| Direction / route (vegvisning) | 33 | 33 | 0 |

Unresolved **official** speed-limit codes (still listed, `"svg": null`): `362.20`, `364.20`, `560.1`, `560.3`, `856`.

### Generated speed-limit plates (derived, not original government art)

In addition to the official NVDB `362.xx` graphics, this catalogue includes **12 generated** speed-limit SVGs for every-5 km/h values that appear in OSM `maxspeed` tagging but have **no NVDB Skiltnummer** / no original Statens vegvesen published plate file:

`362.5`, `362.10`, `362.15`, `362.25`, `362.35`, `362.45`, `362.55`, `362.65`, `362.75`, `362.85`, `362.95`, `362.105`

**Provenance:** each file was composited from digit outlines taken from the existing official NPRA/Kartverket-sourced plates already in this catalogue (and Trafikkalfabetet spacing rules). They are a **derived work** under [NLOD 2.0](https://data.norge.no/nlod/en/2.0), not original government-published art for those codes. Do not treat them as official Skiltnormalen drawings. Catalogue JSON marks them with `conversion_method: digit_composite_from_official_plates` and a generation note on each entry.

See also [`sourcing/README.md`](sourcing/README.md) for the detailed graphic-source audit of the 640/650/723/755–780/790 set (including packs that were checked and contained **zero** hits: markering, underskilt, opplysning, forbud, vikeplikt).

## Contents

| Path | Description |
|------|-------------|
| [`svg/fareskilt/`](svg/fareskilt/) | Warning-sign SVGs |
| [`svg/speed_limit/`](svg/speed_limit/) | Speed-limit and related SVGs |
| [`svg/serviceskilt/`](svg/serviceskilt/) | Service / tourist symbol SVGs |
| [`svg/vegvisning/`](svg/vegvisning/) | Direction / route symbol SVGs |
| [`database/signs.json`](database/signs.json) | Bilingual inventory (Norwegian + English fields) |
| [`database/signs_en.json`](database/signs_en.json) | **English-primary** inventory (`name`, `meaning`, plus `name_nb`) |
| [`database/osm_tags.json`](database/osm_tags.json) | OpenStreetMap tag mapping for each catalogue code (`traffic_sign=NO:…`, `hazard=*`, etc.) |
| [`database/osm_tags.md`](database/osm_tags.md) | Human-readable view of the OSM tag mapping |
| [`tool/`](tool/) | Reproducible download / convert / catalogue pipeline |
| [`sourcing/README.md`](sourcing/README.md) | Sourcing audit for selected 6xx/7xx codes |
| [`reference/trafikkalfabetet.pdf`](reference/trafikkalfabetet.pdf) | Official Trafikkalfabetet type specimen / construction PDF |
| [`reference/trafikkalfabetet.en.pdf`](reference/trafikkalfabetet.en.pdf) | English edition of Trafikkalfabetet (PDF) |
| [`reference/trafikkalfabetet.en.md`](reference/trafikkalfabetet.en.md) | English translation of Trafikkalfabetet text rules |
| [`run.py`](run.py) | CLI entry point |

## Sign catalogue — what each sign means

In the tables below, the **SVG** column links to each vector file (relative links work on GitHub).

Official codes follow Norwegian numbering ([Skiltforskriften](https://lovdata.no/dokument/SF/forskrift/2005-10-07-1219) / Skiltnormalen). English names and meanings below are curated glosses for reuse; Norwegian official wording is in `name_nb` in the JSON files.

### Warning signs (fareskilt)

Yellow triangular signs with a red border. They do **not** set a rule by themselves; they warn of a hazard so you can adapt speed and attention. Many are used with an underskilt (supplementary plate) for distance, extent, or extra detail.

| Code | Name (EN) | Meaning | SVG |
|------|-----------|---------|-----|
| `100.1` | Dangerous bend to the right | Warns of a sharp or otherwise dangerous bend ahead to the right. Reduce speed and prepare to steer right. | [`svg/fareskilt/100_1.svg`](svg/fareskilt/100_1.svg) |
| `100.2` | Dangerous bend to the left | Warns of a sharp or otherwise dangerous bend ahead to the left. Reduce speed and prepare to steer left. | [`svg/fareskilt/100_2.svg`](svg/fareskilt/100_2.svg) |
| `102.1` | Series of dangerous bends, first to the right | Warns of a series of dangerous bends; the first bend is to the right. | [`svg/fareskilt/102_1.svg`](svg/fareskilt/102_1.svg) |
| `102.2` | Series of dangerous bends, first to the left | Warns of a series of dangerous bends; the first bend is to the left. | [`svg/fareskilt/102_2.svg`](svg/fareskilt/102_2.svg) |
| `104.1` | Steep hill upwards | Warns of a steep uphill gradient ahead. Be prepared for reduced speed, especially for heavy vehicles. | [`svg/fareskilt/104_1.svg`](svg/fareskilt/104_1.svg) |
| `104.2` | Steep hill downwards | Warns of a steep downhill gradient ahead. Control speed; use a lower gear if needed. | [`svg/fareskilt/104_2.svg`](svg/fareskilt/104_2.svg) |
| `106.1` | Road narrows on both sides | Warns that the carriageway narrows on both sides ahead. | [`svg/fareskilt/106_1.svg`](svg/fareskilt/106_1.svg) |
| `106.2` | Road narrows on the right | Warns that the carriageway narrows on the right-hand side ahead. | [`svg/fareskilt/106_2.svg`](svg/fareskilt/106_2.svg) |
| `106.3` | Road narrows on the left | Warns that the carriageway narrows on the left-hand side ahead. | [`svg/fareskilt/106_3.svg`](svg/fareskilt/106_3.svg) |
| `108` | Uneven road | Warns of an uneven road surface ahead (potholes, ridges, or similar). | [`svg/fareskilt/108.svg`](svg/fareskilt/108.svg) |
| `109` | Speed hump | Warns of a speed hump (traffic calming bump) ahead. | [`svg/fareskilt/109.svg`](svg/fareskilt/109.svg) |
| `110` | Road works | Warns of road works ahead. Expect workers, equipment, temporary layouts, and lower speeds. | [`svg/fareskilt/110.svg`](svg/fareskilt/110.svg) |
| `112` | Loose chippings | Warns of loose chippings / stone spray from the road surface ahead. | [`svg/fareskilt/112.svg`](svg/fareskilt/112.svg) |
| `114.1` | Falling rocks, right side | Warns of falling rocks or landslide risk from the right-hand side. | [`svg/fareskilt/114_1.svg`](svg/fareskilt/114_1.svg) |
| `114.2` | Falling rocks, left side | Warns of falling rocks or landslide risk from the left-hand side. | [`svg/fareskilt/114_2.svg`](svg/fareskilt/114_2.svg) |
| `116` | Slippery road | Warns that the road may be slippery (ice, water, oil, polished surface, etc.). | [`svg/fareskilt/116.svg`](svg/fareskilt/116.svg) |
| `117` | Soft verges | Warns of a soft, weak, or otherwise dangerous road shoulder / verge. | [`svg/fareskilt/117.svg`](svg/fareskilt/117.svg) |
| `118` | Opening or swing bridge | Warns of an opening, swing, or otherwise movable bridge ahead. | [`svg/fareskilt/118.svg`](svg/fareskilt/118.svg) |
| `120` | Quayside or ferry terminal | Warns of a quay, shore, or ferry berth ahead — risk of driving into water. | [`svg/fareskilt/120.svg`](svg/fareskilt/120.svg) |
| `122` | Tunnel | Warns of a tunnel ahead. Adapt lighting and speed; watch for restrictions. | [`svg/fareskilt/122.svg`](svg/fareskilt/122.svg) |
| `124` | Dangerous junction | Warns of a dangerous road junction ahead. | [`svg/fareskilt/124.svg`](svg/fareskilt/124.svg) |
| `126` | Roundabout | Warns of a roundabout ahead. | [`svg/fareskilt/126.svg`](svg/fareskilt/126.svg) |
| `132` | Traffic signals | Warns of traffic light signals ahead. | [`svg/fareskilt/132.svg`](svg/fareskilt/132.svg) |
| `134` | Level crossing with barrier | Warns of a railway level crossing with barriers/gates ahead. | [`svg/fareskilt/134.svg`](svg/fareskilt/134.svg) |
| `135` | Level crossing without barrier | Warns of a railway level crossing without barriers/gates ahead. | [`svg/fareskilt/135.svg`](svg/fareskilt/135.svg) |
| `136.1h` | Distance to level crossing | Distance marker approaching a level crossing (right-side / countdown panel variant). | [`svg/fareskilt/136_1h.svg`](svg/fareskilt/136_1h.svg) |
| `136.1v` | Distance to level crossing | Distance marker approaching a level crossing (left-side / countdown panel variant). | [`svg/fareskilt/136_1v.svg`](svg/fareskilt/136_1v.svg) |
| `136.2h` | Distance to level crossing | Intermediate distance marker approaching a level crossing (right-side variant). | [`svg/fareskilt/136_2h.svg`](svg/fareskilt/136_2h.svg) |
| `136.2v` | Distance to level crossing | Intermediate distance marker approaching a level crossing (left-side variant). | [`svg/fareskilt/136_2v.svg`](svg/fareskilt/136_2v.svg) |
| `136.3h` | Distance to level crossing | Closest distance marker approaching a level crossing (right-side variant). | [`svg/fareskilt/136_3h.svg`](svg/fareskilt/136_3h.svg) |
| `136.3v` | Distance to level crossing | Closest distance marker approaching a level crossing (left-side variant). | [`svg/fareskilt/136_3v.svg`](svg/fareskilt/136_3v.svg) |
| `138.1` | Single-track railway | Warns of a single-track railway crossing / railway track ahead. | [`svg/fareskilt/138_1.svg`](svg/fareskilt/138_1.svg) |
| `138.2` | Multi-track railway | Warns of a multi-track railway crossing / railway tracks ahead. | [`svg/fareskilt/138_2.svg`](svg/fareskilt/138_2.svg) |
| `139` | Tramway | Warns of a tramway / tram tracks ahead. | [`svg/fareskilt/139.svg`](svg/fareskilt/139.svg) |
| `140` | Distance to pedestrian crossing | Warns of the distance remaining to a pedestrian crossing ahead. | [`svg/fareskilt/140.svg`](svg/fareskilt/140.svg) |
| `142` | Children | Warns that children may be on or near the road (e.g. near schools or playgrounds). | [`svg/fareskilt/142.svg`](svg/fareskilt/142.svg) |
| `144` | Cyclists | Warns of cyclists on or crossing the road ahead. | [`svg/fareskilt/144.svg`](svg/fareskilt/144.svg) |
| `146.1` | Elk / moose | Warns of elk/moose that may cross or be on the road. | [`svg/fareskilt/146_1.svg`](svg/fareskilt/146_1.svg) |
| `146.2` | Reindeer | Warns of reindeer that may cross or be on the road. | [`svg/fareskilt/146_2.svg`](svg/fareskilt/146_2.svg) |
| `146.3` | Deer | Warns of deer that may cross or be on the road. | [`svg/fareskilt/146_3.svg`](svg/fareskilt/146_3.svg) |
| `146.4` | Cattle | Warns of cattle that may be on or crossing the road. | [`svg/fareskilt/146_4.svg`](svg/fareskilt/146_4.svg) |
| `146.5` | Sheep | Warns of sheep that may be on or crossing the road. | [`svg/fareskilt/146_5.svg`](svg/fareskilt/146_5.svg) |
| `148` | Two-way traffic | Warns that two-way traffic begins, or oncoming traffic must be expected. | [`svg/fareskilt/148.svg`](svg/fareskilt/148.svg) |
| `149` | Queue / congestion | Warns of queues / congestion ahead. | [`svg/fareskilt/149.svg`](svg/fareskilt/149.svg) |
| `150` | Low-flying aircraft | Warns of low-flying aircraft or an area near an aerodrome. | [`svg/fareskilt/150.svg`](svg/fareskilt/150.svg) |
| `151` | Military activity | Warns of military activity that may affect the road. | [`svg/fareskilt/151.svg`](svg/fareskilt/151.svg) |
| `152` | Side winds | Warns of strong side winds that may affect vehicle stability. | [`svg/fareskilt/152.svg`](svg/fareskilt/152.svg) |
| `153` | Accident | Warns of a traffic accident / crash scene ahead. | [`svg/fareskilt/153.svg`](svg/fareskilt/153.svg) |
| `154` | Skiers crossing | Warns of skiers crossing or using the road area. | [`svg/fareskilt/154.svg`](svg/fareskilt/154.svg) |
| `155` | Horse riders | Warns of horse riders on or near the road. | [`svg/fareskilt/155.svg`](svg/fareskilt/155.svg) |
| `156` | Other danger | General warning of another hazard not covered by a more specific warning sign. Often combined with a supplementary plate. | [`svg/fareskilt/156.svg`](svg/fareskilt/156.svg) |

### Speed limit and related signs

| Code | Name (EN) | Meaning | SVG |
|------|-----------|---------|-----|
| `362.5` | Speed limit 5 km/h | Mandatory maximum speed limit of 5 km/h begins. | [`svg/speed_limit/362_5.svg`](svg/speed_limit/362_5.svg) **(generated)** |
| `362.10` | Speed limit 10 km/h | Mandatory maximum speed limit of 10 km/h begins. | [`svg/speed_limit/362_10.svg`](svg/speed_limit/362_10.svg) **(generated)** |
| `362.15` | Speed limit 15 km/h | Mandatory maximum speed limit of 15 km/h begins. | [`svg/speed_limit/362_15.svg`](svg/speed_limit/362_15.svg) **(generated)** |
| `362.20` | Speed limit 20 km/h | Mandatory maximum speed limit of 20 km/h begins. | — (no official graphic) |
| `362.25` | Speed limit 25 km/h | Mandatory maximum speed limit of 25 km/h begins. | [`svg/speed_limit/362_25.svg`](svg/speed_limit/362_25.svg) **(generated)** |
| `362.30` | Speed limit 30 km/h | Mandatory maximum speed limit of 30 km/h begins. | [`svg/speed_limit/362_30.svg`](svg/speed_limit/362_30.svg) |
| `362.35` | Speed limit 35 km/h | Mandatory maximum speed limit of 35 km/h begins. | [`svg/speed_limit/362_35.svg`](svg/speed_limit/362_35.svg) **(generated)** |
| `362.40` | Speed limit 40 km/h | Mandatory maximum speed limit of 40 km/h begins. | [`svg/speed_limit/362_40.svg`](svg/speed_limit/362_40.svg) |
| `362.45` | Speed limit 45 km/h | Mandatory maximum speed limit of 45 km/h begins. | [`svg/speed_limit/362_45.svg`](svg/speed_limit/362_45.svg) **(generated)** |
| `362.50` | Speed limit 50 km/h | Mandatory maximum speed limit of 50 km/h begins. | [`svg/speed_limit/362_50.svg`](svg/speed_limit/362_50.svg) |
| `362.55` | Speed limit 55 km/h | Mandatory maximum speed limit of 55 km/h begins. | [`svg/speed_limit/362_55.svg`](svg/speed_limit/362_55.svg) **(generated)** |
| `362.60` | Speed limit 60 km/h | Mandatory maximum speed limit of 60 km/h begins. | [`svg/speed_limit/362_60.svg`](svg/speed_limit/362_60.svg) |
| `362.65` | Speed limit 65 km/h | Mandatory maximum speed limit of 65 km/h begins. | [`svg/speed_limit/362_65.svg`](svg/speed_limit/362_65.svg) **(generated)** |
| `362.70` | Speed limit 70 km/h | Mandatory maximum speed limit of 70 km/h begins. | [`svg/speed_limit/362_70.svg`](svg/speed_limit/362_70.svg) |
| `362.75` | Speed limit 75 km/h | Mandatory maximum speed limit of 75 km/h begins. | [`svg/speed_limit/362_75.svg`](svg/speed_limit/362_75.svg) **(generated)** |
| `362.80` | Speed limit 80 km/h | Mandatory maximum speed limit of 80 km/h begins. | [`svg/speed_limit/362_80.svg`](svg/speed_limit/362_80.svg) |
| `362.85` | Speed limit 85 km/h | Mandatory maximum speed limit of 85 km/h begins. | [`svg/speed_limit/362_85.svg`](svg/speed_limit/362_85.svg) **(generated)** |
| `362.90` | Speed limit 90 km/h | Mandatory maximum speed limit of 90 km/h begins. | [`svg/speed_limit/362_90.svg`](svg/speed_limit/362_90.svg) |
| `362.95` | Speed limit 95 km/h | Mandatory maximum speed limit of 95 km/h begins. | [`svg/speed_limit/362_95.svg`](svg/speed_limit/362_95.svg) **(generated)** |
| `362.100` | Speed limit 100 km/h | Mandatory maximum speed limit of 100 km/h begins. | [`svg/speed_limit/362_100.svg`](svg/speed_limit/362_100.svg) |
| `362.105` | Speed limit 105 km/h | Mandatory maximum speed limit of 105 km/h begins. | [`svg/speed_limit/362_105.svg`](svg/speed_limit/362_105.svg) **(generated)** |
| `362.110` | Speed limit 110 km/h | Mandatory maximum speed limit of 110 km/h begins. | [`svg/speed_limit/362_110.svg`](svg/speed_limit/362_110.svg) |
| `364.20` | End of special speed limit 20 km/h | Ends the special 20 km/h speed limit; the general limit for the road type applies again. | — (no graphic) |
| `364.30` | End of special speed limit 30 km/h | Ends the special 30 km/h speed limit; the general limit for the road type applies again. | [`svg/speed_limit/364_30.svg`](svg/speed_limit/364_30.svg) |
| `364.40` | End of special speed limit 40 km/h | Ends the special 40 km/h speed limit; the general limit for the road type applies again. | [`svg/speed_limit/364_40.svg`](svg/speed_limit/364_40.svg) |
| `364.50` | End of special speed limit 50 km/h | Ends the special 50 km/h speed limit; the general limit for the road type applies again. | [`svg/speed_limit/364_50.svg`](svg/speed_limit/364_50.svg) |
| `364.60` | End of special speed limit 60 km/h | Ends the special 60 km/h speed limit; the general limit for the road type applies again. | [`svg/speed_limit/364_60.svg`](svg/speed_limit/364_60.svg) |
| `364.70` | End of special speed limit 70 km/h | Ends the special 70 km/h speed limit; the general limit for the road type applies again. | [`svg/speed_limit/364_70.svg`](svg/speed_limit/364_70.svg) |
| `366` | Speed limit zone | Marks the start of a speed-limit zone. The zone speed applies until the matching end-of-zone sign. | [`svg/speed_limit/366.svg`](svg/speed_limit/366.svg) |
| `367` | Speed limit zone for small electric vehicles | Marks the start of a speed-limit zone for small electric vehicles (e.g. e-scooters). | [`svg/speed_limit/367.svg`](svg/speed_limit/367.svg) |
| `368` | End of speed limit zone | Marks the end of a speed-limit zone. | [`svg/speed_limit/368.svg`](svg/speed_limit/368.svg) |
| `369` | End of speed limit zone for small electric vehicles | Marks the end of a speed-limit zone for small electric vehicles. | [`svg/speed_limit/369.svg`](svg/speed_limit/369.svg) |
| `560.1` | General speed limits | Information about the general speed limits that apply (built-up area vs. outside). | — (no graphic) |
| `560.3` | Warning of speed measurement | Warns that speed may be measured ahead (speed camera / enforcement warning). | — (no graphic) |
| `812` | Recommended speed | Indicates a recommended (advisory) speed — not the same as a mandatory speed limit. | [`svg/speed_limit/812.svg`](svg/speed_limit/812.svg) |
| `856` | General speed limit (miniature) | Miniature version of the general speed-limit information sign. | — (no graphic) |

#### How the speed-limit series relate

- **`362.xx`** — start of a **mandatory** maximum speed (km/h on the sign).
- **`364.xx`** — **end** of that special mandatory limit; the general limit for the road type applies again.
- **`366` / `368`** — start / end of a **speed-limit zone** (zone rules apply until the end sign).
- **`367` / `369`** — same idea for **small electric vehicles** (e.g. e-scooters).
- **`812`** — **recommended** (advisory) speed only; not a mandatory limit.
- **`560.1` / `856`** — information about **general** speed limits (built-up vs elsewhere).
- **`560.3`** — warning that **speed measurement / enforcement** may occur ahead.

### Service / tourist symbols (serviceskilt)

Brown/white tourist and activity symbols used on service signing (640/650 series).

| Code | Name (EN) | Meaning | SVG |
|------|-----------|---------|-----|
| `640.10` | Point of interest / sightseeing | Tourist symbol for a noteworthy sight. A custom symbol may replace this for sights of particular importance. | [`svg/serviceskilt/640_10.svg`](svg/serviceskilt/640_10.svg) |
| `640.101` | World Heritage | Tourist symbol for a UNESCO World Heritage site. | [`svg/serviceskilt/640_101.svg`](svg/serviceskilt/640_101.svg) |
| `640.102` | National fortifications | Tourist symbol for national fortifications. | [`svg/serviceskilt/640_102.svg`](svg/serviceskilt/640_102.svg) |
| `640.12` | Museum / gallery | Tourist symbol for a museum or gallery. | [`svg/serviceskilt/640_12.svg`](svg/serviceskilt/640_12.svg) |
| `640.20` | Viewpoint | Tourist symbol for a scenic viewpoint. | [`svg/serviceskilt/640_20.svg`](svg/serviceskilt/640_20.svg) |
| `640.30` | Nature conservation area | Tourist symbol for a nature conservation / protected nature area. | [`svg/serviceskilt/640_30.svg`](svg/serviceskilt/640_30.svg) |
| `650.10` | Bathing area | Tourist/activity symbol for a bathing area. | [`svg/serviceskilt/650_10.svg`](svg/serviceskilt/650_10.svg) |
| `650.11` | Fishing spot | Tourist/activity symbol for a fishing spot. | [`svg/serviceskilt/650_11.svg`](svg/serviceskilt/650_11.svg) |
| `650.20` | Hiking trail | Tourist/activity symbol for a hiking trail. | [`svg/serviceskilt/650_20.svg`](svg/serviceskilt/650_20.svg) |
| `650.21` | Ski trail | Tourist/activity symbol for a ski trail / cross-country track. | [`svg/serviceskilt/650_21.svg`](svg/serviceskilt/650_21.svg) |
| `650.22` | Cycle trail | Tourist/activity symbol for a cycle trail. | [`svg/serviceskilt/650_22.svg`](svg/serviceskilt/650_22.svg) |
| `650.40` | Farm food / rural tourism | Tourist symbol for farm food / rural tourism (gardsmat/bygdeturisme). | [`svg/serviceskilt/650_40.svg`](svg/serviceskilt/650_40.svg) |
| `650.41` | Olavsrosa | Tourist symbol for sites marked with the Olavsrosa quality label. | [`svg/serviceskilt/650_41.svg`](svg/serviceskilt/650_41.svg) |

### Direction / route symbols (vegvisning)

Selected route markers and destination symbols from the vegvisningsskilt series.

| Code | Name (EN) | Meaning | SVG |
|------|-----------|---------|-----|
| `723.31` | National tourist route | Route marker for a national tourist road; may also appear on service signs. | [`svg/vegvisning/723_31.svg`](svg/vegvisning/723_31.svg) |
| `723.41` | Diversion for large vehicles | Route marker for a diversion route for large vehicles. | [`svg/vegvisning/723_41.svg`](svg/vegvisning/723_41.svg) |
| `723.51` | Route for dangerous goods | Route marker for transport of dangerous goods. | [`svg/vegvisning/723_51.svg`](svg/vegvisning/723_51.svg) |
| `723.61` | Other diversion route (dash) | Alternative diversion-route symbol (dash). | [`svg/vegvisning/723_61.svg`](svg/vegvisning/723_61.svg) |
| `723.62` | Other diversion route (filled square) | Alternative diversion-route symbol (filled square). | [`svg/vegvisning/723_62.svg`](svg/vegvisning/723_62.svg) |
| `723.63` | Other diversion route (triangle) | Alternative diversion-route symbol (triangle). | [`svg/vegvisning/723_63.svg`](svg/vegvisning/723_63.svg) |
| `723.64` | Other diversion route (hollow square) | Alternative diversion-route symbol (hollow square). | [`svg/vegvisning/723_64.svg`](svg/vegvisning/723_64.svg) |
| `723.65` | Other diversion route (circle) | Alternative diversion-route symbol (circle). | [`svg/vegvisning/723_65.svg`](svg/vegvisning/723_65.svg) |
| `723.66` | Other diversion route (arrow) | Alternative diversion-route symbol (arrow). | [`svg/vegvisning/723_66.svg`](svg/vegvisning/723_66.svg) |
| `723.71` | Junction number — motorway | Junction-number symbol used on motorways with grade-separated junctions. | [`svg/vegvisning/723_71.svg`](svg/vegvisning/723_71.svg) |
| `723.72` | Junction number — other multilane | Junction-number symbol for other multilane roads with grade-separated junctions. | [`svg/vegvisning/723_72.svg`](svg/vegvisning/723_72.svg) |
| `723.73` | Junction number — two-lane | Junction-number symbol for two-lane roads with grade-separated junctions. | [`svg/vegvisning/723_73.svg`](svg/vegvisning/723_73.svg) |
| `755` | Cycle route sign | Direction signing for numbered / marked cycle routes. | [`svg/vegvisning/755.svg`](svg/vegvisning/755.svg) |
| `761` | Motorway | Direction symbol indicating a motorway. | [`svg/vegvisning/761.svg`](svg/vegvisning/761.svg) |
| `763` | Motor traffic road | Direction symbol indicating a motor traffic road (motortrafikkveg). | [`svg/vegvisning/763.svg`](svg/vegvisning/763.svg) |
| `765` | Toll road / road user charging | Direction symbol for a toll road or road-user charging. | [`svg/vegvisning/765.svg`](svg/vegvisning/765.svg) |
| `767` | Parking | Direction symbol for parking. | [`svg/vegvisning/767.svg`](svg/vegvisning/767.svg) |
| `769` | Parking garage | Direction symbol for a parking garage / multi-storey car park. | [`svg/vegvisning/769.svg`](svg/vegvisning/769.svg) |
| `771` | Airport | Direction symbol for an airport. | [`svg/vegvisning/771.svg`](svg/vegvisning/771.svg) |
| `772` | Heliport | Direction symbol for a heliport / helicopter landing site. | [`svg/vegvisning/772.svg`](svg/vegvisning/772.svg) |
| `773` | Bus station / terminal | Direction symbol for a bus station or bus terminal. | [`svg/vegvisning/773.svg`](svg/vegvisning/773.svg) |
| `774` | Railway station / train terminal | Direction symbol for a railway station or train terminal. | [`svg/vegvisning/774.svg`](svg/vegvisning/774.svg) |
| `775` | Car ferry | Direction symbol for a car ferry. | [`svg/vegvisning/775.svg`](svg/vegvisning/775.svg) |
| `776` | Cargo port | Direction symbol for a cargo / freight port. | [`svg/vegvisning/776.svg`](svg/vegvisning/776.svg) |
| `780` | Snow chains | Direction symbol related to snow chains (kjetting). | [`svg/vegvisning/780.svg`](svg/vegvisning/780.svg) |
| `790.10` | Church | Direction symbol for a church. | [`svg/vegvisning/790_10.svg`](svg/vegvisning/790_10.svg) |
| `790.15` | Business / industrial area | Direction symbol for a business or industrial area. | [`svg/vegvisning/790_15.svg`](svg/vegvisning/790_15.svg) |
| `790.16` | Shopping centre | Direction symbol for a shopping centre. | [`svg/vegvisning/790_16.svg`](svg/vegvisning/790_16.svg) |
| `790.20` | Swimming pool | Direction symbol for a swimming hall / indoor pool. | [`svg/vegvisning/790_20.svg`](svg/vegvisning/790_20.svg) |
| `790.30` | Alpine ski centre | Direction symbol for an alpine ski centre. | [`svg/vegvisning/790_30.svg`](svg/vegvisning/790_30.svg) |
| `790.31` | Ski jump | Direction symbol for a ski jump. | [`svg/vegvisning/790_31.svg`](svg/vegvisning/790_31.svg) |
| `790.32` | Ski stadium | Direction symbol for a ski stadium. | [`svg/vegvisning/790_32.svg`](svg/vegvisning/790_32.svg) |
| `790.40` | Golf course | Direction symbol for a golf course. | [`svg/vegvisning/790_40.svg`](svg/vegvisning/790_40.svg) |

## Databases

### [`database/signs_en.json`](database/signs_en.json) (English-primary)

Best starting point for English-language apps and docs. Each entry includes:

| Field | Meaning |
|-------|---------|
| `code` | Official skiltnummer |
| `category` / `category_label` | `fareskilt` / `speed_limit` / `serviceskilt` / `vegvisning`, plus English label |
| `name` | English sign name |
| `name_nb` | Official Norwegian NVDB description |
| `meaning` | Plain-English explanation of what the sign means |
| `svg` | Relative path to SVG, or `null` |
| `conversion_method` | `geonorge_native` \| `eps_converted` \| `jpg_traced` \| `no_source_found` |
| `status` | `ok` \| `no_source_found` \| `conversion_failed` |
| `legal_reference` | Skiltforskriften URL with series hint |
| `source_attribution` | NLOD attribution block |
| `color_codes` | Official PMS values used for traffic-sign production |

### [`database/signs.json`](database/signs.json) (bilingual)

Same inventory with Norwegian-first fields (`name_nb`, `name_en`, `meaning_en`) for consumers that want both languages on equal footing.

**Coverage rule:** every in-scope NVDB code is listed. Gaps are explicit — never silently omitted.

### [`database/osm_tags.json`](database/osm_tags.json) (OpenStreetMap mapping)

Maps each catalogue code to tags that **already exist** in OpenStreetMap today. Built against:

- [No:Road signs in Norway](https://wiki.openstreetmap.org/wiki/No:Road_signs_in_Norway) (authoritative for `traffic_sign=NO:…` in Norway)
- [Key:hazard](https://wiki.openstreetmap.org/wiki/Key:hazard) (approved + documented ad-hoc traffic hazard values)
- [taginfo](https://taginfo.openstreetmap.org/) live counts for `traffic_sign` values starting with `NO:`

Human-readable tables: [`database/osm_tags.md`](database/osm_tags.md).

Regenerate with [`tool/build_osm_tags.py`](tool/build_osm_tags.py):

```bash
python3 tool/build_osm_tags.py
```

| Field | Meaning |
|-------|---------|
| `traffic_sign.preferred` | Canonical `NO:{code}` value |
| `traffic_sign.template` | Form with parameters when the plate is variable (e.g. `NO:140[{distance}]`) |
| `traffic_sign.taginfo_object_count_approx` | Approximate object count from taginfo (includes common variants) |
| `implied_tags` | Companion tags routinely paired with the sign (`hazard=*`, `maxspeed=*`, …) |
| `related_tags` | Feature/POI context tags (crossing, destination amenity, etc.) |
| `match_status` | How the match was established (see `meta.match_status_values` in the JSON) |
| `navi_usable_as_fixed_symbol` | Whether the catalogue SVG is suitable as a fixed navigation icon |
| `variable_fields` | Variable plate content (distance, zone speed, junction number, …) |

Notes for navigation use:

- **136.xh / 136.xv** — level-crossing countdown panels; distances are placement-dependent (not fixed in this DB).
- **140** — distance to pedestrian crossing; OSM example `NO:140[150 m]`.
- **723.71–723.73** — junction-number templates with variable digits; marked `not_for_navigation`.
- **812** — advisory only → `maxspeed:advisory`, never mandatory `maxspeed`.
- Destination / tourist symbols (640/650/790…) rarely appear alone as `traffic_sign` in Norway taginfo; companion tags point at the destination POI class.

**Cross-country / other countries:** Norway is a [Vienna Convention](https://wiki.openstreetmap.org/wiki/Vienna_Convention_on_Road_Signs_and_Signals) party. Most warning triangles and circular speed plates share meaning with other European states. Each entry’s `international` block records:

| Field | Meaning |
|-------|---------|
| `companion_tags_international` | Whether `hazard=*`, `maxspeed=*`, POI keys, etc. apply worldwide |
| `symbol_scope` | `vienna_convention_family` / `nordic_shared` / `generic_poi_icon` / `norway_specific` |
| `graphic_reuse_outside_NO` | `yes` / `with_caveat` / `no` — SVG as a generic European-style navi icon |
| `usable_as_navi_icon_outside_norway` | Combined flag for icon packs outside Norway |
| `equivalent_traffic_sign_ids` | Example same-meaning IDs (e.g. `DE:103-20`, `SE:A1-2`) — illustrative, not exhaustive |

When mapping roads **outside Norway**, use that country’s `traffic_sign=ISO:…` code — never `NO:…`. Norway-specific plates (Olavsrosa, Nasjonale turistveger, small-electric-vehicle zones, general 50/80 info plate) are flagged `norway_specific`.

This file does **not** invent new OSM keys. Where no stable companion tag exists, `match_status` is `traffic_sign_only` and only `NO:{code}` is asserted.

## Trafikkalfabetet (official sign typeface)

Norwegian public traffic signs use a dedicated typeface called **Trafikkalfabetet**
(“Traffic Alphabet”), developed for legibility on roads.

| Resource | Description |
|----------|-------------|
| [`reference/trafikkalfabetet.pdf`](reference/trafikkalfabetet.pdf) | Official Statens vegvesen pattern PDF (N300 annex, Norwegian): glyph drawings, width tables, spacing tables |
| [`reference/trafikkalfabetet.en.pdf`](reference/trafikkalfabetet.en.pdf) | **English PDF edition** — translated rules + original figures with English captions |
| [`reference/trafikkalfabetet.en.md`](reference/trafikkalfabetet.en.md) | English text rules in Markdown |
| [`reference/README.md`](reference/README.md) | Index of reference files |

**Official download:**  
https://www.vegvesen.no/globalassets/fag/handboker/vedlegg-til-n300/trafikkalfabetet.pdf  

Linked from Statens vegvesen’s [Filer og fargekoder for trafikkskilt](https://www.vegvesen.no/fag/veg-og-gate/trafikkskilt-og-vegoppmerking/filer-og-fargekoder-for-trafikkskilt/) page (“Trafikkalfabetet er en egen skrifttype utviklet for tekst på trafikkskilt”).

### Summary of the rules (English)

- Trafikkalfabetet **shall be used for all text** on public traffic signs (with limited handbook exceptions such as variable matrix signs and sign 590).
- Letter text uses an **initial capital + lowercase**, unless a specific sign says otherwise.
- Character size is keyed to capital height **H**; widths and pairwise spacings are tabulated in the PDF for standard heights (e.g. 35–420 mm).
- Word spacing is **5/7 H**; number-to-unit spacing **4/7 H**; baseline spacing is **14/7 H**, **12/7 H**, or **11/7 H** depending on whether lines include symbols, plain text, or split names.

The SVG graphics in this repository are symbol artwork; when you compose complete signs with place names or other lettering, use Trafikkalfabetet per the rules above (and Skiltnormalen / Skiltforskriften).

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
python run.py                              # fareskilt + speed-limit set
python -c "from tool.import_guidance_signs import main; main()"  # 640/650/723/755-790 set
python3 sourcing/generate_readme.py        # refresh sourcing audit
```

Working downloads and unpacked archives live under `work/` (gitignored). Published outputs are `svg/` and `database/*.json`.

## Licence

- **Source data:** [NLOD 2.0](https://data.norge.no/nlod/en/2.0) — Statens vegvesen / Kartverket.
- **Pipeline code in this repository:** available for reuse under the same spirit of open reuse; please retain attribution to Statens vegvesen / NVDB / Geonorge when redistributing the sign graphics or derived database.
