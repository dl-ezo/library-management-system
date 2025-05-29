from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import psycopg
from app.routers import books, feedback, auth
from app.infrastructure.database import init_db

app = FastAPI(title="Company Library Management System")

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://lib-mgmt-dl-ezo-frontend-9f84ec585ef2.herokuapp.com",  # Frontend Heroku domain
        "http://localhost:3000",    # For local development
        "http://localhost:5173",    # For Vite dev server
        "*",                        # Allow all origins as fallback
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(books.router, prefix="/api")
app.include_router(feedback.router, prefix="/api")
app.include_router(auth.router, prefix="/api")

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.get("/api/healthz")
async def api_healthz():
    return {"status": "ok"}

# データベースを初期化
init_db()

if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
