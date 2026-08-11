# OpenStreetMap tag mapping (human-readable)

Readable view of [`osm_tags.json`](osm_tags.json). Machine consumers should use the JSON. Regenerate both with `python3 tool/build_osm_tags.py`.

Generated: `2026-08-11T23:39:32.722219+00:00`
Taginfo data until: `2026-08-11T00:59:35Z`

## Summary

| Metric | Count |
|--------|------:|
| Total catalogue codes | 121 |
| Seen in taginfo as `traffic_sign=NO:…` | 40 |
| Usable as fixed navi symbol | 93 |
| Usable as navi icon outside Norway | 88 |
| With foreign equivalent examples | 47 |

### By match status

| Status | Count | Meaning |
|--------|------:|---------|
| `destination_symbol` | 43 | Service/direction pictogram; maps to destination/POI tags |
| `hazard_convention` | 22 | Mapped via Key:hazard approved or documented ad-hoc values |
| `not_for_navigation` | 3 | Template with variable digits; unsuitable as fixed navi icon |
| `traffic_sign_only` | 14 | NO: code is valid; no stable companion tag |
| `variable_content` | 8 | Sign content varies (distance, speed figure, etc.) |
| `wiki_documented` | 31 | Listed with tags on No:Road_signs_in_Norway |

### By international symbol scope

| Scope | Count | Meaning |
|-------|------:|---------|
| `generic_poi_icon` | 28 | Destination/service icon meaning widely understood |
| `nordic_shared` | 5 | Especially familiar in NO/SE/FI (moose, reindeer, ski, chains) |
| `norway_specific` | 7 | Norwegian law, network, or brand — not local law elsewhere |
| `vienna_convention_family` | 81 | Same hazard/speed pictogram family across VC Europe |

## Conventions

Norway is a Vienna Convention party. Most warning triangles and circular speed plates share meaning with other European countries; OSM companion tags (hazard=*, maxspeed=*, amenity=*, …) are global. Always map foreign roads with that country's traffic_sign=ISO:… ID, never NO:… . Example DE/SE/FI IDs are illustrative same-meaning references from taginfo/wiki, not exhaustive.

- Norwegian roads: `traffic_sign=NO:{code}` plus companion tags below.
- Other countries: use that country’s `traffic_sign=ISO:…` ID; keep `hazard=*`, `maxspeed=*`, POI tags as listed.
- Full Vienna Convention country lists: see `meta.international` in [`osm_tags.json`](osm_tags.json).

## Warning signs (fareskilt)

