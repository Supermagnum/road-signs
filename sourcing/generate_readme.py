#!/usr/bin/env python3
"""Build sourcing/README.md from verified local indexes + NVDB cache."""
from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOWNLOADS = REPO / "work" / "downloads"
GEO_ROOT = REPO / "work" / "unpacked" / "geonorge"
NVDB_CACHE = REPO / "work" / "nvdb_skiltnummer.json"

GEONORGE_PKG = (
    "https://register.geonorge.no/symbol/symbolpackages/download/"
    "1e2f592a-1d69-45a3-9ce1-e55a64fe1dc3"
)
GEONORGE_DIRECT = "https://register.geonorge.no/symbol/files/trafikkskilt/{key}.svg"
VEGVESEN_PAGE = (
    "https://www.vegvesen.no/fag/veg-og-gate/trafikkskilt-og-vegoppmerking/"
    "filer-og-fargekoder-for-trafikkskilt/"
)
LOVDATA = "https://lovdata.no/dokument/SF/forskrift/2005-10-07-1219"
ASSET = "https://www.vegvesen.no/globalassets/fag/veg-og-gate/trafikkskilt-og-vegoppmerking"
ZIP_URLS = {
    "serviceskilt-eps.zip": f"{ASSET}/serviceskilt-eps.zip",
    "serviceskilt-jpg.zip": f"{ASSET}/serviceskilt-jpg.zip",
    "vegvisningsskilt-eps.zip": f"{ASSET}/vegvisningsskilt-eps.zip",
    "vegvisningsskilt-jpg.zip": f"{ASSET}/vegvisningsskilt-jpg.zip",
}

DEFINED_CODES = [
    "640.10", "640.12", "640.20", "640.30", "640.101", "640.102",
    "650.10", "650.11", "650.20", "650.21", "650.22", "650.40", "650.41",
    "723.31", "723.41", "723.51", "723.61", "723.62", "723.63", "723.64",
    "723.65", "723.66", "723.71", "723.72", "723.73",
    "755", "761", "763", "765", "767", "769", "771", "772", "773", "774",
    "775", "776", "780",
    "790.10", "790.15", "790.16", "790.20", "790.30", "790.31", "790.32", "790.40",
]

CONFLICTS = {
    "640.30": (
        "NVDB/Lovdata: «Naturvernområde»; older N300 Del 5 mirror text uses "
        "«Naturfredet område» for the same code family."
    ),
    "650.40": (
        "NVDB: «Gardsmat/Bygdeturisme»; Lovdata snippets: «Gardsmat/bygdeturisme» "
        "(capitalisation only)."
    ),
    "723.71": (
        "NVDB: «Kryssnummer for motorveg»; Lovdata groups 723.71–72 under "
        "«Kryssnummer på flerfeltsveg»."
    ),
    "723.72": (
        "NVDB: «Kryssnummer for annen flerfeltsveg med planskilte kryss»; Lovdata "
        "groups 723.71–72 under «Kryssnummer på flerfeltsveg»."
    ),
}


def candidates(code: str) -> list[str]:
    k = code.replace(".", "_").lower()
    return [k, f"{k}_0"]


def index_geonorge() -> dict[str, str]:
    """Prefer zip-relative member paths (portable in published docs)."""
    idx: dict[str, str] = {}
    zpath = DOWNLOADS / "geonorge-trafikkskilt.zip"
    if not zpath.exists():
        return idx
    with zipfile.ZipFile(zpath) as zf:
        for name in zf.namelist():
            if not name.lower().endswith(".svg"):
                continue
            parts = name.strip("/").split("/")
            code = None
            for part in parts:
                m = re.match(r"^(\d+[A-Za-z]?(?:[_.][\w]+)*)$", part)
                if m:
                    code = m.group(1).replace(".", "_").lower()
                    break
                m = re.match(r"^(\d+[A-Za-z]?(?:[_.][\w]+)?)", part)
                if m and re.match(r"^\d+", part):
                    code = m.group(1).replace(".", "_").lower()
                    break
            if code:
                prev = idx.get(code)
                if prev is None or len(name) < len(prev):
                    idx[code] = name
    return idx


