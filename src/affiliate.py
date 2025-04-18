import os

def setup_affiliate():
    # Placeholder: Setup affiliate logic, e.g., check config, initialize DB
    pass

import os
from .content_generator import generate_article

from .product_discovery import discover_new_products

NICHES = ["tech gadgets", "home fitness", "kitchen tools", "pet supplies"]
PRODUCTS = [
    {"name": "Wireless Earbuds", "asin": "B07PXGQC1Q", "desc": "High-quality sound and long battery life.", "niche": "Tech Gadgets"},
    {"name": "Adjustable Dumbbells", "asin": "B07XQXZXJC", "desc": "Save space and switch weights easily.", "niche": "Home Fitness"},
    {"name": "Air Fryer", "asin": "B07W7X2F5D", "desc": "Cook healthier meals with less oil.", "niche": "Kitchen Tools"},
    {"name": "Robot Vacuum", "asin": "B07DL4QY5V", "desc": "Automate your home cleaning tasks.", "niche": "Tech Gadgets"},
    {"name": "Standing Desk Converter", "asin": "B079JB5FF6", "desc": "Switch between sitting and standing at work.", "niche": "Home Fitness"},
    {"name": "Bluetooth Tracker", "asin": "B07P6Y7954", "desc": "Never lose your keys or wallet again.", "niche": "Tech Gadgets"},
    {"name": "Smart Watch", "asin": "B07T81554H", "desc": "Track fitness, calls, and notifications.", "niche": "Tech Gadgets"},
    {"name": "Eco Products", "asin": "B08J4C1N4C", "desc": "Sustainable and eco-friendly daily items.", "niche": "Home Fitness"},
    {"name": "Home Automation", "asin": "B07FJGGWJL", "desc": "Control lights and devices remotely.", "niche": "Tech Gadgets"},
    {"name": "AI Gadgets", "asin": "B08V8K4Y4V", "desc": "Smart AI-powered home and office tools.", "niche": "Tech Gadgets"},
    {"name": "Health Tech", "asin": "B07VJYZF3L", "desc": "Monitor your health with smart devices.", "niche": "Home Fitness"},
    {"name": "Portable Projector", "asin": "B07VJYZF3L", "desc": "Project movies anywhere, anytime.", "niche": "Tech Gadgets"},
    {"name": "Kitchen Tools", "asin": "B07RJPWXN9", "desc": "Modernize your kitchen with smart gadgets.", "niche": "Kitchen Tools"},
    {"name": "Automatic Pet Feeder", "asin": "B07RJPWXN9", "desc": "Schedule and control your pet's meals from anywhere.", "niche": "Pet Supplies"}
]

import subprocess

