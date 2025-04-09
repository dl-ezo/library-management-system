import pytest
import os
from app.main import app

# テスト用にインメモリSQLiteデータベースを使用するための設定
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/library_test"

@pytest.fixture(scope="function", autouse=True)
def setup_test_db():
    """テスト用データベースのセットアップと終了後のクリーンアップ"""
    from app.infrastructure.database import get_connection, init_db
    
    # データベースを初期化
    init_db()
    
    # テスト実行
    yield
    
    # テスト後のクリーンアップ（テーブルをクリア）
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE books RESTART IDENTITY CASCADE")
        conn.commit()
        conn.close()