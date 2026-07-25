#!/usr/bin/env python3
"""Import serviceskilt / vegvisningssymboler into svg/ + databases.

Prefer Geonorge SVG, then vegvesen EPS, then JPG tracing.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from .config import (
    CONVERSION_NONE,
    DATABASE_DIR,
    DATABASE_PATH,
    NLOD_URL,
    PMS_COLORS,
    REPO_ROOT,
    SVG_DIR,
    WORK_DIR,
)
from .convert import (
    ConversionError,
    catalogue_geonorge_svg,
    convert_eps_to_svg,
    convert_jpg_to_svg,
)
from .meanings_en import SIGN_EN
from .pipeline import build_database, build_english_database
from .sources import index_by_extension, index_geonorge, resolve_sources

CATEGORY_SERVICE = "serviceskilt"
CATEGORY_VEGVISNING = "vegvisning"

DEFINED_CODES = [
    "640.10", "640.12", "640.20", "640.30", "640.101", "640.102",
    "650.10", "650.11", "650.20", "650.21", "650.22", "650.40", "650.41",
    "723.31", "723.41", "723.51", "723.61", "723.62", "723.63", "723.64",
    "723.65", "723.66", "723.71", "723.72", "723.73",
    "755", "761", "763", "765", "767", "769", "771", "772", "773", "774",
    "775", "776", "780",
    "790.10", "790.15", "790.16", "790.20", "790.30", "790.31", "790.32", "790.40",
]

GUIDANCE_EN: dict[str, tuple[str, str]] = {
    "640.10": ("Point of interest / sightseeing", "Tourist symbol for a noteworthy sight. A custom symbol may replace this for sights of particular importance."),
    "640.12": ("Museum / gallery", "Tourist symbol for a museum or gallery."),
    "640.20": ("Viewpoint", "Tourist symbol for a scenic viewpoint."),
    "640.30": ("Nature conservation area", "Tourist symbol for a nature conservation / protected nature area."),
    "640.101": ("World Heritage", "Tourist symbol for a UNESCO World Heritage site."),
    "640.102": ("National fortifications", "Tourist symbol for national fortifications."),
    "650.10": ("Bathing area", "Tourist/activity symbol for a bathing area."),
    "650.11": ("Fishing spot", "Tourist/activity symbol for a fishing spot."),
    "650.20": ("Hiking trail", "Tourist/activity symbol for a hiking trail."),
    "650.21": ("Ski trail", "Tourist/activity symbol for a ski trail / cross-country track."),
    "650.22": ("Cycle trail", "Tourist/activity symbol for a cycle trail."),
    "650.40": ("Farm food / rural tourism", "Tourist symbol for farm food / rural tourism (gardsmat/bygdeturisme)."),
    "650.41": ("Olavsrosa", "Tourist symbol for sites marked with the Olavsrosa quality label."),
    "723.31": ("National tourist route", "Route marker for a national tourist road; may also appear on service signs."),
    "723.41": ("Diversion for large vehicles", "Route marker for a diversion route for large vehicles."),
    "723.51": ("Route for dangerous goods", "Route marker for transport of dangerous goods."),
    "723.61": ("Other diversion route (dash)", "Alternative diversion-route symbol (dash)."),
    "723.62": ("Other diversion route (filled square)", "Alternative diversion-route symbol (filled square)."),
    "723.63": ("Other diversion route (triangle)", "Alternative diversion-route symbol (triangle)."),
    "723.64": ("Other diversion route (hollow square)", "Alternative diversion-route symbol (hollow square)."),
    "723.65": ("Other diversion route (circle)", "Alternative diversion-route symbol (circle)."),
    "723.66": ("Other diversion route (arrow)", "Alternative diversion-route symbol (arrow)."),
    "723.71": ("Junction number — motorway", "Junction-number symbol used on motorways with grade-separated junctions."),
    "723.72": ("Junction number — other multilane", "Junction-number symbol for other multilane roads with grade-separated junctions."),
    "723.73": ("Junction number — two-lane", "Junction-number symbol for two-lane roads with grade-separated junctions."),
    "755": ("Cycle route sign", "Direction signing for numbered / marked cycle routes."),
    "761": ("Motorway", "Direction symbol indicating a motorway."),
    "763": ("Motor traffic road", "Direction symbol indicating a motor traffic road (motortrafikkveg)."),
    "765": ("Toll road / road user charging", "Direction symbol for a toll road or road-user charging."),
    "767": ("Parking", "Direction symbol for parking."),
    "769": ("Parking garage", "Direction symbol for a parking garage / multi-storey car park."),
    "771": ("Airport", "Direction symbol for an airport."),
    "772": ("Heliport", "Direction symbol for a heliport / helicopter landing site."),
    "773": ("Bus station / terminal", "Direction symbol for a bus station or bus terminal."),
    "774": ("Railway station / train terminal", "Direction symbol for a railway station or train terminal."),
    "775": ("Car ferry", "Direction symbol for a car ferry."),
    "776": ("Cargo port", "Direction symbol for a cargo / freight port."),
    "780": ("Snow chains", "Direction symbol related to snow chains (kjetting)."),
    "790.10": ("Church", "Direction symbol for a church."),
    "790.15": ("Business / industrial area", "Direction symbol for a business or industrial area."),
    "790.16": ("Shopping centre", "Direction symbol for a shopping centre."),
    "790.20": ("Swimming pool", "Direction symbol for a swimming hall / indoor pool."),
    "790.30": ("Alpine ski centre", "Direction symbol for an alpine ski centre."),
    "790.31": ("Ski jump", "Direction symbol for a ski jump."),
    "790.32": ("Ski stadium", "Direction symbol for a ski stadium."),
    "790.40": ("Golf course", "Direction symbol for a golf course."),
}


def category_for(code: str) -> str:
    n = int(re.match(r"(\d+)", code).group(1))
    if n in (640, 650):
        return CATEGORY_SERVICE
    return CATEGORY_VEGVISNING


def legal_ref(code: str) -> str:
    n = int(re.match(r"(\d+)", code).group(1))
    base = "https://lovdata.no/dokument/SF/forskrift/2005-10-07-1219"
    if n in (640, 650):
        return f"{base} (serviceskilt / Kap. 6, skilt {code})"
    return f"{base} (vegvisningsskilt / Kap. 8, skilt {code})"


def safe_name(code: str) -> str:
    return code.replace(".", "_").replace("/", "_")


def nvdb_map() -> dict[str, dict[str, Any]]:
    path = WORK_DIR / "nvdb_skiltnummer.json"
    vals = json.loads(path.read_text(encoding="utf-8"))
    out = {}
    for v in vals:
        kn = v.get("kortnavn") or ""
        if kn in DEFINED_CODES:
            out[kn] = v
    return out


def build_indexes():
    geo = index_geonorge(WORK_DIR / "unpacked" / "geonorge")
    eps_roots = [
        WORK_DIR / "unpacked" / "serviceskilt_eps",
        WORK_DIR / "unpacked" / "vegvisningsskilt_eps",
    ]
    jpg_roots = [
        WORK_DIR / "unpacked" / "serviceskilt_jpg",
        WORK_DIR / "unpacked" / "vegvisningsskilt_jpg",
    ]
    return {
        "geonorge": geo,
        "eps": index_by_extension(eps_roots, (".eps",)),
        "jpg": index_by_extension(jpg_roots, (".jpg", ".jpeg", ".png")),
    }


def process_one(code: str, nvdb: dict, indexes) -> dict[str, Any]:
    v = nvdb.get(code, {})
    cat = category_for(code)
    name_nb = (v.get("beskrivelse") or "").strip()
    en = GUIDANCE_EN.get(code)
    name_en = en[0] if en else None
    meaning = en[1] if en else None
    if en:
        SIGN_EN[code] = en

    entry = {
        "code": code,
        "nvdb_enum_id": v.get("id"),
        "category": cat,
        "name_nb": name_nb,
        "name_en": name_en,
        "name_en_machine_translated": False,
        "meaning_en": meaning,
        "nvdb_value": v.get("verdi"),
        "legal_reference": legal_ref(code),
        "sort_order": v.get("sorteringsnummer"),
        "svg": None,
        "conversion_method": CONVERSION_NONE,
        "status": "no_source_found",
        "source_file": None,
        "source_attribution": {
            "license": "NLOD 2.0",
            "license_url": NLOD_URL,
            "attribution": (
                "Inneholder data under norsk lisens for offentlige data (NLOD) "
                "tilgjengeliggjort av Statens vegvesen / Kartverket (Geonorge)."
            ),
            "publishers": ["Statens vegvesen", "Kartverket / Geonorge", "NVDB"],
        },
        "color_codes": PMS_COLORS,
        "notes": [],
    }

    hit = resolve_sources(code, indexes)
    if hit is None:
        entry["notes"].append("No Geonorge SVG / EPS / JPG resolved.")
        return entry

    dest_dir = SVG_DIR / cat
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{safe_name(code)}.svg"
    try:
        rel_src = str(hit.path.relative_to(WORK_DIR))
    except ValueError:
        rel_src = str(hit.path)
    entry["source_file"] = rel_src

    try:
        if hit.method_hint == "geonorge":
            method = catalogue_geonorge_svg(hit.path, dest)
        elif hit.method_hint == "eps":
            method = convert_eps_to_svg(hit.path, dest)
        else:
            method = convert_jpg_to_svg(hit.path, dest)
            entry["notes"].append("Raster-traced; lower fidelity than EPS/SVG.")
        entry["svg"] = dest.relative_to(REPO_ROOT).as_posix()
        entry["conversion_method"] = method
        entry["status"] = "ok"
    except ConversionError as exc:
        entry["notes"].append(f"Conversion failed: {exc}")
        entry["status"] = "conversion_failed"
        if dest.exists():
            dest.unlink()
    return entry


def merge_into_db(new_entries: list[dict[str, Any]]) -> None:
    if DATABASE_PATH.exists():
        db = json.loads(DATABASE_PATH.read_text(encoding="utf-8"))
    else:
        db = {"meta": {}, "signs": []}

    by_code = {e["code"]: e for e in db.get("signs", [])}
    for e in new_entries:
        by_code[e["code"]] = e

    cat_order = {
        "fareskilt": 0,
        "speed_limit": 1,
        CATEGORY_SERVICE: 2,
        CATEGORY_VEGVISNING: 3,
    }
    signs = sorted(
        by_code.values(),
        key=lambda x: (cat_order.get(x.get("category"), 9), x["code"]),
    )

    for code, pair in GUIDANCE_EN.items():
        SIGN_EN[code] = pair

    db = build_database(signs)
    db["meta"]["title"] = "Norwegian traffic signs — SVG catalogue"
    db["meta"]["description"] = (
        "Machine-readable catalogue of Norwegian fareskilt, speed-limit-related signs, "
        "and selected serviceskilt / vegvisningssymboler with SVG graphics where available."
    )
    db["meta"]["packs_checked_empty_for_guidance_codes"] = [
        "markeringsskilt-eps.zip",
        "underskilt-eps.zip",
        "opplysningsskilt-eps.zip",
        "forbudsskilt-eps.zip",
        "vikeplikt-eps.zip",
    ]
    DATABASE_PATH.write_text(
        json.dumps(db, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    db_en = build_english_database(signs)
    for e in db_en["signs"]:
        if e["category"] == CATEGORY_SERVICE:
            e["category_label"] = "Service / tourist symbol"
        elif e["category"] == CATEGORY_VEGVISNING:
            e["category_label"] = "Direction / route symbol"
        if e["code"] in GUIDANCE_EN:
            e["name"], e["meaning"] = GUIDANCE_EN[e["code"]]
    en_path = DATABASE_DIR / "signs_en.json"
    en_path.write_text(
        json.dumps(db_en, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote {DATABASE_PATH}")
    print(f"Wrote {en_path}")
    print(json.dumps(db["meta"]["counts"], indent=2))


def main() -> int:
    nvdb = nvdb_map()
    missing_nvdb = [c for c in DEFINED_CODES if c not in nvdb]
    if missing_nvdb:
        print("WARN missing NVDB:", missing_nvdb)
    indexes = build_indexes()
    print({k: len(v) for k, v in indexes.items()})
    entries = []
    for i, code in enumerate(DEFINED_CODES, 1):
        print(f"[{i}/{len(DEFINED_CODES)}] {code}")
        entries.append(process_one(code, nvdb, indexes))
    merge_into_db(entries)
    ok = sum(1 for e in entries if e["status"] == "ok")
    methods = Counter(e["conversion_method"] for e in entries)
    print(f"guidance import done: {ok}/{len(entries)} ok; methods={dict(methods)}")
    failed = [e for e in entries if e["status"] != "ok"]
    for e in failed:
        print("FAIL", e["code"], e["status"], e.get("notes"))
    return 0 if ok == len(entries) else 1


if __name__ == "__main__":
    raise SystemExit(main())