def schedule_content_generation():
    affiliate_tag = os.getenv("AMAZON_ASSOCIATE_TAG", "")
    static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
    os.makedirs(static_dir, exist_ok=True)
    # Always include core products, but discover new ones each cycle
    all_products = PRODUCTS + discover_new_products()
    GA_TRACKING_ID = os.getenv("GA_TRACKING_ID", "")
    ga_script = f"""
    <!-- Google Analytics -->
    <script async src='https://www.googletagmanager.com/gtag/js?id={GA_TRACKING_ID}'></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{GA_TRACKING_ID}');
    </script>
    <!-- End Google Analytics -->
    """ if GA_TRACKING_ID else ""
    deploy_counter = 0
    for niche in NICHES:
        print(f"[Generator] Generating content for niche: {niche}")
        niche_slug = niche.replace(" ", "-").lower()
        site_folder = os.path.join(static_dir, niche_slug)
        os.makedirs(site_folder, exist_ok=True)
        product_links = []
        # Only include products for this niche
        niche_products = [p for p in all_products if p.get('niche', '').lower() == niche.lower()]
        import csv
        log_path = os.path.join(static_dir, "generated_articles.csv")
        # Load generated articles log
        generated_set = set()
        if os.path.exists(log_path):
            with open(log_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if len(row) == 2:
                        generated_set.add((row[0], row[1]))  # (product_name, niche)
        for product in niche_products:
            file_name = f"{product['name'].replace(' ', '_').lower()}.html"
            file_path = os.path.join(site_folder, file_name)
            # Check persistent log for repeat
            if (product['name'], niche) in generated_set or os.path.exists(file_path):
                print(f"[Generator] Skipping {product['name']} in {niche} (already generated)")
                product_links.append((product['name'], file_name))
                continue
            print(f"[Generator] Generating article for product: {product['name']} in {niche}")
            article_html, meta_title, meta_desc, meta_keywords, structured_data_json = generate_article(product["desc"], niche, affiliate_tag)
            # Logo and recommended products section
            logo_html = "<img src='/static/logo.png' alt='Autom8Deals Logo' style='width:120px;margin:24px auto;display:block;' />"
            # List all recommended products (for profit tracking and cross-promotion)
            recommended_html = "<hr><h3 style='text-align:center;'>More Top Picks from Autom8Deals</h3><ul style='max-width:480px;margin:0 auto 32px auto;'>"
            for rec in all_products:
                recommended_html += f"<li><a href='https://www.amazon.com/dp/{rec['asin']}?tag={affiliate_tag}' target='_blank'>{rec['name']}</a></li>"
            recommended_html += "</ul>"
            # Placeholder for star rating (to be filled by scraping/API in the future)
            star_rating_html = "<div style='text-align:center;margin:12px 0;'><span style='font-size:22px;color:#FFD700;'>★★★★★</span> <span style='color:#888;font-size:16px;'>(4.7/5 avg)</span></div>"
            html = f"""
            <html>
            <head>
                <title>{meta_title or (product['name'] + ' - ' + niche)}</title>
                <meta name='description' content='{meta_desc or product['desc']}' />
                <meta name='keywords' content='{meta_keywords or ''}' />
                <script type='application/ld+json'>{structured_data_json or ''}</script>
                {ga_script}
            </head>
            <body style='font-family:sans-serif;background:#fff;color:#222;'>
                {logo_html}
                <h1 style='text-align:center'>{product['name']} <span style='font-size:16px;color:#888;'>({niche})</span></h1>
                {star_rating_html}
                <div style='max-width:600px;margin:24px auto;'>{article_html}</div>
                <div style='text-align:center;margin:32px 0;'><a href='https://www.amazon.com/dp/{product['asin']}?tag={affiliate_tag}' target='_blank' style='background:#FFB800;color:#0A2540;padding:12px 28px;border-radius:6px;text-decoration:none;font-weight:bold;'>Buy on Amazon</a></div>
                {recommended_html}
            </body></html>
            """
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)
            # Log this product/niche as generated
            with open(log_path, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([product['name'], niche])
            product_links.append((product['name'], file_name))
            deploy_counter += 1
            # Netlify deploys are now handled externally via batch file, so no deploy here.
        # Generate index.html for this niche
        index_html = f"""
        <html><head><title>{niche} - Autom8Deals</title></head>
        <body style='font-family:sans-serif;background:#fff;color:#222;'>
            <h1 style='text-align:center;'>{niche} Picks</h1>
            <ul style='max-width:480px;margin:24px auto;'>
        """
        for prod_name, prod_file in product_links:
            index_html += f"<li><a href='{prod_file}'>{prod_name}</a></li>"
        index_html += """
            </ul>
            <hr style='margin:32px 0;'>
            <p style='text-align:center;font-size:14px;color:#888;'>Affiliate content generated by Autom8Deals. Updated automatically.</p>
            <p style='text-align:center;'><a href='../index.html'>Back to Home</a></p>
        </body></html>
        """
        with open(os.path.join(site_folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(index_html)
    # Netlify deploys are now handled externally via batch file. No deploy triggered here.
