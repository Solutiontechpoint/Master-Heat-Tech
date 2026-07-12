#!/usr/bin/env python3
"""Replace clients.html with company.html from Master-Heat-Tech content."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

COMPANY_MAIN = """
<div class="main-contentarea">
  <div class="breadcrumb">
    <div class="common">
      <div class="inside-tab">
        <ul>
          <li><a href="index-2.html">Home</a></li>
          <li><a href="company.html" class="inside-tab-active">Company</a></li>
        </ul>
      </div>
    </div>
  </div>
  <div class="company-page">
<section class="company-hero">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-6">
                <span class="company-eyebrow">About Masterheat Industries</span>
                <h1 class="company-hero__title">Industrial heating solutions, made in India</h1>
                <p class="company-lead">Masterheat Industries designs and manufactures industrial heating elements and systems in-house. We support OEMs, plant engineers, and commercial operators with reliable, application-specific heating solutions.</p>
                <div class="company-hero__actions">
                    <a href="ceramic-band-heaters.html" class="btn-cflex dark w-icons high" title="Explore products">Explore Products <i class="fa fa-arrow-right" aria-hidden="true"></i></a>
                    <a href="contact-us.html" class="btn-cflex inv w-icons text-dark high" title="Contact us">Contact Us <i class="fa fa-arrow-right" aria-hidden="true"></i></a>
                </div>
            </div>
            <div class="col-lg-6 mt-5 mt-lg-0">
                <div class="company-hero__image">
                    <img src="images/flexible-tubular-heaters.jpg" alt="Industrial tubular heaters manufactured by Masterheat Industries" class="img-fluid" loading="lazy" />
                </div>
            </div>
        </div>
    </div>
</section>

<section class="company-stats">
    <div class="container">
        <div class="company-stats__grid">
            <div class="company-stats__item">
                <span class="company-stats__value">In-house manufacturing</span>
                <span class="company-stats__label">Engineering &amp; production</span>
            </div>
            <div class="company-stats__item">
                <span class="company-stats__value">27ALUPJ4427B1Z2</span>
                <span class="company-stats__label">GSTIN registered</span>
            </div>
            <div class="company-stats__item">
                <span class="company-stats__value">35+ Years</span>
                <span class="company-stats__label">Industrial heating experience</span>
            </div>
            <div class="company-stats__item">
                <span class="company-stats__value">Full Catalogue</span>
                <span class="company-stats__label">Heating elements &amp; systems</span>
            </div>
        </div>
    </div>
</section>

<section class="company-certifications">
    <div class="container">
        <div class="text-center mb-4">
            <span class="company-eyebrow">Quality &amp; compliance</span>
            <h2 class="company-section-title">ISO certifications</h2>
            <p class="company-section-text mx-auto">We maintain quality, safety, and environmental management certifications.</p>
        </div>
        <div class="company-certifications__grid">
            <article class="company-cert-card">
                <h3>ISO 9001:2015</h3>
                <p>Quality management systems</p>
            </article>
            <article class="company-cert-card">
                <h3>ISO 45001:2018</h3>
                <p>Occupational health &amp; safety</p>
            </article>
            <article class="company-cert-card">
                <h3>ISO 14001:2015</h3>
                <p>Environmental management</p>
            </article>
        </div>
    </div>
</section>

<section class="company-about">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-5 order-lg-2">
                <span class="company-eyebrow">Who we are</span>
                <h2 class="company-section-title">Specialists in industrial heating</h2>
                <p class="company-section-text">We are a specialist manufacturer of tubular heaters, mica and ceramic heaters, infrared systems, temperature sensors, and control accessories. From prototype to production run, our team works closely with customers to deliver heating systems that fit exact thermal, mechanical, and electrical requirements.</p>
            </div>
            <div class="col-lg-6 order-lg-1 mt-5 mt-lg-0">
                <div class="company-hero__image">
                    <img src="images/manifold-tubular-heaters.jpg" alt="Manifold tubular heaters at Masterheat Industries" class="img-fluid" loading="lazy" />
                </div>
            </div>
        </div>
    </div>