def index_zip(zip_name: str) -> dict[str, str]:
    zpath = DOWNLOADS / zip_name
    idx: dict[str, str] = {}
    if not zpath.exists():
        return idx
    with zipfile.ZipFile(zpath) as zf:
        for name in zf.namelist():
            if name.endswith("/"):
                continue
            bn = Path(name).name
            stem = Path(bn).stem
            m = re.match(r"^(\d+[A-Za-z]?(?:[_.]\w+)?)", stem, re.I)
            if not m:
                m = re.match(r"^(\d+)", stem)
                if not m:
                    continue
                key = m.group(1).lower()
            else:
                key = m.group(1).replace(".", "_").lower()
            prev = idx.get(key)
            if prev is None or len(bn) < len(Path(prev).name):
                idx[key] = name
    return idx


def resolve(code: str, index: dict[str, str]):
    for c in candidates(code):
        if c in index:
            return c, index[c]
    for c in candidates(code):
        for key, path in index.items():
            if key == c or key.startswith(c + "_"):
                return key, path
    return None


def nvdb_names() -> dict[str, str]:
    vals = json.loads(NVDB_CACHE.read_text(encoding="utf-8"))
    out = {}
    for v in vals:
        kn = v.get("kortnavn") or ""
        if kn in DEFINED_CODES:
            out[kn] = (v.get("beskrivelse") or "").strip().rstrip(".")
    return out