| Code | Name | `traffic_sign` | Implied tags | Related tags | Match | Navi | Outside NO | Scope | Equivalents | Notes |
|------|------|----------------|--------------|--------------|-------|------|------------|-------|-------------|-------|
| [`100.1`](../svg/fareskilt/100_1.svg) | Dangerous bend to the right | `NO:100.1` (~9) | `hazard=curve` | — | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:103-20`, `SE:A1-2` | Wiki also documents traffic_sign=NO:100.1. |
| [`100.2`](../svg/fareskilt/100_2.svg) | Dangerous bend to the left | `NO:100.2` (~10) | `hazard=curve` | — | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:103-10`, `SE:A1-1` | — |
| [`102.1`](../svg/fareskilt/102_1.svg) | Series of dangerous bends, first to the right | `NO:102.1` (~7) | `hazard=curves` | — | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:105-20`, `SE:A2-2` | — |
| [`102.2`](../svg/fareskilt/102_2.svg) | Series of dangerous bends, first to the left | `NO:102.2` (~5) | `hazard=curves` | — | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:105-10`, `SE:A2-1` | — |
| [`104.1`](../svg/fareskilt/104_1.svg) | Steep hill upwards | `NO:104.1` | — | `incline={percent}` | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:110`, `SE:A5-1` | Norwegian wiki lists traffic_sign only for 104.1 (no hazard=* value).; No approved hazard=steep; do not invent one. |
| [`104.2`](../svg/fareskilt/104_2.svg) | Steep hill downwards | `NO:104.2` | — | `incline=-{percent}` | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:108`, `SE:A5-2` | Norwegian wiki lists traffic_sign only for 104.2. |
| [`106.1`](../svg/fareskilt/106_1.svg) | Road narrows on both sides | `NO:106.1` (~3) | `hazard=road_narrows` | — | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:120` | — |
| [`106.2`](../svg/fareskilt/106_2.svg) | Road narrows on the right | `NO:106.2` | `hazard=road_narrows` | — | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:121-20` | Side (right) is not encoded in hazard=*; keep NO:106.2 on the sign node. |
| [`106.3`](../svg/fareskilt/106_3.svg) | Road narrows on the left | `NO:106.3` | `hazard=road_narrows` | — | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:121-10` | Side (left) is not encoded in hazard=*; keep NO:106.3 on the sign node. |
| [`108`](../svg/fareskilt/108.svg) | Uneven road | `NO:108` (~4) | `hazard=damaged_road` | — | `hazard_convention` | yes | yes | `vienna_convention_family` | `DE:112` | traffic_sign=NO:108 is used in OSM; companion hazard tagging is ad-hoc. |
| [`109`](../svg/fareskilt/109.svg) | Speed hump | `NO:109` (~7) | `traffic_calming=hump`; `hazard=bump` | — | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:112` | Companion traffic_calming=hump / hazard=bump apply worldwide. |
| [`110`](../svg/fareskilt/110.svg) | Road works | `NO:110` | `hazard=roadworks` | — | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:123` | OSM guidance prefers permanent/recurring hazards; temporary works are often omitted. |
| [`112`](../svg/fareskilt/112.svg) | Loose chippings | `NO:112` | `hazard=loose_gravel` | — | `hazard_convention` | yes | yes | `vienna_convention_family` | `DE:101` | — |
| [`114.1`](../svg/fareskilt/114_1.svg) | Falling rocks, right side | `NO:114.1` (~2) | `hazard=falling_rocks` | — | `hazard_convention` | yes | yes | `vienna_convention_family` | `DE:115` | Right-side pictogram: encode side via NO:114.1, not a separate hazard value. |
| [`114.2`](../svg/fareskilt/114_2.svg) | Falling rocks, left side | `NO:114.2` (~1) | `hazard=falling_rocks` | — | `hazard_convention` | yes | yes | `vienna_convention_family` | `DE:115` | Left-side pictogram: encode side via NO:114.2. |
| [`116`](../svg/fareskilt/116.svg) | Slippery road | `NO:116` (~2) | `hazard=slippery` | — | `hazard_convention` | yes | yes | `vienna_convention_family` | `DE:114` | — |
| [`117`](../svg/fareskilt/117.svg) | Soft verges | `NO:117` | — | — | `traffic_sign_only` | no | no | `vienna_convention_family` | — | No approved/documented hazard=* for soft verges in Key:hazard tables.; Use traffic_sign=NO:117 on the sign; do not invent hazard=soft_verge.; Soft verge warnings exist in several VC states; no single universal hazard=* value. |
| [`118`](../svg/fareskilt/118.svg) | Opening or swing bridge | `NO:118` | — | `bridge=movable`; `bridge:movable=swing` | `traffic_sign_only` | no | no | `vienna_convention_family` | — | No dedicated hazard=* for opening/swing bridge on Key:hazard.; Movable/opening bridge warnings are VC-family; tag the bridge feature internationally. |
| [`120`](../svg/fareskilt/120.svg) | Quayside or ferry terminal | `NO:120` | — | `man_made=pier`; `amenity=ferry_terminal` | `traffic_sign_only` | no | no | `vienna_convention_family` | — | No dedicated hazard=* for quayside / ferry berth.; Quayside / water-edge warnings appear across VC Europe. |
| [`122`](../svg/fareskilt/122.svg) | Tunnel | `NO:122` (~1) | — | `tunnel=yes` | `traffic_sign_only` | yes | yes | `vienna_convention_family` | — | Warning of tunnel ahead; the tunnel way uses tunnel=yes / highway through tunnel.; Tunnel ahead warnings are widespread; tunnel=yes on the way is global. |
| [`124`](../svg/fareskilt/124.svg) | Dangerous junction | `NO:124` (~3) | `hazard=dangerous_junction` | — | `hazard_convention` | yes | yes | `vienna_convention_family` | `DE:102` | — |
| [`126`](../svg/fareskilt/126.svg) | Roundabout | `NO:126` | `hazard=roundabout` | `junction=roundabout` | `hazard_convention` | yes | yes | `vienna_convention_family` | — | Advance roundabout warning; junction=roundabout on the feature is global. |
| [`132`](../svg/fareskilt/132.svg) | Traffic signals | `NO:132` | `hazard=traffic_signals` | `highway=traffic_signals` | `hazard_convention` | yes | yes | `vienna_convention_family` | `DE:131` | — |
| [`134`](../svg/fareskilt/134.svg) | Level crossing with barrier | `NO:134` | — | `railway=level_crossing`; `crossing:barrier=yes` | `hazard_convention` | yes | yes | `vienna_convention_family` | `DE:150` | Map the crossing with railway=level_crossing; 134 is the advance warning with barriers.; railway=level_crossing + crossing:barrier=* are global. |
| [`135`](../svg/fareskilt/135.svg) | Level crossing without barrier | `NO:135` | — | `railway=level_crossing`; `crossing:barrier=no` | `hazard_convention` | yes | yes | `vienna_convention_family` | `DE:151` | Advance warning of level crossing without barriers. |
| [`136.1h`](../svg/fareskilt/136_1h.svg) | Distance to level crossing | `NO:136.1h` | — | `railway=level_crossing` | `variable_content` | no | no | `vienna_convention_family` | — | Not a fixed navi hazard icon by itself; marks approach to a crossing.; Distances: not standardized in this DB — verify Skiltforskriften / local practice.; Level-crossing countdown panels (stripe count) are a VC European pattern; metre spacing is national/local.; Variable: distance_or_stripe_count |
| [`136.1v`](../svg/fareskilt/136_1v.svg) | Distance to level crossing | `NO:136.1v` | — | `railway=level_crossing` | `variable_content` | no | no | `vienna_convention_family` | — | Variable: distance_or_stripe_count |
| [`136.2h`](../svg/fareskilt/136_2h.svg) | Distance to level crossing | `NO:136.2h` | — | `railway=level_crossing` | `variable_content` | no | no | `vienna_convention_family` | — | Variable: distance_or_stripe_count |
| [`136.2v`](../svg/fareskilt/136_2v.svg) | Distance to level crossing | `NO:136.2v` | — | `railway=level_crossing` | `variable_content` | no | no | `vienna_convention_family` | — | Variable: distance_or_stripe_count |
| [`136.3h`](../svg/fareskilt/136_3h.svg) | Distance to level crossing | `NO:136.3h` | — | `railway=level_crossing` | `variable_content` | no | no | `vienna_convention_family` | — | Variable: distance_or_stripe_count |
| [`136.3v`](../svg/fareskilt/136_3v.svg) | Distance to level crossing | `NO:136.3v` | — | `railway=level_crossing` | `variable_content` | no | no | `vienna_convention_family` | — | Variable: distance_or_stripe_count |
| [`138.1`](../svg/fareskilt/138_1.svg) | Single-track railway | `NO:138.1` | — | `railway=level_crossing`; `railway:track_ref=1` | `traffic_sign_only` | yes | yes | `vienna_convention_family` | — | — |
| [`138.2`](../svg/fareskilt/138_2.svg) | Multi-track railway | `NO:138.2` (~5) | — | `railway=level_crossing` | `traffic_sign_only` | yes | yes | `vienna_convention_family` | — | Multi-track railway warning; used as traffic_sign=NO:138.2 in OSM. |
| [`139`](../svg/fareskilt/139.svg) | Tramway | `NO:139` (~5) | — | `railway=tram`; `railway=tram_crossing` | `traffic_sign_only` | yes | yes | `vienna_convention_family` | — | Tram/tramway warnings are common in VC cities; railway=tram* tags are global. |
| [`140`](../svg/fareskilt/140.svg) | Distance to pedestrian crossing | `NO:140` / `NO:140[{distance}]` (~11) | — | `highway=crossing`; `crossing=uncontrolled` | `variable_content` | no | no | `vienna_convention_family` | `DE:133` | taginfo observes values such as NO:140[150 m].; Useful for navi as crossing-ahead with distance, not as a fixed pictogram alone.; Distance panel is variable; pedestrian crossing tagging is global.; Variable: distance |
| [`142`](../svg/fareskilt/142.svg) | Children | `NO:142` (~9) | `hazard=children` | — | `hazard_convention` | yes | yes | `vienna_convention_family` | `DE:136` | hazard=children is global. |
| [`144`](../svg/fareskilt/144.svg) | Cyclists | `NO:144` | `hazard=cyclists` | — | `hazard_convention` | yes | yes | `vienna_convention_family` | `DE:138` | hazard=cyclists is global. |
| [`146.1`](../svg/fareskilt/146_1.svg) | Elk / moose | `NO:146.1` (~11) | `hazard=animal_crossing`; `hazard:animal=moose` | — | `hazard_convention` | yes | yes | `nordic_shared` | `FI:142`, `SE:A19-1`, `DE:142` | Moose/elg pictogram is strongly Nordic; hazard=animal_crossing + hazard:animal=moose work worldwide. |
| [`146.2`](../svg/fareskilt/146_2.svg) | Reindeer | `NO:146.2` (~1) | `hazard=animal_crossing`; `hazard:animal=reindeer` | — | `hazard_convention` | yes | yes | `nordic_shared` | `SE:A19-1` | Reindeer warnings are primarily Nordic; companion hazard tags are global. |
| [`146.3`](../svg/fareskilt/146_3.svg) | Deer | `NO:146.3` | `hazard=animal_crossing`; `hazard:animal=deer` | — | `hazard_convention` | yes | yes | `vienna_convention_family` | `DE:142` | Standalone hazard=deer also exists in taginfo; prefer animal_crossing + hazard:animal.; Deer/wildlife warnings are widespread; hazard:animal=deer is global. |
| [`146.4`](../svg/fareskilt/146_4.svg) | Cattle | `NO:146.4` (~2) | `hazard=animal_crossing`; `hazard:animal=cattle` | — | `hazard_convention` | yes | yes | `vienna_convention_family` | — | Cattle/livestock warnings exist across VC Europe; hazard:animal=cattle is global. |
| [`146.5`](../svg/fareskilt/146_5.svg) | Sheep | `NO:146.5` | `hazard=animal_crossing`; `hazard:animal=sheep` | — | `hazard_convention` | yes | yes | `vienna_convention_family` | — | Sheep warnings are common in rural VC states; hazard:animal=sheep is global. |
| [`148`](../svg/fareskilt/148.svg) | Two-way traffic | `NO:148` (~2) | `hazard=contraflow` | — | `hazard_convention` | yes | yes | `vienna_convention_family` | `DE:125` | — |
| [`149`](../svg/fareskilt/149.svg) | Queue / congestion | `NO:149` | `hazard=queues_likely` | — | `hazard_convention` | yes | yes | `vienna_convention_family` | `DE:124` | hazard=queues_likely is global. |
| [`150`](../svg/fareskilt/150.svg) | Low-flying aircraft | `NO:150` | `hazard=low_flying_aircraft` | — | `hazard_convention` | yes | yes | `vienna_convention_family` | — | Low-flying aircraft / aerodrome warnings are VC-family; hazard=low_flying_aircraft is global. |
| [`151`](../svg/fareskilt/151.svg) | Military activity | `NO:151` | — | — | `traffic_sign_only` | no | no | `vienna_convention_family` | — | No established hazard=* for military activity on Key:hazard.; Military-activity warnings appear in several countries; tagging remains traffic_sign-national. |
| [`152`](../svg/fareskilt/152.svg) | Side winds | `NO:152` | `hazard=side_winds` | — | `hazard_convention` | yes | yes | `vienna_convention_family` | `DE:117` | hazard=side_winds is global. |
| [`153`](../svg/fareskilt/153.svg) | Accident | `NO:153` | — | — | `traffic_sign_only` | no | no | `vienna_convention_family` | — | Accident warnings are typically temporary; OSM hazard guidance discourages temporary tagging.; Do not invent a permanent hazard=accident mapping for navi basemaps.; Accident warnings are typically temporary everywhere; poor basemap icon fit. |
| [`154`](../svg/fareskilt/154.svg) | Skiers crossing | `NO:154` | — | — | `traffic_sign_only` | no | no | `nordic_shared` | — | No Key:hazard value for skiers crossing; use traffic_sign=NO:154.; Skiers-crossing is mainly Nordic/Alpine; no stable global hazard=* value. |
| [`155`](../svg/fareskilt/155.svg) | Horse riders | `NO:155` | `hazard=horse_riders` | — | `hazard_convention` | yes | yes | `vienna_convention_family` | `DE:140` | hazard=horse_riders is global. |
| [`156`](../svg/fareskilt/156.svg) | Other danger | `NO:156` (~1) | `traffic_sign=hazard` | — | `traffic_sign_only` | yes | yes | `vienna_convention_family` | `DE:101` | General danger; meaning depends on underskilt. No single hazard=* value.; General danger; meaning depends on supplementary plate in every country. |

## Speed limit and related

| Code | Name | `traffic_sign` | Implied tags | Related tags | Match | Navi | Outside NO | Scope | Equivalents | Notes |
|------|------|----------------|--------------|--------------|-------|------|------------|-------|-------------|-------|
| [`362.100`](../svg/speed_limit/362_100.svg) | Speed limit 100 km/h | `NO:362.100` (~4) | `maxspeed=100`; `source:maxspeed=sign` | — | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:274-100` | Norwegian wiki example: traffic_sign=NO:362.60 + maxspeed=60.; Colon form NO:362:100 / NO:362:110 appears in taginfo for 100/110. |
| [`362.110`](../svg/speed_limit/362_110.svg) | Speed limit 110 km/h | `NO:362.110` (~4) | `maxspeed=110`; `source:maxspeed=sign` | — | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:274-110` | Norwegian wiki example: traffic_sign=NO:362.60 + maxspeed=60.; Colon form NO:362:100 / NO:362:110 appears in taginfo for 100/110. |
| `362.20` | Speed limit 20 km/h | `NO:362.20` | `maxspeed=20`; `source:maxspeed=sign` | — | `wiki_documented` | yes | yes | `vienna_convention_family` | — | Norwegian wiki example: traffic_sign=NO:362.60 + maxspeed=60.; Colon form NO:362:100 / NO:362:110 appears in taginfo for 100/110.; maxspeed=* + source:maxspeed=sign are global. |
| [`362.30`](../svg/speed_limit/362_30.svg) | Speed limit 30 km/h | `NO:362.30` (~31) | `maxspeed=30`; `source:maxspeed=sign` | — | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:274-30`, `SE:C31-3[30]` | Norwegian wiki example: traffic_sign=NO:362.60 + maxspeed=60.; Colon form NO:362:100 / NO:362:110 appears in taginfo for 100/110. |
| [`362.40`](../svg/speed_limit/362_40.svg) | Speed limit 40 km/h | `NO:362.40` (~28) | `maxspeed=40`; `source:maxspeed=sign` | — | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:274-40` | Norwegian wiki example: traffic_sign=NO:362.60 + maxspeed=60.; Colon form NO:362:100 / NO:362:110 appears in taginfo for 100/110. |
| [`362.50`](../svg/speed_limit/362_50.svg) | Speed limit 50 km/h | `NO:362.50` (~239) | `maxspeed=50`; `source:maxspeed=sign` | — | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:274-50` | Norwegian wiki example: traffic_sign=NO:362.60 + maxspeed=60.; Colon form NO:362:100 / NO:362:110 appears in taginfo for 100/110. |
| [`362.60`](../svg/speed_limit/362_60.svg) | Speed limit 60 km/h | `NO:362.60` (~517) | `maxspeed=60`; `source:maxspeed=sign` | — | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:274-60` | Norwegian wiki example: traffic_sign=NO:362.60 + maxspeed=60.; Colon form NO:362:100 / NO:362:110 appears in taginfo for 100/110. |
| [`362.70`](../svg/speed_limit/362_70.svg) | Speed limit 70 km/h | `NO:362.70` (~331) | `maxspeed=70`; `source:maxspeed=sign` | — | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:274-70` | Norwegian wiki example: traffic_sign=NO:362.60 + maxspeed=60.; Colon form NO:362:100 / NO:362:110 appears in taginfo for 100/110. |
| [`362.80`](../svg/speed_limit/362_80.svg) | Speed limit 80 km/h | `NO:362.80` (~39) | `maxspeed=80`; `source:maxspeed=sign` | — | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:274-80` | Norwegian wiki example: traffic_sign=NO:362.60 + maxspeed=60.; Colon form NO:362:100 / NO:362:110 appears in taginfo for 100/110. |
| [`362.90`](../svg/speed_limit/362_90.svg) | Speed limit 90 km/h | `NO:362.90` (~87) | `maxspeed=90`; `source:maxspeed=sign` | — | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:274-90` | Norwegian wiki example: traffic_sign=NO:362.60 + maxspeed=60.; Colon form NO:362:100 / NO:362:110 appears in taginfo for 100/110. |
| `364.20` | End of special speed limit 20 km/h | `NO:364.20` | — | `maxspeed={general_limit}` | `wiki_documented` | yes | yes | `vienna_convention_family` | — | 364 does not encode the new limit on the plate; mappers set maxspeed to the applicable general limit. |
| [`364.30`](../svg/speed_limit/364_30.svg) | End of special speed limit 30 km/h | `NO:364.30` (~6) | — | `maxspeed={general_limit}` | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:278-30` | 364 does not encode the new limit on the plate; mappers set maxspeed to the applicable general limit. |
| [`364.40`](../svg/speed_limit/364_40.svg) | End of special speed limit 40 km/h | `NO:364.40` (~1) | — | `maxspeed={general_limit}` | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:278-40` | 364 does not encode the new limit on the plate; mappers set maxspeed to the applicable general limit. |
| [`364.50`](../svg/speed_limit/364_50.svg) | End of special speed limit 50 km/h | `NO:364.50` (~27) | — | `maxspeed={general_limit}` | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:278-50` | 364 does not encode the new limit on the plate; mappers set maxspeed to the applicable general limit. |
| [`364.60`](../svg/speed_limit/364_60.svg) | End of special speed limit 60 km/h | `NO:364.60` (~93) | — | `maxspeed={general_limit}` | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:278-60` | 364 does not encode the new limit on the plate; mappers set maxspeed to the applicable general limit. |
| [`364.70`](../svg/speed_limit/364_70.svg) | End of special speed limit 70 km/h | `NO:364.70` (~36) | — | `maxspeed={general_limit}` | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:278-70` | 364 does not encode the new limit on the plate; mappers set maxspeed to the applicable general limit. |
| [`366`](../svg/speed_limit/366.svg) | Speed limit zone | `NO:366` / `NO:366.{zone_kmh}` (~23) | `maxspeed={zone_kmh}`; `maxspeed:type=NO:zone{zone_kmh}`; `zone:maxspeed=NO:{zone_kmh}` | — | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:274.1` | Wiki example: traffic_sign=NO:366.30 + maxspeed=30.; Zone start plates differ visually by country; maxspeed + maxspeed:type=XX:zoneN pattern is international.; Variable: zone_kmh |
| [`367`](../svg/speed_limit/367.svg) | Speed limit zone for small electric vehicles | `NO:367` / `NO:367[{kmh}]` | `maxspeed:small_electric_vehicle={kmh}` | — | `wiki_documented` | yes | no | `norway_specific` | — | Speed zone for small electric vehicles is a Norwegian regulatory plate; do not present as local law outside NO. maxspeed:small_electric_vehicle=* may still apply where used.; Variable: kmh |
| [`368`](../svg/speed_limit/368.svg) | End of speed limit zone | `NO:368` / `NO:368.{zone_kmh}` (~10) | — | — | `wiki_documented` | yes | yes | `vienna_convention_family` | `DE:274.2` | End of speed-limit zone; remove zone maxspeed tagging after this point.; Variable: zone_kmh |
| [`369`](../svg/speed_limit/369.svg) | End of speed limit zone for small electric vehicles | `NO:369` / `NO:369[{kmh}]` | — | — | `wiki_documented` | yes | no | `norway_specific` | — | End of small-electric-vehicle speed zone.; End of Norwegian small-electric-vehicle speed zone. |
| `560.1` | General speed limits | `NO:560.1` | — | `maxspeed:type=NO:urban`; `maxspeed:type=NO:rural` | `traffic_sign_only` | no | no | `norway_specific` | — | Information about general limits (built-up vs elsewhere); does not itself change maxspeed.; No SVG in this catalogue yet.; Shows Norway’s general limits (urban/rural). Other countries have different default limits — not reusable as local law. |
| `560.3` | Warning of speed measurement | `NO:560.3` | — | `highway=speed_camera`; `enforcement=maxspeed` | `traffic_sign_only` | no | no | `vienna_convention_family` | — | Speed-measurement / enforcement warning; no established NO wiki row yet.; Speed-camera / measurement warnings exist in many countries; enforcement tagging is global. |
| [`812`](../svg/speed_limit/812.svg) | Recommended speed | `NO:812` / `NO:812[{kmh}]` | `maxspeed:advisory={kmh}` | — | `variable_content` | no | no | `vienna_convention_family` | — | Do not set maxspeed= from 812; use maxspeed:advisory.; Advisory speed plates are widespread; use maxspeed:advisory=* (global), not maxspeed.; Variable: kmh |
| `856` | General speed limit (miniature) | `NO:856` | — | — | `traffic_sign_only` | no | no | `norway_specific` | — | Miniature general speed-limit information; same role family as 560.1.; Miniature of Norwegian general speed-limit information (see 560.1). |

