#!/usr/bin/env python3
"""Generate product pages from MHT template and Anupam source HTML."""

import json
import re
import sys
import urllib.request
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "product" / "duct-heater" / "index.html"
ANUPAM_DIR = Path("/home/thanu/anupam-site/www.anupamheaters.com")
MANIFEST = Path(__file__).resolve().parent / "products_manifest.json"
ASSETS = ROOT / "assets"
ANUPAM_BASE = "https://www.anupamheaters.com/"

DEFAULT_FEATURES = [
    "Supply voltage: from 150V to 600V",
    "Power: from 1KW to 75KW",
    "Material: Stainless Steel / Inconel (as applicable)",
    "Available Terminals: Direct lead wire from both ends",
    "Notes: Electrical ratings and dimensions can be customized per client requirements after a feasibility check",
]


def load_template():
    return TEMPLATE.read_text(encoding="utf-8")


def rebrand(text):
    text = re.sub(r"\bAnupam(?:\s+Heaters?|\s+Electroheat)?(?:'s)?\b", "Master Heat Industries", text, flags=re.I)
    text = re.sub(r"Master Heat Industries's\b", "Master Heat Industries'", text)
    text = re.sub(r"info@anupamheaters\.com", "info@masterheattechnology.com", text, flags=re.I)
    text = re.sub(r"\+91-\d+", "", text)
    text = re.sub(r"Mumbai\.?\s*INDIA\.?", "", text, flags=re.I)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def strip_tags(html):
    html = re.sub(r"<br\s*/?>", " ", html, flags=re.I)
    html = re.sub(r"<[^>]+>", "", html)
    return unescape(html).strip()


def strip_html_comments(html):
    return re.sub(r"<!--.*?-->", "", html, flags=re.S)


def jpeg_dimensions(data):
    i = 0
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (
            0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
            0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
        ):
            height = (data[i + 5] << 8) + data[i + 6]
            width = (data[i + 7] << 8) + data[i + 8]
            return width, height
        if marker in (0xD8, 0xD9) or marker == 0x01:
            i += 2
            continue
        if i + 3 >= len(data):
            break
        length = (data[i + 2] << 8) + data[i + 3]
        i += 2 + length
    return None


def is_placeholder_image(data):
    """Detect Anupam's generic grey 'IMAGE PLACEHOLDER' graphic (570x400)."""
    return jpeg_dimensions(data) == (570, 400)


def collect_image_candidates(html, slug):
    active_html = strip_html_comments(html)
    candidates = []

    for pattern in [
        r'<div class="tab-content-image[^"]*">\s*<img[^>]+src="([^"]+)"',
        r'<div class="tab-content-image[^"]*">.*?<img[^>]+src="([^"]+)"',
        r'<div class="slider__item">\s*<img[^>]+src="([^"]+)"',
        r'<div class="product-img"><img[^>]+src="([^"]+)"',
    ]:
        for match in re.finditer(pattern, active_html, re.S):
            path = match.group(1).lstrip("/")
            if path not in candidates:
                candidates.append(path)

    slug_path = f"images/{slug}.jpg"
    if slug_path not in candidates:
        candidates.append(slug_path)

    return candidates


def fetch_image_bytes(url):
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; MHT-Import/1.0)"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        if len(data) > 500:
            return data
    except Exception as exc:
        print(f"  WARN: failed to download {url}: {exc}")
    return None


def download_best_image(candidates, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)

    for image_path in candidates:
        url = ANUPAM_BASE + image_path
        data = fetch_image_bytes(url)
        if not data:
            continue
        if is_placeholder_image(data):
            print(f"  SKIP placeholder: {image_path}")
            continue
        dest.write_bytes(data)
        print(f"  OK: {image_path} ({len(data)} bytes)")
        return True

    return False


def local_image_is_placeholder(path):
    return path.exists() and is_placeholder_image(path.read_bytes())


