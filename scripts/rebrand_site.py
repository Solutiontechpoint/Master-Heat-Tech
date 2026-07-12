#!/usr/bin/env python3
"""Apply Masterheat Industries branding across all site HTML pages."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
LOGO = "master-heat-industries-logo.jpg"

SKIP_DIRS = {"wp-content", "scripts", ".git", "node_modules"}
SKIP_FILES = {"privacy-policy.html", "assets/pdf-viewer.html"}

# Remote carousel filename fragments -> local asset slug (index.html product showcase)
HOME_REMOTE_TO_SLUG = {
    "ITHx-immersion-tubular-heaters-calorflex": "immersion-tubular-heater-ithx",
    "ITFx-flanged-immersion-heaters-calorflex": "immersion-flanged-heater-itfx",
    "IKHx-industrial-kitchen-equipment-heaters-calorflex": "industrial-kitchen-equipment-heater-ikhx",
    "IAHx-air-heaters-calorflex": "air-heater-iahx",
    "HCHx-cartridge-heaters-calorflex": "cartridge-heater-hchx",
    "IBCx-immersion-bobbin-heaters-calorflex": "immersion-bobbin-heater-ibcx",
    "BHCx-BSHx-ceramic-band-heaters-calorlfex": "ceramic-band-heater-bhcxbhsx",
    "IHCx-ceramic-infrared-heaters-calorflex": "ceramic-infra-red-heater-ihcx",
    "IRLx-infrared-heater-lamp-calorflex-hei": "infra-red-heater-lamp-irlx",
    "MBHx-MBSX-mica-band-heaters-calorflex": "mica-band-heater-mbhxmbsx",
    "MNHx-mica-nozzle-heaters-calorflex-hei": "mica-nozzle-heater-mnhx",
    "MSHx-mica-strip-heater-calorflex-hei": "mica-strip-heater-mshx",
    "MBMx-mini-bar-heater-calorflex-hei": "mini-bar-heater-mbmx",
    "CX-heating-cable-calorflex-hei": "heating-cable-cx",
}


def depth_prefix(html_path: Path) -> str:
    rel = html_path.relative_to(ROOT)
    depth = len(rel.parts) - 1
    return "../" * depth if depth else ""


def product_slug_from_path(html_path: Path) -> str | None:
    rel = html_path.relative_to(ROOT)
    if len(rel.parts) >= 2 and rel.parts[0] == "product" and rel.name == "index.html":
        return rel.parts[1]
    return None


def rebrand_content(content: str, html_path: Path) -> str:
    prefix = depth_prefix(html_path)
    logo_path = f"{prefix}assets/{LOGO}"
    contact_php = f"{prefix}php/contact.php"

    content = content.replace("masterheattechnology.com", "www.masterheatindustries.com")
    content = content.replace("http://www.masterheatindustries.com", "https://www.masterheatindustries.com")

    content = re.sub(
        r'https?://(?:www\.)?masterheatindustries\.com/wp-content/[^"\']*calorflex-hei-logo\.(?:png|svg)',
        logo_path,
        content,
    )
    content = content.replace("calorflex-hei-logo.png", LOGO)
    content = content.replace("calorflex-hei-logo.svg", LOGO)

    content = re.sub(
        r'action="https?://(?:www\.)?masterheatindustries\.com[^"]*"',
        f'action="{contact_php}"',
        content,
    )

    content = content.replace("info@calorflexamerica.com", "info@masterheatindustries.com")
    content = content.replace("/calorflex-products/", "/master-heat-tech-products/")
    content = content.replace("calorflex-products", "master-heat-tech-products")
    content = content.replace("calorflex-hei-sectors", "master-heat-tech-sectors")

    content = fix_calorflex_url_damage(content)

    slug = product_slug_from_path(html_path)
    if slug and (ASSETS / f"{slug}.jpg").exists():
        local_img = f"{prefix}assets/{slug}.jpg"
        content = re.sub(
            r'<meta property="og:image" content="[^"]*"',
            f'<meta property="og:image" content="{local_img}"',
            content,
            count=1,
        )

    if html_path.name == "index.html" and html_path.parent == ROOT:
        content = update_home_images(content)

    return content


def fix_calorflex_url_damage(content: str) -> str:
    """Undo accidental calorflex→Masterheat Industries replacements inside URL paths."""
    content = content.replace("-Masterheat Industries-hei", "-calorflex-hei")
    content = content.replace("-Masterheat Industries.svg", "-calorflex.svg")
    content = content.replace("-Masterheat Industries.jpg", "-calorflex.jpg")
    content = content.replace("-Masterheat Industries.png", "-calorflex.png")
    content = re.sub(
        r"-Masterheat Industries(?=-\d+x\d+|-\d+w)",
        "-calorflex",
        content,
    )
    return content


def update_home_images(content: str) -> str:
    for slug_dir in sorted((ROOT / "product").iterdir()):
        if not slug_dir.is_dir():
            continue
        slug = slug_dir.name
        if not (ASSETS / f"{slug}.jpg").exists():
            continue
        content = re.sub(
            rf'(<a href="product/{re.escape(slug)}/index\.html"[^>]*>\s*<figure>\s*<i[^>]*></i>\s*)<img[^>]*>',
            rf'\1<img src="assets/{slug}.jpg" alt="{slug.replace("-", " ").title()} - MHT product image Masterheat Industries" class="img-fluid" />',
            content,
            flags=re.S,
        )

    for fragment, slug in HOME_REMOTE_TO_SLUG.items():
        if not (ASSETS / f"{slug}.jpg").exists():
            continue
        local = f"assets/{slug}.jpg"
        content = re.sub(
            rf'https?://(?:www\.)?masterheatindustries\.com/wp-content/uploads/[^"\']*{re.escape(fragment)}[^"\']*',
            local,
            content,
        )

    content = re.sub(
        r'<meta property="og:image" content="[^"]*services[^"]*"',
        f'<meta property="og:image" content="assets/{LOGO}"',
        content,
        count=1,
    )
    return content


def iter_html_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.html"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_FILES:
            continue
        files.append(path)
    return sorted(files)


def rebrand_file(html_path: Path) -> bool:
    original = html_path.read_text(encoding="utf-8")
    updated = rebrand_content(original, html_path)
    if updated != original:
        html_path.write_text(updated, encoding="utf-8")
        return True
    return False


def validate() -> list[str]:
    errors: list[str] = []

    for path in iter_html_files():
        rel = str(path.relative_to(ROOT))
        text = path.read_text(encoding="utf-8", errors="replace")

        if re.search(r"\bAnupam\b", text, re.I) and 'id="anupam-' not in text:
            errors.append(f"Anupam branding in {rel}")

        if "calorflex-hei-logo" in text:
            errors.append(f"calorflex-hei-logo in {rel}")

        if "masterheattechnology.com" in text:
            errors.append(f"masterheattechnology.com in {rel}")

        if 'action="https://www.masterheatindustries.com' in text:
            errors.append(f"form still posts to remote domain in {rel}")

    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        from mega_menu_data import MEGA_MENU_CATEGORIES

        mega_slugs = {
            p["slug"]
            for cat in MEGA_MENU_CATEGORIES.values()
            for p in cat["products"]
        }
        product_slugs = {
            p.name for p in (ROOT / "product").iterdir() if p.is_dir()
        }
        missing = sorted(product_slugs - mega_slugs)
        if missing:
            errors.append(f"products missing from mega menu: {missing}")
    except Exception as exc:
        errors.append(f"mega menu validation failed: {exc}")

    return errors


def main() -> int:
    if "--validate" in sys.argv:
        errors = validate()
        if errors:
            print("VALIDATION ERRORS:")
            for err in errors:
                print(f"  - {err}")
            return 1
        print("VALIDATION OK")
        return 0

    updated = 0
    for html_path in iter_html_files():
        if rebrand_file(html_path):
            print(f"REBRANDED: {html_path.relative_to(ROOT)}")
            updated += 1

    print(f"\nRebrand complete. updated={updated}")

    errors = validate()
    if errors:
        print("\nPOST-RUN VALIDATION WARNINGS:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("POST-RUN VALIDATION OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
