#!/usr/bin/env python3
"""Rebrand Anupam HTTrack mirror to Masterheat Industries using MHT as source."""

from __future__ import annotations

import json
import re
import shutil
from html import escape, unescape
from pathlib import Path

MIRROR_ROOT = Path(__file__).resolve().parent.parent
MHT_ROOT = Path("/home/thanu/SolutionTechPoint/Master-Heat-Tech")
MANIFEST = MHT_ROOT / "scripts" / "products_manifest.json"
LOGO_SRC = MHT_ROOT / "assets" / "master-heat-industries-logo.jpg"
LOGO_DST = MIRROR_ROOT / "images" / "master-heat-industries-logo.jpg"

SKIP_DIRS = {"scripts", "js"}

HOME_TITLE = "Masterheat Industries | Industrial Heating Elements &amp; Systems"
HOME_DESCRIPTION = (
    "Founded in 2009, Masterheat Industries engineers world-class industrial heating "
    "solutions for India, the Middle East, and Africa. ISO-certified manufacturer of "
    "cartridge, tubular, immersion, and custom heating systems."
)
HOME_KEYWORDS = (
    "industrial heaters manufacturers, industrial heater, industrial heating elements, "
    "heating element manufacturers, heating elements suppliers, ceramic infrared heaters, "
    "vasai, india, masterheat industries"
)

MARQUEE_OLD = (
    '<span>We are looking for agents/dealers worldwide.  Kindly drop us a mail for further discussions.</span>'
    '<span class="last">Anupam is looking for business partners/ventures across the globe.Kindly drop us a mail for more details.</span>'
)
MARQUEE_NEW = (
    '<span>Masterheat Industries manufactures industrial heating elements and systems in-house. Contact us for application-specific solutions.</span>'
    '<span class="last">We support OEMs, plant engineers, and commercial operators across India and overseas markets.</span>'
)

FOOTER_ADDRESS = (
    "Masterheat Industries, Pilot Industrial Estate, Gala No. 36, "
    "Navghar Road, Samarth Krupa Nagar, Vasai-East, Maharashtra &ndash; 401202, India"
)
CONTACT_ADDRESS = (
    "Masterheat Industries<br/>GSTIN: 27ALUPJ4427B1Z2<br/>"
    "Pilot Industrial Estate, Gala No. 36,<br/>"
    "Navghar Road, Samarth Krupa Nagar,<br/>"
    "Vasai-East, Maharashtra &ndash; 401202, India"
)
CONTACT_PHONE = "+91-9358146992"

DISCLAIMER_NEW = (
    'All information in Masterheat Industries catalog &amp; website was considered accurate '
    "and correct at the time of printing &amp; publishing. Masterheat Industries has the "
    "right to make changes to specifications, designs and the Sales Terms and Conditions "
    "without prior notice. Masterheat Industries is not responsible for any typographical errors."
)

ABOUT_PARAS = [
    (
        'Established with a focus on industrial heating excellence, Masterheat Industries '
        "designs and manufactures heating elements and systems in-house. We support OEMs, "
        "plant engineers, and commercial operators with reliable, application-specific "
        "heating solutions across India and overseas markets."
    ),
    (
        "We are a specialist manufacturer of tubular heaters, mica and ceramic heaters, "
        "infrared systems, temperature sensors, and control accessories. From prototype "
        "to production run, our team works closely with customers to deliver heating "
        "systems that fit exact thermal, mechanical, and electrical requirements."
    ),
    (
        "With in-house manufacturing and GSTIN registration (27ALUPJ4427B1Z2), we maintain "
        "ISO 9001:2015, ISO 45001:2018, and ISO 14001:2015 certifications for quality, "
        "occupational health &amp; safety, and environmental management."
    ),
    (
        "As experts in the field of heating elements, we always strive to deliver a solution "
        "to our esteemed customers rather than a mere product. Innovation and continuous "
        "improvement help us develop superior products to serve the market more efficiently."
    ),
]