def parse_anupam(slug):
    path = ANUPAM_DIR / f"{slug}.html"
    if not path.exists():
        raise FileNotFoundError(path)
    html = path.read_text(encoding="utf-8", errors="replace")

    title_match = re.search(r'<h1 class="title3[^"]*">([^<]+)</h1>', html)
    title = strip_tags(title_match.group(1)) if title_match else slug.replace("-", " ").title()

    paras = []
    for m in re.finditer(r'<div class="para1">(.*?)</div>', html, re.S):
        block = m.group(1)
        for p in re.finditer(r"<p[^>]*>(.*?)</p>", block, re.S):
            text = strip_tags(p.group(1))
            if text and not text.upper().startswith("NOTE"):
                paras.append(rebrand(text))
        if len(paras) >= 2:
            break
    description = " ".join(paras[:2]) if paras else (
        f"Master Heat Industries offers high-quality {title.lower()} for industrial heating applications."
    )

    features = []
    for m in re.finditer(r'<ul class="list[^"]*">(.*?)</ul>', html, re.S):
        for li in re.finditer(r"<li[^>]*>(.*?)</li>", m.group(1), re.S):
            item = rebrand(strip_tags(li.group(1)))
            if item and len(item) < 200:
                features.append(item)
        if features:
            break
    if not features:
        features = DEFAULT_FEATURES[:]
    features = features[:8]

    candidates = collect_image_candidates(html, slug)

    return {
        "title": title,
        "description": description,
        "features": features,
        "image_candidates": candidates,
    }


def download_image(url, dest, fallback_url=None):
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt_url in [url, fallback_url]:
        if not attempt_url:
            continue
        data = fetch_image_bytes(attempt_url)
        if data and not is_placeholder_image(data):
            dest.write_bytes(data)
            return True
    return False


def features_html(features):
    lines = "\n".join(f"                                        <li>{f}</li>" for f in features)
    return f"""                                    <ul>
{lines}
                                    </ul>"""


def generate_page(template, slug, display_title, description, features, image_filename):
    full_title = f"{display_title} - MHT"
    page = template

    page = page.replace("Duct Heater - MHT", full_title)
    page = page.replace("duct-heater.jpg", image_filename)
    page = page.replace("infra-red-heater-lamp-irlx", slug)
    page = page.replace('class="infra-red-heater-lamp-irlx ani"', f'class="{slug} ani"')

    desc_pattern = re.compile(
        r"(<div class=\"col-lg-auto col-xl\">\s*)<p>.*?</p>",
        re.S,
    )
    page = desc_pattern.sub(rf"\1<p>{description}</p>", page, count=1)

    feat_pattern = re.compile(
        r"(<h3> Technical Features</h3>\s*<div class=\"row\">\s*<div class=\"col-lg-auto col-xl\">)\s*<ul>.*?</ul>",
        re.S,
    )
    page = feat_pattern.sub(rf"\1\n{features_html(features)}", page, count=1)

    return page


def mht_description(title):
    return (
        f"Master Heat Industries {title} is engineered for reliable performance in demanding "
        f"industrial heating applications. Designed for efficiency and durability, this product "
        f"meets the requirements of modern manufacturing and process industries."
    )


def process_mht_missing(manifest, template, force=False):
    created = []
    for item in manifest["mht_missing"]:
        slug = item["slug"]
        out = ROOT / "product" / slug / "index.html"
        if out.exists() and not force:
            print(f"SKIP (exists): {slug}")
            continue

        title = item["title"]
        image_file = f"{slug}.jpg"
        image_dest = ASSETS / image_file
        if not image_dest.exists() or force:
            ok = download_image(item["image_url"], image_dest)
            if not ok:
                print(f"  WARN: no image for {slug}, copying duct-heater fallback")
                image_dest.write_bytes((ASSETS / "duct-heater.jpg").read_bytes())

        page = generate_page(
            template, slug, title, mht_description(title), DEFAULT_FEATURES, image_file
        )
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")
        print(f"CREATED MHT: {slug}")
        created.append(item)
    return created


def process_anupam(manifest, template, force=False):
    created = []
    for item in manifest["anupam_products"]:
        slug = item["slug"]
        out = ROOT / "product" / slug / "index.html"
        if out.exists() and not force:
            print(f"SKIP (exists): {slug}")
            created.append(item)
            continue

        parsed = parse_anupam(slug)
        title = item.get("title") or parsed["title"]
        image_file = f"{slug}.jpg"
        image_dest = ASSETS / image_file

        needs_image = (
            force
            or not image_dest.exists()
            or local_image_is_placeholder(image_dest)
        )
        if needs_image:
            print(f"  Fetching image for {slug}...")
            ok = download_best_image(parsed["image_candidates"], image_dest)
            if not ok:
                print(f"  WARN: no Anupam image for {slug}, using duct-heater fallback")
                image_dest.write_bytes((ASSETS / "duct-heater.jpg").read_bytes())

        page = generate_page(
            template, slug, title, parsed["description"], parsed["features"], image_file
        )
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")
        print(f"CREATED ANUPAM: {slug}")
        created.append(item)
    return created


