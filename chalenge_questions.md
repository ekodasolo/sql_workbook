# SQL チャレンジ問題集

小売店のデータ分析を題材にした実践的な問題です。
EXERCISES（問題1-37）で学んだ技術を組み合わせて解いてください。

---

## 🔧 この問題集で新たに使う要素

チャレンジ問題では、EXERCISES で扱わなかった以下の要素が登場します。
初めて見る構文ですが、いずれも実務で頻出なので、ここで慣れておきましょう。

### ROUND() — 数値の丸め

小数点以下を指定した桁数に丸める関数です（標準SQL）。

```sql
ROUND(3.14159, 2)  -- 結果: 3.14（小数点以下2桁に丸め）
ROUND(1234.5, 0)   -- 結果: 1235（整数に丸め）
```

分析レポートでは金額や比率を見やすくするために多用します。
この問題集ではほぼ全問で使用します。

### CROSS JOIN — 全行の組み合わせ結合

通常の JOIN は結合条件（ON）で行を対応させますが、CROSS JOIN は条件なしで全ての組み合わせを生成します。

```sql
-- テーブルAが3行、テーブルBが2行なら、結果は 3×2 = 6行
SELECT * FROM table_a CROSS JOIN table_b;
```

「全ての行に同じ値を付けたい」場面で便利です。
特に、集計値（1行だけの結果）を全行に結合する場合に使います。

```sql
-- 例: 全体の日数を各カテゴリ行に付与する
WITH date_range AS (
    SELECT MAX(sale_date) - MIN(sale_date) + 1 AS total_days
    FROM sales
)
SELECT cs.category, cs.count, dr.total_days
FROM category_summary cs
CROSS JOIN date_range dr;  -- date_range は1行なので、各カテゴリ行にtotal_daysが付く
```

この問題集では問題5で使用します。

### SUM() OVER()（PARTITION BY なし）— 全体合計をWindow関数で計算

EXERCISES では `SUM() OVER (PARTITION BY ...)` のようにグループを指定しましたが、
PARTITION BY を省略すると「全行を対象にした合計」を各行に付与できます。

```sql
-- 各行に全体合計を付けて、割合を計算する例
SELECT 
    product_name,
    total_sales,
    SUM(total_sales) OVER () AS overall_total,          -- 全体合計
    total_sales * 100.0 / SUM(total_sales) OVER () AS pct  -- 全体に占める割合
FROM product_summary;
```

この問題集では問題1で使用します。

---

## 🎯 チャレンジ問題 1: 売れ筋商品TOP5の分析｜★★★★☆（目安：20分）

ビジネスシナリオ:
あなたは小売店のデータアナリストです。経営陣から「売上トップ5の商品について、全体売上に占める割合も知りたい」という依頼を受けました。各商品の売上金額、全体に占める割合、累積割合を計算してください。

求める結果:
- 商品名（product_name）
- 売上金額（total_sales）
- 全体売上に占める割合（sales_percentage：%）
- 累積割合（cumulative_percentage：%）

💡 ヒント
- CTEで商品ごとの売上を集計
- Window関数の SUM() OVER() （PARTITION BY なし）で全体売上を計算
- 割合は (商品売上 / 全体売上) * 100
- 累積割合は SUM() OVER (ORDER BY ...) を使用
- ROW_NUMBER() で順位を付けて、上位5件に絞る


✅ 回答例を見る

```sql
WITH product_sales AS (
    SELECT 
        p.product_name,
        SUM(s.quantity * s.unit_price * (1 - s.discount_rate)) AS total_sales
    FROM sales s
    JOIN products p ON s.product_id = p.product_id
    GROUP BY p.product_name
)
SELECT 
    product_name,
    ROUND(total_sales, 2) AS total_sales,
    ROUND(total_sales * 100.0 / SUM(total_sales) OVER (), 2) AS sales_percentage,
    ROUND(SUM(total_sales * 100.0 / SUM(total_sales) OVER ()) OVER (ORDER BY total_sales DESC), 2) AS cumulative_percentage
FROM product_sales
ORDER BY total_sales DESC
LIMIT 5;
```

解説: 
- CTEで商品別売上を集計し、メインクエリでWindow関数を使って割合を計算
- `SUM(total_sales) OVER ()` は PARTITION BY なしなので「全商品の売上合計」を意味する
- 累積割合で、上位商品が全体の何%を占めるかを把握
- パレート分析（20%の商品が80%の売上を作る）に使える


---

## 🎯 チャレンジ問題 2: リピート顧客の購買サイクル分析｜★★★★☆（目安：25分）

