# SQL練習問題集

このファイルには、基礎から応用まで段階的に学べる練習問題が含まれています。
各問題にはヒントと回答例があります。まず自分で考えてから回答を見ましょう。

## 📌 完全標準SQL準拠

このアプリの全てのクエリは標準SQL（ISO/IEC 9075）に準拠しています。
主要なデータベース（PostgreSQL、MySQL 8.0+、SQL Server、Oracle、BigQuery、Snowflakeなど）で動作します。

### 使用している標準SQL機能
- EXTRACT() - 日付から年月日、曜日を抽出
- SUBSTRING() - 文字列の部分取得
- CASE式 - 条件分岐
- Window関数 - RANK, ROW_NUMBER, LAG, LEAD など
- CTE（WITH句）- 複雑なクエリの構造化
- FETCH FIRST n ROWS ONLY - 結果件数の制限

---

## 📚 基礎編（SELECT, WHERE, ORDER BY）

### 問題1: 商品の一覧を確認する

問題: products テーブルから商品の基本情報（product_id, product_name, category）を表示してください。

💡 ヒント
- 必要なカラムだけを指定します（SELECT * は避けましょう）
- 大量データの可能性があるテーブルでは、必ず件数制限を付けます

回答例
```sql
SELECT product_id, product_name, category
FROM products
FETCH FIRST 10 ROWS ONLY;
```

解説: 実務では極力 SELECT * は避けるべきです。理由は：
1. 不要なカラムまで取得するとパフォーマンスが悪化する
2. テーブル構造が変わった時に予期しない動作をする
3. どのカラムを使うか明示することでコードが読みやすくなる

結果件数の制限について:
- 標準SQL: `FETCH FIRST n ROWS ONLY` （SQL:2008で標準化）
- 実務での慣例: `LIMIT n` （PostgreSQL、MySQL、BigQuery、Athena、Snowflake、DuckDBなど主要な分析系DBで広くサポート）

`FETCH FIRST` が標準SQLですが、実務ではほとんどの分析系データベースで `LIMIT n` が使われています。短く書けて読みやすいためです。

このアプリでの方針: 
標準SQLとしては `FETCH FIRST` が正式ですが、実用性を考慮し、以降の問題では `LIMIT n` を使用します。これは BigQuery、Athena、Snowflake など主要なクラウドデータウェアハウスで標準的な書き方です。

---

### 問題2: 特定のカラムだけ表示

問題: sales テーブルから、sale_id, sale_date, quantity の3つのカラムだけを表示してください。最初の10件のみ。

💡 ヒント
- カラム名をカンマ区切りで指定します
- LIMIT で表示件数を制限できます

回答例
```sql
SELECT sale_id, sale_date, quantity
FROM sales
LIMIT 10;
```

解説: 必要なカラムだけを指定することで、結果が見やすくなります。

---

### 問題3: 条件に合うデータを抽出

問題: sales テーブルから、数量（quantity）が5以上の売上データを表示してください。

💡 ヒント
- WHERE 句で条件を指定します
- 比較演算子: =, >, <, >=, <= が使えます
- 実務では必ず LIMIT を付けましょう

回答例
```sql
SELECT 
    sale_id,
    sale_date,
    customer_id,
    product_id,
    quantity,
    unit_price
FROM sales
WHERE quantity >= 5
LIMIT 100;
```

解説: WHERE 句は条件に合う行だけを絞り込みます。
- 必要なカラムだけを明示的に選択
- LIMIT で結果件数を制限（予想外に大量のデータが返ってくることを防ぐ）

---

### 問題4: 複数条件での絞り込み

問題: sales テーブルから、数量が3以上で、かつ割引率が0より大きい（割引が適用されている）売上を表示してください。

💡 ヒント
- AND で複数条件を組み合わせられます
- discount_rate > 0 で割引ありを判定できます

回答例
```sql
SELECT 
    sale_id,
    sale_date,
    product_id,
    quantity,
    unit_price,
    discount_rate
FROM sales
WHERE quantity >= 3
  AND discount_rate > 0
LIMIT 100;
```

