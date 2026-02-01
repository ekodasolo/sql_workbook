# Webブラウザで学ぶSQL入門アプリ

StreamlitとDuckDBを使った、初学者向けのインタラクティブなSQL学習アプリです。

## 特徴

- リアルタイムデータビューワー: SQLの実行結果を即座に確認
- インタラクティブなSQLエディタ: クエリを書いてすぐに試せる
- 豊富なサンプルクエリ: よく使うSQL文の例を用意
- 初学者フレンドリー: エラー時のヒント機能付き
- ポータブル: ローカル、EC2、コンテナどこでも動作

## セットアップ

### ローカル環境

```bash
# リポジトリのクローン（またはファイルのダウンロード）
cd sql_workbook

# 仮想環境の作成（推奨）
python -m venv .venv
source .venv/bin/activate

# 依存パッケージのインストール
pip install -r requirements.txt

# アプリの起動
streamlit run app.py
```

ブラウザで `http://localhost:8501` を開くとアプリが表示されます。

### Docker環境

```bash
# Dockerfileを作成して実行
docker build -t sql-learning-app .
docker run -p 8501:8501 sql-learning-app
```

### EC2/コンテナ環境

```bash
# 必要なパッケージをインストール
pip install -r requirements.txt

# バックグラウンドで起動
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &
```

## 使い方

1. テーブル一覧を確認: 左サイドバーで利用可能なテーブルをクリック
2. 練習問題を見る: サイドバーの「 練習問題」リンクから問題集にアクセス
3. SQLを書く: 左カラムのエディタにSQLクエリを入力
4. 実行: 「▶️ 実行」ボタンをクリック
5. 結果を確認: 右カラムに結果が表示されます

### 練習問題について

`EXERCISES.md` に練習問題があります：

#### 標準SQLと実用性のバランス

このアプリは標準SQL（ISO/IEC 9075）をベースにしていますが、実務での使いやすさも考慮しています。

結果件数の制限について:
- 標準SQL: `FETCH FIRST n ROWS ONLY` （SQL:2008）
- 実務での慣例: `LIMIT n` （PostgreSQL、MySQL、BigQuery、Athena、Snowflake、DuckDBなど）

問題1で `FETCH FIRST` を紹介した上で、以降の問題では実務で一般的な `LIMIT` を使用しています。これは主要なクラウドデータウェアハウスで標準的な書き方です。

使用している標準SQL機能:
- `EXTRACT()` - 日付から年月日・曜日を抽出（SQL:1992）
- `SUBSTRING()` - 文字列の部分取得（SQL:1992）
- `||` - 文字列結合演算子（SQL:1992）
- Window関数 - RANK, ROW_NUMBER, LAG, LEAD など（SQL:2003）
- CTE（WITH句）- 複雑なクエリの構造化（SQL:1999）
- CASE式、JOIN、GROUP BY など基本機能（SQL:1992）

各問題には：
- 問題文
- ヒント
- 回答例
- 解説

が含まれています。初心者は写経で書いてあるコードを書き写して実行することで、手を動かしてください。中級者以上はまず自分で考えてから回答を見るなどレベル別で活用してください。

## サンプルデータ

アプリには小売業の売上データが用意されています：

### `sales` テーブル（売上トランザクション）
- sale_id: 売上ID
- sale_date: 販売日
- customer_id: 顧客ID
- product_id: 商品ID
- store_id: 店舗ID
- quantity: 数量
- unit_price: 単価
- discount_rate: 割引率

### `products` テーブル（商品マスタ）
- product_id: 商品ID
- product_name: 商品名
- category: カテゴリ（家電、家具）
- subcategory: サブカテゴリ
- standard_price: 標準価格

### `customers` テーブル（顧客マスタ）
- customer_id: 顧客ID
- customer_name: 顧客名
- customer_segment: セグメント（VIP、Regular、New）
- registration_date: 登録日
- prefecture: 都道府県
- age_group: 年齢層

### `stores` テーブル（店舗マスタ）
- store_id: 店舗ID
- store_name: 店舗名
- region: 地域
- prefecture: 都道府県
- opening_date: 開店日

## 学習できるSQL文法

このサンプルデータで以下の分析系SQL文法を実践できます：

### 1. 基本的なSELECT
- カラム選択
- LIMIT句（実務で一般的、標準SQLはFETCH FIRST）
- ORDER BY
- AS句による列名指定（ビジネスドメイン用語での命名）