def build_card(item, use_local_image=True):
    slug = item["slug"]
    title = item["title"]
    category = item["category"]
    full = f"{title} - MHT"
    if use_local_image or "image_url" not in item:
        img_src = f"../assets/{slug}.jpg"
        img_tag = f'<img src="{img_src}" alt="{full} product image Master Heat Industries" class="img-fluid" />'
    else:
        url = item["image_url"]
        img_tag = f'<img src="{url}" alt="{full} product image Master Heat Industries" class="img-fluid" />'

    return f"""                <div class="col-xl-4  col-lg-6 col-md-6 mb-5 card-wrapper {category}">
                    <article class="card" id="anupam-{slug}">
                        <a href="../product/{slug}/index.html" title="{full} Master Heat Industries">
                            <figure> <i class="fa fa-arrow-right" aria-hidden="true"></i> {img_tag}</figure>
                            <h2 class="title mt-0"> {full}</h2> </a>
                    </article>
                </div>"""


def update_products_grid(manifest):
    grid_path = ROOT / "master-heat-tech-products" / "index.html"
    content = grid_path.read_text(encoding="utf-8")

    new_filters = [
        ('data-filter=".temperature-sensors"> Temperature Sensors </a></li>',
         'data-filter=".temperature-sensors"> Temperature Sensors </a></li>\n'
         '                        <li> <a href="javascript:;" title="Coil Heaters - Master Heat Industries" class="" data-filter=".coil-heaters"> Coil Heaters </a></li>\n'
         '                        <li> <a href="javascript:;" title="Manifold Heaters - Master Heat Industries" class="" data-filter=".manifold-heaters"> Manifold Heaters </a></li>\n'
         '                        <li> <a href="javascript:;" title="Porcelain Heaters - Master Heat Industries" class="" data-filter=".porcelain-heaters"> Porcelain Heaters </a></li>\n'
         '                        <li> <a href="javascript:;" title="Temperature Controllers - Master Heat Industries" class="" data-filter=".temperature-controllers"> Temperature Controllers </a></li>\n'
         '                        <li> <a href="javascript:;" title="Accessories - Master Heat Industries" class="" data-filter=".accessories"> Accessories </a></li>'),
    ]
    for old, new in new_filters:
        if "coil-heaters" not in content:
            content = content.replace(old, new, 1)

    marker = '                <div class="col-xl-4  col-lg-6 col-md-6 mb-5 card-wrapper flexible-fat-heating-elements">\n                    <article class="card" id="1454">\n                        <a href="../product/drum-heating-system/index.html"'
    if marker in content and "anupam-energy-saving-band-heaters" not in content:
        cards = "\n".join(build_card(p) for p in manifest["anupam_products"])
        insert_after = """                            <h2 class="title mt-0"> Drum Heating System - MHT</h2> </a>
                    </article>
                </div>
            </div>
        </section>"""
        replacement = """                            <h2 class="title mt-0"> Drum Heating System - MHT</h2> </a>
                    </article>
                </div>
""" + cards + """
            </div>
        </section>"""
        content = content.replace(insert_after, replacement, 1)

    grid_path.write_text(content, encoding="utf-8")
    print("UPDATED: master-heat-tech-products/index.html")


NAV_INSERT_AFTER = (
    '<li id="nav-item-1535" class="isotope-filter menu-item menu-item-type-custom '
    'menu-item-object-custom nav-item nav-item-1535"><a class="nav-link" title="Temperature Sensors" '
    'href="../../master-heat-tech-products/index.html#filter=.temperature-sensors">Temperature Sensors</a></li>'
)

NAV_INSERT_BLOCK = """                                        <li id="nav-item-1536" class="isotope-filter menu-item menu-item-type-custom menu-item-object-custom nav-item nav-item-1536"><a class="nav-link" title="Coil Heaters" href="../../master-heat-tech-products/index.html#filter=.coil-heaters">Coil Heaters</a></li>
                                        <li id="nav-item-1537" class="isotope-filter menu-item menu-item-type-custom menu-item-object-custom nav-item nav-item-1537"><a class="nav-link" title="Manifold Heaters" href="../../master-heat-tech-products/index.html#filter=.manifold-heaters">Manifold Heaters</a></li>
                                        <li id="nav-item-1538" class="isotope-filter menu-item menu-item-type-custom menu-item-object-custom nav-item nav-item-1538"><a class="nav-link" title="Porcelain Heaters" href="../../master-heat-tech-products/index.html#filter=.porcelain-heaters">Porcelain Heaters</a></li>
                                        <li id="nav-item-1539" class="isotope-filter menu-item menu-item-type-custom menu-item-object-custom nav-item nav-item-1539"><a class="nav-link" title="Temperature Controllers" href="../../master-heat-tech-products/index.html#filter=.temperature-controllers">Temperature Controllers</a></li>
                                        <li id="nav-item-1540" class="isotope-filter menu-item menu-item-type-custom menu-item-object-custom nav-item nav-item-1540"><a class="nav-link" title="Accessories" href="../../master-heat-tech-products/index.html#filter=.accessories">Accessories</a></li>"""

