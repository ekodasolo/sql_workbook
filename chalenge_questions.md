# SQL チャレンジ問題集

小売店のデータ分析を題材にした実践的な問題です。
EXERCISES（問題1-34）で学んだ技術を組み合わせて解いてください。

---

## 🎯 チャレンジ問題 1: 売れ筋商品TOP5の分析

ビジネスシナリオ:
あなたは小売店のデータアナリストです。経営陣から「売上トップ5の商品について、全体売上に占める割合も知りたい」という依頼を受けました。各商品の売上金額、全体に占める割合、累積割合を計算してください。

求める結果:
- 商品名
- 売上金額
- 全体売上に占める割合（%）
- 累積割合（%）

💡 ヒント
- Window関数の SUM() OVER() で全体売上を計算
- 割合は (商品売上 / 全体売上) * 100
- 累積割合は SUM() OVER (ORDER BY ...) を使用


✅ 回答例を見る

```sql
WITH product_sales AS (
    SELECT 
        p.product_name,
        SUM(s.quantity * s.unit_price * (1 - s.discount_rate)) AS total_sales
    FROM sales s
    JOIN products p ON s.product_id = p.product_id
    GROUP BY p.product_name
),
ranked_products AS (
    SELECT 
        product_name,
        total_sales,
        SUM(total_sales) OVER () AS overall_sales,
        ROW_NUMBER() OVER (ORDER BY total_sales DESC) AS rank
    FROM product_sales
)
SELECT 
    product_name,
    ROUND(total_sales, 2) AS total_sales,
    ROUND((total_sales * 100.0 / overall_sales), 2) AS sales_percentage,
    ROUND(SUM(total_sales * 100.0 / overall_sales) OVER (ORDER BY total_sales DESC), 2) AS cumulative_percentage
FROM ranked_products
WHERE rank <= 5
ORDER BY total_sales DESC;
```

解説: 
- CTEで商品別売上を集計
- Window関数で全体売上を計算（PARTITION BY なし）
- 累積割合で、上位商品が全体の何%を占めるかを把握
- パレート分析（20%の商品が80%の売上を作る）に使える


---

## 🎯 チャレンジ問題 2: リピート顧客の購買サイクル分析

ビジネスシナリオ:
マーケティングチームから「リピート顧客の平均購買サイクル（購入間隔）を知りたい。これを元にリマインドメールのタイミングを決めたい」という依頼がありました。各顧客の平均購買間隔を計算してください。

求める結果:
- 顧客名
- 購入回数
- 平均購買間隔（日数）
- 最終購入日からの経過日数

💡 ヒント
- LAG() で前回購入日を取得
- 日付の引き算で間隔を計算
- AVG() で平均を計算
- 2回以上購入した顧客のみ対象（HAVING）


✅ 回答例を見る

```sql
WITH purchase_intervals AS (
    SELECT 
        customer_id,
        sale_date,
        sale_date - LAG(sale_date) OVER (PARTITION BY customer_id ORDER BY sale_date) AS days_since_last
    FROM sales
),
customer_cycle AS (
    SELECT 
        customer_id,
        COUNT(*) AS purchase_count,
        AVG(days_since_last) AS avg_purchase_interval,
        MAX(sale_date) AS last_purchase_date
    FROM purchase_intervals
    GROUP BY customer_id
    HAVING COUNT(*) >= 2
)
SELECT 
    c.customer_name,
    cc.purchase_count,
    ROUND(cc.avg_purchase_interval, 1) AS avg_interval_days,
    DATE '2024-01-31' - cc.last_purchase_date AS days_since_last_purchase
FROM customer_cycle cc
JOIN customers c ON cc.customer_id = c.customer_id
WHERE cc.avg_purchase_interval IS NOT NULL
ORDER BY cc.purchase_count DESC, cc.avg_purchase_interval
LIMIT 20;
```

解説: 
- LAG()で前回購入日を取得し、間隔を計算
- 平均購買間隔が短い = ロイヤリティが高い顧客
- 最終購入日からの経過日数と比較することで、リマインドタイミングを判断
- リテンションマーケティングの基本分析


---

## 🎯 チャレンジ問題 3: 曜日別の売上パターン分析

ビジネスシナリオ:
店舗マネージャーから「シフト計画を最適化したい。どの曜日が忙しいか分析してほしい」と言われました。曜日ごとの売上件数、平均売上金額、客単価を分析してください。

求める結果:
- 曜日
- 売上件数
- 売上合計
- 平均客単価
- 売上ランキング

💡 ヒント
- EXTRACT(DOW FROM date) で曜日番号を取得
- CASE式で曜日名に変換
- GROUP BY で曜日ごとに集計


