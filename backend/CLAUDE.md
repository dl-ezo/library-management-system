# Library Management System - Backend Tests

## テスト実行方法

テストを実行するには、以下のいずれかの方法を使用してください：

### Dockerを使用してテストを実行する（推奨）

```bash
cd /home/ezo/ghq/github.com/dl-ezo/library-management-system
docker build -f backend/Dockerfile.test -t backend-test ./backend
docker run --rm backend-test
```

これにより、すべてのテストが実行されます。

### ローカルでテストを実行する方法（データベースのセットアップが必要）

1. PostgreSQLが実行されていることを確認
2. テスト用データベースを作成：
   ```bash
   docker exec postgres psql -U postgres -c "CREATE DATABASE library_test"
   ```
3. テストを実行
   ```bash
   cd backend
   python -m pytest
   ```

## API接続に関する問題

APIへの接続に問題がある場合は、以下の点を確認してください：

1. エンドポイントが `/api/books/` で終わるスラッシュを含んでいるか
2. バックエンドのルーティングが `/api` プレフィックスを使用しているか
3. フロントエンドのAPI設定でベースURLが正しく設定されているか

## SQLiteでテストを実行する

テスト用にSQLiteを使用する場合は、以下のように環境変数を設定します：

```bash
export TEST_MODE=1
python -m pytest
```