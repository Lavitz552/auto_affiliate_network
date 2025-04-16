import os

def setup_affiliate():
    # Placeholder: Setup affiliate logic, e.g., check config, initialize DB
    pass

import os
from .content_generator import generate_article

from .product_discovery import discover_new_products

NICHES = ["tech gadgets", "home fitness", "kitchen tools", "pet supplies"]
PRODUCTS = [
    {"name": "Wireless Earbuds", "asin": "B07PXGQC1Q", "desc": "High-quality wireless earbuds with noise cancelling."},
    {"name": "Adjustable Dumbbells", "asin": "B08F2XQ2FZ", "desc": "Space-saving adjustable dumbbells for home workouts."},
    {"name": "Air Fryer", "asin": "B07W67NQJN", "desc": "Healthier cooking with rapid air technology."},
    {"name": "Automatic Pet Feeder", "asin": "B07RJPWXN9", "desc": "Schedule and control your pet's meals from anywhere."}
]

def schedule_content_generation():
    affiliate_tag = os.getenv("AMAZON_ASSOCIATE_TAG", "")
    static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
    os.makedirs(static_dir, exist_ok=True)
    # Always include core products, but discover new ones each cycle
    all_products = PRODUCTS + discover_new_products()
    for niche in NICHES:
        for product in all_products:
            article = generate_article(product["desc"], niche, affiliate_tag)
            # Generate a simple HTML file for the article
            # Logo and recommended products section
            logo_html = "<img src='/static/logo.png' alt='Autom8Deals Logo' style='width:120px;margin:24px auto;display:block;' />"
            # List all recommended products (for profit tracking and cross-promotion)
            recommended_html = "<hr><h3 style='text-align:center;'>More Top Picks from Autom8Deals</h3><ul style='max-width:480px;margin:0 auto 32px auto;'>"
            for rec in all_products:
                recommended_html += f"<li><a href='https://www.amazon.com/dp/{rec['asin']}?tag={affiliate_tag}' target='_blank'>{rec['name']}</a></li>"
            recommended_html += "</ul>"
            html = f"""
            <html><head><title>{product['name']} - {niche}</title></head>
            <body style='font-family:sans-serif;background:#fff;color:#222;'>
                {logo_html}
                <h1 style='text-align:center'>{product['name']} <span style='font-size:16px;color:#888;'>({niche})</span></h1>
                <p style='max-width:600px;margin:24px auto;'>{article}</p>
                <div style='text-align:center;margin:32px 0;'><a href='https://www.amazon.com/dp/{product['asin']}?tag={affiliate_tag}' target='_blank' style='background:#FFB800;color:#0A2540;padding:12px 28px;border-radius:6px;text-decoration:none;font-weight:bold;'>Buy on Amazon</a></div>
                {recommended_html}
            </body></html>
            "
            site_folder = os.path.join(static_dir, niche.replace(" ", "-").lower())
            os.makedirs(site_folder, exist_ok=True)
            file_path = os.path.join(site_folder, f"{product['name'].replace(' ', '_').lower()}.html")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)