解説: 
- AND で条件を繋ぐと、両方を満たす行だけが表示されます
- 実務では「何件ヒットするかわからない検索」が多いため、LIMIT は保険として必須

---

### 問題5: 並び替え

問題: sales テーブルのデータを、販売日（sale_date）の新しい順に並べて表示してください。

💡 ヒント
- ORDER BY で並び替えができます
- DESC で降順（大きい順）、ASC で昇順（小さい順）

回答例
```sql
SELECT 
    sale_id,
    sale_date,
    customer_id,
    product_id,
    quantity,
    unit_price
FROM sales
ORDER BY sale_date DESC
LIMIT 20;
```

解説: 
- ORDER BY sale_date DESC で、最新の売上から順に表示されます
- 実務では「最新20件を見たい」というケースが多いので、LIMIT と組み合わせるのが定石

---

### 問題6: 日付範囲での絞り込み

問題: sales テーブルから、2024年1月15日から1月31日までの売上データを表示してください。

💡 ヒント
- BETWEEN 演算子で範囲指定ができます
- 日付は 'YYYY-MM-DD' の形式で指定します

回答例
```sql
SELECT 
    sale_id,
    sale_date,
    customer_id,
    product_id,
    quantity,
    unit_price,
    discount_rate
FROM sales
WHERE sale_date BETWEEN DATE '2024-01-15' AND DATE '2024-01-31'
ORDER BY sale_date
LIMIT 100;
```

解説: 
- BETWEEN は指定した範囲の値（両端含む）を抽出します
- DATE リテラルを使用（標準SQL）
- 日付範囲でも予想外に大量データがある可能性があるため、LIMIT で上限を設定

---

## 🏷️ 実務編：AS句とビジネスドメイン用語

### 問題7: ビジネスドメインに合わせた列名を付ける

問題: sales テーブルから売上情報を取得し、計算結果にビジネス側がわかる英語の列名を付けてください。またquantityは何の量なのかわかるような表示名に変えてください。

💡 ヒント
- AS で列に別名（エイリアス）を付けられます
- 計算式には必ずASで名前を付けましょう

回答例
```sql
SELECT 
    sale_id,
    sale_date,
    customer_id,
    product_id,
    quantity AS purchase_quantity,
    unit_price,
    discount_rate,
    quantity * unit_price AS amount_before_discount,
    quantity * unit_price * discount_rate AS discount_amount,
    quantity * unit_price * (1 - discount_rate) AS net_amount
FROM sales
LIMIT 20;
```

解説: 
- SELECT句においてASは省略可能ですが、読みやすくわかりやすくなる場面ではASを使って列名をつけます
- 特に分析用のデータマート構築では、最終的にユーザーが見るデータのカラム名が、ビジネスで使っている言葉遣いに沿っているとわかりやすくなります
- 対象のビジネスドメインによって用語を使い分ける場合があり、同じ「顧客」のことを営業部門なら`account`、CS部門なら`customer`と呼ぶなど、言葉遣いを揃えると読みやすくなります
- データを利用する人の目線で、自然な言葉遣いになっている方がわかりやすく、使いやすいデータマートになります

---

### 問題8: 集計結果にわかりやすい名前を付ける

問題: 顧客ごとの購入統計を計算し、全ての列に分析者が理解しやすい英語の列名を付けてください。

回答例
```sql
SELECT 
    customer_id,
    COUNT(*) AS purchase_count,
    SUM(quantity) AS total_quantity,
    SUM(quantity * unit_price * (1 - discount_rate)) AS total_revenue,
    AVG(quantity * unit_price * (1 - discount_rate)) AS average_order_value,
    MIN(sale_date) AS first_purchase_date,
    MAX(sale_date) AS last_purchase_date
FROM sales
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 20;
```

解説: 
- 集計関数には必ずASで名前を付ける（これは実務の絶対ルール）
- 英語の一般的なビジネス用語を使うことで：
  - データマートを使う分析者が理解しやすい
  - BIツールでの表示がそのまま使える

