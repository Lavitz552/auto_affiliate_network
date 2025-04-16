# Automated Affiliate Website Network

This project automatically generates and manages profitable affiliate websites with minimal user intervention. It includes:

- Automated content generation using your ChatGPT Plus API key
- Affiliate link integration (Amazon Associates by default)
- SEO-optimized articles and product reviews
- Backend analytics dashboard for tracking site/item performance
- Automated product/keyword discovery
- Scalable architecture for launching multiple sites

## Quick Start Guide

1. **Install Requirements**
   - Run: `pip install -r requirements.txt`

2. **Add Your API Keys**
   - Open `config.env` and paste your OpenAI API key
   - Add your Amazon Associates tag (after signup)

3. **Run the Program**
   - Run: `python main.py`
   - Follow the prompts to set up your first site

4. **Apply for Affiliate Programs**
   - Start with [Amazon Associates](https://affiliate-program.amazon.com/)
   - Paste your tag into `config.env` when ready

5. **Monitor Analytics**
   - Access the dashboard at `http://localhost:8000/dashboard`
   - See which niches/items perform best and get strategy tips

6. **Scale Up**
   - Use the dashboard to add new sites/niches with a click

---

## Tech Stack
- Python (FastAPI backend)
- Next.js (frontend/dashboard)
- SQLite (database)
- Docker (deployment)

---

## Next Steps
- Get your OpenAI API key ready
- After launch, apply for Amazon Associates
- Let the system run and monitor analytics for growth suggestions

---

For help, just ask Cascade!