NAV_INSERT_BLOCK_ROOT = NAV_INSERT_BLOCK.replace("../../", "")
NAV_INSERT_BLOCK_PRODUCT = NAV_INSERT_BLOCK

FOOTER_INSERT_AFTER = (
    'class="nav-main-link" href="../../master-heat-tech-products/index.html#filter=.temperature-sensors"'
    'title="Temperature Sensors Master Heat Industries">Temperature Sensors</a></li>'
)

FOOTER_INSERT_BLOCK = """                                    <li class="nav-main-item isotope-filter menu-item menu-item-type-custom menu-item-object-custom menu-item-1551"> <a class="nav-main-link" href="../../master-heat-tech-products/index.html#filter=.coil-heaters" title="Coil Heaters Master Heat Industries">Coil Heaters</a></li>
                                    <li class="nav-main-item isotope-filter menu-item menu-item-type-custom menu-item-object-custom menu-item-1552"> <a class="nav-main-link" href="../../master-heat-tech-products/index.html#filter=.manifold-heaters" title="Manifold Heaters Master Heat Industries">Manifold Heaters</a></li>
                                    <li class="nav-main-item isotope-filter menu-item menu-item-type-custom menu-item-object-custom menu-item-1553"> <a class="nav-main-link" href="../../master-heat-tech-products/index.html#filter=.porcelain-heaters" title="Porcelain Heaters Master Heat Industries">Porcelain Heaters</a></li>
                                    <li class="nav-main-item isotope-filter menu-item menu-item-type-custom menu-item-object-custom menu-item-1554"> <a class="nav-main-link" href="../../master-heat-tech-products/index.html#filter=.temperature-controllers" title="Temperature Controllers Master Heat Industries">Temperature Controllers</a></li>
                                    <li class="nav-main-item isotope-filter menu-item menu-item-type-custom menu-item-object-custom menu-item-1555"> <a class="nav-main-link" href="../../master-heat-tech-products/index.html#filter=.accessories" title="Accessories Master Heat Industries">Accessories</a></li>"""


NAV_CATEGORIES = [
    ("Coil Heaters", "coil-heaters", 1536),
    ("Manifold Heaters", "manifold-heaters", 1537),
    ("Porcelain Heaters", "porcelain-heaters", 1538),
    ("Temperature Controllers", "temperature-controllers", 1539),
    ("Accessories", "accessories", 1540),
]


def header_nav_block(href_prefix, indent=""):
    lines = []
    for title, filt, nid in NAV_CATEGORIES:
        lines.append(
            f'{indent}<li id="nav-item-{nid}" class="isotope-filter menu-item menu-item-type-custom '
            f'menu-item-object-custom nav-item nav-item-{nid}"><a class="nav-link" title="{title}" '
            f'href="{href_prefix}index.html#filter=.{filt}">{title}</a></li>'
        )
    return "\n".join(lines)


def side_nav_block(href_prefix, indent=""):
    lines = []
    for title, filt, nid in NAV_CATEGORIES:
        lines.append(
            f'{indent}<li class="isotope-filter menu-item menu-item-type-custom menu-item-object-custom '
            f'nav-item nav-item-{nid}"><a class="nav-link" title="{title}" '
            f'href="{href_prefix}index.html#filter=.{filt}">{title}</a></li>'
        )
    return "\n".join(lines)


def insert_after_temp_sensor_nav(content, href_prefix, header_indent, side_indent):
    header_block = header_nav_block(href_prefix, indent=header_indent)
    side_block = side_nav_block(href_prefix, indent=side_indent)
    esc = re.escape(href_prefix)
    content = re.sub(
        rf'(<li id="nav-item-1535"[^>]*title="Temperature Sensors"[^>]*>'
        rf'Temperature Sensors</a></li>)',
        r"\1\n" + header_block,
        content,
        count=1,
    )
    content = re.sub(
        rf'(<li class="isotope-filter[^>]*title="Temperature Sensors"[^>]*>'
        rf'Temperature Sensors</a></li>)',
        r"\1\n" + side_block,
        content,
        count=1,
    )
    return content


