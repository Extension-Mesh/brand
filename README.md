<p align="center">
  <img src="logo/production/extensionmesh-logo-horizontal.svg" alt="ExtensionMesh" width="560">
</p>

<p align="center"><strong>Open extension distribution.</strong></p>

<p align="center">
  <a href="https://github.com/Extension-Mesh/brand/actions/workflows/build-assets.yml">
    <img src="https://github.com/Extension-Mesh/brand/actions/workflows/build-assets.yml/badge.svg" alt="Build brand assets">
  </a>
</p>

This repository is the canonical source for the ExtensionMesh visual identity.
It contains production-ready logos, editable sources, design tokens and the
sources used to build downloadable brand packages.

ExtensionMesh is an open project for practical extension distribution through
independent registries. The first implementation connects independent
registries with Shopware.

## Repository structure

```text
brand-guide/      Brand guide source
logo/source/      Editable SVG sources with live text
logo/production/  Font-independent SVGs with outlined wordmarks
logo/preview/     Reference sheet source
scripts/          Reproducible asset build
tokens/           CSS design tokens
```

## Ready-to-use assets

Use files from `logo/production/` in applications and documentation. They do
not require local fonts.

- `extensionmesh-logo-horizontal.svg` - primary logo for light surfaces
- `extensionmesh-logo-horizontal-reversed.svg` - primary logo for dark surfaces
- `extensionmesh-mark-color.svg` - standalone color mark
- `extensionmesh-mark-navy.svg` - monochrome mark for small sizes
- `extensionmesh-wordmark.svg` - standalone wordmark

## Build

The build requires Node.js, Python 3 and Inkscape.

```bash
npm ci
python3 -m pip install -r requirements.txt
python3 scripts/build_assets.py
```

Generated PNGs, the PDF brand guide and a complete ZIP package are written to
`dist/`. GitHub Actions runs the same build for every change and publishes
downloadable artifacts. Tagged versions also receive release assets.

## Brand foundations

- Public language: English
- Claim: **Open extension distribution.**
- Display type: Geologica
- Interface type: IBM Plex Sans
- Technical type: IBM Plex Mono
- Core colors: navy `#0F1B2E`, teal `#00AFC1`, warm white `#F7F7F4`

The identity should remain open, technical and neutral. Describe concrete
implementations clearly and avoid universal claims or ideological framing.

## Licensing

Reuse terms for visual assets and build tooling will be finalized separately.
Until explicit license files are added, normal copyright rules apply.
