"""End-to-end pipeline: download, convert, build JSON database."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import (
    CATEGORY_FARESKILT,
    CATEGORY_SPEED_LIMIT,
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
from .download import download_all
from .nvdb import load_or_fetch_in_scope
from .meanings_en import english_for
from .sources import build_source_indexes, resolve_sources


def _safe_filename(code: str) -> str:
    return code.replace(".", "_").replace("/", "_")


def _category_dir(category: str) -> Path:
    if category == CATEGORY_FARESKILT:
        return SVG_DIR / "fareskilt"
    if category == CATEGORY_SPEED_LIMIT:
        return SVG_DIR / "speed_limit"
    return SVG_DIR / "other"


def process_sign(sign: dict[str, Any], indexes: dict) -> dict[str, Any]:
    code = sign["code"]
    category = sign["category"]
    hit = resolve_sources(code, indexes)
    entry = {
        **sign,
        "svg": None,
        "conversion_method": CONVERSION_NONE,
        "status": "no_source_found",
        "source_file": None,
        "source_attribution": {
            "license": "NLOD 2.0",
            "license_url": NLOD_URL,
            "attribution": "Inneholder data under norsk lisens for offentlige data (NLOD) tilgjengeliggjort av Statens vegvesen / Kartverket (Geonorge).",
            "publishers": ["Statens vegvesen", "Kartverket / Geonorge", "NVDB"],
        },
        "color_codes": PMS_COLORS,
        "notes": [],
    }

    if hit is None:
        entry["notes"].append(
            "No Geonorge SVG, EPS, or JPG/PNG graphic could be resolved for this code."
        )
        return entry

    dest_dir = _category_dir(category)
    dest = dest_dir / f"{_safe_filename(code)}.svg"
    entry["source_file"] = str(hit.path.relative_to(WORK_DIR)) if hit.path.is_relative_to(WORK_DIR) else str(hit.path)

    try:
        if hit.method_hint == "geonorge":
            method = catalogue_geonorge_svg(hit.path, dest)
        elif hit.method_hint == "eps":
            method = convert_eps_to_svg(hit.path, dest)
        else:
            method = convert_jpg_to_svg(hit.path, dest)
            entry["notes"].append(
                "Raster-to-vector tracing was used; fidelity is lower than native vector sources."
            )
        rel = dest.relative_to(REPO_ROOT).as_posix()
        entry["svg"] = rel
        entry["conversion_method"] = method
        entry["status"] = "ok"
    except ConversionError as exc:
        entry["notes"].append(f"Conversion failed: {exc}")
        entry["status"] = "conversion_failed"
        entry["conversion_method"] = CONVERSION_NONE
        if dest.exists():
            dest.unlink()
    return entry



def build_english_database(entries: list[dict[str, Any]]) -> dict[str, Any]:
    """English-primary companion database for easier reuse outside Norway."""
    signs_en: list[dict[str, Any]] = []
    for e in entries:
        name_en, meaning = english_for(e["code"])
        signs_en.append(
            {
                "code": e["code"],
                "category": e["category"],
                "category_label": (
                    "Warning sign" if e["category"] == CATEGORY_FARESKILT else "Speed limit / related"
                ),
                "name": name_en or e.get("name_en") or e.get("name_nb"),
                "name_nb": e.get("name_nb"),
                "meaning": meaning or e.get("meaning_en") or e.get("name_en") or e.get("name_nb"),
                "legal_reference": e.get("legal_reference"),
                "svg": e.get("svg"),
                "conversion_method": e.get("conversion_method"),
                "status": e.get("status"),
                "notes": e.get("notes") or [],
                "nvdb_enum_id": e.get("nvdb_enum_id"),
                "source_attribution": e.get("source_attribution"),
                "color_codes": e.get("color_codes"),
            }
        )
    bilingual = build_database(entries)
    return {
        "meta": {
            "title": "Norwegian traffic signs — English catalogue",
            "language": "en",
            "description": (
                "English-primary catalogue of Norwegian warning signs (fareskilt) and "
                "speed-limit-related signs. Names and meanings are in English; official "
                "Norwegian NVDB wording is retained in name_nb."
            ),
            "generated_at": bilingual["meta"]["generated_at"],
            "license": bilingual["meta"]["license"],
            "license_url": bilingual["meta"]["license_url"],
            "companion_database": "database/signs.json",
            "sources": bilingual["meta"]["sources"],
            "counts": bilingual["meta"]["counts"],
            "gaps": bilingual["meta"].get("gaps"),
            "schema": {
                "code": "Official Norwegian skiltnummer",
                "category": "fareskilt | speed_limit",
                "category_label": "Human-readable category in English",
                "name": "English sign name",
                "name_nb": "Official Norwegian name from NVDB",
                "meaning": "Plain-English explanation of what the sign means",
                "legal_reference": "Skiltforskriften reference",
                "svg": "Relative SVG path, or null if unresolved",
                "conversion_method": "geonorge_native | eps_converted | jpg_traced | no_source_found",
                "status": "ok | no_source_found | conversion_failed",
            },
        },
        "signs": signs_en,
    }


def build_database(entries: list[dict[str, Any]], meta_extra: dict[str, Any] | None = None) -> dict[str, Any]:
    by_cat = Counter(e["category"] for e in entries)
    by_method = Counter(e["conversion_method"] for e in entries)
    by_status = Counter(e["status"] for e in entries)
    db = {
        "meta": {
            "title": "Norwegian traffic signs — SVG catalogue",
            "description": (
                "Machine-readable catalogue of Norwegian fareskilt (warning signs) "
                "and speed-limit-related signs with SVG graphics where available."
            ),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "license": "NLOD 2.0",
            "license_url": NLOD_URL,
            "sources": {
                "nvdb": "https://nvdbapiles.atlas.vegvesen.no/ (vegobjekttype 96 Skiltnummer)",
                "vegvesen_files": (
                    "https://www.vegvesen.no/fag/veg-og-gate/trafikkskilt-og-vegoppmerking/"
                    "filer-og-fargekoder-for-trafikkskilt/"
                ),
                "geonorge": (
                    "https://register.geonorge.no/symbol/symbolpackages/details/"
                    "1e2f592a-1d69-45a3-9ce1-e55a64fe1dc3"
                ),
                "skiltforskriften": "https://lovdata.no/dokument/SF/forskrift/2005-10-07-1219",
            },
            "counts": {
                "total": len(entries),
                "by_category": dict(by_cat),
                "by_conversion_method": dict(by_method),
                "by_status": dict(by_status),
            },
            "schema": {
                "code": "Official skiltnummer (NVDB kortnavn)",
                "category": "fareskilt | speed_limit",
                "name_nb": "Official Norwegian description from NVDB",
                "name_en": "English gloss when available (null otherwise)",
                "name_en_machine_translated": "True only if English was machine-translated",
                "legal_reference": "Skiltforskriften URL with series hint",
                "svg": "Relative path to SVG in this repository, or null",
                "conversion_method": (
                    "geonorge_native | eps_converted | jpg_traced | no_source_found"
                ),
                "status": "ok | no_source_found | conversion_failed",
                "source_attribution": "NLOD attribution block",
                "color_codes": "Official PMS values used for traffic signs",
            },
        },
        "signs": entries,
    }
    if meta_extra:
        db["meta"].update(meta_extra)
    return db


def run(skip_download: bool = False, force_download: bool = False) -> dict[str, Any]:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    for sub in (CATEGORY_FARESKILT, CATEGORY_SPEED_LIMIT):
        (SVG_DIR / sub).mkdir(parents=True, exist_ok=True)

    print("== NVDB metadata ==")
    signs = load_or_fetch_in_scope()
    fare_n = sum(1 for s in signs if s["category"] == CATEGORY_FARESKILT)
    speed_n = sum(1 for s in signs if s["category"] == CATEGORY_SPEED_LIMIT)
    print(f"  in-scope signs: {len(signs)} (fareskilt={fare_n}, speed_limit={speed_n})")

    if skip_download:
        unpacked = {
            k: WORK_DIR / "unpacked" / k
            for k in (
                "geonorge",
                "fareskilt_eps",
                "fareskilt_jpg",
                "forbudsskilt_eps",
                "forbudsskilt_jpg",
                "opplysningsskilt_eps",
                "opplysningsskilt_jpg",
                "underskilt_eps",
                "underskilt_jpg",
            )
        }
        print("== Skipping download (using existing work/unpacked) ==")
    else:
        print("== Downloading source archives ==")
        unpacked = download_all(force=force_download)

    print("== Indexing sources ==")
    indexes = build_source_indexes(unpacked)
    for kind, idx in indexes.items():
        print(f"  {kind}: {len(idx)} files")

    print("== Converting / cataloguing ==")
    entries: list[dict[str, Any]] = []
    for i, sign in enumerate(signs, 1):
        print(f"  [{i}/{len(signs)}] {sign['code']} ({sign['category']})")
        entries.append(process_sign(sign, indexes))

    for entry in entries:
        _name, meaning = english_for(entry["code"])
        entry["meaning_en"] = meaning or entry.get("name_en")

    db = build_database(entries)
    db_en = build_english_database(entries)
    en_path = DATABASE_DIR / "signs_en.json"
    en_path.write_text(json.dumps(db_en, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"== Wrote {en_path} ==")
    DATABASE_PATH.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"== Wrote {DATABASE_PATH} ==")
    print(json.dumps(db["meta"]["counts"], ensure_ascii=False, indent=2))
    return db


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build Norwegian traffic sign SVG catalogue and JSON database"
    )
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Reuse already unpacked archives under work/",
    )
    parser.add_argument(
        "--force-download",
        action="store_true",
        help="Re-download archives even if cached",
    )
    args = parser.parse_args(argv)
    try:
        run(skip_download=args.skip_download, force_download=args.force_download)
    except KeyboardInterrupt:
        print("Interrupted", file=sys.stderr)
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