---

## 📅 関数編Part1：日付関数マスター

### 問題9: 日付から年月を取り出す

問題: 売上データから、年と月を取り出して表示してください。

💡 ヒント
- EXTRACT(YEAR FROM 日付) で年を取得
- EXTRACT(MONTH FROM 日付) で月を取得（標準SQL）

回答例
```sql
SELECT 
    sale_id,
    sale_date,
    EXTRACT(YEAR FROM sale_date) AS sale_year,
    EXTRACT(MONTH FROM sale_date) AS sale_month,
    customer_id,
    quantity * unit_price * (1 - discount_rate) AS net_amount
FROM sales
ORDER BY sale_date
LIMIT 20;
```

解説: 
- EXTRACT() は標準SQL関数で、ほぼ全てのデータベースでサポート
- 年月を個別に取得することで、月次集計の準備ができます
- データベース製品固有の方言で同じ用途で使える別の関数が用意されている場合があります

---

### 問題10: 月次集計を行う

問題: 年月ごとの売上件数と売上金額を集計してください。

回答例
```sql
SELECT 
    EXTRACT(YEAR FROM sale_date) AS sale_year,
    EXTRACT(MONTH FROM sale_date) AS sale_month,
    COUNT(*) AS sales_count,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(quantity * unit_price * (1 - discount_rate)) AS monthly_revenue,
    AVG(quantity * unit_price * (1 - discount_rate)) AS avg_order_value
FROM sales
GROUP BY EXTRACT(YEAR FROM sale_date), EXTRACT(MONTH FROM sale_date)
ORDER BY sale_year, sale_month;
```

解説: 
- 月次分析は実務で最頻出のパターン
- 標準SQLでは EXTRACT で年と月を個別に取得して GROUP BY
- 年と月の両方でグループ化することで、年をまたいだデータも正しく集計できます

---

### 問題11: 曜日別の売上傾向を分析

問題: 曜日ごとの売上件数を集計してください。

💡 ヒント
- EXTRACT(DOW FROM 日付) で曜日番号を取得（0=日曜〜6=土曜）
- Day of Week で DOWです
- ここではCASE式で番号を曜日名に変換しています
- CASE式についてはあとの章で詳しく扱います

回答例
```sql
SELECT 
    CASE EXTRACT(DOW FROM sale_date)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END AS day_of_week,
    COUNT(*) AS sales_count,
    SUM(quantity * unit_price * (1 - discount_rate)) AS total_sales,
    AVG(quantity * unit_price * (1 - discount_rate)) AS avg_sales
FROM sales
GROUP BY EXTRACT(DOW FROM sale_date)
ORDER BY EXTRACT(DOW FROM sale_date);
```

解説: 
- 曜日分析は小売・ECで頻出
- EXTRACT(DOW FROM date) は標準SQL（DOW = Day Of Week）
- CASE式で曜日番号を読みやすい名前に変換

---

### 問題12: 期間の計算（日数差）

問題: 各顧客の初回購入日から最終購入日までの日数を計算してください。

回答例
```sql
SELECT 
    customer_id,
    MIN(sale_date) AS first_purchase_date,
    MAX(sale_date) AS last_purchase_date,
    MAX(sale_date) - MIN(sale_date) AS days_active,
    COUNT(*) AS purchase_count
FROM sales
GROUP BY customer_id
HAVING COUNT(*) >= 2
ORDER BY days_active DESC
LIMIT 20;
```

解説: 
- 日付の引き算で経過日数が計算できます（標準SQL）
- 顧客のライフタイム分析でよく使うパターン
- HAVING で2回以上購入した顧客に絞り込み

---

### 問題13: 日付から年・月・日を個別に取り出す

問題: 売上日から、年、月、日をそれぞれ別の列として取り出してください。

