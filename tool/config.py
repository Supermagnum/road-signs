"""URLs, paths, and category definitions for the road-signs pipeline."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WORK_DIR = REPO_ROOT / "work"
SVG_DIR = REPO_ROOT / "svg"
DATABASE_DIR = REPO_ROOT / "database"
DATABASE_PATH = DATABASE_DIR / "signs.json"

NVDB_BASE = "https://nvdbapiles.atlas.vegvesen.no"
NVDB_SKILTPLATE_TYPE = 96
NVDB_SKILTNUMMER_EGENSKAP = 5530

GEONORGE_PACKAGE_UUID = "1e2f592a-1d69-45a3-9ce1-e55a64fe1dc3"
GEONORGE_PACKAGE_URL = (
    f"https://register.geonorge.no/symbol/symbolpackages/download/{GEONORGE_PACKAGE_UUID}"
)
GEONORGE_FILE_BASE = "https://register.geonorge.no/symbol/files/trafikkskilt"

VEGVESEN_FILES_PAGE = (
    "https://www.vegvesen.no/fag/veg-og-gate/trafikkskilt-og-vegoppmerking/"
    "filer-og-fargekoder-for-trafikkskilt/"
)
VEGVESEN_ASSET_BASE = (
    "https://www.vegvesen.no/globalassets/fag/veg-og-gate/trafikkskilt-og-vegoppmerking"
)

# Archives needed for fareskilt + speed-limit-related signs.
DOWNLOADS = {
    "fareskilt_eps": f"{VEGVESEN_ASSET_BASE}/fareskilt-eps.zip",
    "fareskilt_jpg": f"{VEGVESEN_ASSET_BASE}/fareskilt-jpg.zip",
    "forbudsskilt_eps": f"{VEGVESEN_ASSET_BASE}/forbudsskilt-eps.zip",
    "forbudsskilt_jpg": f"{VEGVESEN_ASSET_BASE}/forbudsskilt-jpg-png.zip",
    "opplysningsskilt_eps": f"{VEGVESEN_ASSET_BASE}/opplysningsskilt-eps.zip",
    "opplysningsskilt_jpg": f"{VEGVESEN_ASSET_BASE}/opplysningsskilt-jpg.zip",
    "underskilt_eps": f"{VEGVESEN_ASSET_BASE}/underskilt-eps.zip",
    "underskilt_jpg": f"{VEGVESEN_ASSET_BASE}/underskilt-jpg-og-png.zip",
    "geonorge": GEONORGE_PACKAGE_URL,
}

# Official PMS colour values used for Norwegian traffic signs
# (Statens vegvesen fargekoder overview).
PMS_COLORS = {
    "yellow": {"pms": "116", "hex": "#F7D117", "usage": "fareskilt background"},
    "red": {"pms": "485", "hex": "#DA291C", "usage": "border / forbud"},
    "blue": {"pms": "300", "hex": "#005EB8", "usage": "påbud / opplysning"},
    "green": {"pms": "340", "hex": "#009A44", "usage": "serviceskilt"},
    "orange": {"pms": "165", "hex": "#FF671F", "usage": "temporary / work"},
    "brown": {"pms": "469", "hex": "#693F23", "usage": "tourist"},
    "black": {"pms": "Black", "hex": "#000000", "usage": "symbols / text"},
    "white": {"pms": "White", "hex": "#FFFFFF", "usage": "background / symbols"},
}

SKILTFORSKRIFTEN_URL = "https://lovdata.no/dokument/SF/forskrift/2005-10-07-1219"
NLOD_URL = "https://data.norge.no/nlod/en/2.0"

HTTP_HEADERS = {
    "User-Agent": "road-signs-catalogue/1.0 (open NLOD reuse; github.com/Supermagnum/road-signs)",
    "X-Client": "road-signs-catalogue",
    "X-Kontaktperson": "https://github.com/Supermagnum/road-signs",
}

# Category keys used in the published database.
CATEGORY_FARESKILT = "fareskilt"
CATEGORY_SPEED_LIMIT = "speed_limit"

CONVERSION_GEONORGE = "geonorge_native"
CONVERSION_EPS = "eps_converted"
CONVERSION_JPG = "jpg_traced"
CONVERSION_NONE = "no_source_found"