</section>

<section class="company-services">
    <div class="container">
        <div class="text-center mb-5">
            <span class="company-eyebrow">What we do</span>
            <h2 class="company-section-title">Engineering, manufacturing &amp; support</h2>
        </div>
        <div class="row">
            <div class="col-md-4 mb-4 mb-md-0">
                <div class="company-card">
                    <div class="company-card__icon"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></div>
                    <h3>Application engineering</h3>
                    <p>We help specify the right heater type, watt density, materials, and termination for your process.</p>
                </div>
            </div>
            <div class="col-md-4 mb-4 mb-md-0">
                <div class="company-card">
                    <div class="company-card__icon"><i class="fa fa-industry" aria-hidden="true"></i></div>
                    <h3>In-house manufacturing</h3>
                    <p>In-house production gives us direct control over quality and lead times.</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="company-card">
                    <div class="company-card__icon"><i class="fa fa-life-ring" aria-hidden="true"></i></div>
                    <h3>Support &amp; service</h3>
                    <p>Technical guidance, refurbishment, and responsive communication for industrial and commercial applications.</p>
                </div>
            </div>
        </div>
    </div>
</section>

<section class="company-expertise">
    <div class="container">
        <div class="row">
            <div class="col-lg-5">
                <span class="company-eyebrow">Product expertise</span>
                <h2 class="company-section-title">Solutions across industries</h2>
                <p class="company-section-text">Our catalogue covers a wide range of industrial heating applications, including:</p>
                <ul>
                    <li>Flanged immersion heaters for calorifiers and hot water systems</li>
                    <li>Mica and ceramic band and strip heaters</li>
                    <li>Finned air heaters for ducts</li>
                    <li>Defrost heaters for industrial and commercial refrigeration</li>
                    <li>Industrial kitchen equipment heaters</li>
                </ul>
                <a href="ceramic-band-heaters.html" class="btn-cflex dark w-icons high mt-4" title="View all products">View full catalogue <i class="fa fa-arrow-right" aria-hidden="true"></i></a>
            </div>
            <div class="col-lg-6 ml-auto mt-5 mt-lg-0">
                <div class="company-gallery">
                    <img src="images/ceramic-strip-heaters.jpg" alt="Ceramic strip heaters" loading="lazy" />
                    <img src="images/micro-coil-heaters.jpg" alt="Micro coil heaters" loading="lazy" />
                    <img src="images/pid-controllers.jpg" alt="Temperature controllers" loading="lazy" />
                </div>
            </div>
        </div>
    </div>
</section>

<section class="company-location">
    <div class="container">
        <div class="company-facility">
            <div class="row">
                <div class="col-lg-7">
                    <h2>Our facility</h2>
                    <address>
                        <strong>Masterheat Industries</strong><br>
                        GSTIN: 27ALUPJ4427B1Z2<br>
                        Pilot Industrial Estate, Gala No. 36,<br>
                        Navghar Road, Samarth Krupa Nagar,<br>
                        Vasai-East, Maharashtra &ndash; 401202
                    </address>
                </div>
                <div class="col-lg-5 mt-4 mt-lg-0">
                    <p><i class="fa fa-phone" aria-hidden="true"></i> <a href="tel:+919358146992">+91 9358146992</a></p>
                    <p><i class="fa fa-envelope" aria-hidden="true"></i> <a href="mailto:info@masterheatindustries.com">info@masterheatindustries.com</a></p>
                    <p><i class="fa fa-globe" aria-hidden="true"></i> <a href="https://www.masterheatindustries.com" target="_blank" rel="noopener">www.masterheatindustries.com</a></p>
                </div>
            </div>
        </div>
    </div>
</section>

