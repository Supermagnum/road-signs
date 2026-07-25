"""English names and plain-language meanings for in-scope signs."""

from __future__ import annotations

# code -> (short English name, plain-English meaning)
SIGN_EN: dict[str, tuple[str, str]] = {
    '100.1': (
        'Dangerous bend to the right',
        'Warns of a sharp or otherwise dangerous bend ahead to the right. Reduce speed and prepare to steer right.',
    ),
    '100.2': (
        'Dangerous bend to the left',
        'Warns of a sharp or otherwise dangerous bend ahead to the left. Reduce speed and prepare to steer left.',
    ),
    '102.1': (
        'Series of dangerous bends, first to the right',
        'Warns of a series of dangerous bends; the first bend is to the right.',
    ),
    '102.2': (
        'Series of dangerous bends, first to the left',
        'Warns of a series of dangerous bends; the first bend is to the left.',
    ),
    '104.1': (
        'Steep hill upwards',
        'Warns of a steep uphill gradient ahead. Be prepared for reduced speed, especially for heavy vehicles.',
    ),
    '104.2': (
        'Steep hill downwards',
        'Warns of a steep downhill gradient ahead. Control speed; use a lower gear if needed.',
    ),
    '106.1': (
        'Road narrows on both sides',
        'Warns that the carriageway narrows on both sides ahead.',
    ),
    '106.2': (
        'Road narrows on the right',
        'Warns that the carriageway narrows on the right-hand side ahead.',
    ),
    '106.3': (
        'Road narrows on the left',
        'Warns that the carriageway narrows on the left-hand side ahead.',
    ),
    '108': (
        'Uneven road',
        'Warns of an uneven road surface ahead (potholes, ridges, or similar).',
    ),
    '109': (
        'Speed hump',
        'Warns of a speed hump (traffic calming bump) ahead.',
    ),
    '110': (
        'Road works',
        'Warns of road works ahead. Expect workers, equipment, temporary layouts, and lower speeds.',
    ),
    '112': (
        'Loose chippings',
        'Warns of loose chippings / stone spray from the road surface ahead.',
    ),
    '114.1': (
        'Falling rocks, right side',
        'Warns of falling rocks or landslide risk from the right-hand side.',
    ),
    '114.2': (
        'Falling rocks, left side',
        'Warns of falling rocks or landslide risk from the left-hand side.',
    ),
    '116': (
        'Slippery road',
        'Warns that the road may be slippery (ice, water, oil, polished surface, etc.).',
    ),
    '117': (
        'Soft verges',
        'Warns of a soft, weak, or otherwise dangerous road shoulder / verge.',
    ),
    '118': (
        'Opening or swing bridge',
        'Warns of an opening, swing, or otherwise movable bridge ahead.',
    ),
    '120': (
        'Quayside or ferry terminal',
        'Warns of a quay, shore, or ferry berth ahead — risk of driving into water.',
    ),
    '122': (
        'Tunnel',
        'Warns of a tunnel ahead. Adapt lighting and speed; watch for restrictions.',
    ),
    '124': (
        'Dangerous junction',
        'Warns of a dangerous road junction ahead.',
    ),
    '126': (
        'Roundabout',
        'Warns of a roundabout ahead.',
    ),
    '132': (
        'Traffic signals',
        'Warns of traffic light signals ahead.',
    ),
    '134': (
        'Level crossing with barrier',
        'Warns of a railway level crossing with barriers/gates ahead.',
    ),
    '135': (
        'Level crossing without barrier',
        'Warns of a railway level crossing without barriers/gates ahead.',
    ),
    '136.1h': (
        'Distance to level crossing',
        'Distance marker approaching a level crossing (right-side / countdown panel variant).',
    ),
    '136.1v': (
        'Distance to level crossing',
        'Distance marker approaching a level crossing (left-side / countdown panel variant).',
    ),
    '136.2h': (
        'Distance to level crossing',
        'Intermediate distance marker approaching a level crossing (right-side variant).',
    ),
    '136.2v': (
        'Distance to level crossing',
        'Intermediate distance marker approaching a level crossing (left-side variant).',
    ),
    '136.3h': (
        'Distance to level crossing',
        'Closest distance marker approaching a level crossing (right-side variant).',
    ),
    '136.3v': (
        'Distance to level crossing',
        'Closest distance marker approaching a level crossing (left-side variant).',
    ),
    '138.1': (
        'Single-track railway',
        'Warns of a single-track railway crossing / railway track ahead.',
    ),
    '138.2': (
        'Multi-track railway',
        'Warns of a multi-track railway crossing / railway tracks ahead.',
    ),
    '139': (
        'Tramway',
        'Warns of a tramway / tram tracks ahead.',
    ),
    '140': (
        'Distance to pedestrian crossing',
        'Warns of the distance remaining to a pedestrian crossing ahead.',
    ),
    '142': (
        'Children',
        'Warns that children may be on or near the road (e.g. near schools or playgrounds).',
    ),
    '144': (
        'Cyclists',
        'Warns of cyclists on or crossing the road ahead.',
    ),
    '146.1': (
        'Elk / moose',
        'Warns of elk/moose that may cross or be on the road.',
    ),
    '146.2': (
        'Reindeer',
        'Warns of reindeer that may cross or be on the road.',
    ),
    '146.3': (
        'Deer',
        'Warns of deer that may cross or be on the road.',
    ),
    '146.4': (
        'Cattle',
        'Warns of cattle that may be on or crossing the road.',
    ),
    '146.5': (
        'Sheep',
        'Warns of sheep that may be on or crossing the road.',
    ),
    '148': (
        'Two-way traffic',
        'Warns that two-way traffic begins, or oncoming traffic must be expected.',
    ),
    '149': (
        'Queue / congestion',
        'Warns of queues / congestion ahead.',
    ),
    '150': (
        'Low-flying aircraft',
        'Warns of low-flying aircraft or an area near an aerodrome.',
    ),
    '151': (
        'Military activity',
        'Warns of military activity that may affect the road.',
    ),
    '152': (
        'Side winds',
        'Warns of strong side winds that may affect vehicle stability.',
    ),
    '153': (
        'Accident',
        'Warns of a traffic accident / crash scene ahead.',
    ),
    '154': (
        'Skiers crossing',
        'Warns of skiers crossing or using the road area.',
    ),
    '155': (
        'Horse riders',
        'Warns of horse riders on or near the road.',
    ),
    '156': (
        'Other danger',
        'General warning of another hazard not covered by a more specific warning sign. Often combined with a supplementary plate.',
    ),
    '362.20': (
        'Speed limit 20 km/h',
        'Mandatory maximum speed limit of 20 km/h begins.',
    ),
    '362.30': (
        'Speed limit 30 km/h',
        'Mandatory maximum speed limit of 30 km/h begins.',
    ),
    '362.40': (
        'Speed limit 40 km/h',
        'Mandatory maximum speed limit of 40 km/h begins.',
    ),
    '362.50': (
        'Speed limit 50 km/h',
        'Mandatory maximum speed limit of 50 km/h begins.',
    ),
    '362.60': (
        'Speed limit 60 km/h',
        'Mandatory maximum speed limit of 60 km/h begins.',
    ),
    '362.70': (
        'Speed limit 70 km/h',
        'Mandatory maximum speed limit of 70 km/h begins.',
    ),
    '362.80': (
        'Speed limit 80 km/h',
        'Mandatory maximum speed limit of 80 km/h begins.',
    ),
    '362.90': (
        'Speed limit 90 km/h',
        'Mandatory maximum speed limit of 90 km/h begins.',
    ),
    '362.100': (
        'Speed limit 100 km/h',
        'Mandatory maximum speed limit of 100 km/h begins.',
    ),
    '362.110': (
        'Speed limit 110 km/h',
        'Mandatory maximum speed limit of 110 km/h begins.',
    ),
    '364.20': (
        'End of special speed limit 20 km/h',
        'Ends the special 20 km/h speed limit; the general limit for the road type applies again.',
    ),
    '364.30': (
        'End of special speed limit 30 km/h',
        'Ends the special 30 km/h speed limit; the general limit for the road type applies again.',
    ),
    '364.40': (
        'End of special speed limit 40 km/h',
        'Ends the special 40 km/h speed limit; the general limit for the road type applies again.',
    ),
    '364.50': (
        'End of special speed limit 50 km/h',
        'Ends the special 50 km/h speed limit; the general limit for the road type applies again.',
    ),
    '364.60': (
        'End of special speed limit 60 km/h',
        'Ends the special 60 km/h speed limit; the general limit for the road type applies again.',
    ),
    '364.70': (
        'End of special speed limit 70 km/h',
        'Ends the special 70 km/h speed limit; the general limit for the road type applies again.',
    ),
    '366': (
        'Speed limit zone',
        'Marks the start of a speed-limit zone. The zone speed applies until the matching end-of-zone sign.',
    ),
    '367': (
        'Speed limit zone for small electric vehicles',
        'Marks the start of a speed-limit zone for small electric vehicles (e.g. e-scooters).',
    ),
    '368': (
        'End of speed limit zone',
        'Marks the end of a speed-limit zone.',
    ),
    '369': (
        'End of speed limit zone for small electric vehicles',
        'Marks the end of a speed-limit zone for small electric vehicles.',
    ),
    '560.1': (
        'General speed limits',
        'Information about the general speed limits that apply (built-up area vs. outside).',
    ),
    '560.3': (
        'Warning of speed measurement',
        'Warns that speed may be measured ahead (speed camera / enforcement warning).',
    ),
    '640.10': (
        'Point of interest / sightseeing',
        'Tourist symbol for a noteworthy sight. A custom symbol may replace this for sights of particular importance.',
    ),
    '640.12': (
        'Museum / gallery',
        'Tourist symbol for a museum or gallery.',
    ),
    '640.20': (
        'Viewpoint',
        'Tourist symbol for a scenic viewpoint.',
    ),
    '640.30': (
        'Nature conservation area',
        'Tourist symbol for a nature conservation / protected nature area.',
    ),
    '640.101': (
        'World Heritage',
        'Tourist symbol for a UNESCO World Heritage site.',
    ),
    '640.102': (
        'National fortifications',
        'Tourist symbol for national fortifications.',
    ),
    '650.10': (
        'Bathing area',
        'Tourist/activity symbol for a bathing area.',
    ),
    '650.11': (
        'Fishing spot',
        'Tourist/activity symbol for a fishing spot.',
    ),
    '650.20': (
        'Hiking trail',
        'Tourist/activity symbol for a hiking trail.',
    ),
    '650.21': (
        'Ski trail',
        'Tourist/activity symbol for a ski trail / cross-country track.',
    ),
    '650.22': (
        'Cycle trail',
        'Tourist/activity symbol for a cycle trail.',
    ),
    '650.40': (
        'Farm food / rural tourism',
        'Tourist symbol for farm food / rural tourism (gardsmat/bygdeturisme).',
    ),
    '650.41': (
        'Olavsrosa',
        'Tourist symbol for sites marked with the Olavsrosa quality label.',
    ),
    '723.31': (
        'National tourist route',
        'Route marker for a national tourist road; may also appear on service signs.',
    ),
    '723.41': (
        'Diversion for large vehicles',
        'Route marker for a diversion route for large vehicles.',
    ),
    '723.51': (
        'Route for dangerous goods',
        'Route marker for transport of dangerous goods.',
    ),
    '723.61': (
        'Other diversion route (dash)',
        'Alternative diversion-route symbol (dash).',
    ),
    '723.62': (
        'Other diversion route (filled square)',
        'Alternative diversion-route symbol (filled square).',
    ),
    '723.63': (
        'Other diversion route (triangle)',
        'Alternative diversion-route symbol (triangle).',
    ),
    '723.64': (
        'Other diversion route (hollow square)',
        'Alternative diversion-route symbol (hollow square).',
    ),
    '723.65': (
        'Other diversion route (circle)',
        'Alternative diversion-route symbol (circle).',
    ),
    '723.66': (
        'Other diversion route (arrow)',
        'Alternative diversion-route symbol (arrow).',
    ),
    '723.71': (
        'Junction number — motorway',
        'Junction-number symbol used on motorways with grade-separated junctions.',
    ),
    '723.72': (
        'Junction number — other multilane',
        'Junction-number symbol for other multilane roads with grade-separated junctions.',
    ),
    '723.73': (
        'Junction number — two-lane',
        'Junction-number symbol for two-lane roads with grade-separated junctions.',
    ),
    '755': (
        'Cycle route sign',
        'Direction signing for numbered / marked cycle routes.',
    ),
    '761': (
        'Motorway',
        'Direction symbol indicating a motorway.',
    ),
    '763': (
        'Motor traffic road',
        'Direction symbol indicating a motor traffic road (motortrafikkveg).',
    ),
    '765': (
        'Toll road / road user charging',
        'Direction symbol for a toll road or road-user charging.',
    ),
    '767': (
        'Parking',
        'Direction symbol for parking.',
    ),
    '769': (
        'Parking garage',
        'Direction symbol for a parking garage / multi-storey car park.',
    ),
    '771': (
        'Airport',
        'Direction symbol for an airport.',
    ),
    '772': (
        'Heliport',
        'Direction symbol for a heliport / helicopter landing site.',
    ),
    '773': (
        'Bus station / terminal',
        'Direction symbol for a bus station or bus terminal.',
    ),
    '774': (
        'Railway station / train terminal',
        'Direction symbol for a railway station or train terminal.',
    ),
    '775': (
        'Car ferry',
        'Direction symbol for a car ferry.',
    ),
    '776': (
        'Cargo port',
        'Direction symbol for a cargo / freight port.',
    ),
    '780': (
        'Snow chains',
        'Direction symbol related to snow chains (kjetting).',
    ),
    '790.10': (
        'Church',
        'Direction symbol for a church.',
    ),
    '790.15': (
        'Business / industrial area',
        'Direction symbol for a business or industrial area.',
    ),
    '790.16': (
        'Shopping centre',
        'Direction symbol for a shopping centre.',
    ),
    '790.20': (
        'Swimming pool',
        'Direction symbol for a swimming hall / indoor pool.',
    ),
    '790.30': (
        'Alpine ski centre',
        'Direction symbol for an alpine ski centre.',
    ),
    '790.31': (
        'Ski jump',
        'Direction symbol for a ski jump.',
    ),
    '790.32': (
        'Ski stadium',
        'Direction symbol for a ski stadium.',
    ),
    '790.40': (
        'Golf course',
        'Direction symbol for a golf course.',
    ),
    '812': (
        'Recommended speed',
        'Indicates a recommended (advisory) speed — not the same as a mandatory speed limit.',
    ),
    '856': (
        'General speed limit (miniature)',
        'Miniature version of the general speed-limit information sign.',
    ),
}


def english_for(code: str, fallback_nb: str = "") -> tuple[str | None, str | None]:
    """Return (name_en, meaning_en) for a sign code."""
    hit = SIGN_EN.get(code)
    if hit:
        return hit[0], hit[1]
    return None, None