## Service / tourist symbols (serviceskilt)

| Code | Name | `traffic_sign` | Implied tags | Related tags | Match | Navi | Outside NO | Scope | Equivalents | Notes |
|------|------|----------------|--------------|--------------|-------|------|------------|-------|-------------|-------|
| [`640.10`](../svg/serviceskilt/640_10.svg) | Point of interest / sightseeing | `NO:640.10` | — | `tourism=attraction` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | Brown tourist symbol; rarely tagged alone as traffic_sign in NO taginfo.; Sightseeing / attraction symbol — tourism=* is global. |
| [`640.101`](../svg/serviceskilt/640_101.svg) | World Heritage | `NO:640.101` | — | `heritage=1`; `tourism=yes` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | UNESCO World Heritage symbol is internationally understood; heritage=* is global. |
| [`640.102`](../svg/serviceskilt/640_102.svg) | National fortifications | `NO:640.102` | — | `historic=fort`; `tourism=attraction` | `destination_symbol` | yes | no | `norway_specific` | — | National fortifications programme symbol — Norway-specific programme marking. |
| [`640.12`](../svg/serviceskilt/640_12.svg) | Museum / gallery | `NO:640.12` | — | `tourism=museum` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | — |
| [`640.20`](../svg/serviceskilt/640_20.svg) | Viewpoint | `NO:640.20` | — | `tourism=viewpoint` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | — |
| [`640.30`](../svg/serviceskilt/640_30.svg) | Nature conservation area | `NO:640.30` | — | `leisure=nature_reserve`; `boundary=protected_area` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | — |
| [`650.10`](../svg/serviceskilt/650_10.svg) | Bathing area | `NO:650.10` | — | `leisure=bathing_place`; `natural=beach` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | — |
| [`650.11`](../svg/serviceskilt/650_11.svg) | Fishing spot | `NO:650.11` | — | `leisure=fishing` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | — |
| [`650.20`](../svg/serviceskilt/650_20.svg) | Hiking trail | `NO:650.20` | — | `route=hiking`; `highway=path` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | — |
| [`650.21`](../svg/serviceskilt/650_21.svg) | Ski trail | `NO:650.21` | — | `route=ski`; `piste:type=nordic` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | Nordic/Alpine ski-trail icons are widely understood. |
| [`650.22`](../svg/serviceskilt/650_22.svg) | Cycle trail | `NO:650.22` | — | `route=bicycle`; `highway=cycleway` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | — |
| [`650.40`](../svg/serviceskilt/650_40.svg) | Farm food / rural tourism | `NO:650.40` | — | `tourism=farm`; `shop=farm` | `destination_symbol` | yes | yes | `nordic_shared` | — | Farm food / rural tourism labelling is regional; tourism/shop tags remain global. |
| [`650.41`](../svg/serviceskilt/650_41.svg) | Olavsrosa | `NO:650.41` | — | `tourism=yes`; `brand=Olavsrosa` | `destination_symbol` | yes | no | `norway_specific` | — | Quality label symbol; brand tagging is conventional, not Norway-wiki-mandated.; Olavsrosa is a Norwegian quality label — not an international tourist symbol. |

