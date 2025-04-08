from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import psycopg
from app.routers import books

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

app.include_router(books.router)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

app.mount("/", StaticFiles(directory="static", html=True), name="static")