ビジネスシナリオ:
マーケティングチームから「リピート顧客の平均購買サイクル（購入間隔）を知りたい。これを元にリマインドメールのタイミングを決めたい」という依頼がありました。各顧客の平均購買間隔を計算してください。

求める結果:
- 顧客名（customer_name）
- 購入回数（purchase_count）
- 平均購買間隔（avg_interval_days：日数）
- 最終購入日からの経過日数（days_since_last_purchase）

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

## 🎯 チャレンジ問題 3: ABC分析（商品の重要度分類）｜★★★★☆（目安：25分）

ビジネスシナリオ:
購買部門から「商品ごとの売上貢献度を把握して、仕入れの優先順位を決めたい。売上上位70%を占める商品をAランク、次の20%をBランク、残りをCランクに分類してほしい」という依頼がありました。

求める結果:
- 商品名（product_name）
- 売上金額（total_sales）
- 全体に占める割合（sales_percentage：%）
- 累積割合（cumulative_percentage：%）
- ABCランク（abc_rank）
  - 累積割合が70%以下 → 'A'
  - 累積割合が90%以下 → 'B'
  - それ以外 → 'C'

💡 ヒント
- CTEで商品別売上を集計
- Window関数で全体売上と累積割合を計算
- 累積割合を元にCASE式でA/B/Cに分類
- 売上の大きい順に並べる


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
product_ranking AS (
    SELECT 
        product_name,
        total_sales,
        ROUND(total_sales * 100.0 / SUM(total_sales) OVER (), 2) AS sales_percentage,
        ROUND(SUM(total_sales) OVER (ORDER BY total_sales DESC) * 100.0 / SUM(total_sales) OVER (), 2) AS cumulative_percentage
    FROM product_sales
)
SELECT 
    product_name,
    ROUND(total_sales, 2) AS total_sales,
    sales_percentage,
    cumulative_percentage,
    CASE 
        WHEN cumulative_percentage <= 70 THEN 'A'
        WHEN cumulative_percentage <= 90 THEN 'B'
        ELSE 'C'
    END AS abc_rank