✅ 回答例を見る

```sql
WITH daily_sales AS (
    SELECT 
        EXTRACT(DOW FROM sale_date) AS dow,
        CASE EXTRACT(DOW FROM sale_date)
            WHEN 0 THEN 'Sunday'
            WHEN 1 THEN 'Monday'
            WHEN 2 THEN 'Tuesday'
            WHEN 3 THEN 'Wednesday'
            WHEN 4 THEN 'Thursday'
            WHEN 5 THEN 'Friday'
            WHEN 6 THEN 'Saturday'
        END AS day_of_week,
        COUNT(*) AS transaction_count,
        SUM(quantity * unit_price * (1 - discount_rate)) AS total_sales,
        AVG(quantity * unit_price * (1 - discount_rate)) AS avg_transaction_value
    FROM sales
    GROUP BY EXTRACT(DOW FROM sale_date)
)
SELECT 
    day_of_week,
    transaction_count,
    ROUND(total_sales, 2) AS total_sales,
    ROUND(avg_transaction_value, 2) AS avg_transaction_value,
    RANK() OVER (ORDER BY total_sales DESC) AS sales_rank
FROM daily_sales
ORDER BY dow;
```

解説: 
- 曜日別の売上パターンを把握
- 売上件数が多い曜日と客単価が高い曜日は異なる場合がある
- スタッフ配置、在庫計画、キャンペーン実施日の決定に活用


---

## 🎯 チャレンジ問題 4: 顧客セグメント別の収益性分析

ビジネスシナリオ:
経営陣から「VIP顧客とRegular顧客、どちらに注力すべきか判断材料がほしい」と言われました。セグメント別に、顧客数、平均購入回数、平均LTV（顧客生涯価値）、割引利用率を分析してください。

求める結果:
- 顧客セグメント
- 顧客数
- 平均購入回数
- 平均LTV（総購入金額）
- 割引利用率（%）

💡 ヒント
- まず顧客ごとに集計してから、セグメントごとに平均を取る
- CTEを2段階で使用
- 割引利用率 = 割引を使った取引数 / 全取引数


✅ 回答例を見る

```sql
WITH customer_metrics AS (
    SELECT 
        s.customer_id,
        c.customer_segment,
        COUNT(*) AS purchase_count,
        SUM(s.quantity * s.unit_price * (1 - s.discount_rate)) AS lifetime_value,
        SUM(CASE WHEN s.discount_rate > 0 THEN 1 ELSE 0 END) AS discounted_purchases,
        COUNT(*) AS total_purchases
    FROM sales s
    JOIN customers c ON s.customer_id = c.customer_id
    GROUP BY s.customer_id, c.customer_segment
)
SELECT 
    customer_segment,
    COUNT(DISTINCT customer_id) AS customer_count,
    ROUND(AVG(purchase_count), 2) AS avg_purchase_count,
    ROUND(AVG(lifetime_value), 2) AS avg_lifetime_value,
    ROUND(AVG(discounted_purchases * 100.0 / total_purchases), 2) AS discount_usage_rate
FROM customer_metrics
GROUP BY customer_segment
ORDER BY avg_lifetime_value DESC;
```

解説: 
- セグメント別の収益性を多角的に分析
- VIP顧客の方が購入回数が多く、LTVも高いことを定量的に確認
- マーケティング予算配分、顧客育成戦略の立案に活用


---

## 🎯 チャレンジ問題 5: 商品カテゴリ別の在庫回転分析

ビジネスシナリオ:
在庫管理担当から「カテゴリ別に、どれくらいの頻度で売れているか知りたい。発注計画を立てたい」という要望がありました。カテゴリごとの月平均販売数、販売頻度（平均何日に1回売れるか）を分析してください。

求める結果:
- 商品カテゴリ
- 総販売数
- 販売日数（売れた日の数）
- 1日あたり平均販売数
- 平均販売間隔（日）

💡 ヒント
- COUNT(DISTINCT date) で販売日数を計算
- 全体の日数 / 販売日数で平均間隔を計算


✅ 回答例を見る