回答例
```sql
SELECT 
    sale_id,
    sale_date,
    EXTRACT(YEAR FROM sale_date) AS sale_year,
    EXTRACT(MONTH FROM sale_date) AS sale_month,
    EXTRACT(DAY FROM sale_date) AS sale_day,
    CASE EXTRACT(DOW FROM sale_date)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END AS day_of_week,
    quantity * unit_price * (1 - discount_rate) AS net_amount
FROM sales
LIMIT 20;
```

解説: 
- EXTRACT は日付の部分取得でよく使います（標準SQL）
- 年別、月別の分析に便利

---

## 🔤 関数編Part2：文字列関数マスター

### 問題14: 文字列の結合

問題: 顧客名とセグメントを結合して「山田太郎（VIP）」のような形式で表示してください。

回答例
```sql
SELECT 
    customer_id,
    customer_name,
    customer_segment,
    customer_name || '（' || customer_segment || '）' AS customer_display_name,
    prefecture
FROM customers
LIMIT 20;
```

解説: 
- || 演算子は標準SQLの文字列結合（CONCAT関数も使えますが||がより標準的）
- レポート用の表示名作成でよく使う

---

### 問題15: 文字列の大文字・小文字変換と長さ

問題: 商品カテゴリを大文字に変換し、商品名の文字数も表示してください。

回答例
```sql
SELECT 
    product_id,
    product_name,
    LENGTH(product_name) AS product_name_length,
    category,
    UPPER(category) AS category_upper,
    standard_price
FROM products
LIMIT 10;
```

解説: 
- UPPER/LOWER/LENGTH は全て標準SQL関数
- データクレンジングでよく使う

---

### 問題16: 文字列の部分取得

問題: 商品名の最初の4文字だけを取り出して表示してください。

回答例
```sql
SELECT 
    product_id,
    product_name,
    SUBSTRING(product_name, 1, 4) AS product_short,
    category
FROM products
LIMIT 10;
```

解説: 
- SUBSTRING は標準SQL関数
- SUBSTRING(文字列, 開始位置, 長さ) の形式
- 商品名の略称作成や、データ整形でよく使います

---

## 📊 中級編（JOIN, GROUP BY, 集計）

### 問題17: 2テーブルの結合

問題: sales と products を結合して、売上データに商品名とカテゴリを追加して表示してください。

回答例
```sql
SELECT 
    s.sale_id,
    s.sale_date,
    p.product_name,
    p.category,
    s.quantity AS purchase_quantity,
    s.unit_price,
    s.quantity * s.unit_price * (1 - s.discount_rate) AS net_amount
FROM sales s
JOIN products p ON s.product_id = p.product_id
LIMIT 10;
```

解説: 
- JOIN で売上と商品の情報を組み合わせることができます
- テーブルの別名（s, p）を使うとクエリが読みやすくなる

---

### 問題18: 3テーブルの結合

問題: sales, products, customers を結合して、販売情報を表示してください。

回答例
```sql
SELECT 
    s.sale_date,
    c.customer_name,
    p.product_name,
    s.quantity AS purchase_quantity,
    s.quantity * s.unit_price * (1 - s.discount_rate) AS net_amount
FROM sales s
JOIN customers c ON s.customer_id = c.customer_id
JOIN products p ON s.product_id = p.product_id
LIMIT 10;
```

解説: 
- JOIN を続けて書くことで、複数のテーブルを次々に繋げられます

---

### 問題19: 重複を除外したリストを作る

問題: 顧客が購入したことがある商品カテゴリの一覧を表示してください。

回答例
```sql
SELECT DISTINCT p.category
FROM sales s
JOIN products p ON s.product_id = p.product_id
ORDER BY p.category;
```

解説: 
- SELECT DISTINCT で重複する行を除外
- DISTINCTは処理コストが高いので、本当に必要な時だけ使う

---

## 🎯 応用編Part1：CASE式マスター

### 問題20: CASE式で金額ランク分類

問題: 各売上を金額の大きさに応じて分類してください。

回答例
```sql
SELECT 
    sale_id,
    sale_date,
    quantity * unit_price * (1 - discount_rate) AS sales_amount,
    CASE 
        WHEN quantity * unit_price * (1 - discount_rate) >= 5000 THEN 'High'
        WHEN quantity * unit_price * (1 - discount_rate) >= 2000 THEN 'Medium'
        ELSE 'Low'
    END AS amount_tier
FROM sales
ORDER BY sales_amount DESC
LIMIT 20;
```

