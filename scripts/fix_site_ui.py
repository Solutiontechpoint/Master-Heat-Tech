#!/usr/bin/env python3
"""Apply site-wide UI fixes: nav, links, typos, contacts, CSS injection."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKIP_LINK = '<a class="skip-link" href="#main-content">Skip to main content</a>\n'

CONTACT_BLOCK = """                        <div class="site-contact-block">
                            <ul class="site-footer__contact-list">
                                <li class="site-footer__contact-item">
                                    <i class="fa fa-phone" aria-hidden="true"></i>
                                    <div>
                                        <a href="tel:+97477805150">+974 7780 5150</a>
                                        <a href="tel:+97455359440">+974 5535 9440</a>
                                    </div>
                                </li>
                                <li class="site-footer__contact-item">
                                    <i class="fa fa-envelope" aria-hidden="true"></i>
                                    <div>
                                        <a href="mailto:info@masterheattechnology.com">info@masterheattechnology.com</a>
                                        <a href="mailto:sales@masterheattechnology.com">sales@masterheattechnology.com</a>
                                    </div>
                                </li>
                                <li class="site-footer__contact-item">
                                    <i class="fa fa-map-marker" aria-hidden="true"></i>
                                    <div class="site-footer__addresses">
                                        <div>
                                            <span class="site-footer__address-label">Qatar</span>
                                            <p class="site-footer__address-text">
                                                <a href="https://maps.app.goo.gl/9cGCiE1r5PXho6dN7" rel="nofollow" target="_blank" title="Master Heat Industries on Google Maps">
                                                    PO Box 17115, 1st Floor, Office No. 2,<br>
                                                    Shahama Complex, Zone 55, Street 180,<br>
                                                    Building 45, Aziziya, Doha, Qatar
                                                </a>
                                            </p>
                                        </div>
                                        <div>
                                            <span class="site-footer__address-label">India</span>
                                            <p class="site-footer__address-text">
                                                Pilot Industrial Estate, Gala No. 36,<br>
                                                Navghar Road, Samarth Krupa Nagar,<br>
                                                Vasai, India
                                            </p>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </div>"""

OLD_CONTACTS_SECTION_RE = re.compile(
    r'<div class="contact-details container-fluid mt-3 mt-ld-0">.*?</div>\s*</div>\s*</div>\s*</div>\s*</section>',
    re.DOTALL,
)

DUPLICATE_NAV_MAIN_RE = re.compile(
    r'\s*<li class="nav-main-item isotope-filter menu-item menu-item-type-custom menu-item-object-custom menu-item-1551">'
    r'.*?menu-item-1555">.*?Accessories</a></li>',
    re.DOTALL,
)

NAV_SIDE_RE = re.compile(
    r'(<div class="nav-side"[^>]*>)(.*?)(<div[^>]*class="lights-off"[^>]*>)',
    re.DOTALL,
)

CATEGORIES_FILTER_RE = re.compile(
    r'(<p class="text-uppercase font-weight-bolder font-italic">Select the category</p>\s*)'
    r'(<ul class="categories-filter" id="filter">)',
    re.DOTALL,
)

SITE_CSS_RE = re.compile(
    r'<link[^>]+href="[^"]*site-improvements\.css"[^>]*>\n?',
    re.IGNORECASE,
)

TOGGLER_RE = re.compile(
    r'<button class="navbar-toggler">',
    re.IGNORECASE,
)

TOGGLER_FIXED_RE = re.compile(
    r'<button class="navbar-toggler"[^>]*aria-label=',
    re.IGNORECASE,
)

HEADER_CSS_RE = re.compile(
    r'<link[^>]+href="[^"]*header\.css"[^>]*>\n?',
    re.IGNORECASE,
)

HEADER_JS_RE = re.compile(
    r'<script[^>]+src="[^"]*header\.js"[^>]*>\s*</script>\n?',
    re.IGNORECASE,
)

PRODUCTS_DOUBLE_CLASS_RE = re.compile(
    r'(<a class="nav-link")\s+(title="Products"[^>]*?)\s+class="dropdown-toggle"',
    re.IGNORECASE,
)

DROPDOWN_MISSING_DIV_RE = re.compile(
    r'(title="Accessories"[^>]*>Accessories</a></li>\s*</ul>)\s*(</li>\s*<li[^>]*nav-item-1161)',
    re.IGNORECASE | re.DOTALL,
)

TEMP_SENSOR_DUP_LI_RE = re.compile(
    r'<li id="nav-item-1535"([^>]*)>(\s*<a[^>]*title="Temperature Sensors")',
    re.IGNORECASE,
)

TEMP_SENSOR_DUP_CLASS_RE = re.compile(
    r'nav-item nav-item-1535"><a class="nav-link"\s+title="Temperature Sensors"',
    re.IGNORECASE,
)

TOGGLER_ICON_RE = re.compile(
    r'(<button class="navbar-toggler"[^>]*>)\s*'
    r'(?:<!--.*?-->\s*)*'
    r'(?:<i class="fa fa-bars"[^>]*></i>\s*'
    r'<i class="fa fa-close d-none"[^>]*></i>\s*)'
    r'(?:<!--.*?-->\s*)*'
    r'(</button>)',
    re.DOTALL | re.IGNORECASE,
)

DESKTOP_PRODUCTS_ARIA_RE = re.compile(
    r'(<div class="navbar-collapse[^"]*"[^>]*id="navbar"[^>]*>.*?'
    r'<li[^>]*menu-item-has-children[^>]*>\s*'
    r'<a class="nav-link dropdown-toggle")(?!\s+aria-haspopup)(\s+title="Products")',
    re.DOTALL | re.IGNORECASE,
)


def depth_prefix(html_path: Path) -> str:
    rel = html_path.relative_to(ROOT)
    parts = rel.parts
    if len(parts) == 1:
        return ""
    return "../" * (len(parts) - 1)


def inject_css(content: str, prefix: str) -> str:
    href = f'{prefix}assets/site-improvements.css'
    link = f'    <link rel="stylesheet" href="{href}" media="all" />\n'
    if SITE_CSS_RE.search(content):
        return content
    footer_marker = 'assets/footer.css'
    idx = content.find(footer_marker)
    if idx != -1:
        end = content.find("/>", idx)
        if end != -1:
            insert_at = end + 2
            return content[:insert_at] + "\n" + link + content[insert_at:]
    head_end = content.lower().find("</head>")
    if head_end != -1:
        return content[:head_end] + link + content[head_end:]
    return content


def add_skip_link(content: str) -> str:
    if 'class="skip-link"' in content:
        return content
    for marker in ('<div class="inner-body">', '<body'):
        idx = content.find(marker)
        if idx == -1:
            continue
        if marker == '<body':
            close = content.find('>', idx)
            if close == -1:
                continue
            insert_at = close + 1
        else:
            insert_at = idx + len(marker)
        return content[:insert_at] + "\n        " + SKIP_LINK.strip() + "\n" + content[insert_at:]
    return content


def add_main_content_id(content: str, path: Path) -> str:
    if 'id="main-content"' in content:
        return content
    if path.name == "index.html" and path.parent == ROOT:
        return content.replace(
            '<section class="icons container-fluid',
            '<section id="main-content" class="icons container-fluid',
            1,
        )
    if '<section class="bcrumb-filters' in content:
        return content.replace(
            '<section class="bcrumb-filters',
            '<section id="main-content" class="bcrumb-filters',
            1,
        )
    return re.sub(
        r'<section class="intro-content',
        '<section id="main-content" class="intro-content',
        content,
        count=1,
    )


def fix_nav_side_mobile(content: str) -> str:
    def _fix_block(m: re.Match) -> str:
        opening, block, closing = m.group(1), m.group(2), m.group(3)
        if 'id="mobile-nav"' not in opening:
            opening = opening.replace(
                '<div class="nav-side">',
                '<div class="nav-side" id="mobile-nav">',
            )
        block = re.sub(
            r'(<li[^>]*class=")([^"]*)(")',
            lambda m2: m2.group(1)
            + re.sub(r'\bd-none d-xl-block\b\s*', '', m2.group(2)).strip()
            + m2.group(3),
            block,
        )
        return opening + block + closing

    return NAV_SIDE_RE.sub(_fix_block, content)


def fix_navbar_toggler(content: str) -> str:
    if TOGGLER_FIXED_RE.search(content):
        return content
    return TOGGLER_RE.sub(
        '<button class="navbar-toggler" type="button" '
        'aria-label="Open menu" aria-expanded="false" aria-controls="mobile-nav">',
        content,
    )


def fix_duplicate_menu_ids(content: str) -> str:
    content = re.sub(
        r'(id="navbar"[^>]*>\s*<ul )id="main-menu-left"',
        r'\1id="main-menu-desktop"',
        content,
        count=1,
    )
    content = re.sub(
        r'(id="mobile-nav"[^>]*>\s*<ul )id="main-menu-left"',
        r'\1id="main-menu-mobile"',
        content,
        count=1,
    )
    return content


def fix_duplicate_nav_item_1535(content: str) -> str:
    content = TEMP_SENSOR_DUP_LI_RE.sub(
        r'<li id="nav-item-1541"\1>\2',
        content,
    )
    content = re.sub(
        r'id="nav-item-1535"([^>]*class="[^"]*?)nav-item-1541',
        r'id="nav-item-1541"\1nav-item-1541',
        content,
    )
    content = TEMP_SENSOR_DUP_CLASS_RE.sub(
        r'nav-item nav-item-1541"><a class="nav-link"  title="Temperature Sensors"',
        content,
    )
    return content


def fix_products_link_class(content: str) -> str:
    return PRODUCTS_DOUBLE_CLASS_RE.sub(
        r'<a class="nav-link dropdown-toggle" \2',
        content,
    )


def fix_dropdown_closing_div(content: str) -> str:
    if re.search(r"</ul>\s*</div>\s*</li>\s*<li[^>]*nav-item-1161", content):
        return content
    return DROPDOWN_MISSING_DIV_RE.sub(r"\1\n</div>\2", content)


def add_site_header_class(content: str) -> str:
    if "site-header" in content:
        return content
    return content.replace(
        '<header class="header',
        '<header class="header site-header',
        1,
    )


def fix_nav_semantics(content: str) -> str:
    if 'aria-label="Main"' in content:
        return content
    return content.replace(
        '<nav class="navbar navbar-expand-xl navbar-light py-3">',
        '<nav class="navbar navbar-expand-xl navbar-light py-3" role="navigation" aria-label="Main">',
        1,
    )


def fix_toggler_icon(content: str) -> str:
    if "site-header__menu-icon" in content:
        return content

    def _replace(m: re.Match) -> str:
        return (
            m.group(1)
            + '\n                    <span class="site-header__menu-icon" aria-hidden="true"></span>\n                '
            + m.group(2)
        )

    return TOGGLER_ICON_RE.sub(_replace, content)


def fix_desktop_accordion_aria(content: str) -> str:
    return DESKTOP_PRODUCTS_ARIA_RE.sub(
        r'\1 aria-haspopup="true" aria-expanded="false"\2',
        content,
    )


def fix_mobile_accordion_aria(content: str) -> str:
    def _fix_block(m: re.Match) -> str:
        block = m.group(2)
        block = re.sub(
            r'(<li class="[^"]*menu-item-has-children[^"]*"[^>]*>\s*'
            r'<a class="nav-link[^"]*")(\s+title="Products")',
            r'\1 aria-haspopup="true" aria-expanded="false"\2',
            block,
            count=1,
        )
        return m.group(1) + block + m.group(3)

    return NAV_SIDE_RE.sub(_fix_block, content)


def inject_header_css(content: str, prefix: str) -> str:
    if HEADER_CSS_RE.search(content):
        return content
    href = f'{prefix}assets/header.css'
    link = f'    <link rel="stylesheet" href="{href}" media="all" />\n'
    site_idx = content.find("site-improvements.css")
    if site_idx != -1:
        end = content.find("/>", site_idx)
        if end != -1:
            insert_at = end + 2
            return content[:insert_at] + "\n" + link + content[insert_at:]
    head_end = content.lower().find("</head>")
    if head_end != -1:
        return content[:head_end] + link + content[head_end:]
    return content


def inject_header_js(content: str, prefix: str) -> str:
    if HEADER_JS_RE.search(content):
        return content
    src = f'{prefix}assets/header.js'
    script = f'    <script defer src="{src}"></script>\n'
    body_end = content.lower().rfind("</body>")
    if body_end != -1:
        return content[:body_end] + script + content[body_end:]
    return content


def fix_legacy_links(content: str, path: Path) -> str:
    content = content.replace("calorflex-hei-sectors", "master-heat-tech-sectors")
    rel = path.relative_to(ROOT)
    if len(rel.parts) >= 2:
        prefix = depth_prefix(path)
        content = re.sub(
            r'href="(?!\.{1,2}/)master-heat-tech-products/',
            rf'href="{prefix}master-heat-tech-products/',
            content,
        )
    return content


def fix_typos(content: str) -> str:
    content = content.replace("Cut-to-lenght Cables", "Cut-to-length Cables")
    content = content.replace('title="Cut-to-lenght Cables', 'title="Cut-to-length Cables')
    content = content.replace("Superior Perfomance", "Superior Performance")
    content = content.replace("> Perfomance <", "> Performance <")
    content = content.replace("Caorflex HEI industries", "Master Heat Industries")
    content = content.replace("Caorflex HEI", "Master Heat Industries")
    content = content.replace(
        "<h5 class=\"text-uppercase\"> We're at your service</h6>",
        "<h5 class=\"text-uppercase\"> We're at your service</h5>",
    )
    content = content.replace(
        '<h5 class="text-uppercase"> We\'re at your service</h6>',
        '<h5 class="text-uppercase"> We\'re at your service</h5>',
    )
    return content


def remove_duplicate_header_products(content: str) -> str:
    return DUPLICATE_NAV_MAIN_RE.sub("", content)


def wrap_categories_filter(content: str) -> str:
    if "categories-filter-wrapper" in content:
        return content

    def _wrap(m: re.Match) -> str:
        return (
            f'{m.group(1)}<div class="categories-filter-wrapper">\n                        '
            f'{m.group(2)}'
        )

    content, n = CATEGORIES_FILTER_RE.subn(_wrap, content, count=1)
    if n:
        content = content.replace(
            '</ul>\n                </div>\n            </div>\n        </section>\n        <section class="products-grid',
            '</ul>\n                        </div>\n                </div>\n            </div>\n        </section>\n        <section class="products-grid',
            1,
        )
    return content


def fix_contacts_page(content: str, path: Path) -> str:
    if path.parts[-2:] != ("contacts-us", "index.html"):
        return content
    if "site-contact-block" in content:
        return content
    return OLD_CONTACTS_SECTION_RE.sub(CONTACT_BLOCK + "\n                </div>\n            </div>\n        </section>", content, count=1)


def add_product_grid_css(content: str, prefix: str) -> str:
    if "product-grid.css" in content:
        return content
    if 'class="products-grid' not in content:
        return content
    link = f'    <link rel="stylesheet" href="{prefix}assets/product-grid.css" media="all" />\n'
    site_idx = content.find("site-improvements.css")
    if site_idx != -1:
        end = content.find("/>", site_idx)
        if end != -1:
            insert_at = end + 2
            return content[:insert_at] + "\n" + link + content[insert_at:]
    return content


def process_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    content = original
    prefix = depth_prefix(path)

    content = inject_css(content, prefix)
    content = inject_header_css(content, prefix)
    content = add_skip_link(content)
    content = add_main_content_id(content, path)
    content = add_site_header_class(content)
    content = fix_nav_semantics(content)
    content = fix_nav_side_mobile(content)
    content = fix_navbar_toggler(content)
    content = fix_toggler_icon(content)
    content = fix_duplicate_menu_ids(content)
    content = fix_duplicate_nav_item_1535(content)
    content = fix_products_link_class(content)
    content = fix_dropdown_closing_div(content)
    content = fix_mobile_accordion_aria(content)
    content = fix_desktop_accordion_aria(content)
    content = fix_legacy_links(content, path)
    content = fix_typos(content)
    content = remove_duplicate_header_products(content)
    content = wrap_categories_filter(content)
    content = fix_contacts_page(content, path)
    content = add_product_grid_css(content, prefix)
    content = inject_header_js(content, prefix)

    if content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False


def main():
    updated = []
    for path in sorted(ROOT.rglob("*.html")):
        if "wp-content" in path.parts:
            continue
        if process_file(path):
            updated.append(path.relative_to(ROOT))
    print(f"Updated {len(updated)} file(s)")
    for p in updated:
        print(f"  {p}")


if __name__ == "__main__":
    main()
