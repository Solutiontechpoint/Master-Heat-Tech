#!/usr/bin/env python3
"""Replace Products nav dropdown with grouped mega menu across all site HTML pages."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from mega_menu_data import MEGA_MENU_CATEGORIES, MEGA_MENU_COLUMNS

ROOT = Path(__file__).resolve().parent.parent

SKIP_DIRS = {"wp-content", "scripts", ".git", "node_modules"}
SKIP_FILES = {
    "privacy-policy.html",
    "assets/pdf-viewer.html",
}

DESKTOP_PRODUCTS_RE = re.compile(
    r'<li[^>]*\bid="nav-item-1128"[^>]*>.*?(?:</div>\s*</li>|</ul>\s*</li>)'
    r'(?=\s*<li[^>]*(?:\bid="nav-item-1161"|\bnav-item-1161\b))',
    re.DOTALL,
)

MOBILE_PRODUCTS_RE = re.compile(
    r'<li(?![^>]*\bid="nav-item-1128")[^>]*\bnav-item-1128\b[^>]*>.*?'
    r'(?:</div>\s*</li>|</ul>\s*</li>)'
    r'(?=\s*<li[^>]*(?:\bid="nav-item-1161"|\bnav-item-1161\b))',
    re.DOTALL,
)

HEADER_CSS_LINK_RE = re.compile(
    r'(<link rel="stylesheet" href="[^"]*header\.css)(\?v=\d+)?(" media="all" />)'
)


def resolve_paths(html_path: Path) -> tuple[str, str, bool]:
    rel = html_path.relative_to(ROOT)
    is_products_page = (
        len(rel.parts) >= 1
        and rel.parts[0] == "master-heat-tech-products"
        and rel.name == "index.html"
    )
    depth = len(rel.parts) - 1
    up = "../" * depth if depth else ""
    catalogue_base = "index.html" if is_products_page else f"{up}master-heat-tech-products/index.html"
    product_prefix = "../product/" if is_products_page else f"{up}product/"
    return catalogue_base, product_prefix, is_products_page


def _filter_href(catalogue_base: str, filter_class: str) -> str:
    return f"{catalogue_base}#filter={filter_class}"


def _product_href(product_prefix: str, slug: str) -> str:
    return f"{product_prefix}{slug}/index.html"


def _render_group(
    category_key: str,
    catalogue_base: str,
    product_prefix: str,
    *,
    mobile: bool,
) -> str:
    cat = MEGA_MENU_CATEGORIES[category_key]
    heading = cat["heading"]
    filter_class = cat["filter_class"]
    filter_href = _filter_href(catalogue_base, filter_class)

    lines = [
        '          <div class="products-mega__group">',
        '            <h4 class="products-mega__heading">',
        f'              <a href="{filter_href}" title="{heading}">{heading}</a>',
        "            </h4>",
        '            <ul class="products-mega__list">',
    ]
    for product in cat["products"]:
        href = _product_href(product_prefix, product["slug"])
        title = product["title"]
        lines.append(
            f'              <li><a class="products-mega__link" href="{href}" '
            f'title="{title} Masterheat Industries">{title}</a></li>'
        )
    lines.extend(["            </ul>", "          </div>"])
    if mobile:
        return "\n".join(lines)
    return "\n".join(lines)


def _render_mega_inner(
    catalogue_base: str,
    product_prefix: str,
    *,
    mobile: bool,
) -> str:
    col_blocks = []
    for column_keys in MEGA_MENU_COLUMNS:
        groups = "\n".join(
            _render_group(key, catalogue_base, product_prefix, mobile=mobile)
            for key in column_keys
        )
        col_blocks.append(f'        <div class="products-mega__col">\n{groups}\n        </div>')
    grid = "\n".join(col_blocks)
    if mobile:
        return (
            '<div class="dropdown-container products-mega" role="menu">\n'
            f'      <div class="products-mega__grid products-mega__grid--mobile">\n{grid}\n'
            "      </div>\n"
            "    </div>"
        )
    return (
        '<div class="dropdown-container products-mega" role="menu">\n'
        "      <div class=\"container\">\n"
        f'        <div class="products-mega__grid">\n{grid}\n'
        "        </div>\n"
        "      </div>\n"
        "    </div>"
    )


def render_desktop_mega_menu(catalogue_base: str, product_prefix: str, is_products_page: bool) -> str:
  extra_li = (
      " current-menu-ancestor current-menu-parent current_page_parent "
      "current_page_ancestor current-menu-item current_page_item active"
      if is_products_page
      else ""
  )
  products_href = catalogue_base if is_products_page else catalogue_base
  inner = _render_mega_inner(catalogue_base, product_prefix, mobile=False)
  return (
      f'<li id="nav-item-1128" class="menu-item menu-item-type-post_type '
      f'menu-item-object-page menu-item-has-children nav-item nav-item-1128 '
      f'nav-item dropdown products-mega-parent{extra_li}">'
      f'<a class="nav-link dropdown-toggle" aria-haspopup="true" aria-expanded="false" '
      f'title="Products" href="{products_href}">'
      f'<i class="_mi _before dashicons dashicons-plus" aria-hidden="true"></i>'
      f"<span>Products</span> </a>\n"
      f"    {inner}</li>"
  )


def render_mobile_mega_menu(catalogue_base: str, product_prefix: str, is_products_page: bool) -> str:
    extra_li = " active" if is_products_page else ""
    products_href = catalogue_base if is_products_page else catalogue_base
    inner = _render_mega_inner(catalogue_base, product_prefix, mobile=True)
    return (
        f'<li class="menu-item menu-item-type-post_type menu-item-object-page '
        f'menu-item-has-children nav-item nav-item-1128 nav-item dropdown products-mega-parent{extra_li}">'
        f'<a class="nav-link dropdown-toggle" aria-haspopup="true" aria-expanded="false" '
        f'title="Products" href="{products_href}">'
        f'<i class="_mi _before dashicons dashicons-plus" aria-hidden="true"></i>'
        f"<span>Products</span> </a>\n"
        f"    {inner}</li>"
    )


def update_file(html_path: Path) -> bool:
    content = html_path.read_text(encoding="utf-8")
    if "nav-item-1128" not in content:
        return False

    catalogue_base, product_prefix, is_products_page = resolve_paths(html_path)
    desktop = render_desktop_mega_menu(catalogue_base, product_prefix, is_products_page)
    mobile = render_mobile_mega_menu(catalogue_base, product_prefix, is_products_page)

    new_content, desktop_n = DESKTOP_PRODUCTS_RE.subn(desktop, content, count=1)
    if desktop_n == 0:
        print(f"  WARN: desktop Products nav not found in {html_path.relative_to(ROOT)}", file=sys.stderr)
        return False

    new_content, mobile_n = MOBILE_PRODUCTS_RE.subn(mobile, new_content, count=1)
    if mobile_n == 0:
        print(f"  WARN: mobile Products nav not found in {html_path.relative_to(ROOT)}", file=sys.stderr)
        return False

    new_content = HEADER_CSS_LINK_RE.sub(r"\1?v=2\3", new_content)

    if new_content != content:
        html_path.write_text(new_content, encoding="utf-8")
    return True


def iter_html_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.html"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_FILES:
            continue
        files.append(path)
    return sorted(files)


def main() -> int:
    updated = 0
    skipped = 0
    errors = 0

    for html_path in iter_html_files():
        rel = html_path.relative_to(ROOT)
        if "nav-item-1128" not in html_path.read_text(encoding="utf-8"):
            skipped += 1
            continue
        try:
            if update_file(html_path):
                updated += 1
            else:
                errors += 1
        except Exception as exc:  # noqa: BLE001
            errors += 1
            print(f"ERROR: {rel}: {exc}", file=sys.stderr)

    print(f"\nDone. updated={updated} skipped={skipped} errors={errors}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