<section class="company-why">
    <div class="container">
        <div class="text-center mb-5">
            <span class="company-eyebrow">Why choose us</span>
            <h2 class="company-section-title">Built around your application</h2>
        </div>
        <div class="company-why__grid">
            <div class="company-why__tile">
                <i class="fa fa-users" aria-hidden="true"></i>
                <h3>Customer-focused</h3>
                <p>Solutions shaped around your process and requirements</p>
            </div>
            <div class="company-why__tile">
                <i class="fa fa-wrench" aria-hidden="true"></i>
                <h3>Tailor-made</h3>
                <p>Custom designs from concept through to production</p>
            </div>
            <div class="company-why__tile">
                <i class="fa fa-check-circle" aria-hidden="true"></i>
                <h3>Quality built-in</h3>
                <p>Controlled manufacturing with tested outputs</p>
            </div>
            <div class="company-why__tile">
                <i class="fa fa-clock-o" aria-hidden="true"></i>
                <h3>Fast turnaround</h3>
                <p>From small batches to volume production orders</p>
            </div>
        </div>
    </div>
</section>

<section class="company-cta">
    <div class="container">
        <h2>Ready to discuss your heating requirement?</h2>
        <p>Share your application details and our team will recommend the right product or custom solution.</p>
        <div class="company-cta__actions">
            <a href="contact-us.html" class="btn-cflex dark w-icons high" title="Contact us">Contact Us <i class="fa fa-arrow-right" aria-hidden="true"></i></a>
            <a href="enquiry.html" class="btn-cflex inv w-icons text-dark high" title="Request a quote">Request a Quote <i class="fa fa-arrow-right" aria-hidden="true"></i></a>
        </div>
    </div>
</section>
  </div>
</div>
"""

EDIT_START = '<!-- InstanceBeginEditable name="EditRegion3" -->'
EDIT_END = '<!-- InstanceEndEditable -->'


def build_company_html() -> str:
    clients = (ROOT / "clients.html").read_text(encoding="utf-8")

    # Title and meta
    clients = re.sub(
        r"<title>.*?</title>",
        "<title>Company | Masterheat Industries - Industrial Heating Solutions</title>",
        clients,
        count=1,
        flags=re.DOTALL,
    )
    clients = re.sub(
        r'<meta name="description" content="[^"]*">',
        '<meta name="description" content="Masterheat Industries designs and manufactures industrial heating elements and systems in-house. Learn about our facility, certifications, and engineering capabilities.">',
        clients,
        count=1,
    )

    # Head assets for company page layout
    extra_head = """
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<link rel="stylesheet" href="css/company.css">
"""
    clients = clients.replace(
        '<link rel="stylesheet" href="css/table.css">',
        '<link rel="stylesheet" href="css/table.css">' + extra_head,
        1,
    )

    clients = clients.replace("<body>", '<body class="company">', 1)

    # Replace editable region
    pattern = re.compile(
        re.escape(EDIT_START) + r".*?" + re.escape(EDIT_END),
        re.DOTALL,
    )
    clients = pattern.sub(EDIT_START + COMPANY_MAIN + EDIT_END, clients, count=1)

    # Nav/footer in shell (before site-wide pass)
    clients = clients.replace('href="clients.html">Clients', 'href="company.html">Company')

    return clients


def update_all_links():
    updated = 0
    for path in ROOT.rglob("*.html"):
        if path.name == "clients.html":
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        text = text.replace('href="clients.html"', 'href="company.html"')
        text = text.replace(">Clients</a>", ">Company</a>")
        if text != original:
            path.write_text(text, encoding="utf-8")
            updated += 1
    return updated


def main():
    company_html = build_company_html()
    (ROOT / "company.html").write_text(company_html, encoding="utf-8")
    print("Created company.html")

    count = update_all_links()
    print(f"Updated links in {count} HTML files")

    clients_path = ROOT / "clients.html"
    if clients_path.exists():
        clients_path.unlink()
        print("Removed clients.html")


if __name__ == "__main__":
    main()