```sql
WITH category_sales AS (
    SELECT 
        p.category,
        s.sale_date,
        SUM(s.quantity) AS daily_quantity
    FROM sales s
    JOIN products p ON s.product_id = p.product_id
    GROUP BY p.category, s.sale_date
),
date_range AS (
    SELECT 
        MIN(sale_date) AS start_date,
        MAX(sale_date) AS end_date,
        MAX(sale_date) - MIN(sale_date) + 1 AS total_days
    FROM sales
)
SELECT 
    cs.category,
    SUM(cs.daily_quantity) AS total_quantity_sold,
    COUNT(DISTINCT cs.sale_date) AS days_with_sales,
    ROUND(SUM(cs.daily_quantity) * 1.0 / COUNT(DISTINCT cs.sale_date), 2) AS avg_daily_sales,
    ROUND(dr.total_days * 1.0 / COUNT(DISTINCT cs.sale_date), 2) AS avg_days_between_sales
FROM category_sales cs
CROSS JOIN date_range dr
GROUP BY cs.category, dr.total_days
ORDER BY total_quantity_sold DESC;
```

解説: 
- 販売頻度の高いカテゴリは在庫を多めに確保
- 販売間隔が長いカテゴリは在庫を絞る
- 在庫最適化、発注タイミングの決定に活用


---

## 🎯 チャレンジ問題 6: 月次成長率トレンド分析

ビジネスシナリオ:
投資家向けレポートのために「月次売上の前月比成長率を見せてほしい」と言われました。各月の売上、前月比、成長率を計算してください。

求める結果:
- 年月
- 月次売上
- 前月売上
- 前月比差額
- 成長率（%）

💡 ヒント
- LAG() で前月の売上を取得
- 成長率 = (当月 - 前月) / 前月 * 100


✅ 回答例を見る

```sql
WITH monthly_sales AS (
    SELECT 
        EXTRACT(YEAR FROM sale_date) AS sale_year,
        EXTRACT(MONTH FROM sale_date) AS sale_month,
        SUM(quantity * unit_price * (1 - discount_rate)) AS monthly_revenue
    FROM sales
    GROUP BY EXTRACT(YEAR FROM sale_date), EXTRACT(MONTH FROM sale_date)
)
SELECT 
    sale_year,
    sale_month,
    ROUND(monthly_revenue, 2) AS current_month_revenue,
    ROUND(LAG(monthly_revenue) OVER (ORDER BY sale_year, sale_month), 2) AS previous_month_revenue,
    ROUND(monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY sale_year, sale_month), 2) AS revenue_change,
    ROUND(
        (monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY sale_year, sale_month)) * 100.0 
        / LAG(monthly_revenue) OVER (ORDER BY sale_year, sale_month), 
        2
    ) AS growth_rate_percent
FROM monthly_sales
ORDER BY sale_year, sale_month;
```

解説: 
- 前月比成長率で事業の成長トレンドを把握
- マイナス成長の月は原因分析が必要
- 経営判断、投資家レポート、予算策定に活用


---

## 🎯 チャレンジ問題 7: 割引効果の測定

ビジネスシナリオ:
マーケティング部門から「割引キャンペーンは本当に効果があるのか？割引あり・なしで購入数量や客数を比較したい」という依頼がありました。割引の有無別に分析してください。

求める結果:
- 割引有無
- 取引件数
- ユニーク顧客数
- 平均購入数量
- 平均購入金額
- 総売上
- 割引総額

💡 ヒント
- CASE式で割引有無を分類
- GROUP BYで集計
- COUNT(DISTINCT) でユニーク顧客数


✅ 回答例を見る

```sql
SELECT 
    CASE 
        WHEN discount_rate > 0 THEN 'With Discount'
        ELSE 'No Discount'
    END AS discount_status,
    COUNT(*) AS transaction_count,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(AVG(quantity), 2) AS avg_quantity,
    ROUND(AVG(quantity * unit_price * (1 - discount_rate)), 2) AS avg_transaction_value,
    ROUND(SUM(quantity * unit_price * (1 - discount_rate)), 2) AS total_revenue,
    ROUND(SUM(quantity * unit_price * discount_rate), 2) AS total_discount_given
FROM sales
GROUP BY 
    CASE 
        WHEN discount_rate > 0 THEN 'With Discount'
        ELSE 'No Discount'
    END
ORDER BY total_revenue DESC;
```

解説: 
- 割引の効果を多角的に評価
- 割引で取引件数が増えても、利益率は下がる可能性
- 割引を使わない顧客の方が客単価が高い場合もある
- プロモーション戦略、価格設定の最適化に活用


---

## 🎯 チャレンジ問題 8: RFM分析（優良顧客の特定）

ビジネスシナリオ:
CRM担当から「優良顧客を特定して、特別なサービスを提供したい。RFM分析をしてほしい」と依頼されました。各顧客のRecency（最新購入日）、Frequency（購入回数）、Monetary（総購入金額）を計算し、スコア化してください。

求める結果:
- 顧客名
- 最終購入日
- 最終購入からの日数
- 購入回数
- 総購入金額
- RFMセグメント