FROM product_ranking
ORDER BY total_sales DESC;
```

解説: 
- ABC分析は在庫管理・仕入れ計画の定番フレームワーク
- Aランク商品: 売上の大部分を占める少数の重要商品（最優先で在庫確保）
- Bランク商品: 中程度の貢献（安定供給を維持）
- Cランク商品: 貢献度が低い（在庫を絞る候補）
- パレートの法則（80:20の法則）に基づく分析


---

## 🎯 チャレンジ問題 4: 顧客セグメント別の収益性分析｜★★★★☆（目安：25分）

ビジネスシナリオ:
経営陣から「VIP顧客とRegular顧客、どちらに注力すべきか判断材料がほしい」と言われました。セグメント別に、顧客数、平均購入回数、平均LTV（顧客生涯価値）、割引利用率を分析してください。

求める結果:
- 顧客セグメント（customer_segment）
- 顧客数（customer_count）
- 平均購入回数（avg_purchase_count）
- 平均LTV / 総購入金額（avg_lifetime_value）
- 割引利用率（discount_usage_rate：%）

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

## 🎯 チャレンジ問題 5: 商品カテゴリ別の在庫回転分析｜★★★★☆（目安：25分）

ビジネスシナリオ:
在庫管理担当から「カテゴリ別に、どれくらいの頻度で売れているか知りたい。発注計画を立てたい」という要望がありました。カテゴリごとの月平均販売数、販売頻度（平均何日に1回売れるか）を分析してください。

求める結果:
- 商品カテゴリ（category）
- 総販売数（total_quantity_sold）
- 販売日数 / 売れた日の数（days_with_sales）
- 1日あたり平均販売数（avg_daily_sales）
- 平均販売間隔 / 日（avg_days_between_sales）

💡 ヒント
- CTEを2つ使います：カテゴリ×日ごとの販売数と、全体の日数範囲
- COUNT(DISTINCT date) で販売日数を計算
- 全体の日数 / 販売日数 で平均間隔を計算
- 2つのCTEを CROSS JOIN で結合します
  - date_range は1行だけの結果なので、CROSS JOIN しても行数は増えません
  - 「全カテゴリ行に同じ total_days の値を付ける」ための結合です


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
- date_range CTEは1行だけの結果を返すため、CROSS JOINしても行数に影響しない
- `GROUP BY cs.category, dr.total_days` で dr.total_days を含めているのは、GROUP BY に含まれない列は SELECT で参照できないため（集計関数の外で使う場合）
- 販売頻度の高いカテゴリは在庫を多めに確保
- 販売間隔が長いカテゴリは在庫を絞る
- 在庫最適化、発注タイミングの決定に活用


---

## 🎯 チャレンジ問題 6: 月次成長率トレンド分析｜★★★☆☆（目安：20分）

ビジネスシナリオ:
投資家向けレポートのために「月次売上の前月比成長率を見せてほしい」と言われました。各月の売上、前月比、成長率を計算してください。

求める結果:
- 年（sale_year）
- 月（sale_month）
- 月次売上（current_month_revenue）
- 前月売上（previous_month_revenue）
- 前月比差額（revenue_change）
- 成長率（growth_rate_percent：%）

💡 ヒント
- CTEで月次売上を集計
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

## 🎯 チャレンジ問題 7: 割引効果の測定｜★★★☆☆（目安：15分）

ビジネスシナリオ:
マーケティング部門から「割引キャンペーンは本当に効果があるのか？割引あり・なしで購入数量や客数を比較したい」という依頼がありました。割引の有無別に分析してください。

求める結果:
- 割引有無（discount_status）
- 取引件数（transaction_count）
- ユニーク顧客数（unique_customers）
- 平均購入数量（avg_quantity）
- 平均購入金額（avg_transaction_value）
- 総売上（total_revenue）
- 割引総額（total_discount_given）

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

## 🎯 チャレンジ問題 8: RFM分析（優良顧客の特定）｜★★★★★（目安：30分）

ビジネスシナリオ:
CRM担当から「優良顧客を特定して、特別なサービスを提供したい。RFM分析をしてほしい」と依頼されました。各顧客のRecency（最新購入日）、Frequency（購入回数）、Monetary（総購入金額）を計算し、スコア化してください。

求める結果:
- 顧客名（customer_name）
- 最終購入日（last_purchase_date）
- 最終購入からの日数（recency_days）
- 購入回数（frequency）
- 総購入金額（total_spent）
- 各スコア（recency_score, frequency_score, monetary_score）
- RFMセグメント（customer_segment）
  - frequency_score >= 3 かつ monetary_score >= 3 → 'Champions'
  - recency_score <= 2 かつ frequency_score >= 3 → 'Loyal Customers'
  - recency_score <= 2 かつ monetary_score >= 3 → 'Big Spenders'
  - recency_score >= 3 → 'At Risk'
  - それ以外 → 'Regular'

💡 ヒント
- CTEで各顧客のRFM指標を計算
- NTILE(4) で各指標を4分割してスコア化
  - recency_score: 最近購入した人ほど高スコア（日数の昇順でNTILE）
  - frequency_score: 多く購入した人ほど高スコア（降順でNTILE）
  - monetary_score: 金額が多い人ほど高スコア（降順でNTILE）
- CASE式でスコアの組み合わせからセグメントを分類


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

## 🎯 チャレンジ問題 9: コホート別リテンション分析｜★★★★★（目安：30分）

ビジネスシナリオ:
経営会議で「新規顧客がどれくらいリピートしてくれているのか？初回購入月ごとに、2回目の購入率を追跡したい」という議論になりました。初回購入月（コホート）ごとに、翌月以降の再購入率を分析してください。

求める結果:
- 初回購入の年（cohort_year）
- 初回購入の月（cohort_month）
- コホートの顧客数（cohort_size）
- 翌月に再購入した顧客数（retained_month_1）
- 2ヶ月後に再購入した顧客数（retained_month_2）
- 翌月リテンション率（retention_rate_month_1：%）
- 2ヶ月後リテンション率（retention_rate_month_2：%）

💡 ヒント
- CTEで各顧客の初回購入月（コホート）を求める
- 各売上について、初回購入月からの経過月数を計算する
  - (売上年 - 初回年) * 12 + (売上月 - 初回月) で経過月数が出せる
- 経過月数が1の売上 → 翌月リピート、経過月数が2の売上 → 2ヶ月後リピート
- COUNT(DISTINCT CASE WHEN ...) で各期間のリピート顧客数を集計


✅ 回答例を見る

```sql
WITH customer_cohort AS (
    SELECT 
        customer_id,
        EXTRACT(YEAR FROM MIN(sale_date)) AS cohort_year,
        EXTRACT(MONTH FROM MIN(sale_date)) AS cohort_month
    FROM sales
    GROUP BY customer_id
),
sales_with_cohort AS (
    SELECT 
        s.customer_id,
        cc.cohort_year,
        cc.cohort_month,
        (EXTRACT(YEAR FROM s.sale_date) - cc.cohort_year) * 12 
            + (EXTRACT(MONTH FROM s.sale_date) - cc.cohort_month) AS months_since_first
    FROM sales s
    JOIN customer_cohort cc ON s.customer_id = cc.customer_id
)
SELECT 
    cohort_year,
    cohort_month,
    COUNT(DISTINCT CASE WHEN months_since_first = 0 THEN customer_id END) AS cohort_size,
    COUNT(DISTINCT CASE WHEN months_since_first = 1 THEN customer_id END) AS retained_month_1,
    COUNT(DISTINCT CASE WHEN months_since_first = 2 THEN customer_id END) AS retained_month_2,
    ROUND(
        COUNT(DISTINCT CASE WHEN months_since_first = 1 THEN customer_id END) * 100.0 
        / COUNT(DISTINCT CASE WHEN months_since_first = 0 THEN customer_id END),
        2
    ) AS retention_rate_month_1,
    ROUND(
        COUNT(DISTINCT CASE WHEN months_since_first = 2 THEN customer_id END) * 100.0 
        / COUNT(DISTINCT CASE WHEN months_since_first = 0 THEN customer_id END),
        2
    ) AS retention_rate_month_2
