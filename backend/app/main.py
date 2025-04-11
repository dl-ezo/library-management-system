from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import psycopg
from app.routers import books
from app.infrastructure.init_data import initialize_repository
from app.infrastructure.repositories import InMemoryBookRepository

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

book_repo = InMemoryBookRepository()
initialize_repository(book_repo)

from app.dependencies import get_book_service
from app.application.services import BookService

app.dependency_overrides[get_book_service] = lambda: BookService(repository=book_repo)
app.include_router(books.router)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.get("/api/healthz")
async def api_healthz():
    return {"status": "ok"}

if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