💡 ヒント
- 各指標を計算
- NTILE() で各指標を4分割してスコア化
- スコアの組み合わせでセグメント分類


✅ 回答例を見る

```sql
WITH customer_rfm AS (
    SELECT 
        customer_id,
        MAX(sale_date) AS last_purchase_date,
        DATE '2024-01-31' - MAX(sale_date) AS recency_days,
        COUNT(*) AS frequency,
        SUM(quantity * unit_price * (1 - discount_rate)) AS monetary
    FROM sales
    GROUP BY customer_id
),
rfm_scores AS (
    SELECT 
        customer_id,
        last_purchase_date,
        recency_days,
        frequency,
        monetary,
        NTILE(4) OVER (ORDER BY recency_days) AS recency_score,
        NTILE(4) OVER (ORDER BY frequency DESC) AS frequency_score,
        NTILE(4) OVER (ORDER BY monetary DESC) AS monetary_score
    FROM customer_rfm
)
SELECT 
    c.customer_name,
    rs.last_purchase_date,
    rs.recency_days,
    rs.frequency,
    ROUND(rs.monetary, 2) AS total_spent,
    rs.recency_score,
    rs.frequency_score,
    rs.monetary_score,
    CASE 
        WHEN rs.frequency_score >= 3 AND rs.monetary_score >= 3 THEN 'Champions'
        WHEN rs.recency_score <= 2 AND rs.frequency_score >= 3 THEN 'Loyal Customers'
        WHEN rs.recency_score <= 2 AND rs.monetary_score >= 3 THEN 'Big Spenders'
        WHEN rs.recency_score >= 3 THEN 'At Risk'
        ELSE 'Regular'
    END AS customer_segment
FROM rfm_scores rs
JOIN customers c ON rs.customer_id = c.customer_id
ORDER BY rs.monetary DESC
LIMIT 30;
```

解説: 
- RFM分析はマーケティングの基本フレームワーク
- Champions: 最優良顧客（頻繁に購入、高額、最近も購入）
- At Risk: 離反リスク顧客（最近購入がない）
- 顧客セグメント別のマーケティング施策に活用


---

## 🎯 チャレンジ問題 9: 新規顧客 vs 既存顧客の貢献度分析

ビジネスシナリオ:
経営会議で「新規顧客獲得と既存顧客維持、どちらに投資すべきか？」という議論になりました。月ごとに、新規顧客と既存顧客の売上貢献を分析してください。

求める結果:
- 年月
- 新規顧客数
- 新規顧客売上
- 既存顧客数
- 既存顧客売上
- 新規顧客の売上比率（%）

💡 ヒント
- CTEで各顧客の初回購入月を計算
- 売上月と初回購入月を比較
- CASE式で新規/既存を判定


✅ 回答例を見る

```sql
WITH first_purchase AS (
    SELECT 
        customer_id,
        EXTRACT(YEAR FROM MIN(sale_date)) AS first_purchase_year,
        EXTRACT(MONTH FROM MIN(sale_date)) AS first_purchase_month
    FROM sales
    GROUP BY customer_id
)
SELECT 
    EXTRACT(YEAR FROM s.sale_date) AS sale_year,
    EXTRACT(MONTH FROM s.sale_date) AS sale_month,
    COUNT(DISTINCT CASE 
        WHEN EXTRACT(YEAR FROM s.sale_date) = fp.first_purchase_year 
         AND EXTRACT(MONTH FROM s.sale_date) = fp.first_purchase_month
        THEN s.customer_id 
    END) AS new_customers,
    ROUND(SUM(CASE 
        WHEN EXTRACT(YEAR FROM s.sale_date) = fp.first_purchase_year 
         AND EXTRACT(MONTH FROM s.sale_date) = fp.first_purchase_month
        THEN s.quantity * s.unit_price * (1 - s.discount_rate)
        ELSE 0 
    END), 2) AS new_customer_revenue,
    COUNT(DISTINCT CASE 
        WHEN EXTRACT(YEAR FROM s.sale_date) != fp.first_purchase_year 
          OR EXTRACT(MONTH FROM s.sale_date) != fp.first_purchase_month
        THEN s.customer_id 
    END) AS existing_customers,
    ROUND(SUM(CASE 
        WHEN EXTRACT(YEAR FROM s.sale_date) != fp.first_purchase_year 
          OR EXTRACT(MONTH FROM s.sale_date) != fp.first_purchase_month
        THEN s.quantity * s.unit_price * (1 - s.discount_rate)
        ELSE 0 
    END), 2) AS existing_customer_revenue,
    ROUND(
        SUM(CASE 
            WHEN EXTRACT(YEAR FROM s.sale_date) = fp.first_purchase_year 
             AND EXTRACT(MONTH FROM s.sale_date) = fp.first_purchase_month
            THEN s.quantity * s.unit_price * (1 - s.discount_rate)
            ELSE 0 
        END) * 100.0 / 
        SUM(s.quantity * s.unit_price * (1 - s.discount_rate)), 
        2
    ) AS new_customer_revenue_ratio
FROM sales s
JOIN first_purchase fp ON s.customer_id = fp.customer_id
GROUP BY EXTRACT(YEAR FROM s.sale_date), EXTRACT(MONTH FROM s.sale_date)
ORDER BY sale_year, sale_month;
```

