#!/usr/bin/env python3
"""Replace legacy footer markup with modern responsive footer across site HTML files."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PRODUCTS = [
    ("cartridge-heaters", "Cartridge Heaters"),
    ("ceramic-heaters", "Ceramic Heaters"),
    ("mica-heaters", "Mica Heaters"),
    ("cut-to-lenght-cables", "Cut-to-length Cables"),
    ("cables-on-reels", "Cables on Reels"),
    ("infrared-heaters", "Infrared Heaters"),
    ("flexible-fat-heating-elements", "Flexible Flat Heating Elements"),
    ("tubular-heaters", "Tubular Heaters"),
    ("temperature-sensors", "Temperature Sensors"),
    ("coil-heaters", "Coil Heaters"),
    ("manifold-heaters", "Manifold Heaters"),
    ("porcelain-heaters", "Porcelain Heaters"),
    ("temperature-controllers", "Temperature Controllers"),
    ("accessories", "Accessories"),
]

FOOTER_RE = re.compile(r"<footer[^>]*>.*?</footer>", re.DOTALL | re.IGNORECASE)
CSS_LINK_RE = re.compile(
    r'<link[^>]+href="[^"]*footer\.css"[^>]*>',
    re.IGNORECASE,
)


def depth_prefix(html_path: Path) -> str:
    rel = html_path.relative_to(ROOT)
    parts = rel.parts
    if len(parts) == 1:
        return ""
    return "../" * (len(parts) - 1)


def product_links(prefix: str, items: list[tuple[str, str]]) -> str:
    base = f"{prefix}master-heat-tech-products/index.html#filter=."
    lines = []
    for slug, label in items:
        lines.append(
            f'                                <li><a href="{base}{slug}">{label}</a></li>'
        )
    return "\n".join(lines)


def build_footer(prefix: str) -> str:
    mid = len(PRODUCTS) // 2
    col_a = product_links(prefix, PRODUCTS[:mid])
    col_b = product_links(prefix, PRODUCTS[mid:])
    assets = f"{prefix}assets/master-heat-industries-logo.jpg"
    products_url = f"{prefix}master-heat-tech-products/index.html"
    contacts_url = f"{prefix}contacts-us/index.html"

    return f"""<footer class="site-footer">
    <div class="container">
        <div class="row site-footer__main">
            <div class="col-lg-3 col-md-6 site-footer__brand">
                <img src="{assets}" width="200" height="auto" alt="Masterheat Industries logo" class="img-fluid" loading="lazy" />
                <p class="site-footer__tagline">Heating elements for the industrial sector</p>
            </div>
            <div class="col-lg-4 col-md-6 site-footer__products">
                <h3>Products</h3>
                <div class="row">
                    <div class="col-sm-6">
                        <ul>
{col_a}
                        </ul>
                    </div>
                    <div class="col-sm-6">
                        <ul>
{col_b}
                        </ul>
                    </div>
                </div>
                <a class="site-footer__view-all" href="{products_url}">View all products &rarr;</a>
            </div>
            <div class="col-lg-5 col-md-12 site-footer__contact">
                <h3>Contact Us</h3>
                <ul class="site-footer__contact-list">
                    <li class="site-footer__contact-item">
                        <i class="fa fa-phone" aria-hidden="true"></i>
                        <div>
                            <a href="tel:+919358146992">+91 9358146992</a>
                        </div>
                    </li>
                    <li class="site-footer__contact-item">
                        <i class="fa fa-envelope" aria-hidden="true"></i>
                        <div>
                            <a href="mailto:info@masterheatindustries.com">info@masterheatindustries.com</a>
                        </div>
                    </li>
                    <li class="site-footer__contact-item">
                        <i class="fa fa-globe" aria-hidden="true"></i>
                        <div>
                            <a href="https://www.masterheatindustries.com" target="_blank" rel="noopener">www.masterheatindustries.com</a>
                        </div>
                    </li>
                    <li class="site-footer__contact-item">
                        <i class="fa fa-map-marker" aria-hidden="true"></i>
                        <div class="site-footer__addresses">
                            <div>
                                <p class="site-footer__address-text">
                                    Masterheat Industries<br>
                                    GSTIN: 27ALUPJ4427B1Z2<br>
                                    Pilot Industrial Estate, Gala No. 36,<br>
                                    Navghar Road, Samarth Krupa Nagar,<br>
                                    Vasai-East, Maharashtra &ndash; 401202
                                </p>
                            </div>
                        </div>
                    </li>
                </ul>
                <a class="site-footer__view-all" href="{contacts_url}">Get in touch &rarr;</a>
            </div>
        </div>
        <div class="site-footer__bottom">
            <p>&copy; 2026 Masterheat Industries</p>
            <p><a href="https://solutiontechservices.com/" title="Solution Tech Services" rel="noopener">Credits: Solution Tech Services</a></p>
        </div>
    </div>
</footer>"""


def inject_css_link(content: str, prefix: str) -> str:
    css_href = f'{prefix}assets/footer.css'
    link = f'    <link rel="stylesheet" href="{css_href}" media="all" />\n'
    if CSS_LINK_RE.search(content):
        return content
    # Insert after combined siteground CSS or before </head>
    marker = 'siteground-optimizer-combined-css'
    idx = content.find(marker)
    if idx != -1:
        end = content.find("/>", idx)
        if end != -1:
            insert_at = end + 2
            return content[:insert_at] + "\n" + link + content[insert_at:]
    head_end = content.lower().find("</head>")
    if head_end != -1:
        return content[:head_end] + link + content[head_end:]
    return content


def update_file(html_path: Path) -> bool:
    content = html_path.read_text(encoding="utf-8")
    if not FOOTER_RE.search(content):
        return False

    prefix = depth_prefix(html_path)
    new_footer = build_footer(prefix)
    new_content = FOOTER_RE.sub(new_footer, content, count=1)
    new_content = inject_css_link(new_content, prefix)

    if new_content != content:
        html_path.write_text(new_content, encoding="utf-8")
        return True
    return False


def main():
    updated = []
    skipped = []
    for path in sorted(ROOT.rglob("*.html")):
        if "wp-content" in path.parts:
            continue
        if update_file(path):
            updated.append(path.relative_to(ROOT))
        elif "<footer" in path.read_text(encoding="utf-8").lower():
            skipped.append(path.relative_to(ROOT))

    print(f"Updated {len(updated)} file(s)")
    for p in updated:
        print(f"  {p}")
    if skipped:
        print(f"Skipped {len(skipped)} file(s) (no change)")


if __name__ == "__main__":
    main()
