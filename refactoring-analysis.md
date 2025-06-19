# リファクタリング分析レポート

## 概要
社内図書管理システムのコードベースを分析し、リファクタリングが必要な箇所を特定しました。フロントエンド（React/TypeScript）とバックエンド（Python/FastAPI）の両方で改善の余地があります。

## 🔴 優先度高：フロントエンド

### 1. App.tsx の責務過多 (153行)
**問題点:**
- 状態管理、イベントハンドラー、UI レンダリングが一つのコンポーネントに集約
- 複数の状態変数を個別に管理
- インラインイベントハンドラーが多数

**推奨対応:**
```typescript
// 状態管理をカスタムフックに分離
const useBookManagement = () => {
  const [selectedBookId, setSelectedBookId] = useState<number | null>(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  // ...その他の状態
};

// UIコンポーネントを分離
const BookManagementView = ({ books, onBorrow, onReturn }) => { /* */ };
const MasterManagementView = ({ onClose }) => { /* */ };
```

### 2. 大きなコンポーネントファイル
**問題のあるファイル:**
- `BookList.tsx` (201行) - 検索、ソート、テーブル表示が混在
- `FeedbackForm.tsx` (180行) - フォーム処理とAPI呼び出しが混在
- `BookRecommendations.tsx` (147行) - 推測される大きなファイル

**推奨対応:**
```typescript
// BookList.tsx を分割
const BookSearchFilters = ({ onSearch }) => { /* */ };
const BookTable = ({ books, onAction }) => { /* */ };
const BookListContainer = () => { /* 状態管理とデータフェッチ */ };
```

### 3. API エラーハンドリングの重複
**問題点:**
```typescript
// 各関数で同じパターンを繰り返し
try {
  await returnBook(bookId);
  refreshBooks();
} catch (error) {
  console.error('Failed to return book:', error);
}
```

**推奨対応:**
```typescript
// カスタムフックで共通化
const useApiCall = () => {
  const executeWithErrorHandling = async (apiCall, onSuccess?) => {
    try {
      const result = await apiCall();
      onSuccess?.(result);
      return result;
    } catch (error) {
      // 共通エラーハンドリング
    }
  };
};
```

### 4. 手動リフレッシュトリガーの問題
**問題点:**
```typescript
const [refreshTrigger, setRefreshTrigger] = useState(0);
const refreshBooks = () => setRefreshTrigger(prev => prev + 1);
```

**推奨対応:**
```typescript
// React Query または SWR を使用
const { data: books, mutate } = useSWR('/api/books', fetchBooks);
```

## 🟡 優先度中：バックエンド

### 5. dependencies.py のグローバル状態
**問題点:**
```python
# グローバル変数によるシングルトン管理
_repository_instance = None
_service_instance = None
```

**推奨対応:**
```python
# 依存性注入コンテナを使用
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    book_repository = providers.Factory(PostgresBookRepository)
    book_service = providers.Factory(BookService, repository=book_repository)
```

### 6. ルーターでのDTO定義
**問題点:**
```python
# routers/books.py 内でDTOを定義
class BookBase(BaseModel):
    title: str
```

**推奨対応:**
```python
# schemas/book.py に分離
from app.schemas.book import BookResponse, BookCreate, BookUpdate
```

### 7. PostgreSQL リポジトリのフォールバック処理
**問題点:**
```python
# postgres_repository.py で複数箇所で同じフォールバック
except Exception as e:
    from app.infrastructure.repositories import InMemoryBookRepository
    fallback_repo = InMemoryBookRepository()
```

**推奨対応:**
```python
# 設定ベースのリポジトリ選択
def get_repository():
    if settings.USE_POSTGRES:
        return PostgresBookRepository()
    return InMemoryBookRepository()
```

### 8. 外部API呼び出しの直接実装
**問題点:**
```python
# recommendations.py で直接 Anthropic API を呼び出し
import anthropic
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
```

**推奨対応:**
```python
# サービス層に抽象化
class AIRecommendationService:
    def get_recommendations(self, query: str) -> List[str]:
        # プロバイダー抽象化
```

## 🟢 優先度低：改善提案

### 9. TypeScript型定義の改善
- Union型やDiscriminated Unionの活用
- より厳密な型チェック

### 10. テストコードの拡充
- フロントエンドのユニットテスト不足
- インテグレーションテストの拡充

### 11. パフォーマンス最適化
- React.memoの適用検討
- 不要な再レンダリングの削減

## 推奨実装順序

1. **フロントエンド - カスタムフック作成** (useBookManagement, useApiCall)
2. **フロントエンド - App.tsx の分割** (最も影響範囲が大きい)
3. **フロントエンド - 大きなコンポーネントの分割**
4. **バックエンド - スキーマ分離** (DTOを別ファイルに)
5. **バックエンド - 依存性注入の導入**
6. **バックエンド - リポジトリパターンの改善**

## 推定工数
- 優先度高の対応: 2-3週間
- 優先度中の対応: 1-2週間
- 優先度低の対応: 1週間

## リスク評価
- **低リスク**: カスタムフック作成、スキーマ分離
- **中リスク**: App.tsx 分割、コンポーネント分割
- **高リスク**: 依存性注入導入（既存動作への影響大）

---
*分析日時: 2024年12月*
*対象: 社内図書管理システム*