解説: 
- 新規顧客獲得と既存顧客維持のバランスを可視化
- 既存顧客売上が大半を占めるのが健全（リテンションが機能している証拠）
- 新規顧客売上比率が高すぎる = リテンション施策が不足
- マーケティング予算配分、事業の持続可能性評価に活用


---

## 🎯 チャレンジ問題 10: 店舗別パフォーマンスランキング

ビジネスシナリオ:
店舗運営部門から「全店舗のパフォーマンスを比較したい。売上だけでなく、客数、客単価、商品カテゴリ別構成比も見たい」と依頼されました。店舗別の総合評価レポートを作成してください。

求める結果:
- 店舗名
- 総売上
- 取引件数
- ユニーク顧客数
- 平均客単価
- 家電売上比率（%）
- 家具売上比率（%）
- 売上ランク

💡 ヒント
- 店舗ごとに集計
- CASE式でカテゴリ別売上を計算（ピボット）
- 割合計算
- RANK() で順位付け


✅ 回答例を見る

```sql
WITH store_performance AS (
    SELECT 
        st.store_name,
        COUNT(*) AS transaction_count,
        COUNT(DISTINCT s.customer_id) AS unique_customers,
        SUM(s.quantity * s.unit_price * (1 - s.discount_rate)) AS total_revenue,
        AVG(s.quantity * s.unit_price * (1 - s.discount_rate)) AS avg_transaction_value,
        SUM(CASE WHEN p.category = '家電' 
            THEN s.quantity * s.unit_price * (1 - s.discount_rate) 
            ELSE 0 
        END) AS electronics_revenue,
        SUM(CASE WHEN p.category = '家具' 
            THEN s.quantity * s.unit_price * (1 - s.discount_rate) 
            ELSE 0 
        END) AS furniture_revenue
    FROM sales s
    JOIN stores st ON s.store_id = st.store_id
    JOIN products p ON s.product_id = p.product_id
    GROUP BY st.store_name
)
SELECT 
    store_name,
    ROUND(total_revenue, 2) AS total_revenue,
    transaction_count,
    unique_customers,
    ROUND(avg_transaction_value, 2) AS avg_transaction_value,
    ROUND(electronics_revenue * 100.0 / total_revenue, 2) AS electronics_ratio,
    ROUND(furniture_revenue * 100.0 / total_revenue, 2) AS furniture_ratio,
    RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank,
    RANK() OVER (ORDER BY avg_transaction_value DESC) AS avg_value_rank
FROM store_performance
ORDER BY total_revenue DESC;
```

解説: 
- 店舗パフォーマンスを多角的に評価
- 売上が高い店舗と客単価が高い店舗は異なる場合がある
- カテゴリ構成比で各店舗の特徴を把握
- 店舗運営改善、優秀店舗のベストプラクティス抽出に活用


---

## 📚 チャレンジ問題で使った技術のまとめ

これら10問を通じて、以下の実務スキルを習得できます：

### 分析テクニック
1. 割合・比率計算: パレート分析、成長率、構成比
2. Window関数の応用: 累積計算、ランキング、前月比
3. 時系列分析: トレンド、季節性、成長率
4. 顧客分析: RFM、セグメンテーション、LTV
5. 効果測定: 割引効果、A/Bテスト的な比較

### SQL技術
- 複数段階のCTE
- Window関数（LAG, LEAD, NTILE, RANK, SUM() OVER()）
- CASE式の複雑な使い方
- 日付計算（EXTRACT, 日付の引き算）
- 割合・比率計算
- GROUP BY + HAVING
- サブクエリとJOIN

### ビジネス応用
- 在庫管理
- マーケティング最適化
- 顧客セグメンテーション
- 店舗運営改善
- 経営判断支援

これらの問題を解けるようになれば、実務のデータ分析業務に十分対応できます！ 🎉
