import csv
import os
from datetime import datetime
try:
    from catalog_db import upsert_product, init_db
except ModuleNotFoundError:
    from .catalog_db import upsert_product, init_db

def import_products(csv_path):
    print(f"Importing products from {csv_path} ...")
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))
        count = 0
        # Calculate top products for each section
        sorted_by_rating = sorted(reader, key=lambda r: float(r.get('rating', '0') or 0), reverse=True)
        sorted_by_percent_off = sorted(reader, key=lambda r: float(r.get('percent_off', '0') or 0), reverse=True)
        trending_asins = set(r.get('asin', '') for r in sorted_by_rating[:20])
        big_sale_asins = set(r.get('asin', '') for r in sorted_by_percent_off[:20])
        for row in reader:
            # Prepare product dict for upsert
            # Robustly parse ratings_count
            num_reviews_val = row.get('num_reviews', '0')
            try:
                ratings_count = int(num_reviews_val)
            except Exception:
                print(f"[WARN] Invalid num_reviews value '{num_reviews_val}' for ASIN {row.get('asin', '')}, setting to 0.")
                ratings_count = 0
            percent_off_val = float(row.get('percent_off', '0') or 0)
            asin = row.get('asin', '')
            product = {
                'asin': asin,
                'name': row.get('name', ''),
                'description': row.get('description', ''),
                'summary': row.get('summary', ''),
                'image_url': row.get('image_url', ''),
                'images': row.get('images', ''),
                'brand': row.get('brand', ''),
                'badge': row.get('badge', ''),
                'prime': int(row.get('prime', '0') == 'True' or row.get('prime', '0') == '1'),
                'percent_off': percent_off_val,
                'shipping': row.get('shipping', ''),
                'stock_status': row.get('stock_status', ''),
                'price': float(row.get('price', '0') or 0),
                'original_price': float(row.get('original_price', '0') or 0),
                'rating': float(row.get('rating', '0') or 0),
                'ratings_count': ratings_count,
                'trending': 1 if asin in trending_asins else 0,
                'on_sale': 1 if percent_off_val > 10 else 0,
                'big_sale': 1 if asin in big_sale_asins else 0,
                'last_checked': datetime.utcnow().isoformat(),
                'affiliate_link': row.get('affiliate_link', ''),
                'review_summary': row.get('review_summary', ''),
            }
            upsert_product(product)
            count += 1
    print(f"Imported {count} products into the database.")
    

if __name__ == '__main__':
    init_db()
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    csv_path = os.path.join(project_root, 'bestseller_products_with_reviews.csv')
    import_products(csv_path)