解説: 
- CASE式で金額に応じたランク付けができます（標準SQL）
- 条件は上から順に評価されます

---

### 問題21: CASE式で複数条件の組み合わせ

問題: 顧客セグメントと購入金額を組み合わせて、優先度を判定してください。

回答例
```sql
SELECT 
    s.sale_id,
    s.sale_date,
    c.customer_name,
    c.customer_segment,
    s.quantity * s.unit_price * (1 - s.discount_rate) AS sales_amount,
    CASE 
        WHEN c.customer_segment = 'VIP' AND s.quantity * s.unit_price * (1 - s.discount_rate) >= 3000 THEN 'Top Priority'
        WHEN c.customer_segment = 'VIP' THEN 'High Priority'
        WHEN c.customer_segment = 'Regular' AND s.quantity * s.unit_price * (1 - s.discount_rate) >= 5000 THEN 'High Priority'
        ELSE 'Normal'
    END AS priority_level
FROM sales s
JOIN customers c ON s.customer_id = c.customer_id
ORDER BY s.sale_date DESC
LIMIT 20;
```

解説: 
- 実務では複雑なビジネスルールをCASE式で表現
- AND/ORで条件を組み合わせて柔軟な分類が可能

---

### 問題22: CASE式を集計関数内で使う（条件付き集計）

問題: 商品カテゴリごとに、割引ありの売上と割引なしの売上を別々に集計してください。

回答例
```sql
SELECT 
    p.category,
    COUNT(*) AS total_transactions,
    SUM(CASE WHEN s.discount_rate > 0 
        THEN s.quantity * s.unit_price * (1 - s.discount_rate) 
        ELSE 0 
    END) AS discounted_sales,
    SUM(CASE WHEN s.discount_rate = 0 
        THEN s.quantity * s.unit_price 
        ELSE 0 
    END) AS full_price_sales,
    SUM(s.quantity * s.unit_price * (1 - s.discount_rate)) AS total_sales
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.category
ORDER BY total_sales DESC;
```

解説: 
- 条件付き集計は実務で超頻出
- SUM(CASE WHEN ...) のパターンは必ず覚えましょう

---

### 問題23: CASE式で順序付け（カスタムソート）

問題: 顧客セグメントを「VIP → Regular → New」の順で並べて表示してください。

回答例
```sql
SELECT 
    customer_id,
    customer_name,
    customer_segment,
    registration_date
FROM customers
ORDER BY 
    CASE 
        WHEN customer_segment = 'VIP' THEN 1
        WHEN customer_segment = 'Regular' THEN 2
        WHEN customer_segment = 'New' THEN 3
    END,
    registration_date
LIMIT 20;
```

解説: 
- ビジネスロジックに基づいた並び順を実現
- ORDER BY 内でCASE式を使用（標準SQL）

---

## 🔄 応用編Part2：縦持ち⇔横持ち変換マスター

### 問題24: 縦持ちから横持ちへ（ピボット）

問題: 年月ごと・カテゴリごとの売上を、「年月」を行、「カテゴリ」を列にして表示してください。

回答例
```sql
SELECT 
    EXTRACT(YEAR FROM s.sale_date) AS sale_year,
    EXTRACT(MONTH FROM s.sale_date) AS sale_month,
    SUM(CASE WHEN p.category = '家電' 
        THEN s.quantity * s.unit_price * (1 - s.discount_rate) 
        ELSE 0 
    END) AS electronics_sales,
    SUM(CASE WHEN p.category = '家具' 
        THEN s.quantity * s.unit_price * (1 - s.discount_rate) 
        ELSE 0 
    END) AS furniture_sales,
    SUM(s.quantity * s.unit_price * (1 - s.discount_rate)) AS total_sales
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY EXTRACT(YEAR FROM s.sale_date), EXTRACT(MONTH FROM s.sale_date)
ORDER BY sale_year, sale_month;
```

