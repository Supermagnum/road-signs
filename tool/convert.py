"""Convert source graphics to validated SVG files."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from .config import CONVERSION_EPS, CONVERSION_GEONORGE, CONVERSION_JPG


class ConversionError(RuntimeError):
    pass


def validate_svg(path: Path) -> None:
    """Basic XML + root-element check. Raises ConversionError on failure."""
    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        raise ConversionError(f"SVG XML parse failed for {path}: {exc}") from exc
    root = tree.getroot()
    tag = root.tag.lower()
    if not (tag == "svg" or tag.endswith("}svg")):
        raise ConversionError(f"Root element is not svg in {path}: {root.tag}")
    text = path.read_text(encoding="utf-8", errors="replace")
    if "<svg" not in text.lower():
        raise ConversionError(f"No <svg> marker in {path}")


def _which(*names: str) -> str | None:
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    return None


def convert_eps_to_svg(eps_path: Path, svg_path: Path) -> str:
    """Convert EPS to SVG.

    Prefers Inkscape CLI when available. Falls back to Ghostscript (EPS->PDF)
    + pdftocairo (PDF->SVG), which preserves vector data without re-tracing.
    """
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    inkscape = _which("inkscape")
    if inkscape:
        cmd = [inkscape, str(eps_path), "-o", str(svg_path)]
        # Older Inkscape used -l / --export-plain-svg
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            cmd = [
                inkscape,
                str(eps_path),
                "--export-type=svg",
                f"--export-filename={svg_path}",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0 or not svg_path.exists():
            raise ConversionError(
                f"Inkscape failed for {eps_path}: {result.stderr or result.stdout}"
            )
        validate_svg(svg_path)
        return CONVERSION_EPS

    gs = _which("gs")
    pdftocairo = _which("pdftocairo")
    if not gs or not pdftocairo:
        raise ConversionError(
            "Neither Inkscape nor (gs + pdftocairo) available for EPS conversion"
        )

    with tempfile.TemporaryDirectory(prefix="eps2svg-") as tmp:
        pdf_path = Path(tmp) / "sign.pdf"
        gs_cmd = [
            gs,
            "-dSAFER",
            "-dBATCH",
            "-dNOPAUSE",
            "-dEPSCrop",
            "-sDEVICE=pdfwrite",
            f"-sOutputFile={pdf_path}",
            str(eps_path),
        ]
        result = subprocess.run(gs_cmd, capture_output=True, text=True)
        if result.returncode != 0 or not pdf_path.exists():
            raise ConversionError(
                f"Ghostscript EPS->PDF failed for {eps_path}: {result.stderr}"
            )
        produced = Path(tmp) / "sign.svg"
        cairo_cmd = ["pdftocairo", "-svg", str(pdf_path), str(produced)]
        result = subprocess.run(cairo_cmd, capture_output=True, text=True)
        if not produced.exists():
            # Some pdftocairo builds write the basename without forcing .svg
            candidates = sorted(Path(tmp).glob("sign*"))
            candidates = [c for c in candidates if c.is_file() and c.suffix != ".pdf"]
            if not candidates:
                raise ConversionError(
                    f"pdftocairo produced no SVG for {eps_path}: "
                    f"rc={result.returncode} stderr={result.stderr!r} stdout={result.stdout!r}"
                )
            produced = candidates[0]
        shutil.copy2(produced, svg_path)

    validate_svg(svg_path)
    return CONVERSION_EPS


def convert_jpg_to_svg(raster_path: Path, svg_path: Path) -> str:
    """Trace raster JPG/PNG to SVG via vtracer (lower fidelity than vector EPS)."""
    try:
        import vtracer
    except ImportError as exc:
        raise ConversionError("vtracer is required for JPG tracing") from exc

    svg_path.parent.mkdir(parents=True, exist_ok=True)
    vtracer.convert_image_to_svg_py(
        str(raster_path),
        str(svg_path),
        colormode="color",
        hierarchical="stacked",
        mode="spline",
        filter_speckle=4,
        color_precision=6,
        layer_difference=16,
        corner_threshold=60,
        length_threshold=4.0,
        max_iterations=10,
        splice_threshold=45,
        path_precision=3,
    )
    if not svg_path.exists():
        raise ConversionError(f"vtracer produced no output for {raster_path}")
    validate_svg(svg_path)
    return CONVERSION_JPG


def catalogue_geonorge_svg(src: Path, dest: Path) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    validate_svg(dest)
    return CONVERSION_GEONORGE