ABOUT_TABLEFT = [
    (
        "Masterheat Industries is a professionally managed company that believes in "
        "maintaining sustainable long-term relationships with employees, customers, "
        "and suppliers. In-house engineering and production give us direct control over "
        "quality and lead times."
    ),
    (
        "Our customer-centric approach, coupled with a continuous quest for world-class "
        "quality, helps us deliver dedicated service, efficient performance, and on-time "
        "results for industrial heating applications."
    ),
    "<b>If Heating is your Problem ... We are your Solution.</b>",
]


def strip_tags(html: str) -> str:
    html = re.sub(r"<br\s*/?>", " ", html, flags=re.I)
    html = re.sub(r"<[^>]+>", "", html)
    return re.sub(r"\s+", " ", unescape(html)).strip()


def copy_logo() -> None:
    if not LOGO_SRC.exists():
        raise FileNotFoundError(f"Logo not found: {LOGO_SRC}")
    LOGO_DST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(LOGO_SRC, LOGO_DST)


def fix_possessive(text: str) -> str:
    return text.replace("Masterheat Industries's", "Masterheat Industries'")


def global_rebrand(content: str) -> str:
    replacements = [
        ("Anupam Heaters &amp; Controls Pvt. Ltd.", "Masterheat Industries"),
        ("Anupam Heaters & Controls Pvt. Ltd.", "Masterheat Industries"),
        ("Anupam Heaters &amp; Controls", "Masterheat Industries"),
        ("Anupam Heaters & Controls", "Masterheat Industries"),
        ("Anupam Electroheat", "Masterheat Industries"),
        ("Anupam Heaters", "Masterheat Industries"),
        ("Anupam's", "Masterheat Industries'"),
        ("ANUPAM", "Masterheat Industries"),
        ("info@anupamheaters.com", "info@masterheatindustries.com"),
        ("images/anupam-electroheat-logo.png", "images/master-heat-industries-logo.jpg"),
        ("Anupam - Industrial Heaters Manufacturers", "Masterheat Industries - Industrial Heaters Manufacturers"),
        ("Anupam code No.", "Masterheat Industries code No."),
        ("© Copyrights 2018 Anupam Heaters. All Rights Reserved.", "© 2026 Masterheat Industries. All Rights Reserved."),
        ("© Copyrights 2018 Masterheat Industries. All Rights Reserved.", "© 2026 Masterheat Industries. All Rights Reserved."),
        (
            "A-284, Sumangal, Road No. 30, Wagle Industrial Estate, Thane (W) - 400 604. Mumbai. INDIA .",
            FOOTER_ADDRESS,
        ),
        (
            "Tel : +91-9819030025, +91-22-62478000, +91-22-25838051, +91-22-25838052, +91-22-25838053 |  Fax : +91-22-25838054  |  Email :",
            "Tel : +91-9358146992  |  Email :",
        ),
        (
            "Tel : +91-9819030025, +91-22-62478000, +91-22-25838051, +91-22-25838052, +91-22-25838053 |  Fax : +91-22-25838054 |  Email :",
            "Tel : +91-9358146992  |  Email :",
        ),
        ("+91-9819030025", "+91-9358146992"),
        ("+91-22-62478000", ""),
        ("+91-22-25838051", ""),
        ("+91-22-25838052", ""),
        ("+91-22-25838053", ""),
        ("+91-22-25838054", ""),
        ("+91-22-2583 8051 / 52 / 53 <br>", ""),
        ("+91-22-6247 8000", ""),
        ("<b>Fax:</b> +91-22-25838054", ""),
        ("<b>Fax:</b>", ""),
        (MARQUEE_OLD, MARQUEE_NEW),
    ]
    for old, new in replacements:
        content = content.replace(old, new)

    content = re.sub(r"\bAnupam\b", "Masterheat Industries", content, flags=re.I)
    content = re.sub(r"\banupam['\u2019]s\b", "Masterheat Industries'", content, flags=re.I)
    content = re.sub(r"\banupam heaters\b", "Masterheat Industries", content, flags=re.I)
    content = fix_possessive(content)

    content = content.replace(
        "https://www.anupamheaters.com/mailto.php",
        "mailto:info@masterheatindustries.com",
    )
    content = content.replace("http://www.anupamheaters.com/", "https://www.masterheatindustries.com/")
    content = content.replace("images/anupam-heaters-logo.jpg", "images/master-heat-industries-logo.jpg")
    content = content.replace(
        "126 & 127, Punjani Industrial Estate Pokhran Road No. 1, Khopat Thane (W) 400 601. Mumbai. India.",
        FOOTER_ADDRESS,
    )
    content = re.sub(
        r'"Masterheat Industries is a 100% Subsidiary of Masterheat Industries"',
        '"Masterheat Industries - Industrial Heating Elements &amp; Systems"',
        content,
    )
    content = re.sub(
        r'content="[^"]*anupam[^"]*"',
        lambda m: re.sub(r"anupam['\u2019]s?", "Masterheat Industries'", m.group(0), flags=re.I),
        content,
        flags=re.I,
    )

    content = re.sub(
        r'<link rel="shortcut icon" href="favicon\.ico"[^>]*>\s*<link rel="icon" href="favicon\.ico"[^>]*>',
        '<link rel="shortcut icon" href="images/master-heat-industries-logo.jpg" type="image/jpeg">'
        '<link rel="icon" href="images/master-heat-industries-logo.jpg" type="image/jpeg">',
        content,
    )
    content = content.replace(
        '<link rel="shortcut icon" type="image/x-icon" href="favicon.ico">',
        '<link rel="shortcut icon" type="image/jpeg" href="images/master-heat-industries-logo.jpg">',
    )

    content = content.replace("mumbai, india", "vasai, india")
    content = content.replace("Mumbai, India", "Vasai, India")
    content = content.replace("Mumbai. INDIA", "Vasai, India")

    return content


