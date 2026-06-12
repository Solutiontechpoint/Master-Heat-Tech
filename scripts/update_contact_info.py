#!/usr/bin/env python3
"""Apply India-only contact details and Master Heat Industries branding site-wide."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CONTACT_LIST_BLOCK = """                                <li class="site-footer__contact-item">
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
                                                Master Heat Industries<br>
                                                GSTIN: 27ALUPJ4427B1Z2<br>
                                                Pilot Industrial Estate, Gala No. 36,<br>
                                                Navghar Road, Samarth Krupa Nagar,<br>
                                                Vasai-East, Maharashtra &ndash; 401202
                                            </p>
                                        </div>
                                    </div>
                                </li>"""

OLD_CONTACT_BLOCK_RE = re.compile(
    r'<li class="site-footer__contact-item">\s*'
    r'<i class="fa fa-phone"[^>]*></i>\s*'
    r'<div>.*?</div>\s*'
    r'</li>\s*'
    r'<li class="site-footer__contact-item">\s*'
    r'<i class="fa fa-envelope"[^>]*></i>\s*'
    r'<div>.*?</div>\s*'
    r'</li>\s*'
    r'<li class="site-footer__contact-item">\s*'
    r'<i class="fa fa-map-marker"[^>]*></i>\s*'
    r'<div class="site-footer__addresses">.*?</div>\s*'
    r'</li>',
    re.DOTALL,
)

QATAR_ADDRESS_RE = re.compile(
    r'\s*<div>\s*'
    r'<span class="site-footer__address-label">Qatar</span>.*?</div>\s*',
    re.DOTALL,
)

MISSION_OLD = (
    "Masterheat Technologies , a superlative Doha,Qatar based company which\n"
    "primarily provides turnkey heating solutions for industrial, commercial\n"
    "and also domestic purposes. Our company currently functions through\n"
    "three dedicated plants using various heating technologies and employs\n"
    "over 50 dedicated employees. It began its operations in 1989 as the\n"
    "first heating solution company and presently has placed itself as the\n"
    "foremost renowned heating manufacturer/solution provider in the UAE,\n"
    "serving the needs of the entire gulf region. With a rich background of\n"
    "dwelling in varied technological challenges and delivery of robust\n"
    "systems for the past 35 years, MHt now intends to capitalize on the\n"
    "rapidly growing demand of heating applications, thus enriching the high\n"
    "yield potential of the industrial sectors and in turn its economy across\n"
    "the gulf region. MHT is and will remain the foremost leading heating\n"
    "solutions organization in the gulf creating a portal which will offer,\n"
    "periodically."
)

MISSION_NEW = (
    "Master Heat Industries is a Vasai, Maharashtra based company that provides "
    "turnkey heating solutions for industrial, commercial, and domestic applications. "
    "Our manufacturing facility at Pilot Industrial Estate delivers high-quality "
    "heating elements and systems using advanced heating technologies. With decades "
    "of experience in varied technological challenges and robust system delivery, "
    "we serve customers across India with reliable, efficient heating solutions "
    "tailored to their needs."
)

WORLD_SECTION_OLD = (
    "We also have direct manufacturing facilities in Qatar, Saudi Arabia and India. "
    "Visit the website of our offices and consult our entire product catalogue."
)

WORLD_SECTION_NEW = (
    "Master Heat Industries manufactures heating elements and industrial heating "
    "systems from our facility in Vasai, Maharashtra. Visit our website to explore "
    "our full product catalogue."
)


def apply_replacements(content: str) -> str:
    content = content.replace(MISSION_OLD, MISSION_NEW)
    content = content.replace(WORLD_SECTION_OLD, WORLD_SECTION_NEW)
    content = content.replace("Masterheat Technologies", "Master Heat Industries")
    content = content.replace("Master Heat Technology", "Master Heat Industries")
    content = content.replace("info@masterheattechnology.com", "info@masterheatindustries.com")

    content = re.sub(
        r'\s*<a href="mailto:sales@masterheattechnology\.com">sales@masterheattechnology\.com</a>',
        "",
        content,
    )
    content = re.sub(
        r'\s*<a href="tel:\+97477805150">\+974 7780 5150</a>',
        "",
        content,
    )
    content = content.replace('tel:+97455359440', 'tel:+919358146992')
    content = content.replace('+974 5535 9440', '+91 9358146992')
    content = content.replace('Call us (Qatar)', 'Call us')
    content = content.replace('Call us (India)', 'Call us')
    content = content.replace('tel:+91 9358146992', 'tel:+919358146992')

    content = QATAR_ADDRESS_RE.sub("\n", content)

    content = content.replace(
        "Pilot Industrial Estate, Gala No. 36,<br>\n"
        "                                    Navghar Road, Samarth Krupa Nagar,<br>\n"
        "                                    Vasai, India",
        "Master Heat Industries<br>\n"
        "                                    GSTIN: 27ALUPJ4427B1Z2<br>\n"
        "                                    Pilot Industrial Estate, Gala No. 36,<br>\n"
        "                                    Navghar Road, Samarth Krupa Nagar,<br>\n"
        "                                    Vasai-East, Maharashtra &ndash; 401202",
    )
    content = content.replace(
        "Pilot Industrial Estate, Gala No. 36,<br>\n"
        "                                                Navghar Road, Samarth Krupa Nagar,<br>\n"
        "                                                Vasai, India",
        "Master Heat Industries<br>\n"
        "                                                GSTIN: 27ALUPJ4427B1Z2<br>\n"
        "                                                Pilot Industrial Estate, Gala No. 36,<br>\n"
        "                                                Navghar Road, Samarth Krupa Nagar,<br>\n"
        "                                                Vasai-East, Maharashtra &ndash; 401202",
    )

    content = re.sub(
        r'\s*<span class="site-footer__address-label">India</span>\s*',
        "\n",
        content,
    )

    content = OLD_CONTACT_BLOCK_RE.sub(CONTACT_LIST_BLOCK, content)

    content = content.replace(
        "MORE: Master Heat Industries IN THE WORLD",
        "MORE: Master Heat Industries",
    )

    return content


def process_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    updated = apply_replacements(original)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def main():
    updated_files = []
    for path in sorted(ROOT.rglob("*.html")):
        if "wp-content" in path.parts:
            continue
        if process_file(path):
            updated_files.append(path.relative_to(ROOT))

    php_path = ROOT / "php" / "contact.php"
    if php_path.exists():
        original = php_path.read_text(encoding="utf-8")
        new_content = apply_replacements(original)
        if new_content != original:
            php_path.write_text(new_content, encoding="utf-8")
            updated_files.append(php_path.relative_to(ROOT))

    print(f"Updated {len(updated_files)} file(s)")
    for p in updated_files:
        print(f"  {p}")


if __name__ == "__main__":
    main()