解説: 
- ピボット（縦→横）は、CASE式を集計関数内で使うのが基本
- 完全に標準SQL準拠

---

### 問題25: 複数軸のピボット

問題: 顧客セグメントごと・カテゴリごとの売上を、セグメントを行、カテゴリを列にして表示してください。

回答例
```sql
SELECT 
    c.customer_segment,
    SUM(CASE WHEN p.category = '家電' 
        THEN s.quantity * s.unit_price * (1 - s.discount_rate) 
        ELSE 0 
    END) AS electronics_sales,
    SUM(CASE WHEN p.category = '家具' 
        THEN s.quantity * s.unit_price * (1 - s.discount_rate) 
        ELSE 0 
    END) AS furniture_sales,
    SUM(s.quantity * s.unit_price * (1 - s.discount_rate)) AS total_sales
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN customers c ON s.customer_id = c.customer_id
GROUP BY c.customer_segment
ORDER BY total_sales DESC;
```

解説: 
- クロス集計は実務で超頻出
- 「どのセグメントが、どのカテゴリを買っているか」が一目でわかる

---

### 問題26: 横持ちから縦持ちへ（アンピボット）

問題: 複数指標を縦持ちにしてください。

回答例
```sql
WITH monthly_metrics AS (
    SELECT 
        EXTRACT(YEAR FROM sale_date) AS sale_year,
        EXTRACT(MONTH FROM sale_date) AS sale_month,
        COUNT(*) AS sales_count,
        SUM(quantity * unit_price * (1 - discount_rate)) AS revenue,
        COUNT(DISTINCT customer_id) AS customer_count
    FROM sales
    GROUP BY EXTRACT(YEAR FROM sale_date), EXTRACT(MONTH FROM sale_date)
)
SELECT 
    sale_year,
    sale_month,
    'Sales Count' AS metric_name,
    CAST(sales_count AS DECIMAL(18,2)) AS metric_value
FROM monthly_metrics

UNION ALL

SELECT 
    sale_year,
    sale_month,
    'Revenue' AS metric_name,
    revenue AS metric_value
FROM monthly_metrics

UNION ALL

SELECT 
    sale_year,
    sale_month,
    'Customer Count' AS metric_name,
    CAST(customer_count AS DECIMAL(18,2)) AS metric_value
FROM monthly_metrics

ORDER BY sale_year, sale_month, metric_name;
```

解説: 
- アンピボット（横→縦）は UNION ALL で実現（標準SQL）
- 複数のKPIを縦持ちにすることで、BIツールでの可視化が楽になる

---

## 🪟 応用編Part3：Window関数マスター

### 問題27: ROW_NUMBER vs RANK vs DENSE_RANK

問題: 商品ごとの売上を計算し、3種類のランキング関数の違いを確認してください。

回答例
```sql
SELECT 
    p.product_name,
    SUM(s.quantity * s.unit_price * (1 - s.discount_rate)) AS total_sales,
    ROW_NUMBER() OVER (ORDER BY SUM(s.quantity * s.unit_price * (1 - s.discount_rate)) DESC) AS row_num,
    RANK() OVER (ORDER BY SUM(s.quantity * s.unit_price * (1 - s.discount_rate)) DESC) AS rank,
    DENSE_RANK() OVER (ORDER BY SUM(s.quantity * s.unit_price * (1 - s.discount_rate)) DESC) AS dense_rank
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_sales DESC;
```

解説: 
- ランキング関数の使い分けは実務で重要（全て標準SQL）
- ROW_NUMBER: 常に連番
- RANK: 同点は同順位、次の順位は飛ぶ
- DENSE_RANK: 同点は同順位、次の順位は連続

---

### 問題28: 顧客別の累積売上（PARTITION BY）

問題: 各顧客について、購入日順に累積売上金額を計算してください。