FROM sales_with_cohort
GROUP BY cohort_year, cohort_month
ORDER BY cohort_year, cohort_month;
```

解説: 
- コホートリテンション分析は SaaS・EC の最重要KPI
- 「初回購入月からの経過月数」を計算し、各月にリピートした顧客をカウント
- リテンション率が月を追うごとにどう変化するかで、顧客維持施策の効果がわかる
- リテンション率が低い → 商品品質・顧客体験の改善が必要
- リテンション率が安定 → 健全なビジネスモデルの証拠


---

## 🎯 チャレンジ問題 10: 店舗別パフォーマンスランキング｜★★★★★（目安：30分）

ビジネスシナリオ:
店舗運営部門から「全店舗のパフォーマンスを比較したい。売上だけでなく、客数、客単価、商品カテゴリ別構成比も見たい」と依頼されました。店舗別の総合評価レポートを作成してください。

**この問題で使用する追加テーブル:**

stores テーブル:

| カラム名 | 型 | 説明 |
|:---|:---|:---|
| store_id | INTEGER | 店舗ID（主キー） |
| store_name | VARCHAR | 店舗名 |

sales テーブルには store_id カラムがあり、stores テーブルと結合できます。

求める結果:
- 店舗名（store_name）
- 総売上（total_revenue）
- 取引件数（transaction_count）
- ユニーク顧客数（unique_customers）
- 平均客単価（avg_transaction_value）
- 家電売上比率（electronics_ratio：%）
- 家具売上比率（furniture_ratio：%）
- 売上ランク（revenue_rank）
- 客単価ランク（avg_value_rank）

💡 ヒント
- sales, stores, products の3テーブルを結合
- CASE式でカテゴリ別売上を計算（ピボット）
- 構成比 = カテゴリ売上 / 総売上 * 100
- RANK() OVER() で売上ランクと客単価ランクを付ける


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

これら10問を通じて、以下の実務スキルを習得できます。

### 分析テクニック
1. 割合・比率計算: パレート分析、ABC分析、成長率、構成比
2. Window関数の応用: 累積計算、ランキング、前月比、全体合計
3. 時系列分析: トレンド、成長率、コホート別リテンション
4. 顧客分析: RFM、セグメンテーション、LTV、リテンション率
5. 効果測定: 割引効果、A/Bテスト的な比較

### SQL技術
- 複数段階のCTE
- Window関数（LAG, NTILE, RANK, SUM() OVER(), SUM() OVER(ORDER BY)）
- CASE式の複雑な使い方
- 日付計算（EXTRACT, 日付の引き算, 経過月数の計算）
- ROUND() による数値の丸め
- CROSS JOIN（1行テーブルとの結合）
- 割合・比率計算
- GROUP BY + HAVING
- サブクエリとJOIN

### ビジネス応用
- 在庫管理（ABC分析、販売頻度分析）
- マーケティング最適化（割引効果、リテンション分析）
- 顧客セグメンテーション（RFM分析、LTV）
- 店舗運営改善（パフォーマンス比較）
- 経営判断支援（成長率トレンド、パレート分析）

これらの問題を解けるようになれば、実務のデータ分析業務に十分対応できます！ 🎉
