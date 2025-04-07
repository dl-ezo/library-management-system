import os
from typing import Optional
import psycopg
from app.config import settings

def get_connection():
    """データベース接続を取得する"""
    if settings.DATABASE_URL:
        return psycopg.connect(settings.DATABASE_URL)
    else:
        return None

def init_db():
    """データベースを初期化する"""
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                borrower_name TEXT,
                return_date DATE
            )
            """)
        conn.commit()
        conn.close()