回答例
```sql
SELECT 
    customer_id,
    sale_date,
    quantity * unit_price * (1 - discount_rate) AS purchase_amount,
    SUM(quantity * unit_price * (1 - discount_rate)) 
        OVER (PARTITION BY customer_id ORDER BY sale_date) AS cumulative_revenue
FROM sales
ORDER BY customer_id, sale_date
LIMIT 30;
```

解説: 
- Window関数の SUM() OVER で累積計算（標準SQL）
- PARTITION BY で顧客ごとに分割

---

### 問題29: LAGとLEADで前後の行を参照

問題: 各顧客の購入履歴で、前回購入からの経過日数を計算してください。

回答例
```sql
SELECT 
    customer_id,
    sale_date,
    LAG(sale_date) OVER (PARTITION BY customer_id ORDER BY sale_date) AS previous_purchase_date,
    sale_date - LAG(sale_date) OVER (PARTITION BY customer_id ORDER BY sale_date) AS days_since_last
FROM sales
ORDER BY customer_id, sale_date
LIMIT 30;
```

解説: 
- LAG() で前の行を参照（標準SQL）
- 購買頻度分析でよく使う

---

### 問題30: 移動平均（ウィンドウフレーム）

問題: 日付順に、直近3件の売上の移動平均を計算してください。

回答例
```sql
SELECT 
    sale_date,
    sale_id,
    quantity * unit_price * (1 - discount_rate) AS sales_amount,
    AVG(quantity * unit_price * (1 - discount_rate)) 
        OVER (ORDER BY sale_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg_3
FROM sales
ORDER BY sale_date
LIMIT 30;
```

解説: 
- 移動平均はトレンド分析の基本（標準SQL）
- ROWS BETWEEN でウィンドウの範囲を制御

---

### 問題31: NTILE（パーセンタイル分割）

問題: 顧客を売上金額で4つのグループ（四分位）に分けてください。

回答例
```sql
WITH customer_revenue AS (
    SELECT 
        customer_id,
        SUM(quantity * unit_price * (1 - discount_rate)) AS total_revenue
    FROM sales
    GROUP BY customer_id
)
SELECT 
    cr.customer_id,
    c.customer_name,
    cr.total_revenue,
    NTILE(4) OVER (ORDER BY cr.total_revenue DESC) AS revenue_quartile,
    CASE 
        WHEN NTILE(4) OVER (ORDER BY cr.total_revenue DESC) = 1 THEN 'Top 25%'
        WHEN NTILE(4) OVER (ORDER BY cr.total_revenue DESC) = 2 THEN 'Upper Middle'
        WHEN NTILE(4) OVER (ORDER BY cr.total_revenue DESC) = 3 THEN 'Lower Middle'
        ELSE 'Bottom 25%'
    END AS revenue_segment
FROM customer_revenue cr
JOIN customers c ON cr.customer_id = c.customer_id
ORDER BY cr.total_revenue DESC;
```

解説: 
- NTILE は顧客セグメンテーションでよく使う（標準SQL）
- RFM分析、ABC分析などで活用

---

## 🎓 応用編Part4：CTE（WITH句）マスター

### 問題32: CTEを使った段階的な集計

問題: CTEを使って、顧客ごとの合計購入金額を計算し、顧客名と表示してください。

回答例
```sql
WITH customer_totals AS (
    SELECT 
        customer_id,
        SUM(quantity * unit_price * (1 - discount_rate)) AS total_revenue
    FROM sales
    GROUP BY customer_id
)
SELECT 
    c.customer_name,
    ct.total_revenue
FROM customer_totals ct
JOIN customers c ON ct.customer_id = c.customer_id
ORDER BY ct.total_revenue DESC;
```

解説: 
- WITH句で中間結果に名前をつける（標準SQL）
- 複雑な集計を段階的に書ける

---

### 問題33: 複数のCTEを組み合わせる

問題: 複数のCTEを使って、VIP顧客が最もよく購入している商品カテゴリを分析してください。