def update_nav_in_file(path, depth):
    """depth: 0=root, 1=products page, 2=product detail pages"""
    content = path.read_text(encoding="utf-8")
    if "nav-item-1536" in content and (depth != 2 or "menu-item-1551" in content):
        return False

    if depth == 0:
        content = insert_after_temp_sensor_nav(
            content, "master-heat-tech-products/", "                                        ", "                            "
        )
        footer_anchor = (
            'href="master-heat-tech-products/index.html#filter=.temperature-sensors"'
            'title="Temperature Sensors Master Heat Industries">Temperature Sensors</a></li>'
        )
        content = content.replace(
            footer_anchor, footer_anchor + "\n" + FOOTER_INSERT_BLOCK.replace("../../", ""), 1
        )
    elif depth == 1:
        content = insert_after_temp_sensor_nav(content, "", "                                        ", "                            ")
    else:
        content = insert_after_temp_sensor_nav(
            content, "../../master-heat-tech-products/", "                                        ", "                            "
        )
        if "menu-item-1551" not in content:
            content = content.replace(
                FOOTER_INSERT_AFTER, FOOTER_INSERT_AFTER + "\n" + FOOTER_INSERT_BLOCK, 1
            )

    path.write_text(content, encoding="utf-8")
    return True


def update_all_nav():
    nav_files = [
        (ROOT / "index.html", 0),
        (ROOT / "master-heat-tech-products" / "index.html", 1),
        (ROOT / "master-heat-tech-sectors" / "index.html", 0),
        (ROOT / "services" / "index.html", 0),
        (ROOT / "contacts-us" / "index.html", 0),
    ]
    for p in (ROOT / "product").glob("*/index.html"):
        nav_files.append((p, 2))

    for path, depth in nav_files:
        if path.exists() and update_nav_in_file(path, depth):
            print(f"UPDATED NAV: {path.relative_to(ROOT)}")


def validate(manifest):
    errors = []
    grid = (ROOT / "master-heat-tech-products" / "index.html").read_text(encoding="utf-8")
    links = re.findall(r'href="\.\./product/([^/]+)/index\.html"', grid)
    for slug in set(links):
        if not (ROOT / "product" / slug / "index.html").exists():
            errors.append(f"Missing page: product/{slug}/index.html")

    for slug in links:
        page = (ROOT / "product" / slug / "index.html").read_text(encoding="utf-8", errors="replace")
        if re.search(r"\bAnupam\b", page, re.I):
            errors.append(f"Anupam branding in product/{slug}/index.html")
        img = re.search(r'src="\.\./\.\./assets/([^"]+)"', page)
        if img and not (ASSETS / img.group(1)).exists():
            errors.append(f"Missing asset: assets/{img.group(1)} for {slug}")

    if errors:
        print("VALIDATION ERRORS:")
        for e in errors:
            print(f"  - {e}")
        return False
    print(f"VALIDATION OK: {len(set(links))} product links checked")
    return True


def refresh_anupam_images(manifest):
    for item in manifest["anupam_products"]:
        slug = item["slug"]
        image_dest = ASSETS / f"{slug}.jpg"
        if not image_dest.exists() or local_image_is_placeholder(image_dest):
            parsed = parse_anupam(slug)
            print(f"Refreshing image: {slug}")
            ok = download_best_image(parsed["image_candidates"], image_dest)
            if not ok:
                print(f"  WARN: could not refresh image for {slug}")


def main():
    force = "--force" in sys.argv
    refresh_images = "--refresh-images" in sys.argv
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    template = load_template()

    if refresh_images:
        print("=== Refresh Anupam product images ===")
        refresh_anupam_images(manifest)
        sys.exit(0)

    print("=== Phase 1: MHT missing pages ===")
    process_mht_missing(manifest, template, force=force)

    print("\n=== Phase 2: Anupam products ===")
    process_anupam(manifest, template, force=force)

    print("\n=== Phase 3: Products grid ===")
    update_products_grid(manifest)

    print("\n=== Phase 4: Navigation ===")
    update_all_nav()

    print("\n=== Phase 5: Validation ===")
    ok = validate(manifest)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
