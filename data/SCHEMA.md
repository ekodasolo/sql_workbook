# データスキーマ仕様

## テーブル構造とリレーション

```
customers (顧客マスタ)
    └─ customer_id (PK)
         ↓
sales (売上トランザクション)
    ├─ customer_id (FK) → customers
    ├─ product_id (FK) → products
    └─ store_id (FK) → stores

products (商品マスタ)
    └─ product_id (PK)

stores (店舗マスタ)
    └─ store_id (PK)
```

## テーブル詳細

### sales（売上トランザクション）
**目的**: 各販売取引の記録

| カラム名 | 型 | 説明 | 例 |
|---------|------|------|-----|
| sale_id | INTEGER | 売上ID（主キー） | 1 |
| sale_date | DATE | 販売日 | 2024-01-05 |
| customer_id | INTEGER | 顧客ID（外部キー） | 101 |
| product_id | INTEGER | 商品ID（外部キー） | 1001 |
| store_id | INTEGER | 店舗ID（外部キー） | 1 |
| quantity | INTEGER | 購入数量 | 2 |
| unit_price | INTEGER | 単価 | 1200 |
| discount_rate | DECIMAL | 割引率（0.00〜1.00） | 0.10 |

**計算カラム例**:
- 売上金額: `quantity * unit_price * (1 - discount_rate)`
- 割引額: `quantity * unit_price * discount_rate`

**レコード数**: 100件（2024年1月〜2月）

---

### products（商品マスタ）
**目的**: 商品の基本情報

| カラム名 | 型 | 説明 | 例 |
|---------|------|------|-----|
| product_id | INTEGER | 商品ID（主キー） | 1001 |
| product_name | VARCHAR | 商品名 | ノートパソコン |
| category | VARCHAR | カテゴリ | 家電 |
| subcategory | VARCHAR | サブカテゴリ | PC・タブレット |
| standard_price | INTEGER | 標準価格 | 1200 |

**カテゴリ構造**:
- 家電
  - PC・タブレット
  - PC周辺機器
  - ディスプレイ
  - 照明
- 家具
  - チェア
  - デスク

**レコード数**: 10件

---

### customers（顧客マスタ）
**目的**: 顧客の属性情報

| カラム名 | 型 | 説明 | 例 |
|---------|------|------|-----|
| customer_id | INTEGER | 顧客ID（主キー） | 101 |
| customer_name | VARCHAR | 顧客名 | 山田太郎 |
| customer_segment | VARCHAR | セグメント | VIP |
| registration_date | DATE | 登録日 | 2023-01-15 |
| prefecture | VARCHAR | 都道府県 | 東京都 |
| age_group | VARCHAR | 年齢層 | 30代 |

**セグメント分類**:
- VIP: 優良顧客
- Regular: 一般顧客
- New: 新規顧客

**都道府県分布**: 東京都、神奈川県、大阪府、愛知県、福岡県、埼玉県、千葉県

**レコード数**: 137件

---

### stores（店舗マスタ）
**目的**: 店舗の基本情報

| カラム名 | 型 | 説明 | 例 |
|---------|------|------|-----|
| store_id | INTEGER | 店舗ID（主キー） | 1 |
| store_name | VARCHAR | 店舗名 | 新宿店 |
| region | VARCHAR | 地域 | 関東 |
| prefecture | VARCHAR | 都道府県 | 東京都 |
| opening_date | DATE | 開店日 | 2020-04-01 |

**店舗一覧**:
1. 新宿店（関東・東京都）
2. 梅田店（関西・大阪府）
3. 博多店（九州・福岡県）

**レコード数**: 3件

---

## 分析用途別クエリパターン

### 時系列分析
- 日別・週別・月別売上推移
- 曜日別の購買傾向
- 季節性分析

### 商品分析
- カテゴリ別売上
- 人気商品ランキング
- 在庫回転率（数量ベース）

### 顧客分析
- セグメント別購買パターン
- RFM分析（最終購入日、頻度、金額）
- リピート率
- 年齢層別・地域別傾向

### 店舗分析
- 店舗別売上比較
- 地域別パフォーマンス

### クロス分析
- セグメント × カテゴリ
- 店舗 × 商品カテゴリ
- 時間帯 × 顧客属性

---

## データ生成の想定

このサンプルデータは以下の傾向を持つように設計されています：

- **売上期間**: 2024年1月〜2月（2ヶ月間）
- **顧客行動**: 
  - VIP顧客: 高頻度購入、高額商品選好
  - Regular顧客: 中程度の購入頻度
  - New顧客: 低頻度、様子見傾向
- **商品傾向**:
  - 家電が主力（PC関連、ディスプレイが人気）
  - 家具は単価高め
- **割引**: 一部商品に10-20%の割引適用
- **地域性**: 東京・大阪・福岡の3拠点

---

## 学習推奨順序

### 初級（基礎）
1. 単一テーブルのSELECT
2. WHERE条件
3. ORDER BY、LIMIT
4. 基本的な集計（COUNT, SUM, AVG）

### 中級（結合と集計）
5. 2テーブルのJOIN
6. GROUP BY集計
7. CASE式
8. 日付関数

### 上級（分析）
9. 複数テーブルJOIN
10. Window関数
11. CTE（WITH句）
12. 複雑なサブクエリ
