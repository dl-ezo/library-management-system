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
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

app.include_router(books.router)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