## Direction / route symbols (vegvisning)

| Code | Name | `traffic_sign` | Implied tags | Related tags | Match | Navi | Outside NO | Scope | Equivalents | Notes |
|------|------|----------------|--------------|--------------|-------|------|------------|-------|-------------|-------|
| [`723.31`](../svg/vegvisning/723_31.svg) | National tourist route | `NO:723.31` (~3) | — | `route=road`; `network=no:national_tourist_route` | `destination_symbol` | yes | no | `norway_specific` | — | National tourist route marker; some NO:723.* traffic_sign usage exists.; Nasjonale turistveger marker — Norwegian national tourist-route network. |
| [`723.41`](../svg/vegvisning/723_41.svg) | Diversion for large vehicles | `NO:723.41` | — | `hgv=destination` | `destination_symbol` | no | no | `vienna_convention_family` | — | Diversion for large vehicles — usually on temporary/diversion signing.; HGV diversion markers exist in many countries; often temporary. |
| [`723.51`](../svg/vegvisning/723_51.svg) | Route for dangerous goods | `NO:723.51` | — | `hazmat=destination` | `destination_symbol` | no | no | `vienna_convention_family` | — | Dangerous-goods route markers exist across VC Europe; hazmat=* is global. |
| [`723.61`](../svg/vegvisning/723_61.svg) | Other diversion route (dash) | `NO:723.61` | — | — | `destination_symbol` | no | no | `vienna_convention_family` | — | Alternative diversion symbol (dash); often temporary — poor navi basemap fit.; Generic diversion symbols — often temporary. |
| [`723.62`](../svg/vegvisning/723_62.svg) | Other diversion route (filled square) | `NO:723.62` | — | — | `destination_symbol` | no | no | `vienna_convention_family` | — | Alternative diversion symbol (filled square). |
| [`723.63`](../svg/vegvisning/723_63.svg) | Other diversion route (triangle) | `NO:723.63` | — | — | `destination_symbol` | no | no | `vienna_convention_family` | — | Alternative diversion symbol (triangle). |
| [`723.64`](../svg/vegvisning/723_64.svg) | Other diversion route (hollow square) | `NO:723.64` | — | — | `destination_symbol` | no | no | `vienna_convention_family` | — | Alternative diversion symbol (hollow square). |
| [`723.65`](../svg/vegvisning/723_65.svg) | Other diversion route (circle) | `NO:723.65` | — | — | `destination_symbol` | no | no | `vienna_convention_family` | — | Alternative diversion symbol (circle). |
| [`723.66`](../svg/vegvisning/723_66.svg) | Other diversion route (arrow) | `NO:723.66` | — | — | `destination_symbol` | no | no | `vienna_convention_family` | — | Alternative diversion symbol (arrow). |
| [`723.71`](../svg/vegvisning/723_71.svg) | Junction number — motorway | `NO:723.71` | — | `noref={junction_number}` | `not_for_navigation` | no | no | `vienna_convention_family` | — | SVG is a template with variable digits — not usable as a fixed navi icon.; Junction-number template with variable digits — same idea on many motorways, not a fixed icon.; Variable: junction_number |
| [`723.72`](../svg/vegvisning/723_72.svg) | Junction number — other multilane | `NO:723.72` | — | — | `not_for_navigation` | no | no | `vienna_convention_family` | — | Variable junction number — not a fixed navi symbol.; Variable: junction_number |
| [`723.73`](../svg/vegvisning/723_73.svg) | Junction number — two-lane | `NO:723.73` | — | — | `not_for_navigation` | no | no | `vienna_convention_family` | — | Variable junction number — not a fixed navi symbol.; Variable: junction_number |
| [`755`](../svg/vegvisning/755.svg) | Cycle route sign | `NO:755` (~12) | — | `route=bicycle`; `network=lcn` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | Cycle route direction signing; traffic_sign=NO:755 appears in taginfo.; Numbered cycle-route signing is common across Europe. |
| [`761`](../svg/vegvisning/761.svg) | Motorway | `NO:761` | — | `highway=motorway` | `destination_symbol` | yes | yes | `vienna_convention_family` | — | Direction symbol for motorway; related info sign 502 uses highway=motorway on wiki.; Motorway class symbol; highway=motorway is global (national plate design differs). |
| [`763`](../svg/vegvisning/763.svg) | Motor traffic road | `NO:763` | — | `motorroad=yes` | `destination_symbol` | yes | yes | `vienna_convention_family` | — | Motortrafikkveg symbol; wiki maps info sign 503 to motorroad=yes.; Motorroad / motortrafikkveg class; motorroad=yes is used in several VC countries. |
| [`765`](../svg/vegvisning/765.svg) | Toll road / road user charging | `NO:765` | — | `toll=yes` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | Toll / road-user charging; toll=yes is global. |
| [`767`](../svg/vegvisning/767.svg) | Parking | `NO:767` (~6) | — | `amenity=parking` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | — |
| [`769`](../svg/vegvisning/769.svg) | Parking garage | `NO:769` | — | `amenity=parking`; `parking=multi-storey` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | — |
| [`771`](../svg/vegvisning/771.svg) | Airport | `NO:771` | — | `aeroway=aerodrome` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | — |
| [`772`](../svg/vegvisning/772.svg) | Heliport | `NO:772` | — | `aeroway=helipad` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | — |
| [`773`](../svg/vegvisning/773.svg) | Bus station / terminal | `NO:773` | — | `amenity=bus_station` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | — |
| [`774`](../svg/vegvisning/774.svg) | Railway station / train terminal | `NO:774` | — | `railway=station`; `public_transport=station` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | — |
| [`775`](../svg/vegvisning/775.svg) | Car ferry | `NO:775` | — | `amenity=ferry_terminal`; `route=ferry` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | — |
| [`776`](../svg/vegvisning/776.svg) | Cargo port | `NO:776` | — | `industrial=port`; `harbour=yes` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | — |
| [`780`](../svg/vegvisning/780.svg) | Snow chains | `NO:780` | — | `snow_chains=required` | `destination_symbol` | yes | yes | `nordic_shared` | — | Snow-chains related direction/info symbol; tagging on ways is uncommon.; Snow-chains related signing is common in Nordic/Alpine states; snow_chains=* is global but uncommon. |
| [`790.10`](../svg/vegvisning/790_10.svg) | Church | `NO:790.10` | — | `amenity=place_of_worship`; `religion=christian` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | — |
| [`790.15`](../svg/vegvisning/790_15.svg) | Business / industrial area | `NO:790.15` | — | `landuse=industrial`; `landuse=commercial` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | — |
| [`790.16`](../svg/vegvisning/790_16.svg) | Shopping centre | `NO:790.16` | — | `shop=mall` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | — |
| [`790.20`](../svg/vegvisning/790_20.svg) | Swimming pool | `NO:790.20` | — | `leisure=sports_centre`; `leisure=swimming_pool` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | — |
| [`790.30`](../svg/vegvisning/790_30.svg) | Alpine ski centre | `NO:790.30` | — | `piste:type=downhill` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | — |
| [`790.31`](../svg/vegvisning/790_31.svg) | Ski jump | `NO:790.31` | — | `piste:type=ski_jump` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | — |
| [`790.32`](../svg/vegvisning/790_32.svg) | Ski stadium | `NO:790.32` | — | `leisure=sports_centre`; `sport=skiing` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | — |
| [`790.40`](../svg/vegvisning/790_40.svg) | Golf course | `NO:790.40` | — | `leisure=golf_course` | `destination_symbol` | yes | yes | `generic_poi_icon` | — | — |

## Sources

- osm_wiki_norway: https://wiki.openstreetmap.org/wiki/No:Road_signs_in_Norway
- osm_wiki_hazard: https://wiki.openstreetmap.org/wiki/Key:hazard
- osm_wiki_traffic_sign: https://wiki.openstreetmap.org/wiki/Key:traffic_sign
- osm_wiki_vienna_convention: https://wiki.openstreetmap.org/wiki/Vienna_Convention_on_Road_Signs_and_Signals
- wikipedia_eu_comparison: https://en.wikipedia.org/wiki/Comparison_of_European_road_signs
- wikipedia_norway_signs: https://en.wikipedia.org/wiki/Road_signs_in_Norway
- taginfo: https://taginfo.openstreetmap.org/

This mapping file is project documentation. OSM data is ODbL; sign graphics remain under NLOD 2.0 as in the catalogue. Norwegian SVGs are national designs — usable as generic European-style icons where marked, but not as official local traffic signs in other countries.
