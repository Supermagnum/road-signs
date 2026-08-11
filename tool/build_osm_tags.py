#!/usr/bin/env python3
"""Build database/osm_tags.json — catalogue codes mapped to live OSM tags.

Sources (checked against what exists today, not invented schemes):
  - https://wiki.openstreetmap.org/wiki/No:Road_signs_in_Norway
  - https://wiki.openstreetmap.org/wiki/Key:hazard (approved + documented ad-hoc)
  - https://wiki.openstreetmap.org/wiki/Key:traffic_sign (NO: country prefix)
  - https://wiki.openstreetmap.org/wiki/Vienna_Convention_on_Road_Signs_and_Signals
  - taginfo.openstreetmap.org usage counts for traffic_sign=NO:* and hazard=*

Also records cross-country reuse: companion tags (hazard=*, maxspeed=*, POI keys)
are global; national traffic_sign IDs differ; many SVGs are Vienna-Convention-family
pictograms usable as generic European-style navi icons outside Norway (with design caveats).

Coverage rule: every catalogue code is listed. Gaps are explicit.
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SIGNS_EN = ROOT / "database" / "signs_en.json"
OUT = ROOT / "database" / "osm_tags.json"
OUT_MD = ROOT / "database" / "osm_tags.md"
TAGINFO_UA = "road-signs-catalogue/1.0 (https://github.com/Supermagnum/road-signs)"

WIKI_NO = "https://wiki.openstreetmap.org/wiki/No:Road_signs_in_Norway"
WIKI_HAZARD = "https://wiki.openstreetmap.org/wiki/Key:hazard"
WIKI_TRAFFIC_SIGN = "https://wiki.openstreetmap.org/wiki/Key:traffic_sign"
WIKI_VIENNA = "https://wiki.openstreetmap.org/wiki/Vienna_Convention_on_Road_Signs_and_Signals"
WIKI_EU_COMPARE = "https://en.wikipedia.org/wiki/Comparison_of_European_road_signs"
WIKI_NO_SIGNS_EN = "https://en.wikipedia.org/wiki/Road_signs_in_Norway"
TAGINFO_TS = "https://taginfo.openstreetmap.org/tags/traffic_sign="
TAGINFO_DATA_UNTIL = None

# ISO countries that are Vienna Convention parties (or largely aligned) where
# triangular red-border warning pictograms and circular speed plates are familiar.
# Source: Wikipedia Comparison of European road signs / UNECE treaty status.
VIENNA_FAMILY_COUNTRIES = [
    "AL", "AD", "AM", "AT", "BY", "BE", "BA", "BG", "HR", "CY", "CZ", "DK", "EE",
    "FI", "FR", "GE", "DE", "GR", "HU", "IT", "LV", "LI", "LT", "LU", "MD", "ME",
    "NL", "MK", "NO", "PL", "PT", "RO", "RU", "SM", "RS", "SK", "SI", "ES", "SE",
    "CH", "TR", "UA", "GB",
]
# Aligned but not signed (Wikipedia): IS, IE, MT — still broadly European-style.
VIENNA_ALIGNED_EXTRA = ["IS", "IE", "MT"]


def equiv(country: str, sign_id: str, relation: str = "same_meaning", **meta: Any) -> dict[str, Any]:
    """Example national traffic_sign ID with the same/similar meaning (not for tagging NO roads)."""
    row: dict[str, Any] = {
        "country": country,
        "traffic_sign": sign_id,
        "relation": relation,
    }
    row.update(meta)
    return row

# Hazard values documented on Key:hazard (approved list + further ad-hoc table).
HAZARD_APPROVED = {
    "animal_crossing",
    "bump",
    "children",
    "curve",
    "curves",
    "cyclists",
    "dangerous_junction",
    "dip",
    "falling_rocks",
    "frost_heave",
    "horse_riders",
    "ice",
    "landslide",
    "loose_gravel",
    "low_flying_aircraft",
    "pedestrians",
    "queues_likely",
    "school_zone",
    "side_winds",
    "slippery",
    "turn",
    "turns",
}
HAZARD_ADHOC = {
    "collapse",
    "contraflow",
    "damaged_road",
    "emergency_vehicles",
    "falling_trees",
    "fog",
    "frail_pedestrians",
    "ground_clearance",
    "illegal_crossing",
    "pedestrian_crossing",
    "road_narrows",
    "roadworks",
    "roundabout",
    "silver_zone",
    "traffic_signals",
}


def tag(key: str, value: str | None = None, **meta: Any) -> dict[str, Any]:
    row: dict[str, Any] = {"key": key}
    if value is not None:
        row["value"] = value
    row.update(meta)
    return row


def hazard(value: str, **meta: Any) -> dict[str, Any]:
    if value in HAZARD_APPROVED:
        status = "approved"
    elif value in HAZARD_ADHOC:
        status = "ad-hoc_documented"
    else:
        status = "observed_or_proposed"
    return tag("hazard", value, role="hazard", osm_status=status, **meta)


# Curated per-code mapping. Keys are NVDB skiltnummer strings from signs_en.json.
# implied_tags: tags that OSM routinely pairs with the sign (way/node semantics).
# match_status values:
#   wiki_documented — listed on No:Road_signs_in_Norway
#   hazard_convention — mapped via Key:hazard (approved/ad-hoc) + Vienna-style meaning
#   speed_convention — maxspeed / zone tagging used in Norway OSM
#   destination_symbol — typically destination/POI context, rare as lone traffic_sign
#   traffic_sign_only — NO: code exists as convention; no stable companion tags
#   variable_content — sign carries variable text/distance/number; template only
#   not_for_navigation — fixed SVG not usable as a navi symbol (variable digits etc.)
MAPPINGS: dict[str, dict[str, Any]] = {
    # --- fareskilt ---
    "100.1": {
        "match_status": "wiki_documented",
        "implied_tags": [hazard("curve", source=WIKI_NO)],
        "sources": [WIKI_NO, WIKI_HAZARD],
        "notes": ["Wiki also documents traffic_sign=NO:100.1."],
    },
    "100.2": {
        "match_status": "wiki_documented",
        "implied_tags": [hazard("curve", source=WIKI_NO)],
        "sources": [WIKI_NO, WIKI_HAZARD],
    },
    "102.1": {
        "match_status": "wiki_documented",
        "implied_tags": [hazard("curves", source=WIKI_NO)],
        "sources": [WIKI_NO, WIKI_HAZARD],
    },
    "102.2": {
        "match_status": "wiki_documented",
        "implied_tags": [hazard("curves", source=WIKI_NO)],
        "sources": [WIKI_NO, WIKI_HAZARD],
    },
    "104.1": {
        "match_status": "wiki_documented",
        "implied_tags": [],
        "related_tags": [
            tag(
                "incline",
                "{percent}",
                role="optional_from_underskilt",
                note="Gradient often given on underskilt 813.1; not on 104.1 itself.",
            )
        ],
        "sources": [WIKI_NO],
        "notes": [
            "Norwegian wiki lists traffic_sign only for 104.1 (no hazard=* value).",
            "No approved hazard=steep; do not invent one.",
        ],
    },
    "104.2": {
        "match_status": "wiki_documented",
        "implied_tags": [],
        "related_tags": [
            tag(
                "incline",
                "-{percent}",
                role="optional_from_underskilt",
                note="Gradient often given on underskilt 813.2; not on 104.2 itself.",
            )
        ],
        "sources": [WIKI_NO],
        "notes": ["Norwegian wiki lists traffic_sign only for 104.2."],
    },
    "106.1": {
        "match_status": "wiki_documented",
        "implied_tags": [hazard("road_narrows", source=WIKI_NO)],
        "sources": [WIKI_NO, WIKI_HAZARD],
    },
    "106.2": {
        "match_status": "wiki_documented",
        "implied_tags": [hazard("road_narrows", source=WIKI_NO)],
        "sources": [WIKI_NO, WIKI_HAZARD],
        "notes": ["Side (right) is not encoded in hazard=*; keep NO:106.2 on the sign node."],
    },
    "106.3": {
        "match_status": "wiki_documented",
        "implied_tags": [hazard("road_narrows", source=WIKI_NO)],
        "sources": [WIKI_NO, WIKI_HAZARD],
        "notes": ["Side (left) is not encoded in hazard=*; keep NO:106.3 on the sign node."],
    },
    "108": {
        "match_status": "hazard_convention",
        "implied_tags": [
            hazard(
                "damaged_road",
                source=WIKI_HAZARD,
                note="Closest documented hazard value for uneven carriageway; not on NO wiki yet.",
            )
        ],
        "sources": [WIKI_HAZARD],
        "notes": ["traffic_sign=NO:108 is used in OSM; companion hazard tagging is ad-hoc."],
    },
    "109": {
        "match_status": "wiki_documented",
        "implied_tags": [
            tag("traffic_calming", "hump", role="feature", source=WIKI_NO, osm_status="established"),
            hazard("bump", source=WIKI_HAZARD),
        ],
        "sources": [WIKI_NO, WIKI_HAZARD],
    },
    "110": {
        "match_status": "wiki_documented",
        "implied_tags": [hazard("roadworks", source=WIKI_NO)],
        "sources": [WIKI_NO, WIKI_HAZARD],
        "notes": [
            "OSM guidance prefers permanent/recurring hazards; temporary works are often omitted.",
        ],
    },
    "112": {
        "match_status": "hazard_convention",
        "implied_tags": [hazard("loose_gravel", source=WIKI_HAZARD)],
        "sources": [WIKI_HAZARD],
    },
    "114.1": {
        "match_status": "hazard_convention",
        "implied_tags": [hazard("falling_rocks", source=WIKI_HAZARD)],
        "sources": [WIKI_HAZARD],
        "notes": ["Right-side pictogram: encode side via NO:114.1, not a separate hazard value."],
    },
    "114.2": {
        "match_status": "hazard_convention",
        "implied_tags": [hazard("falling_rocks", source=WIKI_HAZARD)],
        "sources": [WIKI_HAZARD],
        "notes": ["Left-side pictogram: encode side via NO:114.2."],
    },
    "116": {
        "match_status": "hazard_convention",
        "implied_tags": [hazard("slippery", source=WIKI_HAZARD)],
        "sources": [WIKI_HAZARD],
    },
    "117": {
        "match_status": "traffic_sign_only",
        "implied_tags": [],
        "sources": [WIKI_TRAFFIC_SIGN],
        "notes": [
            "No approved/documented hazard=* for soft verges in Key:hazard tables.",
            "Use traffic_sign=NO:117 on the sign; do not invent hazard=soft_verge.",
        ],
    },
    "118": {
        "match_status": "traffic_sign_only",
        "implied_tags": [],
        "related_tags": [
            tag("bridge", "movable", role="feature_context", note="Tag the bridge feature, not only the warning."),
            tag("bridge:movable", "swing", role="example_value"),
        ],
        "sources": [WIKI_TRAFFIC_SIGN],
        "notes": ["No dedicated hazard=* for opening/swing bridge on Key:hazard."],
    },
    "120": {
        "match_status": "traffic_sign_only",
        "implied_tags": [],
        "related_tags": [
            tag("man_made", "pier", role="feature_context"),
            tag("amenity", "ferry_terminal", role="feature_context"),
        ],
        "sources": [WIKI_TRAFFIC_SIGN],
        "notes": ["No dedicated hazard=* for quayside / ferry berth."],
    },
    "122": {
        "match_status": "traffic_sign_only",
        "implied_tags": [],
        "related_tags": [tag("tunnel", "yes", role="feature_context")],
        "sources": [WIKI_TRAFFIC_SIGN],
        "notes": ["Warning of tunnel ahead; the tunnel way uses tunnel=yes / highway through tunnel."],
    },
    "124": {
        "match_status": "hazard_convention",
        "implied_tags": [hazard("dangerous_junction", source=WIKI_HAZARD)],
        "sources": [WIKI_HAZARD],
    },
    "126": {
        "match_status": "hazard_convention",
        "implied_tags": [hazard("roundabout", source=WIKI_HAZARD)],
        "related_tags": [
            tag(
                "junction",
                "roundabout",
                role="feature",
                note="Use on the roundabout itself; 126 is only the advance warning.",
            )
        ],
        "sources": [WIKI_HAZARD],
    },
    "132": {
        "match_status": "hazard_convention",
        "implied_tags": [hazard("traffic_signals", source=WIKI_HAZARD)],
        "related_tags": [tag("highway", "traffic_signals", role="feature")],
        "sources": [WIKI_HAZARD],
    },
    "134": {
        "match_status": "hazard_convention",
        "implied_tags": [],
        "related_tags": [
            tag("railway", "level_crossing", role="feature"),
            tag("crossing:barrier", "yes", role="feature"),
        ],
        "sources": [WIKI_TRAFFIC_SIGN],
        "notes": [
            "Map the crossing with railway=level_crossing; 134 is the advance warning with barriers.",
        ],
    },
    "135": {
        "match_status": "hazard_convention",
        "implied_tags": [],
        "related_tags": [
            tag("railway", "level_crossing", role="feature"),
            tag("crossing:barrier", "no", role="feature"),
        ],
        "sources": [WIKI_TRAFFIC_SIGN],
        "notes": ["Advance warning of level crossing without barriers."],
    },
    "136.1h": {
        "match_status": "variable_content",
        "navi_usable": False,
        "implied_tags": [],
        "related_tags": [tag("railway", "level_crossing", role="feature_ahead")],
        "variable_fields": [
            {
                "name": "distance_or_stripe_count",
                "description": (
                    "Countdown panel approaching a level crossing (right-side / h variant). "
                    "Stripe count decreases 136.1 → 136.3; exact metre spacing is placement-dependent "
                    "and not fixed in this catalogue."
                ),
            }
        ],
        "sources": [WIKI_TRAFFIC_SIGN],
        "notes": [
            "Not a fixed navi hazard icon by itself; marks approach to a crossing.",
            "Distances: not standardized in this DB — verify Skiltforskriften / local practice.",
        ],
    },
    "136.1v": {
        "match_status": "variable_content",
        "navi_usable": False,
        "implied_tags": [],
        "related_tags": [tag("railway", "level_crossing", role="feature_ahead")],
        "variable_fields": [
            {
                "name": "distance_or_stripe_count",
                "description": "Left-side (v) countdown panel; see 136.1h.",
            }
        ],
        "sources": [WIKI_TRAFFIC_SIGN],
    },
    "136.2h": {
        "match_status": "variable_content",
        "navi_usable": False,
        "implied_tags": [],
        "related_tags": [tag("railway", "level_crossing", role="feature_ahead")],
        "variable_fields": [
            {"name": "distance_or_stripe_count", "description": "Intermediate right-side countdown panel."}
        ],
        "sources": [WIKI_TRAFFIC_SIGN],
    },
    "136.2v": {
        "match_status": "variable_content",
        "navi_usable": False,
        "implied_tags": [],
        "related_tags": [tag("railway", "level_crossing", role="feature_ahead")],
        "variable_fields": [
            {"name": "distance_or_stripe_count", "description": "Intermediate left-side countdown panel."}
        ],
        "sources": [WIKI_TRAFFIC_SIGN],
    },
    "136.3h": {
        "match_status": "variable_content",
        "navi_usable": False,
        "implied_tags": [],
        "related_tags": [tag("railway", "level_crossing", role="feature_ahead")],
        "variable_fields": [
            {"name": "distance_or_stripe_count", "description": "Closest right-side countdown panel."}
        ],
        "sources": [WIKI_TRAFFIC_SIGN],
    },
    "136.3v": {
        "match_status": "variable_content",
        "navi_usable": False,
        "implied_tags": [],
        "related_tags": [tag("railway", "level_crossing", role="feature_ahead")],
        "variable_fields": [
            {"name": "distance_or_stripe_count", "description": "Closest left-side countdown panel."}
        ],
        "sources": [WIKI_TRAFFIC_SIGN],
    },
    "138.1": {
        "match_status": "traffic_sign_only",
        "implied_tags": [],
        "related_tags": [
            tag("railway", "level_crossing", role="feature"),
            tag("railway:track_ref", "1", role="hint", note="Single-track warning; track count belongs on the railway."),
        ],
        "sources": [WIKI_TRAFFIC_SIGN],
    },
    "138.2": {
        "match_status": "traffic_sign_only",
        "implied_tags": [],
        "related_tags": [tag("railway", "level_crossing", role="feature")],
        "sources": [WIKI_TRAFFIC_SIGN],
        "notes": ["Multi-track railway warning; used as traffic_sign=NO:138.2 in OSM."],
    },
    "139": {
        "match_status": "traffic_sign_only",
        "implied_tags": [],
        "related_tags": [
            tag("railway", "tram", role="feature_context"),
            tag("railway", "tram_crossing", role="feature_context"),
        ],
        "sources": [WIKI_TRAFFIC_SIGN],
    },
    "140": {
        "match_status": "variable_content",
        "implied_tags": [],
        "related_tags": [
            tag("highway", "crossing", role="feature_ahead"),
            tag("crossing", "uncontrolled", role="example"),
        ],
        "traffic_sign_template": "NO:140[{distance}]",
        "variable_fields": [
            {
                "name": "distance",
                "example": "150 m",
                "osm_example": "NO:140[150 m]",
                "description": "Distance remaining to pedestrian crossing, shown under the symbol.",
            }
        ],
        "sources": [WIKI_TRAFFIC_SIGN],
        "notes": [
            "taginfo observes values such as NO:140[150 m].",
            "Useful for navi as crossing-ahead with distance, not as a fixed pictogram alone.",
        ],
    },
    "142": {
        "match_status": "hazard_convention",
        "implied_tags": [hazard("children", source=WIKI_HAZARD)],
        "sources": [WIKI_HAZARD],
    },
    "144": {
        "match_status": "hazard_convention",
        "implied_tags": [hazard("cyclists", source=WIKI_HAZARD)],
        "sources": [WIKI_HAZARD],
    },
    "146.1": {
        "match_status": "hazard_convention",
        "implied_tags": [
            hazard("animal_crossing", source=WIKI_HAZARD),
            tag(
                "hazard:animal",
                "moose",
                role="species_detail",
                osm_status="approved",
                note="Norwegian elg / Eurasian moose; taginfo uses moose far more than elk.",
                source="https://wiki.openstreetmap.org/wiki/Key:hazard:animal",
            ),
        ],
        "sources": [WIKI_HAZARD, "https://wiki.openstreetmap.org/wiki/Key:hazard:animal"],
    },
    "146.2": {
        "match_status": "hazard_convention",
        "implied_tags": [
            hazard("animal_crossing", source=WIKI_HAZARD),
            tag("hazard:animal", "reindeer", role="species_detail", osm_status="approved"),
        ],
        "sources": [WIKI_HAZARD, "https://wiki.openstreetmap.org/wiki/Key:hazard:animal"],
    },
    "146.3": {
        "match_status": "hazard_convention",
        "implied_tags": [
            hazard("animal_crossing", source=WIKI_HAZARD),
            tag("hazard:animal", "deer", role="species_detail", osm_status="approved"),
        ],
        "sources": [WIKI_HAZARD, "https://wiki.openstreetmap.org/wiki/Key:hazard:animal"],
        "notes": ["Standalone hazard=deer also exists in taginfo; prefer animal_crossing + hazard:animal."],
    },
    "146.4": {
        "match_status": "hazard_convention",
        "implied_tags": [
            hazard("animal_crossing", source=WIKI_HAZARD),
            tag("hazard:animal", "cattle", role="species_detail", osm_status="approved"),
        ],
        "sources": [WIKI_HAZARD, "https://wiki.openstreetmap.org/wiki/Key:hazard:animal"],
    },
    "146.5": {
        "match_status": "hazard_convention",
        "implied_tags": [
            hazard("animal_crossing", source=WIKI_HAZARD),
            tag("hazard:animal", "sheep", role="species_detail", osm_status="approved"),
        ],
        "sources": [WIKI_HAZARD, "https://wiki.openstreetmap.org/wiki/Key:hazard:animal"],
    },
    "148": {
        "match_status": "hazard_convention",
        "implied_tags": [
            hazard(
                "contraflow",
                source=WIKI_HAZARD,
                note="Documented ad-hoc value; low global usage. Alternative observed: hazard=two_way_traffic.",
            )
        ],
        "sources": [WIKI_HAZARD],
    },
    "149": {
        "match_status": "hazard_convention",
        "implied_tags": [hazard("queues_likely", source=WIKI_HAZARD)],
        "sources": [WIKI_HAZARD],
    },
    "150": {
        "match_status": "hazard_convention",
        "implied_tags": [hazard("low_flying_aircraft", source=WIKI_HAZARD)],
        "sources": [WIKI_HAZARD],
    },
    "151": {
        "match_status": "traffic_sign_only",
        "implied_tags": [],
        "sources": [WIKI_TRAFFIC_SIGN],
        "notes": ["No established hazard=* for military activity on Key:hazard."],
    },
    "152": {
        "match_status": "hazard_convention",
        "implied_tags": [hazard("side_winds", source=WIKI_HAZARD)],
        "sources": [WIKI_HAZARD],
    },
    "153": {
        "match_status": "traffic_sign_only",
        "navi_usable": False,
        "implied_tags": [],
        "sources": [WIKI_TRAFFIC_SIGN, WIKI_HAZARD],
        "notes": [
            "Accident warnings are typically temporary; OSM hazard guidance discourages temporary tagging.",
            "Do not invent a permanent hazard=accident mapping for navi basemaps.",
        ],
    },
    "154": {
        "match_status": "traffic_sign_only",
        "implied_tags": [],
        "sources": [WIKI_TRAFFIC_SIGN],
        "notes": ["No Key:hazard value for skiers crossing; use traffic_sign=NO:154."],
    },
    "155": {
        "match_status": "hazard_convention",
        "implied_tags": [hazard("horse_riders", source=WIKI_HAZARD)],
        "sources": [WIKI_HAZARD],
    },
    "156": {
        "match_status": "traffic_sign_only",
        "implied_tags": [
            tag(
                "traffic_sign",
                "hazard",
                role="generic_alternative",
                note="Generic hazard sign class; prefer NO:156 when the Norwegian code is known.",
            )
        ],
        "sources": [WIKI_HAZARD, WIKI_TRAFFIC_SIGN],
        "notes": [
            "General danger; meaning depends on underskilt. No single hazard=* value.",
        ],
    },
    # --- speed_limit ---
    # Templates filled in build for 362/364 variants.
}


def _speed_start(kmh: int) -> dict[str, Any]:
    return {
        "match_status": "wiki_documented",
        "implied_tags": [
            tag("maxspeed", str(kmh), role="regulation", source=WIKI_NO, osm_status="established"),
            tag("source:maxspeed", "sign", role="provenance", osm_status="established"),
        ],
        "traffic_sign_template": f"NO:362.{kmh}",
        "traffic_sign_variants": (
            [f"NO:362:{kmh}"] if kmh >= 100 else [f"NO:362[{kmh}]", f"NO:362:{kmh}"]
        ),
        "sources": [WIKI_NO, WIKI_TRAFFIC_SIGN],
        "notes": [
            "Norwegian wiki example: traffic_sign=NO:362.60 + maxspeed=60.",
            "Colon form NO:362:100 / NO:362:110 appears in taginfo for 100/110.",
        ],
    }


def _speed_end(kmh: int) -> dict[str, Any]:
    return {
        "match_status": "wiki_documented",
        "implied_tags": [],
        "related_tags": [
            tag(
                "maxspeed",
                "{general_limit}",
                role="after_sign",
                note=(
                    "End of special limit; resume general limit for road type "
                    "(wiki example shows maxspeed=80 after NO:364.60)."
                ),
                source=WIKI_NO,
            )
        ],
        "traffic_sign_template": f"NO:364.{kmh}",
        "sources": [WIKI_NO],
        "notes": [
            "364 does not encode the new limit on the plate; mappers set maxspeed to the applicable general limit.",
        ],
    }


for _v in (20, 30, 40, 50, 60, 70, 80, 90, 100, 110):
    MAPPINGS[f"362.{_v}"] = _speed_start(_v)
    if _v <= 70:  # catalogue has end signs through 70 plus unresolved 20
        MAPPINGS[f"364.{_v}"] = _speed_end(_v)

# Catalogue only has 364 up to 70 (and 364.20 unresolved); ensure 364.20 exists
MAPPINGS["364.20"] = _speed_end(20)

MAPPINGS.update(
    {
        "366": {
            "match_status": "wiki_documented",
            "implied_tags": [
                tag("maxspeed", "{zone_kmh}", role="regulation", source=WIKI_NO),
                tag(
                    "maxspeed:type",
                    "NO:zone{zone_kmh}",
                    role="zone",
                    note="taginfo has substantial NO:zone30 (and some NO:zone40/50).",
                    osm_status="established",
                ),
                tag(
                    "zone:maxspeed",
                    "NO:{zone_kmh}",
                    role="zone_alternative",
                    note="Also seen as zone:maxspeed=NO:30.",
                ),
            ],
            "traffic_sign_template": "NO:366.{zone_kmh}",
            "traffic_sign_variants": ["NO:366[{zone_kmh}]", "NO:366"],
            "variable_fields": [
                {
                    "name": "zone_kmh",
                    "description": "Zone speed shown on the sign (commonly 30).",
                    "osm_examples": ["NO:366.30", "NO:366[30]", "NO:366"],
                }
            ],
            "sources": [WIKI_NO],
            "notes": ["Wiki example: traffic_sign=NO:366.30 + maxspeed=30."],
        },
        "367": {
            "match_status": "wiki_documented",
            "implied_tags": [
                tag(
                    "maxspeed:small_electric_vehicle",
                    "{kmh}",
                    role="regulation",
                    source=WIKI_NO,
                )
            ],
            "traffic_sign_template": "NO:367[{kmh}]",
            "variable_fields": [
                {"name": "kmh", "example": "6", "description": "Limit for small electric vehicles."}
            ],
            "sources": [WIKI_NO],
        },
        "368": {
            "match_status": "wiki_documented",
            "implied_tags": [],
            "traffic_sign_template": "NO:368.{zone_kmh}",
            "traffic_sign_variants": ["NO:368[{zone_kmh}]", "NO:368"],
            "variable_fields": [
                {"name": "zone_kmh", "description": "Often mirrors the zone start speed on the plate."}
            ],
            "sources": [WIKI_NO],
            "notes": ["End of speed-limit zone; remove zone maxspeed tagging after this point."],
        },
        "369": {
            "match_status": "wiki_documented",
            "implied_tags": [],
            "traffic_sign_template": "NO:369[{kmh}]",
            "sources": [WIKI_NO],
            "notes": ["End of small-electric-vehicle speed zone."],
        },
        "560.1": {
            "match_status": "traffic_sign_only",
            "implied_tags": [],
            "related_tags": [
                tag("maxspeed:type", "NO:urban", role="context"),
                tag("maxspeed:type", "NO:rural", role="context"),
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
            "notes": [
                "Information about general limits (built-up vs elsewhere); does not itself change maxspeed.",
                "No SVG in this catalogue yet.",
            ],
        },
        "560.3": {
            "match_status": "traffic_sign_only",
            "implied_tags": [],
            "related_tags": [
                tag(
                    "highway",
                    "speed_camera",
                    role="feature_ahead",
                    note="Only if a camera/enforcement device exists; 560.3 is a warning plate.",
                ),
                tag("enforcement", "maxspeed", role="possible"),
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
            "notes": ["Speed-measurement / enforcement warning; no established NO wiki row yet."],
        },
        "812": {
            "match_status": "variable_content",
            "implied_tags": [
                tag(
                    "maxspeed:advisory",
                    "{kmh}",
                    role="advisory",
                    osm_status="established",
                    note="Advisory only — not a mandatory maxspeed.",
                )
            ],
            "traffic_sign_template": "NO:812[{kmh}]",
            "variable_fields": [
                {"name": "kmh", "description": "Recommended speed shown on the sign."}
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
            "notes": ["Do not set maxspeed= from 812; use maxspeed:advisory."],
        },
        "856": {
            "match_status": "traffic_sign_only",
            "implied_tags": [],
            "sources": [WIKI_TRAFFIC_SIGN],
            "notes": ["Miniature general speed-limit information; same role family as 560.1."],
        },
        # --- serviceskilt (destination / tourist symbols) ---
        "640.10": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [tag("tourism", "attraction", role="destination_poi")],
            "sources": [WIKI_TRAFFIC_SIGN],
            "notes": ["Brown tourist symbol; rarely tagged alone as traffic_sign in NO taginfo."],
        },
        "640.101": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [
                tag("heritage", "1", role="destination_poi"),
                tag("tourism", "yes", role="destination_poi"),
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "640.102": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [
                tag("historic", "fort", role="destination_poi"),
                tag("tourism", "attraction", role="destination_poi"),
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "640.12": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [tag("tourism", "museum", role="destination_poi")],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "640.20": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [tag("tourism", "viewpoint", role="destination_poi")],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "640.30": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [
                tag("leisure", "nature_reserve", role="destination_poi"),
                tag("boundary", "protected_area", role="destination_poi"),
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "650.10": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [
                tag("leisure", "bathing_place", role="destination_poi"),
                tag("natural", "beach", role="destination_poi"),
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "650.11": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [tag("leisure", "fishing", role="destination_poi")],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "650.20": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [
                tag("route", "hiking", role="destination_poi"),
                tag("highway", "path", role="destination_poi"),
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "650.21": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [
                tag("route", "ski", role="destination_poi"),
                tag("piste:type", "nordic", role="destination_poi"),
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "650.22": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [
                tag("route", "bicycle", role="destination_poi"),
                tag("highway", "cycleway", role="destination_poi"),
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "650.40": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [
                tag("tourism", "farm", role="destination_poi"),
                tag("shop", "farm", role="destination_poi"),
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "650.41": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [
                tag("tourism", "yes", role="destination_poi"),
                tag("brand", "Olavsrosa", role="destination_poi"),
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
            "notes": ["Quality label symbol; brand tagging is conventional, not Norway-wiki-mandated."],
        },
        # --- vegvisning ---
        "723.31": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [
                tag("route", "road", role="network_context"),
                tag("network", "no:national_tourist_route", role="suggested"),
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
            "notes": ["National tourist route marker; some NO:723.* traffic_sign usage exists."],
        },
        "723.41": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [tag("hgv", "destination", role="routing_context")],
            "sources": [WIKI_TRAFFIC_SIGN],
            "notes": ["Diversion for large vehicles — usually on temporary/diversion signing."],
        },
        "723.51": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [tag("hazmat", "destination", role="routing_context")],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "723.61": {
            "match_status": "destination_symbol",
            "navi_usable": False,
            "implied_tags": [],
            "sources": [WIKI_TRAFFIC_SIGN],
            "notes": ["Alternative diversion symbol (dash); often temporary — poor navi basemap fit."],
        },
        "723.62": {
            "match_status": "destination_symbol",
            "navi_usable": False,
            "implied_tags": [],
            "sources": [WIKI_TRAFFIC_SIGN],
            "notes": ["Alternative diversion symbol (filled square)."],
        },
        "723.63": {
            "match_status": "destination_symbol",
            "navi_usable": False,
            "implied_tags": [],
            "sources": [WIKI_TRAFFIC_SIGN],
            "notes": ["Alternative diversion symbol (triangle)."],
        },
        "723.64": {
            "match_status": "destination_symbol",
            "navi_usable": False,
            "implied_tags": [],
            "sources": [WIKI_TRAFFIC_SIGN],
            "notes": ["Alternative diversion symbol (hollow square)."],
        },
        "723.65": {
            "match_status": "destination_symbol",
            "navi_usable": False,
            "implied_tags": [],
            "sources": [WIKI_TRAFFIC_SIGN],
            "notes": ["Alternative diversion symbol (circle)."],
        },
        "723.66": {
            "match_status": "destination_symbol",
            "navi_usable": False,
            "implied_tags": [],
            "sources": [WIKI_TRAFFIC_SIGN],
            "notes": ["Alternative diversion symbol (arrow)."],
        },
        "723.71": {
            "match_status": "not_for_navigation",
            "navi_usable": False,
            "implied_tags": [],
            "related_tags": [tag("noref", "{junction_number}", role="variable")],
            "variable_fields": [
                {
                    "name": "junction_number",
                    "example": "25",
                    "description": "Motorway junction number printed with the symbol.",
                }
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
            "notes": [
                "SVG is a template with variable digits — not usable as a fixed navi icon.",
            ],
        },
        "723.72": {
            "match_status": "not_for_navigation",
            "navi_usable": False,
            "implied_tags": [],
            "variable_fields": [
                {"name": "junction_number", "description": "Junction number on other multilane roads."}
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
            "notes": ["Variable junction number — not a fixed navi symbol."],
        },
        "723.73": {
            "match_status": "not_for_navigation",
            "navi_usable": False,
            "implied_tags": [],
            "variable_fields": [
                {"name": "junction_number", "description": "Junction number on two-lane grade-separated roads."}
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
            "notes": ["Variable junction number — not a fixed navi symbol."],
        },
        "755": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [
                tag("route", "bicycle", role="network"),
                tag("network", "lcn", role="example"),
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
            "notes": ["Cycle route direction signing; traffic_sign=NO:755 appears in taginfo."],
        },
        "761": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [tag("highway", "motorway", role="destination_class")],
            "sources": [WIKI_TRAFFIC_SIGN, WIKI_NO],
            "notes": ["Direction symbol for motorway; related info sign 502 uses highway=motorway on wiki."],
        },
        "763": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [tag("motorroad", "yes", role="destination_class")],
            "sources": [WIKI_NO],
            "notes": ["Motortrafikkveg symbol; wiki maps info sign 503 to motorroad=yes."],
        },
        "765": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [tag("toll", "yes", role="destination_class")],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "767": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [tag("amenity", "parking", role="destination_poi")],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "769": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [
                tag("amenity", "parking", role="destination_poi"),
                tag("parking", "multi-storey", role="destination_poi"),
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "771": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [tag("aeroway", "aerodrome", role="destination_poi")],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "772": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [tag("aeroway", "helipad", role="destination_poi")],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "773": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [tag("amenity", "bus_station", role="destination_poi")],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "774": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [
                tag("railway", "station", role="destination_poi"),
                tag("public_transport", "station", role="destination_poi"),
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "775": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [
                tag("amenity", "ferry_terminal", role="destination_poi"),
                tag("route", "ferry", role="destination_poi"),
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "776": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [
                tag("industrial", "port", role="destination_poi"),
                tag("harbour", "yes", role="destination_poi"),
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "780": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [
                tag(
                    "snow_chains",
                    "required",
                    role="possible",
                    note="Low global usage; confirm local meaning before applying to ways.",
                )
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
            "notes": ["Snow-chains related direction/info symbol; tagging on ways is uncommon."],
        },
        "790.10": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [
                tag("amenity", "place_of_worship", role="destination_poi"),
                tag("religion", "christian", role="destination_poi"),
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "790.15": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [
                tag("landuse", "industrial", role="destination_poi"),
                tag("landuse", "commercial", role="destination_poi"),
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "790.16": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [tag("shop", "mall", role="destination_poi")],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "790.20": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [
                tag("leisure", "sports_centre", role="destination_poi"),
                tag("leisure", "swimming_pool", role="destination_poi"),
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "790.30": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [tag("piste:type", "downhill", role="destination_poi")],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "790.31": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [tag("piste:type", "ski_jump", role="destination_poi")],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "790.32": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [
                tag("leisure", "sports_centre", role="destination_poi"),
                tag("sport", "skiing", role="destination_poi"),
            ],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
        "790.40": {
            "match_status": "destination_symbol",
            "implied_tags": [],
            "related_tags": [tag("leisure", "golf_course", role="destination_poi")],
            "sources": [WIKI_TRAFFIC_SIGN],
        },
    }
)


def http_json(url: str) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": TAGINFO_UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def fetch_traffic_sign_usage() -> tuple[dict[str, int], dict[str, list[tuple[int, str]]], str | None]:
    """Return per-code approximate counts and example values from taginfo."""
    global TAGINFO_DATA_UNTIL
    usage: dict[str, int] = defaultdict(int)
    examples: dict[str, list[tuple[int, str]]] = defaultdict(list)
    data_until = None
    page = 1
    while page <= 20:
        url = (
            "https://taginfo.openstreetmap.org/api/4/key/values"
            f"?key=traffic_sign&filter=all&sortname=count&sortorder=desc&rp=500&page={page}&query="
            + urllib.parse.quote("NO:")
        )
        payload = http_json(url)
        data_until = payload.get("data_until") or data_until
        rows = payload.get("data") or []
        if not rows:
            break
        for row in rows:
            value = row["value"]
            count = int(row["count"])
            for code in extract_no_codes(value):
                usage[code] += count
                if len(examples[code]) < 8:
                    examples[code].append((count, value))
        total = int(payload.get("total") or 0)
        if page * 500 >= total:
            break
        page += 1
    TAGINFO_DATA_UNTIL = data_until
    return dict(usage), dict(examples), data_until


def extract_no_codes(value: str) -> list[str]:
    """Extract Norwegian skiltnummer-like codes from a traffic_sign value."""
    found: list[str] = []
    parts = re.split(r"[;,]", value)
    for part in parts:
        part = part.strip()
        # NO:362:100 (colon used instead of dot for some speeds) — check before dotted form
        m = re.match(r"(?i)(?:no:)?NO:([0-9]+):([0-9]+)\b", part)
        if m:
            found.append(f"{m.group(1)}.{m.group(2)}")
            continue
        # NO:362.60, NO:140[150 m], NO:366[30], NO:136.1h
        m = re.match(
            r"(?i)(?:no:)?NO:([0-9]+(?:\.[0-9A-Za-z]+)*)",
            part,
        )
        if m:
            found.append(m.group(1))
    return found


def default_navi_usable(match_status: str, explicit: bool | None) -> bool:
    if explicit is not None:
        return explicit
    return match_status not in {
        "not_for_navigation",
        "variable_content",
        "destination_symbol",
        "traffic_sign_only",
    }


# Cross-country / international reuse metadata per catalogue code.
# companion_tags (hazard=*, maxspeed=*, amenity=*, …) are global OSM keys.
# traffic_sign=NO:* is Norway-only when mapping Norwegian roads; other countries
# use their own ISO prefix (DE:, SE:, FI:, …) per Key:traffic_sign.
# symbol_scope:
#   vienna_convention_family — same hazard/speed pictogram family across VC Europe
#   nordic_shared — common in NO/SE/FI (and often neighbouring VC states)
#   generic_poi_icon — destination/service icon meaning is widely understood
#   norway_specific — legal/network/brand meaning is Norway-only; do not present as local law elsewhere
# graphic_reuse_outside_NO:
#   yes — SVG usable as generic European-style navi icon (design details still NO)
#   with_caveat — usable as icon but national drawings differ (arrows, animals, colours)
#   no — Norway-specific meaning or unsuitable template

def _xc(
    symbol_scope: str,
    graphic_reuse: str,
    *,
    equivalents: list[dict[str, Any]] | None = None,
    notes: list[str] | None = None,
    companion_tags_international: bool = True,
) -> dict[str, Any]:
    return {
        "symbol_scope": symbol_scope,
        "graphic_reuse_outside_NO": graphic_reuse,
        "companion_tags_international": companion_tags_international,
        "equivalent_traffic_sign_ids": equivalents or [],
        "notes": notes or [],
    }


CROSS_COUNTRY: dict[str, dict[str, Any]] = {
    # Warning signs — Vienna Convention A-series family; DE StVO Gefahrzeichen examples
    # are widely used in OSM taginfo and document same meanings.
    "100.1": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[
            equiv("DE", "DE:103-20", note="Rechtskurve; high taginfo usage"),
            equiv("SE", "SE:A1-2", note="Kurva höger (Swedish A-series)"),
        ],
    ),
    "100.2": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[
            equiv("DE", "DE:103-10", note="Linkskurve"),
            equiv("SE", "SE:A1-1", note="Kurva vänster"),
        ],
    ),
    "102.1": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[
            equiv("DE", "DE:105-20", note="Doppelkurve, zuerst rechts"),
            equiv("SE", "SE:A2-2"),
        ],
    ),
    "102.2": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[
            equiv("DE", "DE:105-10", note="Doppelkurve, zuerst links"),
            equiv("SE", "SE:A2-1"),
        ],
    ),
    "104.1": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:110", note="Steigung"), equiv("SE", "SE:A5-1")],
    ),
    "104.2": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:108", note="Gefälle"), equiv("SE", "SE:A5-2")],
    ),
    "106.1": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:120", note="Verengte Fahrbahn")],
    ),
    "106.2": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:121-20", relation="similar_meaning", note="einseitige Verengung rechts")],
    ),
    "106.3": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:121-10", relation="similar_meaning", note="einseitige Verengung links")],
    ),
    "108": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:112", note="Unebene Fahrbahn")],
    ),
    "109": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[
            equiv(
                "DE",
                "DE:112",
                relation="similar_meaning",
                note="Often signed as uneven road / traffic calming; traffic_calming=hump is global.",
            )
        ],
        notes=["Companion traffic_calming=hump / hazard=bump apply worldwide."],
    ),
    "110": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:123", note="Arbeitsstelle")],
    ),
    "112": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[
            equiv(
                "DE",
                "DE:101",
                relation="similar_meaning",
                note="Loose chippings often via general danger + plate; hazard=loose_gravel is global.",
            )
        ],
    ),
    "114.1": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:115", note="Steinschlag")],
    ),
    "114.2": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:115", relation="similar_meaning", note="Same hazard; side via national variant")],
    ),
    "116": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:114", note="Schleudergefahr")],
    ),
    "117": _xc(
        "vienna_convention_family",
        "with_caveat",
        notes=["Soft verge warnings exist in several VC states; no single universal hazard=* value."],
    ),
    "118": _xc(
        "vienna_convention_family",
        "with_caveat",
        notes=["Movable/opening bridge warnings are VC-family; tag the bridge feature internationally."],
    ),
    "120": _xc(
        "vienna_convention_family",
        "with_caveat",
        notes=["Quayside / water-edge warnings appear across VC Europe."],
    ),
    "122": _xc(
        "vienna_convention_family",
        "with_caveat",
        notes=["Tunnel ahead warnings are widespread; tunnel=yes on the way is global."],
    ),
    "124": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:102", relation="similar_meaning", note="Kreuzung / dangerous junction family")],
    ),
    "126": _xc(
        "vienna_convention_family",
        "with_caveat",
        notes=["Advance roundabout warning; junction=roundabout on the feature is global."],
    ),
    "132": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:131", note="Lichtzeichenanlage")],
    ),
    "134": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:150", relation="similar_meaning", note="Bahnübergang mit Schranken")],
        notes=["railway=level_crossing + crossing:barrier=* are global."],
    ),
    "135": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:151", relation="similar_meaning", note="Bahnübergang ohne Schranken")],
    ),
    "136.1h": _xc(
        "vienna_convention_family",
        "with_caveat",
        notes=[
            "Level-crossing countdown panels (stripe count) are a VC European pattern; "
            "metre spacing is national/local.",
        ],
    ),
    "136.1v": _xc("vienna_convention_family", "with_caveat"),
    "136.2h": _xc("vienna_convention_family", "with_caveat"),
    "136.2v": _xc("vienna_convention_family", "with_caveat"),
    "136.3h": _xc("vienna_convention_family", "with_caveat"),
    "136.3v": _xc("vienna_convention_family", "with_caveat"),
    "138.1": _xc("vienna_convention_family", "with_caveat"),
    "138.2": _xc("vienna_convention_family", "with_caveat"),
    "139": _xc(
        "vienna_convention_family",
        "with_caveat",
        notes=["Tram/tramway warnings are common in VC cities; railway=tram* tags are global."],
    ),
    "140": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:133", relation="similar_meaning", note="Fußgänger — related family")],
        notes=["Distance panel is variable; pedestrian crossing tagging is global."],
    ),
    "142": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:136", note="Kinder")],
        notes=["hazard=children is global."],
    ),
    "144": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:138", note="Radfahrer")],
        notes=["hazard=cyclists is global."],
    ),
    "146.1": _xc(
        "nordic_shared",
        "with_caveat",
        equivalents=[
            equiv("FI", "FI:142", relation="similar_meaning", note="Eläimiä (wild animals) family in FI taginfo"),
            equiv("SE", "SE:A19-1", relation="similar_meaning", note="Djur (animal warning)"),
            equiv("DE", "DE:142", relation="similar_meaning", note="Wildwechsel — generic wildlife, not moose-specific"),
        ],
        notes=[
            "Moose/elg pictogram is strongly Nordic; hazard=animal_crossing + hazard:animal=moose work worldwide.",
        ],
    ),
    "146.2": _xc(
        "nordic_shared",
        "with_caveat",
        equivalents=[
            equiv("SE", "SE:A19-1", relation="similar_meaning", note="Often used with reindeer plate in SE/NO/FI"),
        ],
        notes=["Reindeer warnings are primarily Nordic; companion hazard tags are global."],
    ),
    "146.3": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:142", relation="similar_meaning")],
        notes=["Deer/wildlife warnings are widespread; hazard:animal=deer is global."],
    ),
    "146.4": _xc(
        "vienna_convention_family",
        "with_caveat",
        notes=["Cattle/livestock warnings exist across VC Europe; hazard:animal=cattle is global."],
    ),
    "146.5": _xc(
        "vienna_convention_family",
        "with_caveat",
        notes=["Sheep warnings are common in rural VC states; hazard:animal=sheep is global."],
    ),
    "148": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:125", note="Gegenverkehr")],
    ),
    "149": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:124", note="Stau")],
        notes=["hazard=queues_likely is global."],
    ),
    "150": _xc(
        "vienna_convention_family",
        "with_caveat",
        notes=["Low-flying aircraft / aerodrome warnings are VC-family; hazard=low_flying_aircraft is global."],
    ),
    "151": _xc(
        "vienna_convention_family",
        "with_caveat",
        notes=["Military-activity warnings appear in several countries; tagging remains traffic_sign-national."],
    ),
    "152": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:117", note="Seitenwind")],
        notes=["hazard=side_winds is global."],
    ),
    "153": _xc(
        "vienna_convention_family",
        "no",
        notes=["Accident warnings are typically temporary everywhere; poor basemap icon fit."],
    ),
    "154": _xc(
        "nordic_shared",
        "with_caveat",
        notes=["Skiers-crossing is mainly Nordic/Alpine; no stable global hazard=* value."],
    ),
    "155": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:140", note="Reiter")],
        notes=["hazard=horse_riders is global."],
    ),
    "156": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:101", note="Gefahrstelle / general danger")],
        notes=["General danger; meaning depends on supplementary plate in every country."],
    ),
    # Speed — circular red-ring maxspeed is VC-standard; zone designs vary nationally.
    "362.20": _xc("vienna_convention_family", "yes", notes=["maxspeed=* + source:maxspeed=sign are global."]),
    "362.30": _xc(
        "vienna_convention_family",
        "yes",
        equivalents=[
            equiv("DE", "DE:274-30", note="Zulässige Höchstgeschwindigkeit 30"),
            equiv("SE", "SE:C31-3[30]", relation="similar_meaning"),
        ],
    ),
    "362.40": _xc(
        "vienna_convention_family",
        "yes",
        equivalents=[equiv("DE", "DE:274-40")],
    ),
    "362.50": _xc(
        "vienna_convention_family",
        "yes",
        equivalents=[equiv("DE", "DE:274-50")],
    ),
    "362.60": _xc(
        "vienna_convention_family",
        "yes",
        equivalents=[equiv("DE", "DE:274-60")],
    ),
    "362.70": _xc(
        "vienna_convention_family",
        "yes",
        equivalents=[equiv("DE", "DE:274-70")],
    ),
    "362.80": _xc(
        "vienna_convention_family",
        "yes",
        equivalents=[equiv("DE", "DE:274-80")],
    ),
    "362.90": _xc(
        "vienna_convention_family",
        "yes",
        equivalents=[equiv("DE", "DE:274-90")],
    ),
    "362.100": _xc(
        "vienna_convention_family",
        "yes",
        equivalents=[equiv("DE", "DE:274-100")],
    ),
    "362.110": _xc(
        "vienna_convention_family",
        "yes",
        equivalents=[equiv("DE", "DE:274-110")],
    ),
    "364.20": _xc("vienna_convention_family", "yes"),
    "364.30": _xc(
        "vienna_convention_family",
        "yes",
        equivalents=[equiv("DE", "DE:278-30", note="Ende der zulässigen Höchstgeschwindigkeit")],
    ),
    "364.40": _xc("vienna_convention_family", "yes", equivalents=[equiv("DE", "DE:278-40")]),
    "364.50": _xc("vienna_convention_family", "yes", equivalents=[equiv("DE", "DE:278-50")]),
    "364.60": _xc("vienna_convention_family", "yes", equivalents=[equiv("DE", "DE:278-60")]),
    "364.70": _xc("vienna_convention_family", "yes", equivalents=[equiv("DE", "DE:278-70")]),
    "366": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[
            equiv("DE", "DE:274.1", relation="similar_meaning", note="Beginn einer Tempo-30-Zone (design differs)"),
        ],
        notes=[
            "Zone start plates differ visually by country; maxspeed + maxspeed:type=XX:zoneN pattern is international.",
        ],
    ),
    "367": _xc(
        "norway_specific",
        "no",
        notes=[
            "Speed zone for small electric vehicles is a Norwegian regulatory plate; "
            "do not present as local law outside NO. maxspeed:small_electric_vehicle=* may still apply where used.",
        ],
    ),
    "368": _xc(
        "vienna_convention_family",
        "with_caveat",
        equivalents=[equiv("DE", "DE:274.2", relation="similar_meaning", note="Ende einer Tempo zone")],
    ),
    "369": _xc(
        "norway_specific",
        "no",
        notes=["End of Norwegian small-electric-vehicle speed zone."],
    ),
    "560.1": _xc(
        "norway_specific",
        "no",
        notes=[
            "Shows Norway’s general limits (urban/rural). Other countries have different default limits — not reusable as local law.",
        ],
    ),
    "560.3": _xc(
        "vienna_convention_family",
        "with_caveat",
        notes=["Speed-camera / measurement warnings exist in many countries; enforcement tagging is global."],
    ),
    "812": _xc(
        "vienna_convention_family",
        "with_caveat",
        notes=["Advisory speed plates are widespread; use maxspeed:advisory=* (global), not maxspeed."],
    ),
    "856": _xc(
        "norway_specific",
        "no",
        notes=["Miniature of Norwegian general speed-limit information (see 560.1)."],
    ),
    # Service / tourist — brown/white destination icons are European-familiar; some brands are NO-only.
    "640.10": _xc("generic_poi_icon", "yes", notes=["Sightseeing / attraction symbol — tourism=* is global."]),
    "640.101": _xc(
        "generic_poi_icon",
        "yes",
        notes=["UNESCO World Heritage symbol is internationally understood; heritage=* is global."],
    ),
    "640.102": _xc(
        "norway_specific",
        "no",
        notes=["National fortifications programme symbol — Norway-specific programme marking."],
    ),
    "640.12": _xc("generic_poi_icon", "yes"),
    "640.20": _xc("generic_poi_icon", "yes"),
    "640.30": _xc("generic_poi_icon", "yes"),
    "650.10": _xc("generic_poi_icon", "yes"),
    "650.11": _xc("generic_poi_icon", "yes"),
    "650.20": _xc("generic_poi_icon", "yes"),
    "650.21": _xc("generic_poi_icon", "yes", notes=["Nordic/Alpine ski-trail icons are widely understood."]),
    "650.22": _xc("generic_poi_icon", "yes"),
    "650.40": _xc(
        "nordic_shared",
        "with_caveat",
        notes=["Farm food / rural tourism labelling is regional; tourism/shop tags remain global."],
    ),
    "650.41": _xc(
        "norway_specific",
        "no",
        notes=["Olavsrosa is a Norwegian quality label — not an international tourist symbol."],
    ),
    # Direction / route
    "723.31": _xc(
        "norway_specific",
        "no",
        notes=["Nasjonale turistveger marker — Norwegian national tourist-route network."],
    ),
    "723.41": _xc(
        "vienna_convention_family",
        "with_caveat",
        notes=["HGV diversion markers exist in many countries; often temporary."],
    ),
    "723.51": _xc(
        "vienna_convention_family",
        "with_caveat",
        notes=["Dangerous-goods route markers exist across VC Europe; hazmat=* is global."],
    ),
    "723.61": _xc("vienna_convention_family", "with_caveat", notes=["Generic diversion symbols — often temporary."]),
    "723.62": _xc("vienna_convention_family", "with_caveat"),
    "723.63": _xc("vienna_convention_family", "with_caveat"),
    "723.64": _xc("vienna_convention_family", "with_caveat"),
    "723.65": _xc("vienna_convention_family", "with_caveat"),
    "723.66": _xc("vienna_convention_family", "with_caveat"),
    "723.71": _xc(
        "vienna_convention_family",
        "no",
        notes=["Junction-number template with variable digits — same idea on many motorways, not a fixed icon."],
    ),
    "723.72": _xc("vienna_convention_family", "no"),
    "723.73": _xc("vienna_convention_family", "no"),
    "755": _xc("generic_poi_icon", "yes", notes=["Numbered cycle-route signing is common across Europe."]),
    "761": _xc(
        "vienna_convention_family",
        "with_caveat",
        notes=["Motorway class symbol; highway=motorway is global (national plate design differs)."],
    ),
    "763": _xc(
        "vienna_convention_family",
        "with_caveat",
        notes=["Motorroad / motortrafikkveg class; motorroad=yes is used in several VC countries."],
    ),
    "765": _xc("generic_poi_icon", "yes", notes=["Toll / road-user charging; toll=yes is global."]),
    "767": _xc("generic_poi_icon", "yes"),
    "769": _xc("generic_poi_icon", "yes"),
    "771": _xc("generic_poi_icon", "yes"),
    "772": _xc("generic_poi_icon", "yes"),
    "773": _xc("generic_poi_icon", "yes"),
    "774": _xc("generic_poi_icon", "yes"),
    "775": _xc("generic_poi_icon", "yes"),
    "776": _xc("generic_poi_icon", "yes"),
    "780": _xc(
        "nordic_shared",
        "with_caveat",
        notes=["Snow-chains related signing is common in Nordic/Alpine states; snow_chains=* is global but uncommon."],
    ),
    "790.10": _xc("generic_poi_icon", "yes"),
    "790.15": _xc("generic_poi_icon", "yes"),
    "790.16": _xc("generic_poi_icon", "yes"),
    "790.20": _xc("generic_poi_icon", "yes"),
    "790.30": _xc("generic_poi_icon", "yes"),
    "790.31": _xc("generic_poi_icon", "yes"),
    "790.32": _xc("generic_poi_icon", "yes"),
    "790.40": _xc("generic_poi_icon", "yes"),
}


def resolve_international(code: str, category: str, navi_fixed: bool) -> dict[str, Any]:
    """Build the per-sign international reuse block."""
    base = CROSS_COUNTRY.get(code)
    if base is None:
        # Conservative fallback by category
        if category == "fareskilt":
            base = _xc("vienna_convention_family", "with_caveat")
        elif category == "speed_limit":
            base = _xc("vienna_convention_family", "with_caveat")
        else:
            base = _xc("generic_poi_icon", "with_caveat")

    graphic = base["graphic_reuse_outside_NO"]
    usable_icon = graphic in {"yes", "with_caveat"} and navi_fixed
    if graphic == "no":
        usable_icon = False

    return {
        "companion_tags_international": base["companion_tags_international"],
        "symbol_scope": base["symbol_scope"],
        "graphic_reuse_outside_NO": graphic,
        "usable_as_navi_icon_outside_norway": usable_icon,
        "equivalent_traffic_sign_ids": base["equivalent_traffic_sign_ids"],
        "mapping_note": (
            "When mapping roads outside Norway, use that country's traffic_sign=ISO:code, "
            "not NO:{code}. Companion tags (hazard=*, maxspeed=*, amenity=*, …) stay the same. "
            "See meta.international for Vienna Convention country lists."
        ),
        "notes": base["notes"],
    }


def build(offline: bool = False) -> dict[str, Any]:
    catalogue = json.loads(SIGNS_EN.read_text(encoding="utf-8"))
    signs = catalogue["signs"]

    usage: dict[str, int] = {}
    examples: dict[str, list[tuple[int, str]]] = {}
    data_until = None
    if not offline:
        usage, examples, data_until = fetch_traffic_sign_usage()

    entries: list[dict[str, Any]] = []
    missing_mappings: list[str] = []

    for sign in signs:
        code = sign["code"]
        mapping = MAPPINGS.get(code)
        if mapping is None:
            missing_mappings.append(code)
            mapping = {
                "match_status": "traffic_sign_only",
                "implied_tags": [],
                "notes": ["No curated OSM mapping row yet; traffic_sign=NO:{code} remains valid."],
                "sources": [WIKI_TRAFFIC_SIGN],
            }

        preferred = f"NO:{code}"
        template = mapping.get("traffic_sign_template", preferred)
        variants = list(mapping.get("traffic_sign_variants") or [])

        # taginfo: exact code + colon variant for dotted codes
        count = usage.get(code, 0)
        if "." in code:
            base, rest = code.split(".", 1)
            count += usage.get(f"{base}:{rest}", 0)  # if extract ever keeps colon form
            # Also values already normalized to dotted form in extract_no_codes

        obs_examples = [
            {"count": c, "value": v}
            for c, v in sorted(examples.get(code, []), key=lambda x: -x[0])[:5]
        ]

        match_status = mapping["match_status"]
        navi = default_navi_usable(match_status, mapping.get("navi_usable"))

        # Destination symbols / traffic_sign_only can still be navi-useful as icons
        # when they are fixed pictograms — override for fixed destination icons.
        if match_status == "destination_symbol" and code not in {
            "723.61",
            "723.62",
            "723.63",
            "723.64",
            "723.65",
            "723.66",
            "723.41",
            "723.51",
        }:
            # Fixed tourist/direction pictograms are usable as destination icons;
            # diversions stay false via explicit navi_usable in mapping.
            if mapping.get("navi_usable") is None:
                navi = True

        if match_status == "traffic_sign_only" and code not in {"153", "151", "154", "117", "118", "120"}:
            # Fixed warning pictograms without hazard=* are still usable as icons.
            if mapping.get("navi_usable") is None and sign["category"] == "fareskilt":
                navi = True

        international = resolve_international(code, sign["category"], navi)

        entry = {
            "code": code,
            "category": sign["category"],
            "name": sign["name"],
            "name_nb": sign["name_nb"],
            "svg": sign.get("svg"),
            "traffic_sign": {
                "preferred": preferred,
                "template": template,
                "variants_documented": variants,
                "taginfo_object_count_approx": count,
                "taginfo_examples": obs_examples,
                "taginfo_url": TAGINFO_TS + urllib.parse.quote(preferred),
            },
            "implied_tags": mapping.get("implied_tags") or [],
            "related_tags": mapping.get("related_tags") or [],
            "match_status": match_status,
            "navi_usable_as_fixed_symbol": navi,
            "international": international,
            "variable_fields": mapping.get("variable_fields") or [],
            "notes": mapping.get("notes") or [],
            "sources": mapping.get("sources") or [WIKI_TRAFFIC_SIGN],
        }
        entries.append(entry)

    by_status: dict[str, int] = defaultdict(int)
    by_scope: dict[str, int] = defaultdict(int)
    by_graphic: dict[str, int] = defaultdict(int)
    with_usage = 0
    intl_icon = 0
    with_equivs = 0
    for e in entries:
        by_status[e["match_status"]] += 1
        intl = e["international"]
        by_scope[intl["symbol_scope"]] += 1
        by_graphic[intl["graphic_reuse_outside_NO"]] += 1
        if intl["usable_as_navi_icon_outside_norway"]:
            intl_icon += 1
        if intl["equivalent_traffic_sign_ids"]:
            with_equivs += 1
        if e["traffic_sign"]["taginfo_object_count_approx"] > 0:
            with_usage += 1

    meta = {
        "title": "Norwegian traffic signs — OpenStreetMap tag mapping",
        "description": (
            "Maps each catalogue skiltnummer to traffic_sign=NO:* and companion OSM tags "
            "that exist in the wiki / taginfo today. Records which symbols/tags are reusable "
            "outside Norway (Vienna Convention family vs Norway-specific). "
            "Does not invent new OSM keys."
        ),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "taginfo_data_until": data_until,
        "catalogue": "database/signs_en.json",
        "license_note": (
            "This mapping file is project documentation. OSM data is ODbL; "
            "sign graphics remain under NLOD 2.0 as in the catalogue. "
            "Norwegian SVGs are national designs — usable as generic European-style icons "
            "where marked, but not as official local traffic signs in other countries."
        ),
        "sources": {
            "osm_wiki_norway": WIKI_NO,
            "osm_wiki_hazard": WIKI_HAZARD,
            "osm_wiki_traffic_sign": WIKI_TRAFFIC_SIGN,
            "osm_wiki_vienna_convention": WIKI_VIENNA,
            "wikipedia_eu_comparison": WIKI_EU_COMPARE,
            "wikipedia_norway_signs": WIKI_NO_SIGNS_EN,
            "taginfo": "https://taginfo.openstreetmap.org/",
        },
        "match_status_values": {
            "wiki_documented": "Listed with tags on No:Road_signs_in_Norway",
            "hazard_convention": "Mapped via Key:hazard approved or documented ad-hoc values",
            "speed_convention": "Unused — speed signs use wiki_documented",
            "destination_symbol": "Service/direction pictogram; maps to destination/POI tags",
            "traffic_sign_only": "NO: code is valid; no stable companion tag",
            "variable_content": "Sign content varies (distance, speed figure, etc.)",
            "not_for_navigation": "Template with variable digits; unsuitable as fixed navi icon",
        },
        "international": {
            "summary": (
                "Norway is a Vienna Convention party. Most warning triangles and circular speed "
                "plates share meaning with other European countries; OSM companion tags "
                "(hazard=*, maxspeed=*, amenity=*, …) are global. Always map foreign roads with "
                "that country's traffic_sign=ISO:… ID, never NO:… . Example DE/SE/FI IDs are "
                "illustrative same-meaning references from taginfo/wiki, not exhaustive."
            ),
            "symbol_scope_values": {
                "vienna_convention_family": "Same hazard/speed pictogram family across VC Europe",
                "nordic_shared": "Especially familiar in NO/SE/FI (moose, reindeer, ski, chains)",
                "generic_poi_icon": "Destination/service icon meaning widely understood",
                "norway_specific": "Norwegian law, network, or brand — not local law elsewhere",
            },
            "graphic_reuse_values": {
                "yes": "SVG fine as a generic European-style navi icon",
                "with_caveat": "Usable as icon; national drawings/colours still differ",
                "no": "Do not reuse as a foreign official sign or fixed navi law icon",
            },
            "vienna_convention_family_countries": VIENNA_FAMILY_COUNTRIES,
            "vienna_aligned_extra_countries": VIENNA_ALIGNED_EXTRA,
        },
        "counts": {
            "total": len(entries),
            "with_taginfo_traffic_sign_usage": with_usage,
            "by_match_status": dict(sorted(by_status.items())),
            "navi_usable_as_fixed_symbol": sum(
                1 for e in entries if e["navi_usable_as_fixed_symbol"]
            ),
            "usable_as_navi_icon_outside_norway": intl_icon,
            "with_foreign_equivalent_examples": with_equivs,
            "by_symbol_scope": dict(sorted(by_scope.items())),
            "by_graphic_reuse_outside_NO": dict(sorted(by_graphic.items())),
        },
        "missing_curated_mappings": missing_mappings,
        "conventions": {
            "country_prefix": "NO",
            "traffic_sign_syntax": (
                "traffic_sign=NO:{skiltnummer} with optional [parameter] for variable panels; "
                "compound signs use ';' or ',' per Key:traffic_sign / Norwegian wiki."
            ),
            "hazard_on_sign": (
                "Prefer traffic_sign=NO:… on the sign node, plus hazard=* (and hazard:animal=* "
                "where relevant) on the sign and/or affected highway segment."
            ),
            "speed_limits": (
                "362.xx → maxspeed + source:maxspeed=sign; "
                "366 → maxspeed + maxspeed:type=NO:zone{n}; "
                "812 → maxspeed:advisory only."
            ),
            "cross_country": (
                "Companion tags are international. National traffic_sign IDs are not. "
                "See each entry's international block and meta.international."
            ),
        },
    }

    return {"meta": meta, "signs": entries}


CATEGORY_LABELS = {
    "fareskilt": "Warning signs (fareskilt)",
    "speed_limit": "Speed limit and related",
    "serviceskilt": "Service / tourist symbols (serviceskilt)",
    "vegvisning": "Direction / route symbols (vegvisning)",
}


def _fmt_tag(t: dict[str, Any]) -> str:
    key = t.get("key", "")
    if "value" in t and t["value"] is not None:
        return f"`{key}={t['value']}`"
    return f"`{key}=*`"


def _fmt_tags(tags: list[dict[str, Any]]) -> str:
    if not tags:
        return "—"
    return "; ".join(_fmt_tag(t) for t in tags)


def _fmt_equivs(equivs: list[dict[str, Any]]) -> str:
    if not equivs:
        return "—"
    parts = []
    for e in equivs:
        parts.append(f"`{e['traffic_sign']}`")
    return ", ".join(parts)


def _yes_no(flag: bool) -> str:
    return "yes" if flag else "no"


def _md_escape_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def write_markdown(db: dict[str, Any], path: Path) -> None:
    """Write a human-readable Markdown companion to osm_tags.json."""
    meta = db["meta"]
    counts = meta["counts"]
    lines: list[str] = []
    lines.append("# OpenStreetMap tag mapping (human-readable)")
    lines.append("")
    lines.append(
        "Readable view of [`osm_tags.json`](osm_tags.json). "
        "Machine consumers should use the JSON. Regenerate both with "
        "`python3 tool/build_osm_tags.py`."
    )
    lines.append("")
    lines.append(f"Generated: `{meta.get('generated_at', '')}`")
    if meta.get("taginfo_data_until"):
        lines.append(f"Taginfo data until: `{meta['taginfo_data_until']}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Metric | Count |")
    lines.append("|--------|------:|")
    lines.append(f"| Total catalogue codes | {counts['total']} |")
    lines.append(
        f"| Seen in taginfo as `traffic_sign=NO:…` | {counts['with_taginfo_traffic_sign_usage']} |"
    )
    lines.append(
        f"| Usable as fixed navi symbol | {counts['navi_usable_as_fixed_symbol']} |"
    )
    lines.append(
        f"| Usable as navi icon outside Norway | {counts['usable_as_navi_icon_outside_norway']} |"
    )
    lines.append(
        f"| With foreign equivalent examples | {counts['with_foreign_equivalent_examples']} |"
    )
    lines.append("")
    lines.append("### By match status")
    lines.append("")
    lines.append("| Status | Count | Meaning |")
    lines.append("|--------|------:|---------|")
    for status, n in counts["by_match_status"].items():
        meaning = meta["match_status_values"].get(status, "")
        lines.append(f"| `{status}` | {n} | {_md_escape_cell(meaning)} |")
    lines.append("")
    lines.append("### By international symbol scope")
    lines.append("")
    lines.append("| Scope | Count | Meaning |")
    lines.append("|-------|------:|---------|")
    scope_meanings = meta["international"]["symbol_scope_values"]
    for scope, n in counts["by_symbol_scope"].items():
        lines.append(
            f"| `{scope}` | {n} | {_md_escape_cell(scope_meanings.get(scope, ''))} |"
        )
    lines.append("")
    lines.append("## Conventions")
    lines.append("")
    lines.append(meta["international"]["summary"])
    lines.append("")
    lines.append(
        "- Norwegian roads: `traffic_sign=NO:{code}` plus companion tags below."
    )
    lines.append(
        "- Other countries: use that country’s `traffic_sign=ISO:…` ID; keep "
        "`hazard=*`, `maxspeed=*`, POI tags as listed."
    )
    lines.append(
        "- Full Vienna Convention country lists: see `meta.international` in "
        "[`osm_tags.json`](osm_tags.json)."
    )
    lines.append("")

    # Group signs by category preserving catalogue order
    by_cat: dict[str, list[dict[str, Any]]] = {}
    for sign in db["signs"]:
        by_cat.setdefault(sign["category"], []).append(sign)

    for cat in ("fareskilt", "speed_limit", "serviceskilt", "vegvisning"):
        signs = by_cat.get(cat) or []
        if not signs:
            continue
        lines.append(f"## {CATEGORY_LABELS.get(cat, cat)}")
        lines.append("")
        lines.append(
            "| Code | Name | `traffic_sign` | Implied tags | Related tags | "
            "Match | Navi | Outside NO | Scope | Equivalents | Notes |"
        )
        lines.append(
            "|------|------|----------------|--------------|--------------|"
            "-------|------|------------|-------|-------------|-------|"
        )
        for s in signs:
            intl = s["international"]
            ts = s["traffic_sign"]
            preferred = ts.get("preferred", f"NO:{s['code']}")
            template = ts.get("template") or preferred
            ts_cell = f"`{preferred}`"
            if template != preferred:
                ts_cell += f" / `{template}`"
            count = ts.get("taginfo_object_count_approx") or 0
            if count:
                ts_cell += f" (~{count})"

            notes_parts: list[str] = []
            notes_parts.extend(s.get("notes") or [])
            notes_parts.extend(intl.get("notes") or [])
            if s.get("variable_fields"):
                vf = ", ".join(
                    f["name"] for f in s["variable_fields"] if f.get("name")
                )
                if vf:
                    notes_parts.append(f"Variable: {vf}")
            notes = "; ".join(notes_parts) if notes_parts else "—"

            svg = s.get("svg")
            code_cell = f"`{s['code']}`"
            if svg:
                code_cell = f"[`{s['code']}`](../{svg})"

            lines.append(
                "| "
                + " | ".join(
                    [
                        code_cell,
                        _md_escape_cell(s.get("name") or ""),
                        ts_cell,
                        _md_escape_cell(_fmt_tags(s.get("implied_tags") or [])),
                        _md_escape_cell(_fmt_tags(s.get("related_tags") or [])),
                        f"`{s.get('match_status', '')}`",
                        _yes_no(bool(s.get("navi_usable_as_fixed_symbol"))),
                        _yes_no(bool(intl.get("usable_as_navi_icon_outside_norway"))),
                        f"`{intl.get('symbol_scope', '')}`",
                        _md_escape_cell(_fmt_equivs(intl.get("equivalent_traffic_sign_ids") or [])),
                        _md_escape_cell(notes),
                    ]
                )
                + " |"
            )
        lines.append("")

    lines.append("## Sources")
    lines.append("")
    for key, url in (meta.get("sources") or {}).items():
        lines.append(f"- {key}: {url}")
    lines.append("")
    lines.append(meta.get("license_note", ""))
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Skip taginfo fetch (counts will be 0).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=OUT,
        help=f"JSON output path (default: {OUT})",
    )
    parser.add_argument(
        "--markdown",
        type=Path,
        default=OUT_MD,
        help=f"Markdown output path (default: {OUT_MD})",
    )
    args = parser.parse_args(argv)

    # Ensure every catalogue code has a mapping key before build warnings
    catalogue_codes = {s["code"] for s in json.loads(SIGNS_EN.read_text(encoding="utf-8"))["signs"]}
    mapped = set(MAPPINGS)
    cross = set(CROSS_COUNTRY)
    extra = sorted(mapped - catalogue_codes)
    missing = sorted(catalogue_codes - mapped)
    missing_xc = sorted(catalogue_codes - cross)
    extra_xc = sorted(cross - catalogue_codes)
    if extra:
        print(f"Warning: mappings not in catalogue: {extra}")
    if missing:
        print(f"Warning: catalogue codes without curated mapping: {missing}")
    if missing_xc:
        print(f"Warning: catalogue codes without cross-country row: {missing_xc}")
    if extra_xc:
        print(f"Warning: cross-country rows not in catalogue: {extra_xc}")

    db = build(offline=args.offline)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(db, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")
    write_markdown(db, args.markdown)
    print(f"Wrote {args.markdown}")
    print(json.dumps(db["meta"]["counts"], indent=2))
    if db["meta"]["missing_curated_mappings"]:
        print("Missing curated mappings:", db["meta"]["missing_curated_mappings"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
