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

## 依存関係管理の重要事項

新しいPythonパッケージを追加する際は、以下の**手順を必ず守ってください**：

### ⚠️ 重要な手順（CI/CDテスト失敗を防ぐため）

1. **`pyproject.toml`を更新** - Poetry用の依存関係定義（CI/CDで使用）
2. **`requirements.txt`を更新** - Herokuデプロイ用の依存関係定義
3. **`poetry lock`を実行** - poetry.lockファイルを更新（**これを忘れるとCI/CDが失敗します**）

### 実行手順

```bash
# 1. pyproject.tomlに依存関係を追加
# 2. requirements.txtに依存関係を追加
# 3. 重要：poetry.lockファイルを更新
cd backend
poetry lock
```

### 例：Anthropic APIパッケージの追加

```toml
# pyproject.toml の [tool.poetry.dependencies] セクションに追加
anthropic = "^0.40.0"
```

```txt
# requirements.txt に追加
anthropic>=0.40.0
```

```bash
# 必須：poetry.lockを更新
poetry lock
```

### よくある失敗パターン

❌ **やってはいけないこと**：
- `pyproject.toml`のみ更新して`poetry lock`を忘れる
- `requirements.txt`の更新を忘れる

✅ **正しい手順**：
1. 両方のファイルを更新
2. `poetry lock`を実行
3. 変更をコミット・プッシュ

**注意**: `poetry.lock`の更新を忘れると「pyproject.toml changed significantly since poetry.lock was last generated」エラーでCI/CDテストが失敗します。