import os
import sqlite3
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'catalog.db')

app = Flask(__name__)

@app.route('/api/search')
def search():
    q = request.args.get('q', '').strip().lower()
    if not q:
        return jsonify({'results': []})
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Search in name, description, summary, and review_summary
    c.execute('''SELECT asin, name, description, summary, image_url, price, original_price, percent_off, rating, ratings_count, affiliate_link, review_summary FROM products WHERE \
        lower(name) LIKE ? OR lower(description) LIKE ? OR lower(summary) LIKE ? OR lower(review_summary) LIKE ? ORDER BY rating DESC LIMIT 30''',
        (f'%{q}%', f'%{q}%', f'%{q}%', f'%{q}%'))
    rows = c.fetchall()
    conn.close()
    results = []
    for row in rows:
        results.append({
            'asin': row[0],
            'name': row[1],
            'description': row[2],
            'summary': row[3],
            'image_url': row[4],
            'price': row[5],
            'original_price': row[6],
            'percent_off': row[7],
            'rating': row[8],
            'ratings_count': row[9],
            'affiliate_link': row[10],
            'review_summary': row[11],
        })
    return jsonify({'results': results})

@app.route('/')
def health():
    return 'OK', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
