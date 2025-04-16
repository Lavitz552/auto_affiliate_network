import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from src.affiliate import setup_affiliate, schedule_content_generation
from src.scheduler import continuous_scheduler
from src.analytics import get_dashboard_data

load_dotenv("config.env")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def startup_event():
    setup_affiliate()
    schedule_content_generation()
    continuous_scheduler()

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    data = get_dashboard_data()
    return data  # Will be replaced with real HTML rendering

@app.get("/")
def root():
    return RedirectResponse(url="/dashboard")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
