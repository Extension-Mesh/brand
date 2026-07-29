from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
RASTER = BUILD / "raster"
PACKAGE = BUILD / "package" / "extensionmesh-assets-v0.1"
DIST = ROOT / "dist"


def require_inside_root(path: Path) -> None:
    if ROOT not in path.resolve().parents:
        raise RuntimeError(f"Refusing generated path outside repository: {path}")


def fresh_directory(path: Path) -> None:
    require_inside_root(path)
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def run(*args: str) -> None:
    print("+", " ".join(args))
    subprocess.run(args, cwd=ROOT, check=True)


def export_png(source: Path, target: Path, width: int) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    run(
        "inkscape",
        str(source),
        f"--export-filename={target}",
        f"--export-width={width}",
    )


def build_rasters() -> None:
    production = ROOT / "logo" / "production"
    export_png(
        production / "extensionmesh-mark-color.svg",
        RASTER / "extensionmesh-mark-color-512.png",
        512,
    )
    export_png(
        production / "extensionmesh-mark-reversed.svg",
        RASTER / "extensionmesh-mark-reversed-512.png",
        512,
    )
    export_png(
        production / "extensionmesh-logo-horizontal.svg",
        RASTER / "extensionmesh-logo-horizontal-1600.png",
        1600,
    )
    export_png(
        production / "extensionmesh-logo-horizontal-reversed.svg",
        RASTER / "extensionmesh-logo-horizontal-reversed-1600.png",
        1600,
    )
    export_png(
        ROOT / "logo" / "preview" / "extensionmesh-brand-preview.svg",
        RASTER / "extensionmesh-logo-preview.png",
        1600,
    )


def build_guide() -> Path:
    run(sys.executable, "brand-guide/source/create_brand_guide.py")
    guide = BUILD / "ExtensionMesh-Brand-Guide-v0.1.pdf"
    if not guide.is_file():
        raise RuntimeError("Brand guide build did not produce the expected PDF")
    return guide


def build_package(guide: Path) -> None:
    fresh_directory(PACKAGE)
    shutil.copytree(ROOT / "logo" / "production", PACKAGE / "logo")
    shutil.copytree(RASTER, PACKAGE / "png")
    shutil.copytree(ROOT / "tokens", PACKAGE / "tokens")
    shutil.copy2(guide, PACKAGE / guide.name)
    shutil.copy2(ROOT / "README.md", PACKAGE / "README.md")

    DIST.mkdir(parents=True, exist_ok=True)
    shutil.copy2(guide, DIST / guide.name)
    shutil.copy2(
        RASTER / "extensionmesh-logo-preview.png",
        DIST / "extensionmesh-logo-preview.png",
    )
    shutil.copytree(RASTER, DIST / "png", dirs_exist_ok=True)
    shutil.make_archive(
        str(DIST / "extensionmesh-assets-v0.1"),
        "zip",
        PACKAGE.parent,
        PACKAGE.name,
    )


def main() -> None:
    fresh_directory(BUILD)
    fresh_directory(DIST)
    RASTER.mkdir(parents=True)
    build_rasters()
    guide = build_guide()
    build_package(guide)
    print(f"Assets written to {DIST}")


if __name__ == "__main__":
    main()