### 2. 日付・文字列関数
日付関数:
- `DATE_TRUNC()`: 月次集計
- `DAYNAME()`: 曜日別分析
- `EXTRACT()`: 年・月・日の抽出
- `BETWEEN`: 日付範囲抽出
- 日付の引き算（期間計算）

文字列関数:
- `CONCAT()`: 文字列結合
- `UPPER()`, `LOWER()`: 大文字小文字変換
- `LENGTH()`: 文字数取得
- `SUBSTRING()`, `LEFT()`: 部分文字列取得

### 3. WHERE条件
- 比較演算子（>=, <=, =）
- 論理演算子（AND, OR）
- 日付範囲指定

### 4. JOIN（テーブル結合）
- INNER JOIN
- 2テーブル結合
- 3テーブル以上の多重結合

### 5. GROUP BY集計
- `COUNT()`, `SUM()`, `AVG()`
- `COUNT(DISTINCT)`
- カテゴリ別・セグメント別集計

### 6. CASE式
- 条件分岐
- ランク分類
- ピボット集計（カテゴリ別売上を列に展開）

### 7. 縦持ち⇔横持ち変換
- ピボット（縦→横）: CASE式 + GROUP BY でカテゴリを列に展開
- アンピボット（横→縦）: UNION ALL で列を行に変換
- 実務で頻出のデータ整形テクニック

### 8. Window関数
- `RANK()`, `ROW_NUMBER()`: ランキング
- `SUM() OVER()`: 累積集計
- `LAG()`, `LEAD()`: 前後行参照
- `PARTITION BY`: グループ別Window関数
- 購買頻度分析（前回購買日からの日数）

### 9. CTE（Common Table Expression）
- `WITH`句
- 複数CTEの組み合わせ
- 段階的なデータ加工
- 可読性の高いクエリ記述

## カスタマイズ

### 独自のデータを追加

`data/` フォルダに独自のCSVファイルを配置し、`app.py` の `init_db()` 関数を編集：

```python
# 独自のCSVファイルから読み込む例
con.execute(f"""
    CREATE TABLE my_table AS 
    SELECT * FROM read_csv_auto('{data_dir}/my_data.csv')
""")
```

### データの要件

DuckDBは以下の形式に対応しています：
- CSV（自動型推論）
- Parquet
- JSON

CSVは1行目がヘッダー（カラム名）である必要があります。

### S3からデータを読み込む（EC2でIAM Role使用時）

```python
# DuckDBのhttpfs拡張を有効化
con.execute("INSTALL httpfs; LOAD httpfs;")
con.execute("SET s3_region='ap-northeast-1';")

# S3からParquetを読み込む
con.execute("""
    CREATE TABLE my_s3_table AS 
    SELECT * FROM read_parquet('s3://my-bucket/data/*.parquet')
""")
```

## 技術スタック

- Streamlit: Webアプリフレームワーク
- DuckDB: 高速なインメモリSQL分析データベース
- Pandas: データ操作

---

##  SQL標準と実用性のバランス

このアプリは標準SQL（ISO/IEC 9075）をベースにしていますが、実務での使いやすさも考慮しています。

### 標準SQL機能のみを使用（LIMITを除く）

SQL:1992（SQL-92）:
- SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY
- JOIN（INNER, LEFT, RIGHT, FULL OUTER）
- CASE式、集計関数（COUNT, SUM, AVG, MIN, MAX）
- DISTINCT、UNION、SUBSTRING、UPPER、LOWER、CHAR_LENGTH
- EXTRACT（日付部分の取得）

SQL:1999（SQL3）:
- CTE（WITH句）

SQL:2003:
- Window関数（RANK, ROW_NUMBER, DENSE_RANK, LAG, LEAD, NTILE など）

### 結果件数の制限について

標準SQL（SQL:2008）: `FETCH FIRST n ROWS ONLY`

実務での慣例: `LIMIT n`
- PostgreSQL、MySQL、BigQuery、Athena、Snowflake、DuckDBなど主要な分析系DBで広くサポート
- 短く書けて読みやすい
- このアプリでは実用性を重視し、`LIMIT` を使用しています

問題1で `FETCH FIRST` を紹介した上で、以降の問題では `LIMIT` を使用しています。

### データベース互換性

このアプリのクエリは標準SQLに概ね準拠しているため、以下のデータベースで動作する想定です（DuckDB以外の環境での動作検証はしていません）：
- DuckDB
- Amazon Athena（Apache Trino）
- Snowflake
- BigQuery