def main() -> None:
    geo = index_geonorge()
    svc_eps = index_zip("serviceskilt-eps.zip")
    svc_jpg = index_zip("serviceskilt-jpg.zip")
    veg_eps = index_zip("vegvisningsskilt-eps.zip")
    veg_jpg = index_zip("vegvisningsskilt-jpg.zip")
    names = nvdb_names()
    if not names:
        raise SystemExit("NVDB cache missing")
    if not geo:
        raise SystemExit("Geonorge index empty")
    if not svc_eps or not veg_eps:
        raise SystemExit("vegvesen zips missing")

    table_lines = []
    not_located = []

    for code in DEFINED_CODES:
        desc = names.get(code, "(description not found in NVDB enum)")
        g = resolve(code, geo)
        n = int(re.match(r"(\d+)", code).group(1))
        if n in (640, 650):
            e = resolve(code, svc_eps)
            j = resolve(code, svc_jpg)
            pack_eps, pack_jpg = "serviceskilt-eps.zip", "serviceskilt-jpg.zip"
        else:
            e = resolve(code, veg_eps)
            j = resolve(code, veg_jpg)
            pack_eps, pack_jpg = "vegvisningsskilt-eps.zip", "vegvisningsskilt-jpg.zip"

        formats = []
        sources = []
        if g:
            formats.append("SVG")
            gkey, gpath = g
            sources.append(
                f"Geonorge Trafikkskilt package member `{gpath}` "
                f"(key `{gkey}`; package [download]({GEONORGE_PKG}); "
                f"[direct SVG]({GEONORGE_DIRECT.format(key=gkey)}))"
            )
        if e:
            formats.append("EPS")
            sources.append(
                f"vegvesen [{pack_eps}]({ZIP_URLS[pack_eps]}) → `{e[1]}`"
            )
        if j:
            formats.append("JPG")
            sources.append(
                f"vegvesen [{pack_jpg}]({ZIP_URLS[pack_jpg]}) → `{j[1]}`"
            )

        if sources:
            vector = "Yes" if ("SVG" in formats or "EPS" in formats) else "No"
            source_cell = "; ".join(sources)
            if "SVG" in formats:
                action = "None — prefer Geonorge SVG."
            elif "EPS" in formats:
                action = (
                    "Convert EPS→SVG (Inkscape or Ghostscript+pdftocairo). "
                    "Prefer EPS over JPG."
                )
            else:
                action = (
                    "Only JPG found — lower fidelity; locate EPS/SVG before "
                    "production use."
                )
            if code == "723.31" and "EPS" not in formats and "SVG" in formats:
                action = (
                    "Prefer Geonorge SVG. EPS member not present in current "
                    f"`{pack_eps}` listing (JPG is present)."
                )
            if code == "790.40" and "JPG" not in formats and "EPS" in formats:
                action = (
                    "Convert EPS→SVG. JPG member not present in current "
                    f"`{pack_jpg}` listing."
                )
            if code in CONFLICTS:
                action = f"CONFLICT: {CONFLICTS[code]} {action}"
        else:
            vector = "No"
            source_cell = (
                "NOT LOCATED in Geonorge package or vegvesen "
                "serviceskilt/vegvisningsskilt EPS/JPG archives"
            )
            action = (
                "Contact Vegdirektoratet (skiltnormaler) for reference artwork. "
                "Do not invent a design."
            )
            not_located.append(code)

        fmt_cell = ", ".join(formats) if formats else "—"
        table_lines.append(
            f"| `{code}` | {desc} | {vector} | {source_cell} | {fmt_cell} | {action} |"
        )

    vector_yes = sum(1 for line in table_lines if "| Yes |" in line)

    lines = []
    a = lines.append
    a("# Sourcing status — selected Norwegian traffic sign codes")
    a("")
    a(
        "Audit of official / semi-official **graphic** sources for a specific set of "
        "skiltnummer codes (serviceskilt / vegvisningssymboler). This document records "
        "**where** each graphic was found and in **what format**. It does **not** "
        "reproduce or embed the artwork."
    )
    a("")
    a(
        f"Legal definitions: [skiltforskriften FOR-2005-10-07-1219]({LOVDATA}). "
        "Metadata cross-check: NVDB API Les v4 `vegobjekttyper/96` → egenskap `5530` "
        "Skiltnummer. Descriptions in the table are from **NVDB** (authoritative "
        "machine-readable names)."
    )
    a("")
    a("## Sources checked (priority order)")
    a("")
    a("| # | Source | Role | Access used in this audit |")
    a("|---|--------|------|---------------------------|")
    a(
        f"| 1 | [Statens vegvesen filer og fargekoder]({VEGVESEN_PAGE}) | "
        "Official EPS/JPG production files | Downloaded `serviceskilt-eps.zip`, "
        "`serviceskilt-jpg.zip`, `vegvisningsskilt-eps.zip`, "
        "`vegvisningsskilt-jpg.zip` and indexed member filenames |"
    )
    a(
        "| 2 | [Geonorge Trafikkskilt symbol package]"
        "(https://register.geonorge.no/symbol/symbolpackages/details/"
        "1e2f592a-1d69-45a3-9ce1-e55a64fe1dc3) | Official SVG (Statens vegvesen) | "
        "Indexed local unpack / package zip; confirmed missing codes via HTTP check "
        "on direct SVG URLs |"
    )
    a(
        "| 3 | [NVDB trafikkskilt dataset]"
        "(https://dataut.vegvesen.no/dataset/trafikkskilt) | Metadata only "
        "(no graphics) | Skiltnummer enum from API Les v4 |"
    )
    a(
        "| 4 | Lovdata regulation text | Legal listing / optional low-res GIF "
        "illustrations | **No bulk fetch** (robots.txt). Code existence and headings "
        "confirmed via web-search snippets only |"
    )
    a(
        "| 5 | [Trafikksiden skiltforskriften mirror]"
        "(https://trafikksiden.motocross.io/regelverk/Skiltforskriften.html) | "
        "Non-authoritative locator | Secondary cross-check via search hits / N300 "
        "mirrors — not a graphic source of truth |"
    )
    a("")
    a("## Important: ranges vs defined codes")
    a("")
    a(
        "Prompt phrasing «640.10 through 640.102» does **not** match a contiguous "
        "code list. Skiltforskriften/NVDB only define discrete codes "
        "`640.10`, `640.12`, `640.20`, `640.30`, `640.101`, `640.102`. Intermediate "
        "numbers (e.g. `640.11`, `640.13`–`640.19`, `640.21`–`640.29`, "
        "`640.31`–`640.100`) are **not defined sign codes**."
    )
    a("")
    a(
        "Likewise, «650.10 through 650.41» only covers discrete codes "
        "`650.10`, `650.11`, `650.20`, `650.21`, `650.22`, `650.40`, `650.41`."
    )
    a("")
    a(
        "For **790**, Lovdata/NVDB list: `790.10`, `790.15`, `790.16`, `790.20`, "
        "`790.30`, `790.31`, `790.32`, `790.40` (not an open continuum beyond those)."
    )
    a("")
    a(
        "Undefined intermediate numbers are **not** listed as «NOT LOCATED artwork» — "
        "they are simply not defined codes in the regulation."
    )
    a("")
    a("## Sourcing table")
    a("")
    a(
        "| Sign code | Description (NO) | Found in vector source? | "
        "Source & path | Format | Manual action needed |"
    )
    a("|---|---|---|---|---|---|")
    lines.extend(table_lines)
    a("")
    a("## Summary")
    a("")
    a("| Result | Count |")
    a("|--------|------:|")
    a(f"| Defined codes in scope | {len(DEFINED_CODES)} |")
    a(f"| With vector graphic (SVG and/or EPS) | {vector_yes} |")
    a(f"| Graphics NOT LOCATED in sources #1/#2 | {len(not_located)} |")
    a("")
    a("### Codes present in vegvesen EPS but missing from Geonorge SVG")
    a("")
    a(
        "Verified absent from Geonorge package / direct SVG URL (HTTP 404) while "
        "present as EPS in vegvesen packs:"
    )
    a("")
    a("- `650.10`, `650.22` — in `serviceskilt-eps.zip`")
    a("- `769`, `780`, `790.16`, `790.40` — in `vegvisningsskilt-eps.zip`")
    a("")
    a("### Notable pack gaps (still have a vector elsewhere)")
    a("")
    a(
        "- `723.31` — Geonorge **SVG** yes; **EPS** not in current "
        "`vegvisningsskilt-eps.zip`; JPG yes."
    )
    a(
        "- `790.40` — vegvesen **EPS** yes; **JPG** not in current "
        "`vegvisningsskilt-jpg.zip`; Geonorge SVG no."
    )
    a("")
    a("## Codes not found in any official source")
    a("")
    if not_located:
        a(
            "The following defined codes had **no** Geonorge SVG and **no** matching "
            "member in the vegvesen serviceskilt/vegvisningsskilt EPS/JPG archives:"
        )
        a("")
        for c in not_located:
            a(f"- `{c}`")
        a("")
        a("### Searches already tried")
        a("")
        a("For each missing code:")
        a("")
        a(
            "1. Geonorge package index + direct URL "
            "`https://register.geonorge.no/symbol/files/trafikkskilt/{CODE}.svg` "
            "(and `{CODE}_0.svg` where applicable)"
        )
        a(
            "2. Member filename scan of `serviceskilt-eps.zip`, `serviceskilt-jpg.zip`, "
            "`vegvisningsskilt-eps.zip`, `vegvisningsskilt-jpg.zip`"
        )
        a("3. NVDB Skiltnummer enum confirmation that the code exists as metadata")
        a(
            "4. Web search snippets for Lovdata listing "
            "(no automated Lovdata download)"
        )
        a("")
        a("### Recommendation")
        a("")
        a(
            "Contact **Statens vegvesen, Vegdirektoratet (skiltnormaler)** for "
            "reference artwork. Some newer or rarely used codes may not yet be "
            "digitized in the public file packs."
        )
    else:
        a(
            "**None.** Every code that is actually defined in skiltforskriften/NVDB "
            "for this request was located in at least one official vector source "
            "(Geonorge SVG and/or Statens vegvesen EPS)."
        )
        a("")
        a(
            "No Lovdata-only GIF fallback was required for graphics location. Lovdata "
            "was used only (via search snippets) to confirm legal listings and to flag "
            "description/grouping conflicts noted in the table."
        )
    a("")
    a("## How to regenerate this audit")
    a("")
    a("```bash")
    a("python3 sourcing/generate_readme.py")
    a("```")
    a("")
    a(f"Primary download page: {VEGVESEN_PAGE}")
    a("")
    a(f"Geonorge package: {GEONORGE_PKG}")
    a("")

    out = Path(__file__).resolve().parent / "README.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out} ({out.stat().st_size} bytes)")
    print(f"not_located={not_located}")
    print(f"vector_yes={vector_yes}/{len(DEFINED_CODES)}")


if __name__ == "__main__":
    main()
