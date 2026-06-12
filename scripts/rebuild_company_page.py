#!/usr/bin/env python3
"""Replace legacy company page content with India-focused modern layout."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPANY_HTML = ROOT / "company" / "index.html"

NEW_MAIN = """<div class="company-page">
<section class="company-hero">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-6 ani" data-josh-anim-name="slideInUp">
                <span class="company-eyebrow">About Master Heat Industries</span>
                <h1 class="company-hero__title">Industrial heating solutions, made in India</h1>
                <p class="company-lead">Master Heat Industries designs and manufactures industrial heating elements and systems from our facility in Vasai, Maharashtra. We support OEMs, plant engineers, and commercial operators with reliable, application-specific heating solutions.</p>
                <div class="company-hero__actions">
                    <a href="../master-heat-tech-products/index.html" class="btn-cflex dark w-icons high" title="Explore products">Explore Products <i class="fa fa-arrow-right" aria-hidden="true"></i></a>
                    <a href="../contacts-us/index.html" class="btn-cflex inv w-icons text-dark high" title="Contact us">Contact Us <i class="fa fa-arrow-right" aria-hidden="true"></i></a>
                </div>
            </div>
            <div class="col-lg-6 mt-5 mt-lg-0 ani" data-josh-anim-name="slideInRight">
                <div class="company-hero__image">
                    <img src="../assets/flexible-tubular-heaters.jpg" alt="Industrial tubular heaters manufactured by Master Heat Industries" class="img-fluid" loading="lazy" />
                </div>
            </div>
        </div>
    </div>
</section>

<section class="company-stats">
    <div class="container">
        <div class="company-stats__grid">
            <div class="company-stats__item">
                <span class="company-stats__value">Vasai, Maharashtra</span>
                <span class="company-stats__label">India manufacturing base</span>
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

<section class="company-about">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-5 order-lg-2 ani" data-josh-anim-name="slideInRight">
                <span class="company-eyebrow">Who we are</span>
                <h2 class="company-section-title">Specialists in industrial heating</h2>
                <p class="company-section-text">We are a specialist manufacturer of tubular heaters, mica and ceramic heaters, infrared systems, temperature sensors, and control accessories. From prototype to production run, our team works closely with customers to deliver heating systems that fit exact thermal, mechanical, and electrical requirements.</p>
            </div>
            <div class="col-lg-6 order-lg-1 mt-5 mt-lg-0 ani" data-josh-anim-name="slideInUp">
                <div class="company-hero__image">
                    <img src="../assets/manifold-tubular-heaters.jpg" alt="Manifold tubular heaters at Master Heat Industries" class="img-fluid" loading="lazy" />
                </div>
            </div>
        </div>
    </div>
</section>

<section class="company-services">
    <div class="container">
        <div class="text-center mb-5 ani" data-josh-anim-name="slideInUp">
            <span class="company-eyebrow">What we do</span>
            <h2 class="company-section-title">Engineering, manufacturing &amp; support</h2>
        </div>
        <div class="row">
            <div class="col-md-4 mb-4 mb-md-0 ani" data-josh-anim-name="slideInUp">
                <div class="company-card">
                    <div class="company-card__icon"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></div>
                    <h3>Application engineering</h3>
                    <p>We help specify the right heater type, watt density, materials, and termination for your process.</p>
                </div>
            </div>
            <div class="col-md-4 mb-4 mb-md-0 ani" data-josh-anim-name="slideInUp">
                <div class="company-card">
                    <div class="company-card__icon"><i class="fa fa-industry" aria-hidden="true"></i></div>
                    <h3>In-house manufacturing</h3>
                    <p>Production at Pilot Industrial Estate, Vasai-East gives us direct control over quality and lead times.</p>
                </div>
            </div>
            <div class="col-md-4 ani" data-josh-anim-name="slideInUp">
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
            <div class="col-lg-5 ani" data-josh-anim-name="slideInUp">
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
                <a href="../master-heat-tech-products/index.html" class="btn-cflex dark w-icons high mt-4" title="View all products">View full catalogue <i class="fa fa-arrow-right" aria-hidden="true"></i></a>
            </div>
            <div class="col-lg-6 ml-auto mt-5 mt-lg-0 ani" data-josh-anim-name="slideInRight">
                <div class="company-gallery">
                    <img src="../assets/ceramic-strip-heaters.jpg" alt="Ceramic strip heaters" loading="lazy" />
                    <img src="../assets/micro-coil-heaters.jpg" alt="Micro coil heaters" loading="lazy" />
                    <img src="../assets/pid-controllers.jpg" alt="Temperature controllers" loading="lazy" />
                </div>
            </div>
        </div>
    </div>
</section>

<section class="company-location">
    <div class="container">
        <div class="company-facility ani" data-josh-anim-name="zoomIn">
            <div class="row">
                <div class="col-lg-7">
                    <h2>Our facility</h2>
                    <address>
                        <strong>Master Heat Industries</strong><br>
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
        <div class="text-center mb-5 ani" data-josh-anim-name="slideInUp">
            <span class="company-eyebrow">Why choose us</span>
            <h2 class="company-section-title">Built around your application</h2>
        </div>
        <div class="company-why__grid ani" data-josh-anim-name="fadeIn">
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
    <div class="container ani" data-josh-anim-name="zoomIn">
        <h2>Ready to discuss your heating requirement?</h2>
        <p>Share your application details and our team will recommend the right product or custom solution.</p>
        <div class="company-cta__actions">
            <a href="../contacts-us/index.html" class="btn-cflex dark w-icons high" title="Contact us">Contact Us <i class="fa fa-arrow-right" aria-hidden="true"></i></a>
            <a data-fancybox href="#product-modal-form-contacts" class="btn-cflex inv w-icons text-dark high" title="Request a quote">Request a Quote <i class="fa fa-arrow-right" aria-hidden="true"></i></a>
        </div>
    </div>
</section>
</div>
"""

START = '<section class="intro-content"><div class="container"><div class="row"><div class="col-lg-6 ani" data-josh-anim-name="slideInUp"><h1 class="subtitle"> COMPANY</h1>'
END = '<section class="cta container-fluid">'


def main():
    content = COMPANY_HTML.read_text(encoding="utf-8")

    if "company-page" in content:
        print("Company page already rebuilt.")
        return

    start_idx = content.find(START)
    end_idx = content.find(END)
    if start_idx == -1 or end_idx == -1:
        raise SystemExit(f"Markers not found (start={start_idx}, end={end_idx})")

    content = content[:start_idx] + NEW_MAIN + content[end_idx:]

    css_link = '    <link rel="stylesheet" href="../assets/company.css" media="all" />\n'
    if "company.css" not in content:
        content = content.replace(
            '    <link rel="stylesheet" href="../assets/header.css" media="all" />',
            '    <link rel="stylesheet" href="../assets/header.css" media="all" />\n' + css_link,
        )

    meta_old = 'content="Company - Master Heat Industries"'
    meta_new = 'content="About Us | Master Heat Industries - Industrial heating manufacturer in Vasai, Maharashtra"'
    content = content.replace('<title>Company - Master Heat Industries</title>', '<title>About Us | Master Heat Industries</title>')
    content = content.replace('content="Company - Master Heat Industries"', meta_new, 2)

    COMPANY_HTML.write_text(content, encoding="utf-8")
    print("Rebuilt company/index.html")


if __name__ == "__main__":
    main()