def update_home(content: str) -> str:
    content = re.sub(
        r"<title>.*?</title>",
        f"<title>{HOME_TITLE}</title>",
        content,
        count=1,
        flags=re.S,
    )
    content = re.sub(
        r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="{HOME_DESCRIPTION}"',
        content,
        count=1,
    )
    if 'name="keywords"' in content:
        content = re.sub(
            r'<meta name="keywords" content="[^"]*"',
            f'<meta name="keywords" content="{HOME_KEYWORDS}"',
            content,
            count=1,
        )
    content = re.sub(
        r"Anupam's pioneer product with still the best way to heat barrels\.",
        "Masterheat Industries' pioneer product with still the best way to heat barrels.",
        content,
    )
    return content


def update_about(content: str) -> str:
    delays = ["0.1s", "0.2s", "0.3s", "0.4s"]
    for delay, para in zip(delays, ABOUT_PARAS):
        content = re.sub(
            rf'<p class="wow fadeInUp" data-wow-delay="{delay}">.*?</p>',
            f'<p class="wow fadeInUp" data-wow-delay="{delay}">{para}</p>',
            content,
            count=1,
            flags=re.S,
        )

    tableft_match = re.search(
        r'(<div class="tableft wow fadeInUp" data-wow-delay="0\.6s">\s*)(.*?)(\s*</div>)',
        content,
        flags=re.S,
    )
    if tableft_match:
        inner = "\n".join(f"\t\t\t\t\t<p>{p}</p>" for p in ABOUT_TABLEFT)
        content = (
            content[: tableft_match.start()]
            + tableft_match.group(1)
            + inner
            + tableft_match.group(3)
            + content[tableft_match.end() :]
        )

    content = re.sub(
        r"<title>.*?</title>",
        "<title>About Us | Masterheat Industries - Industrial Heating Manufacturer India</title>",
        content,
        count=1,
        flags=re.S,
    )
    content = re.sub(
        r'<meta name="description" content="[^"]*"',
        '<meta name="description" content="Masterheat Industries manufactures industrial heating elements and systems in-house for OEMs, plant engineers, and commercial operators across India."',
        content,
        count=1,
    )
    return content


