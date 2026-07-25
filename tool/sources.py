"""Index Geonorge SVG / EPS / raster files and resolve them by sign code."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SourceHit:
    method_hint: str  # geonorge | eps | jpg
    path: Path
    key: str


def _norm_key(text: str) -> str:
    text = text.strip().lower().replace(".", "_").replace("-", "_").replace(" ", "_")
    text = re.sub(r"_+", "_", text)
    return text


def _code_from_filename(name: str) -> str | None:
    """Extract a sign-code-like key from a filename stem."""
    stem = Path(name).stem
    # Patterns: 362_30, 100_1, 151 Militar aktivitet, 367 Fartsgrensesone...
    m = re.match(
        r"^(\d+[a-z]?(?:[_.]\w+)?)",
        stem,
        flags=re.IGNORECASE,
    )
    if not m:
        return None
    return _norm_key(m.group(1))


def candidates_for_code(code: str) -> list[str]:
    """Generate possible source keys for an NVDB kortnavn."""
    k = _norm_key(code)
    cands = [k, f"{k}_0"]

    # 136.1h / 136.1v share the base graphic 136_1
    m = re.match(r"^(\d+_\d+)([hv])$", k)
    if m:
        base = m.group(1)
        cands.extend([base, f"{base}_0", f"{base}{m.group(2)}"])

    # EPS legacy: 362_3 means 30 km/h (NVDB 362.30)
    m = re.match(r"^(\d+)_(\d+)$", k)
    if m:
        base, rest = m.group(1), m.group(2)
        if len(rest) == 2 and rest.endswith("0") and rest != "00":
            cands.append(f"{base}_{rest[0]}")
        if len(rest) == 1:
            cands.append(f"{base}_{rest}0")

    if "_" not in k:
        cands.append(f"{k}_0")

    # Preserve order, unique
    seen: set[str] = set()
    out: list[str] = []
    for c in cands:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def index_geonorge(root: Path) -> dict[str, Path]:
    index: dict[str, Path] = {}
    if not root.exists():
        return index
    root = root.resolve()
    for path in root.rglob("*.svg"):
        # Only inspect path segments under root — never the absolute prefix
        # (which may contain digits, e.g. a disk UUID).
        try:
            rel_parts = path.resolve().relative_to(root).parts
        except ValueError:
            rel_parts = path.parts
        code = None
        for part in rel_parts:
            m = re.match(r"^(\d+[A-Za-z]?(?:[_.][\w]+)*)$", part)
            if m:
                code = _norm_key(m.group(1))
                break
            m = re.match(r"^(\d+[A-Za-z]?(?:[_.][\w]+)?)", part)
            if m and re.match(r"^\d+", part):
                code = _norm_key(m.group(1))
                break
        if code is None:
            code = _code_from_filename(path.name)
        if not code:
            continue
        prev = index.get(code)
        if prev is None or len(str(path)) < len(str(prev)):
            index[code] = path
    return index


def index_by_extension(roots: list[Path], extensions: tuple[str, ...]) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in extensions:
                continue
            code = _code_from_filename(path.name)
            if not code:
                # Fuzzy: "151 Militar aktivitet.eps"
                m = re.match(r"^(\d+)", path.stem.strip(), flags=re.IGNORECASE)
                if m:
                    code = _norm_key(m.group(1))
                else:
                    continue
            # Prefer exact code filenames over descriptive ones when equal keys collide
            prev = index.get(code)
            if prev is None:
                index[code] = path
            else:
                # Prefer shorter stem (usually the clean code form)
                if len(path.stem) < len(prev.stem):
                    index[code] = path
    return index


def build_source_indexes(unpacked: dict[str, Path]) -> dict[str, dict[str, Path]]:
    geonorge = index_geonorge(unpacked.get("geonorge", Path(".")))
    eps_roots = [
        unpacked[k]
        for k in (
            "fareskilt_eps",
            "forbudsskilt_eps",
            "opplysningsskilt_eps",
            "underskilt_eps",
        )
        if k in unpacked
    ]
    jpg_roots = [
        unpacked[k]
        for k in (
            "fareskilt_jpg",
            "forbudsskilt_jpg",
            "opplysningsskilt_jpg",
            "underskilt_jpg",
        )
        if k in unpacked
    ]
    return {
        "geonorge": geonorge,
        "eps": index_by_extension(eps_roots, (".eps",)),
        "jpg": index_by_extension(jpg_roots, (".jpg", ".jpeg", ".png")),
    }


def resolve_sources(code: str, indexes: dict[str, dict[str, Path]]) -> SourceHit | None:
    """Prefer Geonorge SVG, then EPS, then JPG/PNG."""
    for method, index_key in (
        ("geonorge", "geonorge"),
        ("eps", "eps"),
        ("jpg", "jpg"),
    ):
        index = indexes[index_key]
        for cand in candidates_for_code(code):
            if cand in index:
                return SourceHit(method_hint=method, path=index[cand], key=cand)
        # Prefix fallback for fuzzy names like 151_militar...
        for cand in candidates_for_code(code):
            for key, path in index.items():
                if key == cand or key.startswith(cand + "_"):
                    return SourceHit(method_hint=method, path=path, key=key)
    return None
