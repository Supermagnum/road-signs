"""Download and unpack Statens vegvesen and Geonorge source archives."""

from __future__ import annotations

import zipfile
from pathlib import Path

import requests

from .config import DOWNLOADS, HTTP_HEADERS, WORK_DIR


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update(HTTP_HEADERS)
    return s


def download_file(url: str, dest: Path, force: bool = False) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0 and not force:
        print(f"  cached: {dest.name} ({dest.stat().st_size} bytes)")
        return dest
    print(f"  downloading: {url}")
    with _session().get(url, stream=True, timeout=600) as resp:
        resp.raise_for_status()
        tmp = dest.with_suffix(dest.suffix + ".part")
        with tmp.open("wb") as fh:
            for chunk in resp.iter_content(chunk_size=1024 * 256):
                if chunk:
                    fh.write(chunk)
        tmp.replace(dest)
    print(f"  saved: {dest.name} ({dest.stat().st_size} bytes)")
    return dest


def unpack_zip(zip_path: Path, dest_dir: Path, force: bool = False) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    marker = dest_dir / ".unpacked"
    if marker.exists() and not force:
        print(f"  already unpacked: {dest_dir.name}")
        return dest_dir
    print(f"  unpacking: {zip_path.name} -> {dest_dir}")
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(dest_dir)
    marker.write_text(zip_path.name, encoding="utf-8")
    return dest_dir


def download_all(force: bool = False) -> dict[str, Path]:
    """Download all configured archives into work/downloads and unpack them."""
    downloads_dir = WORK_DIR / "downloads"
    unpacked_dir = WORK_DIR / "unpacked"
    downloads_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}

    for key, url in DOWNLOADS.items():
        filename = url.rstrip("/").split("/")[-1].split("?")[0]
        if key == "geonorge":
            filename = "geonorge-trafikkskilt.zip"
        zip_path = downloads_dir / filename
        download_file(url, zip_path, force=force)
        dest = unpacked_dir / key
        unpack_zip(zip_path, dest, force=force)
        paths[key] = dest
    return paths
