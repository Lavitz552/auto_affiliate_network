import os
import openai

from openai import OpenAI
import os
import json

def generate_article(product_info, niche, affiliate_tag):
    """
    Generate an SEO-optimized affiliate article, meta tags, and structured data using OpenAI.
    Returns: (article_html, meta_title, meta_desc, meta_keywords, structured_data_json)
    """
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    prompt = (
        f"Write a detailed, SEO-optimized review for the following product in the {niche} niche. "
        f"Include pros, cons, and a call-to-action with this Amazon affiliate tag: {affiliate_tag}. "
        f"Product info: {product_info}\n"
        f"Return your answer as JSON with these keys: article_html, meta_title, meta_desc, meta_keywords, structured_data_json. "
        f"Meta title should be 60 chars or less, meta desc 155 chars or less, keywords as comma-separated list. "
        f"Structured data should be JSON-LD for a Product review."
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    ai_result = response.choices[0].message.content
    # Try to parse JSON, fallback to just the article if needed
    try:
        data = json.loads(ai_result)
        return (
            data.get("article_html", ""),
            data.get("meta_title", ""),
            data.get("meta_desc", ""),
            data.get("meta_keywords", ""),
            data.get("structured_data_json", "")
        )
    except Exception:
        return (ai_result, "", "", "", "")
