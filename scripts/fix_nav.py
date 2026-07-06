#!/usr/bin/env python3
"""Deduplicate footer nav and add missing category links across site HTML files.

Note: The Products dropdown mega menu is maintained by scripts/update_mega_menu.py
and scripts/mega_menu_data.py. Do not edit category/product nav lists here.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FOOTER_BLOCK = re.compile(
    r'\s*<li class="nav-main-item isotope-filter menu-item menu-item-type-custom menu-item-object-custom menu-item-1551">'
    r'.*?menu-item-1555">.*?Accessories</a></li>',
    re.S,
)

HEADER_BLOCK_PRODUCT = """
                                        <li id="nav-item-1536" class="isotope-filter menu-item menu-item-type-custom menu-item-object-custom nav-item nav-item-1536"><a class="nav-link" title="Coil Heaters" href="../../master-heat-tech-products/index.html#filter=.coil-heaters">Coil Heaters</a></li>
                                        <li id="nav-item-1537" class="isotope-filter menu-item menu-item-type-custom menu-item-object-custom nav-item nav-item-1537"><a class="nav-link" title="Manifold Heaters" href="../../master-heat-tech-products/index.html#filter=.manifold-heaters">Manifold Heaters</a></li>
                                        <li id="nav-item-1538" class="isotope-filter menu-item menu-item-type-custom menu-item-object-custom nav-item nav-item-1538"><a class="nav-link" title="Porcelain Heaters" href="../../master-heat-tech-products/index.html#filter=.porcelain-heaters">Porcelain Heaters</a></li>
                                        <li id="nav-item-1539" class="isotope-filter menu-item menu-item-type-custom menu-item-object-custom nav-item nav-item-1539"><a class="nav-link" title="Temperature Controllers" href="../../master-heat-tech-products/index.html#filter=.temperature-controllers">Temperature Controllers</a></li>
                                        <li id="nav-item-1540" class="isotope-filter menu-item menu-item-type-custom menu-item-object-custom nav-item nav-item-1540"><a class="nav-link" title="Accessories" href="../../master-heat-tech-products/index.html#filter=.accessories">Accessories</a></li>"""

SIDE_BLOCK_PRODUCT = """
                            <li class="isotope-filter menu-item menu-item-type-custom menu-item-object-custom nav-item nav-item-1536"><a class="nav-link" title="Coil Heaters" href="../../master-heat-tech-products/index.html#filter=.coil-heaters">Coil Heaters</a></li>
                            <li class="isotope-filter menu-item menu-item-type-custom menu-item-object-custom nav-item nav-item-1537"><a class="nav-link" title="Manifold Heaters" href="../../master-heat-tech-products/index.html#filter=.manifold-heaters">Manifold Heaters</a></li>
                            <li class="isotope-filter menu-item menu-item-type-custom menu-item-object-custom nav-item nav-item-1538"><a class="nav-link" title="Porcelain Heaters" href="../../master-heat-tech-products/index.html#filter=.porcelain-heaters">Porcelain Heaters</a></li>
                            <li class="isotope-filter menu-item menu-item-type-custom menu-item-object-custom nav-item nav-item-1539"><a class="nav-link" title="Temperature Controllers" href="../../master-heat-tech-products/index.html#filter=.temperature-controllers">Temperature Controllers</a></li>
                            <li class="isotope-filter menu-item menu-item-type-custom menu-item-object-custom nav-item nav-item-1540"><a class="nav-link" title="Accessories" href="../../master-heat-tech-products/index.html#filter=.accessories">Accessories</a></li>"""

FOOTER_BLOCK_HTML = """
                                    <li class="nav-main-item isotope-filter menu-item menu-item-type-custom menu-item-object-custom menu-item-1551"> <a class="nav-main-link" href="../../master-heat-tech-products/index.html#filter=.coil-heaters" title="Coil Heaters Masterheat Industries">Coil Heaters</a></li>
                                    <li class="nav-main-item isotope-filter menu-item menu-item-type-custom menu-item-object-custom menu-item-1552"> <a class="nav-main-link" href="../../master-heat-tech-products/index.html#filter=.manifold-heaters" title="Manifold Heaters Masterheat Industries">Manifold Heaters</a></li>
                                    <li class="nav-main-item isotope-filter menu-item menu-item-type-custom menu-item-object-custom menu-item-1553"> <a class="nav-main-link" href="../../master-heat-tech-products/index.html#filter=.porcelain-heaters" title="Porcelain Heaters Masterheat Industries">Porcelain Heaters</a></li>
                                    <li class="nav-main-item isotope-filter menu-item menu-item-type-custom menu-item-object-custom menu-item-1554"> <a class="nav-main-link" href="../../master-heat-tech-products/index.html#filter=.temperature-controllers" title="Temperature Controllers Masterheat Industries">Temperature Controllers</a></li>
                                    <li class="nav-main-item isotope-filter menu-item menu-item-type-custom menu-item-object-custom menu-item-1555"> <a class="nav-main-link" href="../../master-heat-tech-products/index.html#filter=.accessories" title="Accessories Masterheat Industries">Accessories</a></li>"""

HEADER_BLOCK_ROOT = HEADER_BLOCK_PRODUCT.replace("../../master-heat-tech-products/", "master-heat-tech-products/")
SIDE_BLOCK_ROOT = SIDE_BLOCK_PRODUCT.replace("../../master-heat-tech-products/", "master-heat-tech-products/")
FOOTER_BLOCK_ROOT = FOOTER_BLOCK_HTML.replace("../../master-heat-tech-products/", "master-heat-tech-products/")


def dedupe_footer(content):
    matches = list(FOOTER_BLOCK.finditer(content))
    if len(matches) <= 1:
        return content
    for m in reversed(matches[1:]):
        content = content[: m.start()] + content[m.end() :]
    return content


def insert_after_temp_sensor(content, header_block, side_block, footer_block, href_prefix):
    if "nav-item-1536" not in content:
        ts_href = f'{href_prefix}index.html#filter=.temperature-sensors'
        # Header dropdown: second nav-item-1535 is Temperature Sensors
        header_pat = (
            rf'(<li id="nav-item-1535"[^>]*href="{re.escape(ts_href)}"[^>]*>'
            rf'Temperature Sensors</a></li>)'
        )
        content, n = re.subn(header_pat, r"\1" + header_block, content, count=1)
        if n == 0:
            header_pat2 = (
                rf'(<li id="nav-item-1535"[^>]*title="Temperature Sensors"[^>]*>'
                rf'Temperature Sensors</a></li>)'
            )
            content = re.sub(header_pat2, r"\1" + header_block, content, count=1)

        side_pat = (
            rf'(<li class="isotope-filter[^>]*href="{re.escape(ts_href)}"[^>]*>'
            rf'Temperature Sensors</a></li>)'
        )
        content, n = re.subn(side_pat, r"\1" + side_block, content, count=1)
        if n == 0:
            side_pat2 = (
                rf'(<li class="isotope-filter[^>]*title="Temperature Sensors"[^>]*>'
                rf'Temperature Sensors</a></li>)'
            )
            content = re.sub(side_pat2, r"\1" + side_block, content, count=1)

    if footer_block and "menu-item-1551" not in content:
        footer_anchor = (
            f'href="{href_prefix}index.html#filter=.temperature-sensors"'
        )
        # match footer temperature sensors line (flexible spacing)
        content = re.sub(
            rf'({re.escape(footer_anchor)}[^<]*Temperature Sensors</a></li>)',
            r"\1" + footer_block,
            content,
            count=1,
        )

    return dedupe_footer(content)


def fix_file(path):
    content = path.read_text(encoding="utf-8")
    original = content
    rel = path.relative_to(ROOT)

    if rel.parts[0] == "product":
        content = insert_after_temp_sensor(
            content, HEADER_BLOCK_PRODUCT, SIDE_BLOCK_PRODUCT, FOOTER_BLOCK_HTML,
            "../../master-heat-tech-products/",
        )
    elif rel.name == "index.html" and len(rel.parts) == 1:
        content = insert_after_temp_sensor(
            content, HEADER_BLOCK_ROOT, SIDE_BLOCK_ROOT, FOOTER_BLOCK_ROOT,
            "master-heat-tech-products/",
        )
    elif rel.name == "index.html" and rel.parts[0] == "master-heat-tech-products":
        content = dedupe_footer(content)
    elif rel.name == "index.html" and rel.parts[0] in (
        "master-heat-tech-sectors", "services", "contacts-us",
    ):
        content = insert_after_temp_sensor(
            content, HEADER_BLOCK_ROOT, SIDE_BLOCK_ROOT, FOOTER_BLOCK_ROOT,
            "master-heat-tech-products/",
        )
    else:
        content = dedupe_footer(content)

    if content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False


def main():
    files = list(ROOT.glob("**/*.html"))
    targets = [
        p for p in files
        if "wp-content" not in p.parts and "scripts" not in p.parts
    ]
    changed = 0
    for p in targets:
        if fix_file(p):
            print(f"FIXED: {p.relative_to(ROOT)}")
            changed += 1
    print(f"Done. {changed} files updated.")


if __name__ == "__main__":
    main()
