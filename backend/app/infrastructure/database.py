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
        
        # ユーザーテーブル
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            display_name VARCHAR(100) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )
        """)
        
        # 既存のbooksテーブル（そのまま維持）
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            borrower_name TEXT,
            return_date DATE
        )
        """)
        
        # フィードバックテーブルも更新（もし存在すれば）
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            author_name TEXT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            github_issue_url TEXT
        )
        """)
        
        conn.commit()
        conn.close()