def update_contact(content: str) -> str:
    content = re.sub(
        r'(<div class="contact-textarea">)(?:A-284, Sumangal|Masterheat Industries).*?(</div>)',
        rf"\1{CONTACT_ADDRESS}\2",
        content,
        flags=re.S,
    )
    content = re.sub(
        r'(<div class="contact-iconarea"><img src="images/tel-icon\.png"[^>]*/></div>\s*<div class="contact-textarea">).*?(</div>)',
        rf"\1 {CONTACT_PHONE}\2",
        content,
        count=1,
        flags=re.S,
    )
    content = re.sub(
        r"<title>.*?</title>",
        "<title>Contact Us | Masterheat Industries</title>",
        content,
        count=1,
        flags=re.S,
    )
    content = re.sub(
        r'<meta name="description" content="[^"]*"',
        '<meta name="description" content="Contact Masterheat Industries for industrial heating elements, systems, and application engineering support."',
        content,
        count=1,
    )
    return content


def extract_mht_product_intro(slug: str) -> str | None:
    path = MHT_ROOT / "product" / slug / "index.html"
    if not path.exists():
        return None
    html = path.read_text(encoding="utf-8")
    match = re.search(
        r'class="[^"]*product-details[^"]*"[^>]*>.*?'
        r'class="[^"]*dyn-block[^"]*"[^>]*>.*?<p>(.*?)</p>',
        html,
        flags=re.S | re.I,
    )
    if not match:
        return None
    return strip_tags(match.group(1))


def update_product_intro(content: str, slug: str) -> str:
    intro = extract_mht_product_intro(slug)
    if intro:
        escaped = intro.replace("&", "&amp;")
        content = re.sub(
            r'(<div class="para1">\s*)<p>.*?</p>',
            rf"\1<p>{escaped}</p>",
            content,
            count=1,
            flags=re.S,
        )

    mht_path = MHT_ROOT / "product" / slug / "index.html"
    if mht_path.exists():
        mht_html = mht_path.read_text(encoding="utf-8")
        title_match = re.search(r"<title>(.*?)</title>", mht_html, re.S)
        if title_match:
            title = strip_tags(title_match.group(1))
            content = re.sub(
                r"<title>.*?</title>",
                f"<title>{title}</title>",
                content,
                count=1,
                flags=re.S,
            )
        desc_match = re.search(
            r'<meta name="description" content="([^"]*)"',
            mht_html,
        )
        if desc_match and 'name="description"' in content:
            desc = desc_match.group(1)
            content = re.sub(
                r'<meta name="description" content="[^"]*"',
                f'<meta name="description" content="{desc}"',
                content,
                count=1,
            )

    return content


def iter_html_files() -> list[Path]:
    files: list[Path] = []
    for path in MIRROR_ROOT.rglob("*.html"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def process_file(path: Path, product_slugs: set[str]) -> bool:
    original = path.read_text(encoding="utf-8")
    content = global_rebrand(original)

    name = path.name
    if name in ("index.html", "index-2.html") and path.parent == MIRROR_ROOT:
        content = update_home(content)
    elif name == "about-us.html":
        content = update_about(content)
    elif name == "contact-us.html":
        content = update_contact(content)
    elif name.endswith(".html") and path.stem in product_slugs:
        content = update_product_intro(content, path.stem)

    if content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False


def main() -> None:
    copy_logo()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    product_slugs = {p["slug"] for p in manifest["anupam_products"]}

    updated: list[Path] = []
    for path in iter_html_files():
        if process_file(path, product_slugs):
            updated.append(path.relative_to(MIRROR_ROOT))

    print(f"Updated {len(updated)} file(s)")
    for rel in updated:
        print(f"  {rel}")


if __name__ == "__main__":
    main()