回答例
```sql
WITH vip_purchases AS (
    SELECT 
        s.sale_id,
        s.customer_id,
        s.product_id,
        s.quantity * s.unit_price * (1 - s.discount_rate) AS sales_amount
    FROM sales s
    JOIN customers c ON s.customer_id = c.customer_id
    WHERE c.customer_segment = 'VIP'
)
SELECT 
    p.category,
    COUNT(*) AS vip_purchase_count,
    SUM(vp.sales_amount) AS vip_total_sales,
    AVG(vp.sales_amount) AS vip_avg_purchase
FROM vip_purchases vp
JOIN products p ON vp.product_id = p.product_id
GROUP BY p.category
ORDER BY vip_total_sales DESC;
```

解説: 
- 複雑な分析は複数のCTEで段階的に組み立てる
- 各CTEで中間結果に名前を付けることで、コードの意図が明確になります

---

## 🎓 チャレンジ問題

### 問題34: 月別コホート分析（新規・既存顧客）

問題: 月ごとに、新規顧客と既存顧客の売上を分けて集計してください。

回答例
```sql
WITH first_purchase AS (
    SELECT 
        customer_id,
        MIN(sale_date) AS first_purchase_date
    FROM sales
    GROUP BY customer_id
)
SELECT 
    EXTRACT(YEAR FROM s.sale_date) AS sale_year,
    EXTRACT(MONTH FROM s.sale_date) AS sale_month,
    SUM(CASE 
        WHEN EXTRACT(YEAR FROM s.sale_date) = EXTRACT(YEAR FROM fp.first_purchase_date)
         AND EXTRACT(MONTH FROM s.sale_date) = EXTRACT(MONTH FROM fp.first_purchase_date)
        THEN s.quantity * s.unit_price * (1 - s.discount_rate)
        ELSE 0 
    END) AS new_customer_revenue,
    SUM(CASE 
        WHEN EXTRACT(YEAR FROM s.sale_date) != EXTRACT(YEAR FROM fp.first_purchase_date)
          OR EXTRACT(MONTH FROM s.sale_date) != EXTRACT(MONTH FROM fp.first_purchase_date)
        THEN s.quantity * s.unit_price * (1 - s.discount_rate)
        ELSE 0 
    END) AS existing_customer_revenue,
    COUNT(DISTINCT CASE 
        WHEN EXTRACT(YEAR FROM s.sale_date) = EXTRACT(YEAR FROM fp.first_purchase_date)
         AND EXTRACT(MONTH FROM s.sale_date) = EXTRACT(MONTH FROM fp.first_purchase_date)
        THEN s.customer_id 
    END) AS new_customers,
    COUNT(DISTINCT CASE 
        WHEN EXTRACT(YEAR FROM s.sale_date) != EXTRACT(YEAR FROM fp.first_purchase_date)
          OR EXTRACT(MONTH FROM s.sale_date) != EXTRACT(MONTH FROM fp.first_purchase_date)
        THEN s.customer_id 
    END) AS existing_customers
FROM sales s
JOIN first_purchase fp ON s.customer_id = fp.customer_id
GROUP BY EXTRACT(YEAR FROM s.sale_date), EXTRACT(MONTH FROM s.sale_date)
ORDER BY sale_year, sale_month;
```

解説: 
- コホート分析は実務で重要な分析手法
- CTE + CASE式 + EXTRACT の総合的な活用
- 完全に標準SQL準拠

---

## 🎯 学習の進め方

1. 基礎編（1-6）: SELECT と WHERE に慣れる
2. 実務編（7-8）: AS句とビジネスドメイン用語の重要性を理解
3. 関数編（9-16）: 日付・文字列関数をマスター（全て標準SQL）
4. 中級編（17-19）: JOIN と集計をマスター
5. 応用編Part1（20-23）: CASE式で複雑なロジックを表現
6. 応用編Part2（24-26）: 縦持ち⇔横持ち変換をマスター
7. 応用編Part3（27-31）: Window関数で高度な分析
8. 応用編Part4（32-33）: CTEで読みやすいクエリを書く技術
9. チャレンジ（34）: 総合的な実践問題

全34問、全て標準SQL準拠です。頑張ってください！