"""Fetch and classify sign metadata from the NVDB API Les v4 datakatalog."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import requests

from .meanings_en import english_for
from .config import (
    CATEGORY_FARESKILT,
    CATEGORY_SPEED_LIMIT,
    HTTP_HEADERS,
    NVDB_BASE,
    NVDB_SKILTNUMMER_EGENSKAP,
    NVDB_SKILTPLATE_TYPE,
    SKILTFORSKRIFTEN_URL,
    WORK_DIR,
)

# English glosses for common sign descriptions (hand-curated, not machine-translated).
EN_GLOSSES: dict[str, str] = {
    "Farlig sving, til høyre.": "Dangerous bend to the right",
    "Farlig sving, til venstre.": "Dangerous bend to the left",
    "Farlige svinger, den første til høyre.": "Series of dangerous bends, first to the right",
    "Farlige svinger, den første til venstre.": "Series of dangerous bends, first to the left",
    "Bratt bakke, stigning.": "Steep hill upwards",
    "Bratt bakke, fall.": "Steep hill downwards",
    "Smalere veg, Innsnevring på begge sider.": "Road narrows on both sides",
    "Smalere veg, Innsnevring på høyre side.": "Road narrows on the right",
    "Smalere veg, Innsnevring på venstre side.": "Road narrows on the left",
    "Ujevn veg.": "Uneven road",
    "Fartshump.": "Speed hump",
    "Vegarbeid.": "Road works",
    "Steinsprut.": "Loose chippings",
    "Rasfare, høyre side.": "Falling rocks, right side",
    "Rasfare, venstre side.": "Falling rocks, left side",
    "Glatt kjørebane.": "Slippery road",
    "Farlig vegskulder.": "Soft verges",
    "Bevegelig bru.": "Opening or swing bridge",
    "Kai, strand eller ferjeleie.": "Quayside or ferry terminal",
    "Tunnel.": "Tunnel",
    "Farlig vegkryss.": "Dangerous junction",
    "Rundkjøring.": "Roundabout",
    "Trafikklyssignal.": "Traffic signals",
    "Planovergang med bom.": "Level crossing with barrier",
    "Planovergang uten bom.": "Level crossing without barrier",
    "Avstandsskilt.": "Distance to level crossing",
    "Jernbanespor, enkeltsporet.": "Single-track railway",
    "Jernbanespor, flersporet.": "Multi-track railway",
    "Sporvogn.": "Tramway",
    "Avstand til gangfelt.": "Distance to pedestrian crossing",
    "Barn.": "Children",
    "Syklende.": "Cyclists",
    "Elg.": "Elk / moose",
    "Rein.": "Reindeer",
    "Hjort.": "Deer",
    "Ku.": "Cattle",
    "Sau.": "Sheep",
    "Møtende trafikk.": "Two-way traffic",
    "Kø.": "Queue / congestion",
    "Fly.": "Low-flying aircraft",
    "Militær aktivitet.": "Military activity",
    "Sidevind.": "Side winds",
    "Trafikkulykke.": "Accident",
    "Skiløpere.": "Skiers crossing",
    "Ridende.": "Horse riders",
    "Annen fare.": "Other danger",
    "Fartsgrensesone.": "Speed limit zone",
    "Fartsgrensesone for liten elektrisk motorvogn.": "Speed limit zone for small electric vehicles",
    "Slutt på fartsgrensesone.": "End of speed limit zone",
    "Slutt på fartsgrensesone for liten elektrisk motorvogn.": "End of speed limit zone for small electric vehicles",
    "Anbefalt fart.": "Recommended speed",
    "Generelle fartsgrenser.": "General speed limits",
    "Generell fartsgrense i miniatyr": "General speed limit (miniature)",
}


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update(HTTP_HEADERS)
    s.headers["Accept"] = "application/json"
    return s


def fetch_skiltnummer_values(cache_path: Path | None = None) -> list[dict[str, Any]]:
    """Return all allowed Skiltnummer enum values from vegobjekttype 96."""
    cache_path = cache_path or (WORK_DIR / "nvdb_skiltnummer.json")
    WORK_DIR.mkdir(parents=True, exist_ok=True)

    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))

    url = f"{NVDB_BASE}/vegobjekttyper/{NVDB_SKILTPLATE_TYPE}"
    resp = _session().get(url, timeout=120)
    resp.raise_for_status()
    payload = resp.json()

    values: list[dict[str, Any]] = []
    for egenskap in payload.get("egenskapstyper", []):
        if egenskap.get("id") == NVDB_SKILTNUMMER_EGENSKAP:
            values = egenskap.get("tillatte_verdier") or []
            break
    if not values:
        raise RuntimeError("NVDB response did not include Skiltnummer tillatte_verdier")

    cache_path.write_text(json.dumps(values, ensure_ascii=False, indent=2), encoding="utf-8")
    # Also keep the raw type document for auditing.
    (WORK_DIR / "nvdb_vegobjekttype_96.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return values


def _leading_number(kortnavn: str) -> int | None:
    m = re.match(r"U?(\d+)", kortnavn or "")
    return int(m.group(1)) if m else None


def is_fareskilt(kortnavn: str) -> bool:
    n = _leading_number(kortnavn)
    return n is not None and 100 <= n < 200


def is_speed_limit_related(kortnavn: str) -> bool:
    """Speed limits and directly related opplysnings-/forbudsskilt.

    Includes fartsgrense start/end, zone variants, recommended speed, and
    the general-speed-limit information signs. Excludes parking zones and
    lane/fartsøkning directional signs.
    """
    kn = kortnavn or ""
    n = _leading_number(kn)
    if n is None:
        return False
    if n in (362, 364, 366, 367, 368, 369, 812, 856):
        return True
    # Exact codes only — do not treat 560.11 / 560.12 as speed signs.
    if kn in ("560.1", "560.3"):
        return True
    return False


def legal_reference_for(kortnavn: str) -> str:
    """Skiltforskriften section hint derived from official series numbering."""
    n = _leading_number(kortnavn)
    if n is None:
        return SKILTFORSKRIFTEN_URL
    if 100 <= n < 200:
        return f"{SKILTFORSKRIFTEN_URL} (fareskilt, skilt {kortnavn})"
    if 300 <= n < 400:
        return f"{SKILTFORSKRIFTEN_URL} (forbudsskilt, skilt {kortnavn})"
    if 500 <= n < 600:
        return f"{SKILTFORSKRIFTEN_URL} (opplysningsskilt, skilt {kortnavn})"
    if 800 <= n < 900:
        return f"{SKILTFORSKRIFTEN_URL} (underskilt, skilt {kortnavn})"
    return f"{SKILTFORSKRIFTEN_URL} (skilt {kortnavn})"


def english_name(description_nb: str, kortnavn: str) -> tuple[str | None, bool]:
    """Return (english, machine_translated_flag).

    Prefer curated glosses from meanings_en. For patterned speed-limit names,
    derive English deterministically (not machine translation).
    """
    name_en, _meaning = english_for(kortnavn)
    if name_en:
        return name_en, False

    desc = (description_nb or "").strip()
    if desc in EN_GLOSSES:
        return EN_GLOSSES[desc], False

    m = re.match(r"Fartsgrense (\d+) km/t\.?", desc)
    if m:
        return f"Speed limit {m.group(1)} km/h", False
    m = re.match(r"Slutt på særskilt fartsgrense (\d+) km/t\.?", desc)
    if m:
        return f"End of special speed limit {m.group(1)} km/h", False
    if desc.startswith("Forvarsling om fartsmåling"):
        return "Warning of speed measurement", False

    return None, False


def select_in_scope(values: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Filter NVDB enum values to fareskilt + speed-limit-related signs."""
    selected: list[dict[str, Any]] = []
    for v in values:
        kn = v.get("kortnavn") or ""
        # Skip withdrawn (U-prefixed) codes unless they are the only form.
        if kn.startswith("U"):
            continue
        if is_fareskilt(kn):
            category = CATEGORY_FARESKILT
        elif is_speed_limit_related(kn):
            category = CATEGORY_SPEED_LIMIT
        else:
            continue

        desc = (v.get("beskrivelse") or "").strip()
        en, machine = english_name(desc, kn)
        selected.append(
            {
                "code": kn,
                "nvdb_enum_id": v.get("id"),
                "category": category,
                "name_nb": desc,
                "name_en": en,
                "name_en_machine_translated": machine,
                "nvdb_value": v.get("verdi"),
                "legal_reference": legal_reference_for(kn),
                "sort_order": v.get("sorteringsnummer"),
            }
        )
    selected.sort(key=lambda x: (0 if x["category"] == CATEGORY_FARESKILT else 1, x["code"]))
    return selected


def load_or_fetch_in_scope() -> list[dict[str, Any]]:
    values = fetch_skiltnummer_values()
    selected = select_in_scope(values)
    out = WORK_DIR / "nvdb_in_scope.json"
    out.write_text(json.dumps(selected, ensure_ascii=False, indent=2), encoding="utf-8")
    return selected
