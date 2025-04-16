import os
import openai

def generate_article(product_info, niche, affiliate_tag):
    """
    Generate an SEO-optimized affiliate article using OpenAI.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = (
        f"Write a detailed, SEO-optimized review for the following product in the {niche} niche. "
        f"Include pros, cons, and a call-to-action with this Amazon affiliate tag: {affiliate_tag}. "
        f"Product info: {product_info}"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800
    )
    return response.choices[0].message['content']
