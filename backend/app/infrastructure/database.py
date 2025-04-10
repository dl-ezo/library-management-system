import os
from typing import Optional
import psycopg
from app.config import settings

# テストモードかどうかを確認
is_test_mode = os.environ.get("TEST_MODE", "0") == "1"

def get_connection():
    """データベース接続を取得する"""
    if is_test_mode:
        return None
    
    # 通常モードの場合はPostgreSQLを使用
    if settings.DATABASE_URL:
        db_url = settings.DATABASE_URL
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
        return psycopg.connect(db_url)
    else:
        return None

def init_db():
    """データベースを初期化する"""
    conn = get_connection()
    if conn:
        # PostgreSQL用のテーブル作成クエリ
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            borrower_name TEXT,
            return_date DATE
        )
        """)
        conn.commit()
        conn.close()
