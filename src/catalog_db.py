import sqlite3
from datetime import datetime

DB_PATH = 'catalog.db'

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asin TEXT UNIQUE,
                name TEXT,
                description TEXT,
                summary TEXT,
                image_url TEXT,
                images TEXT,
                brand TEXT,
                badge TEXT,
                prime INTEGER,
                percent_off REAL,
                shipping TEXT,
                stock_status TEXT,
                price REAL,
                original_price REAL,
                rating REAL,
                ratings_count INTEGER,
                trending INTEGER,
                on_sale INTEGER,
                big_sale INTEGER,
                last_checked TEXT,
                affiliate_link TEXT,
                review_summary TEXT
            )
        ''')
        conn.commit()

def upsert_product(product):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO products (asin, name, description, summary, image_url, price, original_price, percent_off, rating, ratings_count, trending, on_sale, big_sale, last_checked, affiliate_link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(asin) DO UPDATE SET
                name=excluded.name,
                description=excluded.description,
                summary=excluded.summary,
                image_url=excluded.image_url,
                price=excluded.price,
                original_price=excluded.original_price,
                percent_off=excluded.percent_off,
                rating=excluded.rating,
                ratings_count=excluded.ratings_count,
                trending=excluded.trending,
                on_sale=excluded.on_sale,
                big_sale=excluded.big_sale,
                last_checked=excluded.last_checked,
                affiliate_link=excluded.affiliate_link
        ''', (
            product['asin'],
            product['name'],
            product.get('description', ''),
            product.get('summary', ''),
            product.get('image_url', ''),
            product.get('price', 0.0),
            product.get('original_price', 0.0),
            product.get('percent_off', 0.0),
            product.get('rating', 0.0),
            product.get('ratings_count', 0),
            int(product.get('trending', False)),
            int(product.get('on_sale', False)),
            int(product.get('big_sale', False)),
            product.get('last_checked', datetime.utcnow().isoformat()),
            product.get('affiliate_link', '')
        ))
        conn.commit()

def get_section_products(section):
    with get_connection() as conn:
        c = conn.cursor()
        if section == 'trending':
            c.execute('SELECT * FROM products WHERE trending=1 ORDER BY last_checked DESC')
        elif section == 'on_sale':
            c.execute('SELECT * FROM products WHERE on_sale=1 ORDER BY percent_off DESC')
        elif section == 'big_sale':
            c.execute('SELECT * FROM products WHERE big_sale=1 ORDER BY percent_off DESC')
        else:
            c.execute('SELECT * FROM products ORDER BY last_checked DESC')
        return [dict(zip([col[0] for col in c.description], row)) for row in c.fetchall()]

# Call this once at startup to ensure DB exists
if __name__ == '__main__':
    init_db()
    print('Catalog DB initialized.')
