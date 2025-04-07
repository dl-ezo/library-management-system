# 社内図書管理システム

社内の図書を管理するためのWebアプリケーションです。本の登録、貸出管理、検索機能を提供します。

## 機能

- 本の登録（タイトルのみ）
- 貸出管理（借りる人の名前と返却予定日）
- 検索機能（タイトルと借りている人の名前で検索）
- 図書一覧表示

## 技術スタック

### バックエンド
- FastAPI (Python)
- PostgreSQL（本番環境）/ インメモリDB（開発環境）
- Poetry（パッケージ管理）

### フロントエンド
- React
- TypeScript
- Tailwind CSS
- Vite

## ローカル開発環境のセットアップ

### 前提条件
- Python 3.10以上
- Node.js 18以上
- Poetry
- Git

### バックエンドのセットアップ

```bash
# リポジトリをクローン
git clone https://github.com/dl-ezo/library-management-system.git
cd library-management-system

# バックエンドの依存関係をインストール
cd backend
poetry install

# 開発サーバーを起動
poetry run uvicorn app.main:app --reload
```

バックエンドサーバーは http://localhost:8000 で実行されます。
APIドキュメントは http://localhost:8000/docs で確認できます。

### フロントエンドのセットアップ

```bash
# 別のターミナルで
cd library-management-system/frontend

# 依存関係をインストール
npm install

# 開発サーバーを起動
npm run dev
```

フロントエンドは http://localhost:5173 で実行されます。

## テスト

```bash
# バックエンドのテストを実行
cd backend
poetry run pytest
```

## Herokuへのデプロイ

### 前提条件
- Herokuアカウント
- Heroku CLI
- Heroku API Key

### デプロイ手順

1. Herokuアプリを作成

```bash
heroku create library-management-system
```

2. PostgreSQLアドオンを追加

```bash
heroku addons:create heroku-postgresql:mini
```

3. 環境変数を設定

```bash
heroku config:set PYTHON_VERSION=3.10.0
```

4. デプロイ

```bash
git push heroku main
```

または、GitHub Actionsを使用して自動デプロイを設定することもできます。その場合は、GitHub SecretsにHEROKU_API_KEYとHEROKU_EMAILを設定してください。

## CI/CD

このプロジェクトはGitHub Actionsを使用してCI/CDを設定しています。

- プルリクエスト時にテストが実行されます
- mainブランチへのプッシュ時に自動的にHerokuへデプロイされます

## ドメイン駆動設計（DDD）

このプロジェクトはドメイン駆動設計の原則に従って実装されています。

- `domain`: ドメインモデルとリポジトリインターフェース
- `application`: アプリケーションサービス
- `infrastructure`: リポジトリの実装
- `routers`: APIエンドポイント

## テスト駆動開発（TDD）

このプロジェクトはテスト駆動開発の手法で実装されています。各機能の実装前にテストを作成し、テストが通るように実装を進めています。
