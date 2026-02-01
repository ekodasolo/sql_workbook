# SQL練習問題集

このファイルには、基礎から応用まで段階的に学べる練習問題が含まれています。
各問題にはヒントと回答例があります。まず自分で考えてから回答を見ましょう。

## 📌 完全標準SQL準拠

このドキュメントのクエリは標準SQL（ISO/IEC 9075）に準拠しています。(一部例外あり)
主要なデータベース（PostgreSQL、MySQL 8.0+、SQL Server、Oracle、BigQuery、Snowflakeなど）で動作します。

### 使用している標準SQL機能
- EXTRACT() - 日付から年月日、曜日を抽出
- SUBSTRING() - 文字列の部分取得
- CASE式 - 条件分岐
- Window関数 - RANK, ROW_NUMBER, LAG, LEAD など
- CTE（WITH句）- 複雑なクエリの構造化
- FETCH FIRST n ROWS ONLY - 結果件数の制限

---

## 📖 この資料の使い方

この問題集は「写経 → 改変 → 自力」の3つのステップで段階的に取り組むことを想定しています。
最初から自力で書ける必要はありません。自分のレベルに合ったステップから始めてください。

### ステップ1: 写経（基礎編におすすめ）
回答例を見ながら、そのままSQLを打ち込んで実行してください。
正しく動くことを確認しながら、構文の形に手を慣らす段階です。
「こう書くとこう動く」を体で覚えましょう。

### ステップ2: 改変（中級編におすすめ）
回答例を一度動かした後、条件や値を自分で変えてみてください。

- 「`quantity >= 5` を `>= 10` に変えたら結果はどう変わる？」
- 「カテゴリを `'家電'` から `'家具'` に変えたら？」
- 「`ORDER BY DESC` を `ASC` に変えたら？」

構文の意味を理解しているか、変えた結果から確認する段階です。

### ステップ3: 自力（応用編〜におすすめ）
回答例を見ずに、問題文とヒントだけでSQLを書いてみてください。
詰まったら「考え方のステップ」を参考にし、それでも書けなければ回答例を見てOKです。
最終的に自力で書けることがゴールですが、最初から完璧を目指す必要はありません。

---

## 📋 目次

- **📚 基礎編（SELECT, WHERE, ORDER BY）**
  - 問題1: 商品の一覧を確認する｜★☆☆☆☆（3分）— SELECT, FETCH FIRST
  - 問題2: 特定のカラムだけ表示｜★☆☆☆☆（3分）— SELECT, LIMIT
  - 💡 SQLの書き方スタイル（重要）— カンマの位置、改行、インデント
  - 問題3: 条件に合うデータを抽出｜★☆☆☆☆（5分）— WHERE, 比較演算子
  - 問題4: 複数条件での絞り込み｜★☆☆☆☆（5分）— WHERE, AND
  - 問題5: 並び替え｜★☆☆☆☆（5分）— ORDER BY, DESC
  - 問題6: 日付範囲での絞り込み｜★★☆☆☆（5分）— BETWEEN, DATE リテラル
- **🏷️ 実務編：AS句とビジネスドメイン用語**
  - 問題7: ビジネスドメインに合わせた列名を付ける｜★★☆☆☆（10分）— AS, 算術演算子
  - 問題8: 集計結果にわかりやすい名前を付ける｜★★☆☆☆（10分）— GROUP BY, COUNT, SUM, AVG, MIN, MAX
- **📅 関数編Part1：日付関数マスター**
  - 問題9: 日付から年月を取り出す｜★★☆☆☆（5分）— EXTRACT(YEAR / MONTH)
  - 問題10: 月次集計を行う｜★★☆☆☆（10分）— EXTRACT, GROUP BY, COUNT(DISTINCT)
  - 問題11: 曜日別の売上傾向を分析｜★★★☆☆（10分）— EXTRACT(DOW), CASE式
  - 問題12: 期間の計算（日数差）｜★★☆☆☆（10分）— 日付の引き算, HAVING
  - 問題13: 日付から年・月・日を個別に取り出す｜★★☆☆☆（5分）— EXTRACT(DAY / DOW), CASE式
- **🔤 関数編Part2：文字列関数マスター**
  - 問題14: 文字列の結合｜★☆☆☆☆（5分）— || 演算子
  - 問題15: 文字列の大文字・小文字変換と長さ｜★☆☆☆☆（5分）— UPPER, LENGTH
  - 問題16: 文字列の部分取得｜★☆☆☆☆（5分）— SUBSTRING
- **📊 中級編（JOIN, GROUP BY, 集計）**
  - 問題17: 2テーブルの結合｜★★☆☆☆（10分）— JOIN, ON, テーブル別名
  - 問題18: 3テーブルの結合｜★★☆☆☆（10分）— JOIN（複数テーブル）
  - 問題19: 重複を除外したリストを作る｜★★☆☆☆（5分）— DISTINCT, JOIN
- **📝 実践編：サブクエリとビュー**
  - 問題20: サブクエリの基礎（WHERE句内）｜★★☆☆☆（10分）— サブクエリ, WHERE, AVG
  - 問題21: サブクエリでテーブルを作る（FROM句内）｜★★★☆☆（10分）— FROM句サブクエリ（導出テーブル）, JOIN
  - 問題22: ビューを作成して利用する｜★★☆☆☆（10分）— CREATE VIEW, SELECT
- **🎯 応用編Part1：CASE式マスター**
  - 問題23: CASE式で金額ランク分類｜★★☆☆☆（10分）— CASE WHEN, ELSE
  - 問題24: CASE式で複数条件の組み合わせ｜★★★☆☆（15分）— CASE WHEN, AND, JOIN
  - 問題25: CASE式を集計関数内で使う（条件付き集計）｜★★★☆☆（15分）— SUM(CASE WHEN), GROUP BY
  - 問題26: CASE式で順序付け（カスタムソート）｜★★☆☆☆（10分）— ORDER BY 内の CASE式
- **🔄 応用編Part2：縦持ち⇔横持ち変換マスター**
  - 問題27: 縦持ちから横持ちへ（ピボット）｜★★★☆☆（15分）— SUM(CASE WHEN), EXTRACT, JOIN
  - 問題28: 複数軸のピボット｜★★★☆☆（15分）— SUM(CASE WHEN), JOIN（3テーブル）
  - 問題29: 横持ちから縦持ちへ（アンピボット）｜★★★★☆（20分）— WITH(CTE), UNION ALL, CAST
- **🪟 応用編Part3：Window関数マスター**
  - 問題30: ROW_NUMBER vs RANK vs DENSE_RANK｜★★★☆☆（15分）— ROW_NUMBER, RANK, DENSE_RANK, OVER
  - 問題31: 顧客別の累積売上（PARTITION BY）｜★★★☆☆（10分）— SUM() OVER(PARTITION BY)
  - 問題32: LAGとLEADで前後の行を参照｜★★★☆☆（10分）— LAG() OVER(PARTITION BY)
  - 問題33: 移動平均（ウィンドウフレーム）｜★★★☆☆（10分）— AVG() OVER(ROWS BETWEEN)
  - 問題34: NTILE（パーセンタイル分割）｜★★★★☆（20分）— WITH(CTE), NTILE, CASE式
- **🎓 応用編Part4：CTE（WITH句）マスター**
  - 問題35: CTEを使った段階的な集計｜★★★☆☆（10分）— WITH(CTE), JOIN, SUM
  - 問題36: CTEでVIP顧客の購買分析｜★★★☆☆（15分）— WITH(CTE), JOIN, WHERE, GROUP BY
- **🎓 チャレンジ問題**
  - 問題37: 月別コホート分析（新規・既存顧客）｜★★★★★（30分）— WITH(CTE), JOIN, EXTRACT, SUM(CASE WHEN), COUNT(DISTINCT CASE WHEN)

---

## 📚 基礎編（SELECT, WHERE, ORDER BY）

### 🧠 SQLを組み立てる思考順序

SQLを書くとき、SELECT句から考え始めると手が止まりがちです。
以下の順番で考えると、自然にクエリが組み立てられます。

| 考える順番 | 対応するSQL句 | 考えること |
|:---:|:---|:---|
| 1 | FROM / JOIN | どのテーブルにデータがあるか？結合は必要か？ |
| 2 | WHERE | どの行を使うか？不要な行を除外する条件は？ |
| 3 | GROUP BY | 何の単位で集計するか？（集計が必要な場合） |
| 4 | SELECT | 最終的に何を表示するか？ |

この順番は、データベースエンジンがクエリを内部的に処理する実行順序と一致しています。
SQLの記述順序（SELECT → FROM → WHERE → ...）とは異なることに注意してください。

「今どんな中間テーブルができているか」を頭の中でイメージしながら、上から順に組み立てていくのがコツです。

以降の問題では、この思考順序に沿った「🔍 考え方のステップ」を示している問題があります。
問題を読んだら、まず自分で考え方を整理してから、SQLを書いてみましょう。

---

### 問題1: 商品の一覧を確認する｜★☆☆☆☆（目安：3分）

問題: products テーブルから商品の基本情報（product_id, product_name, category）を表示してください。結果は10件に制限してください。

💡 ヒント
- 必要なカラムだけを指定します（SELECT * は避けましょう）
- 大量データの可能性があるテーブルでは、必ず件数制限を付けます
- 標準SQLでは `FETCH FIRST n ROWS ONLY` で件数制限できます

回答例
```sql
SELECT
      product_id
    , product_name
    , category
FROM
    products
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

このドキュメントでの方針: 
標準SQLとしては `FETCH FIRST` が正式ですが、実用性を考慮し、以降の問題では `LIMIT n` を使用します。これは BigQuery、Athena、Snowflake など主要なクラウドデータウェアハウスで標準的な書き方です。

---

### 問題2: 特定のカラムだけ表示｜★☆☆☆☆（目安：3分）

問題: sales テーブルから、sale_id, sale_date, quantity の3つのカラムだけを表示してください。最初の10件のみ。

💡 ヒント
- カラム名をカンマ区切りで指定します
- LIMIT で表示件数を制限できます

回答例
```sql
SELECT
      sale_id
    , sale_date
    , quantity
FROM
    sales
LIMIT 10;
```

解説: 必要なカラムだけを指定することで、結果が見やすくなります。

---

## 💡 SQLの書き方スタイル（重要）

### なぜスタイルが大切なのか

SQLは「動けば何でもいい」わけではありません。実務では：
- 他の人があなたのクエリを読む
- 将来の自分が過去のクエリを修正する
- チームで同じスタイルを使うと、コードレビューが効率的になる

使い捨てのコードではなく継続的にメンテする可能性があるなら、**最初から読みやすいスタイルで書く習慣**をつけましょう。

---

### このドキュメントで採用しているスタイル

#### ✅ ルール1: カンマは次の項目の行頭に置く

```sql
-- ❌ 避けるべき書き方
SELECT product_id, product_name, category
FROM products;

-- ✅ 推奨する書き方
SELECT
      product_id
    , product_name
    , category
FROM
    products;
```

**メリット**:
- カラムの追加・削除が簡単（最後の行もカンマで終われる）
- 1カラムの追加・変更は1行のコード変更だけになる（カンマが前の行にあると2行変更することになる）
- どのカラムが選択されているか一目瞭然
- Gitなどで行単位で変更差分を管理した場合に変更箇所が行単位で明確

---

#### ✅ ルール2: FROMの後は改行してテーブル名を書く

```sql
-- ❌ 避けるべき書き方
SELECT product_id FROM products;

-- ✅ 推奨する書き方
SELECT
      product_id
FROM
    products;
```

**メリット**:
- 後でJOINを追加するときに修正が最小限
- クエリの構造が視覚的に分かりやすい

---

#### ✅ ルール3: JOINは独立した行に、ON句はインデント

```sql
-- ❌ 避けるべき書き方
SELECT s.sale_id, p.product_name
FROM sales s
JOIN products p ON s.product_id = p.product_id;

-- ✅ 推奨する書き方
SELECT
      s.sale_id
    , p.product_name
FROM
    sales s
    JOIN products p
        ON s.product_id = p.product_id;
```

**メリット**:
- 複数のJOINがある場合でも読みやすい
- ON条件が複雑な場合も整理しやすい

---

#### ✅ ルール4: WHERE条件は1行1条件

```sql
-- ❌ 避けるべき書き方
SELECT sale_id FROM sales
WHERE quantity >= 5 AND discount_rate > 0;

-- ✅ 推奨する書き方
SELECT
      sale_id
FROM
    sales
WHERE
    quantity >= 5
    AND discount_rate > 0;
```

**メリット**:
- 条件の追加・削除が簡単
- 各条件を個別にコメントアウトできる

---

### 実務での重要性

このスタイルは以下の環境で広く使われています：
- **クラウドデータウェアハウス**: BigQuery, Snowflake, Redshift, Athena
- **データ変換ツール**: dbt, Dataform
- **データエンジニアリングチーム**: 保守性を重視するプロジェクト

特にAWS Glue/Athenaを使う環境では、クエリの修正や拡張が頻繁にあるため、このスタイルの恩恵は大きいです。

---

### 今すぐ実践しよう

以降の問題では、すべてこのスタイルで書かれています。
最初は慣れないかもしれませんが、**写経の段階からこのスタイルで書く**ことで、自然に身につきます。

**良いスタイルは、将来の自分への贈り物です。**

---

### 問題3: 条件に合うデータを抽出｜★☆☆☆☆（目安：5分）

問題: sales テーブルから、数量（quantity）が5以上の売上データを表示してください。表示するカラムは sale_id, sale_date, customer_id, product_id, quantity, unit_price とし、結果は100件以内に制限してください。

🔍 考え方のステップ
1. **FROM**: salesテーブルを使う（他のテーブルとの結合は不要）
2. **WHERE**: quantity >= 5 で行を絞り込む
3. **GROUP BY**: 集計はしない（個別の行をそのまま表示）
4. **SELECT**: 指定された6つのカラムを選ぶ

💡 ヒント
- WHERE 句で条件を指定します
- 比較演算子: =, >, <, >=, <= が使えます
- 実務では必ず LIMIT を付けましょう

回答例
```sql
SELECT
      sale_id
    , sale_date
    , customer_id
    , product_id
    , quantity
    , unit_price
FROM
    sales
WHERE
    quantity >= 5
LIMIT 100;
```

解説: WHERE 句は条件に合う行だけを絞り込みます。
- 必要なカラムだけを明示的に選択
- LIMIT で結果件数を制限（予想外に大量のデータが返ってくることを防ぐ）

---

### 問題4: 複数条件での絞り込み｜★☆☆☆☆（目安：5分）

問題: sales テーブルから、数量が3以上で、かつ割引率（discount_rate）が0より大きい（割引が適用されている）売上を表示してください。表示するカラムは sale_id, sale_date, product_id, quantity, unit_price, discount_rate とし、結果は100件以内に制限してください。

🔍 考え方のステップ
1. **FROM**: salesテーブルを使う
2. **WHERE**: 2つの条件を両方満たす行が欲しい → AND で繋ぐ
   - quantity >= 3
   - discount_rate > 0
3. **GROUP BY**: 集計はしない
4. **SELECT**: 指定されたカラムを選ぶ

💡 ヒント
- AND で複数条件を組み合わせられます
- discount_rate > 0 で割引ありを判定できます

回答例
```sql
SELECT
      sale_id
    , sale_date
    , product_id
    , quantity
    , unit_price
    , discount_rate
FROM
    sales
WHERE
    quantity >= 3
    AND discount_rate > 0
LIMIT 100;
```

解説: 
- AND で条件を繋ぐと、両方を満たす行だけが表示されます
- 実務では「何件ヒットするかわからない検索」が多いため、LIMIT は保険として必須

---

### 問題5: 並び替え｜★☆☆☆☆（目安：5分）

問題: sales テーブルのデータを、販売日（sale_date）の新しい順に並べて、最新の20件だけを表示してください。表示するカラムは sale_id, sale_date, customer_id, product_id, quantity, unit_price です。

🔍 考え方のステップ
1. **FROM**: salesテーブルを使う
2. **WHERE**: 絞り込み条件なし（全行が対象）
3. **GROUP BY**: 集計はしない
4. **SELECT**: 指定されたカラムを選ぶ
5. **ORDER BY**: sale_date を DESC（降順＝新しい順）で並べる
6. **LIMIT**: 20件に制限

💡 ヒント
- ORDER BY で並び替えができます
- DESC で降順（大きい順）、ASC で昇順（小さい順）

回答例
```sql
SELECT
      sale_id
    , sale_date
    , customer_id
    , product_id
    , quantity
    , unit_price
FROM
    sales
ORDER BY
    sale_date DESC
LIMIT 20;
```

解説: 
- ORDER BY sale_date DESC で、最新の売上から順に表示されます
- 実務では「最新20件を見たい」というケースが多いので、LIMIT と組み合わせるのが定石

---

### 問題6: 日付範囲での絞り込み｜★★☆☆☆（目安：5分）

問題: sales テーブルから、2024年1月15日から1月31日までの売上データを表示してください。表示するカラムは sale_id, sale_date, customer_id, product_id, quantity, unit_price, discount_rate とし、販売日の昇順で並べ、結果は100件以内に制限してください。

🔍 考え方のステップ
1. **FROM**: salesテーブルを使う
2. **WHERE**: sale_date の範囲を指定する → BETWEEN が使える
3. **GROUP BY**: 集計はしない
4. **SELECT**: 指定されたカラムを選ぶ
5. **ORDER BY**: sale_date 昇順（古い順）

💡 ヒント
- BETWEEN 演算子で範囲指定ができます
- 日付は DATE '2024-01-15' のように DATE リテラルで指定するのが標準SQLです

回答例
```sql
SELECT
      sale_id
    , sale_date
    , customer_id
    , product_id
    , quantity
    , unit_price
    , discount_rate
FROM
    sales
WHERE
    sale_date BETWEEN DATE '2024-01-15' AND DATE '2024-01-31'
ORDER BY
    sale_date
LIMIT 100;
```

解説: 
- BETWEEN は指定した範囲の値（両端含む）を抽出します
- DATE リテラルを使用（標準SQL）
- 日付範囲でも予想外に大量データがある可能性があるため、LIMIT で上限を設定

---

## 🏷️ 実務編：AS句とビジネスドメイン用語

### 問題7: ビジネスドメインに合わせた列名を付ける｜★★☆☆☆（目安：10分）

問題: sales テーブルから売上情報を取得してください。以下の要件を満たしてください。
- quantity を、何の量か明確にわかる列名（purchase_quantity）に変更する
- 割引前金額（amount_before_discount）を `quantity * unit_price` で計算する
- 割引額（discount_amount）を `quantity * unit_price * discount_rate` で計算する
- 割引後の純売上額（net_amount）を `quantity * unit_price * (1 - discount_rate)` で計算する
- 全ての計算列にはASで英語の列名を付ける
- 結果は20件に制限する

💡 ヒント
- AS で列に別名（エイリアス）を付けられます
- 計算式には必ずASで名前を付けましょう

回答例
```sql
SELECT
      sale_id
    , sale_date
    , customer_id
    , product_id
    , quantity AS purchase_quantity
    , unit_price
    , discount_rate
    , quantity * unit_price AS amount_before_discount
    , quantity * unit_price * discount_rate AS discount_amount
    , quantity * unit_price * (1 - discount_rate) AS net_amount
FROM
    sales
LIMIT 20;
```

解説: 
- SELECT句においてASは省略可能ですが、読みやすくわかりやすくなる場面ではASを使って列名をつけます
- 特に分析用のデータマート構築では、最終的にユーザーが見るデータのカラム名が、ビジネスで使っている言葉遣いに沿っているとわかりやすくなります
- 対象のビジネスドメインによって用語を使い分ける場合があり、同じ「顧客」のことを営業部門なら`account`、CS部門なら`customer`と呼ぶなど、言葉遣いを揃えると読みやすくなります
- データを利用する人の目線で、自然な言葉遣いになっている方がわかりやすく、使いやすいデータマートになります

---

### 問題8: 集計結果にわかりやすい名前を付ける｜★★☆☆☆（目安：10分）

問題: 顧客（customer_id）ごとに以下の購入統計を計算し、全ての列に分析者が理解しやすい英語の列名を付けてください。
- 購入回数（purchase_count）
- 合計購入数量（total_quantity）
- 合計売上金額：割引後（total_revenue） ※ `quantity * unit_price * (1 - discount_rate)` の合計
- 平均注文金額（average_order_value） ※ 上記の割引後金額の平均
- 初回購入日（first_purchase_date）
- 最終購入日（last_purchase_date）

結果は合計売上金額の大きい順に並べ、20件に制限してください。

🔍 考え方のステップ
1. **FROM**: salesテーブルを使う
2. **WHERE**: 条件なし（全顧客が対象）
3. **GROUP BY**: customer_id でグループ化（「顧客ごと」に集計するため）
4. **SELECT**: customer_id と、各集計関数（COUNT, SUM, AVG, MIN, MAX）の結果

💡 ヒント
- GROUP BY で集計の単位を指定します
- COUNT(*) で行数、SUM() で合計、AVG() で平均、MIN()/MAX() で最小/最大値を計算
- 集計関数を使ったら、必ずASで列名を付けましょう

> #### ✅ GROUP BY の効果を確認してみよう
> 
> GROUP BY を初めて使うときは、その前後でデータがどう変わるかを確認するのがおすすめです。
> 
> ```sql
> -- まず sales テーブルの全体の行数を確認
> SELECT COUNT(*) FROM sales;
> 
> -- GROUP BY すると、行数がユニークな customer_id の数に減る
> SELECT customer_id, COUNT(*) 
> FROM sales 
> GROUP BY customer_id;
> ```
> 
> GROUP BY を適用すると、同じ customer_id を持つ複数の行が「1行に束ねられ」ます。
> 束ねられた行に対して、COUNT や SUM などの集計関数で値を計算します。

回答例
```sql
SELECT
      customer_id
    , COUNT(*) AS purchase_count
    , SUM(quantity) AS total_quantity
    , SUM(quantity * unit_price * (1 - discount_rate)) AS total_revenue
    , AVG(quantity * unit_price * (1 - discount_rate)) AS average_order_value
    , MIN(sale_date) AS first_purchase_date
    , MAX(sale_date) AS last_purchase_date
FROM
    sales
GROUP BY
    customer_id
ORDER BY
    total_revenue DESC
LIMIT 20;
```

解説: 
- 集計関数には必ずASで名前を付ける（これは実務の絶対ルール）
- 英語の一般的なビジネス用語を使うことで：
  - データマートを使う分析者が理解しやすい
  - BIツールでの表示がそのまま使える

---

## 📅 関数編Part1：日付関数マスター

### 問題9: 日付から年月を取り出す｜★★☆☆☆（目安：5分）

問題: 売上データから、年と月をそれぞれ別の列として取り出して表示してください。表示するカラムは sale_id, sale_date, 年（sale_year）、月（sale_month）、customer_id、および割引後の売上金額（net_amount = `quantity * unit_price * (1 - discount_rate)`）です。販売日の昇順で並べ、20件に制限してください。

💡 ヒント
- EXTRACT(YEAR FROM 日付) で年を取得
- EXTRACT(MONTH FROM 日付) で月を取得（標準SQL）

回答例
```sql
SELECT
      sale_id
    , sale_date
    , EXTRACT(YEAR FROM sale_date) AS sale_year
    , EXTRACT(MONTH FROM sale_date) AS sale_month
    , customer_id
    , quantity * unit_price * (1 - discount_rate) AS net_amount
FROM
    sales
ORDER BY
    sale_date
LIMIT 20;
```

解説: 
- EXTRACT() は標準SQL関数で、ほぼ全てのデータベースでサポート
- 年月を個別に取得することで、月次集計の準備ができます
- データベース製品固有の方言で同じ用途で使える別の関数が用意されている場合があります

---

### 問題10: 月次集計を行う｜★★☆☆☆（目安：10分）

問題: 年月ごとに以下の指標を集計してください。
- 売上件数（sales_count）
- ユニーク顧客数（unique_customers）
- 月間売上金額：割引後（monthly_revenue）
- 平均注文金額（avg_order_value）

年、月の昇順で並べてください。

🔍 考え方のステップ
1. **FROM**: salesテーブルを使う
2. **WHERE**: 条件なし
3. **GROUP BY**: 何の単位で集計？→「年月ごと」なので、年と月をそれぞれ EXTRACT で取得してグループ化
4. **SELECT**: 年、月、各集計関数の結果

💡 ヒント
- EXTRACT でグループ化のキーを作ります
- COUNT(DISTINCT ...) でユニーク数を数えられます
- GROUP BY には、SELECT で使った EXTRACT 式と同じ式を書きます

回答例
```sql
SELECT
      EXTRACT(YEAR FROM sale_date) AS sale_year
    , EXTRACT(MONTH FROM sale_date) AS sale_month
    , COUNT(*) AS sales_count
    , COUNT(DISTINCT customer_id) AS unique_customers
    , SUM(quantity * unit_price * (1 - discount_rate)) AS monthly_revenue
    , AVG(quantity * unit_price * (1 - discount_rate)) AS avg_order_value
FROM
    sales
GROUP BY
    EXTRACT(YEAR FROM sale_date)
    , EXTRACT(MONTH FROM sale_date)
ORDER BY
    sale_year
    , sale_month;
```

解説: 
- 月次分析は実務で最頻出のパターン
- 標準SQLでは EXTRACT で年と月を個別に取得して GROUP BY
- 年と月の両方でグループ化することで、年をまたいだデータも正しく集計できます

---

### 問題11: 曜日別の売上傾向を分析｜★★★☆☆（目安：10分）

問題: 曜日ごとに、売上件数（sales_count）、合計売上金額（total_sales：割引後）、平均売上金額（avg_sales：割引後）を集計してください。曜日は番号ではなく英語の曜日名（Sunday, Monday, ...）で表示し、日曜日から順に並べてください。

💡 ヒント
- EXTRACT(DOW FROM 日付) で曜日番号を取得（0=日曜〜6=土曜）
- Day of Week で DOWです
- CASE式で番号を曜日名に変換できます
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
      END AS day_of_week
    , COUNT(*) AS sales_count
    , SUM(quantity * unit_price * (1 - discount_rate)) AS total_sales
    , AVG(quantity * unit_price * (1 - discount_rate)) AS avg_sales
FROM
    sales
GROUP BY
    EXTRACT(DOW FROM sale_date)
ORDER BY
    EXTRACT(DOW FROM sale_date);
```

解説: 
- 曜日分析は小売・ECで頻出
- EXTRACT(DOW FROM date) は標準SQL（DOW = Day Of Week）
- CASE式で曜日番号を読みやすい名前に変換

---

### 問題12: 期間の計算（日数差）｜★★☆☆☆（目安：10分）

問題: 各顧客の初回購入日（first_purchase_date）、最終購入日（last_purchase_date）、その間の日数（days_active）、購入回数（purchase_count）を計算してください。ただし、2回以上購入した顧客のみを対象とし、アクティブ日数が長い順に並べて20件表示してください。

💡 ヒント
- 日付の引き算で経過日数が計算できます
- HAVING で集計結果に対する条件を指定できます

回答例
```sql
SELECT
      customer_id
    , MIN(sale_date) AS first_purchase_date
    , MAX(sale_date) AS last_purchase_date
    , MAX(sale_date) - MIN(sale_date) AS days_active
    , COUNT(*) AS purchase_count
FROM
    sales
GROUP BY
    customer_id
HAVING
    COUNT(*) >= 2
ORDER BY
    days_active DESC
LIMIT 20;
```

解説: 
- 日付の引き算で経過日数が計算できます（標準SQL）
- 顧客のライフタイム分析でよく使うパターン
- HAVING で2回以上購入した顧客に絞り込み

---

### 問題13: 日付から年・月・日を個別に取り出す｜★★☆☆☆（目安：5分）

問題: 売上データから、年（sale_year）、月（sale_month）、日（sale_day）をそれぞれ別の列として取り出してください。さらに曜日名（day_of_week：Sunday〜Saturday）と、割引後の売上金額（net_amount）も表示してください。結果は20件に制限してください。

💡 ヒント
- EXTRACT(DAY FROM 日付) で日を取得
- 曜日名への変換は問題11と同じ方法です

回答例
```sql
SELECT
      sale_id
    , sale_date
    , EXTRACT(YEAR FROM sale_date) AS sale_year
    , EXTRACT(MONTH FROM sale_date) AS sale_month
    , EXTRACT(DAY FROM sale_date) AS sale_day
    , CASE EXTRACT(DOW FROM sale_date)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
      END AS day_of_week
    , quantity * unit_price * (1 - discount_rate) AS net_amount
FROM
    sales
LIMIT 20;
```

解説: 
- EXTRACT は日付の部分取得でよく使います（標準SQL）
- 年別、月別の分析に便利

---

## 🔤 関数編Part2：文字列関数マスター

### 問題14: 文字列の結合｜★☆☆☆☆（目安：5分）

問題: customers テーブルから、customer_id, customer_name, customer_segment, prefecture を表示してください。さらに、顧客名とセグメントを結合して「山田太郎（VIP）」のような形式の表示名（customer_display_name）を作成してください。結果は20件に制限してください。

💡 ヒント
- || 演算子で文字列を結合できます（標準SQL）
- 全角カッコ「（」「）」で囲みます

回答例
```sql
SELECT
      customer_id
    , customer_name
    , customer_segment
    , customer_name || '（' || customer_segment || '）' AS customer_display_name
    , prefecture
FROM
    customers
LIMIT 20;
```

解説: 
- || 演算子は標準SQLの文字列結合（CONCAT関数も使えますが||がより標準的）
- レポート用の表示名作成でよく使う

---

### 問題15: 文字列の大文字・小文字変換と長さ｜★☆☆☆☆（目安：5分）

問題: products テーブルから、product_id, product_name, category, standard_price を表示してください。加えて、商品名の文字数（product_name_length）と、カテゴリの大文字変換（category_upper）も表示してください。結果は10件に制限してください。

💡 ヒント
- LENGTH() で文字列の長さを取得できます
- UPPER() で大文字に変換できます

回答例
```sql
SELECT
      product_id
    , product_name
    , LENGTH(product_name) AS product_name_length
    , category
    , UPPER(category) AS category_upper
    , standard_price
FROM
    products
LIMIT 10;
```

解説: 
- UPPER/LOWER/LENGTH は全て標準SQL関数
- データクレンジングでよく使う

---

### 問題16: 文字列の部分取得｜★☆☆☆☆（目安：5分）

問題: products テーブルから、product_id, product_name, category を表示してください。加えて、商品名の最初の4文字だけを取り出した略称（product_short）も表示してください。結果は10件に制限してください。

💡 ヒント
- SUBSTRING(文字列, 開始位置, 長さ) で部分文字列を取得できます
- SQLの文字列は1始まりです

回答例
```sql
SELECT
      product_id
    , product_name
    , SUBSTRING(product_name, 1, 4) AS product_short
    , category
FROM
    products
LIMIT 10;
```

解説: 
- SUBSTRING は標準SQL関数
- SUBSTRING(文字列, 開始位置, 長さ) の形式
- 商品名の略称作成や、データ整形でよく使います

---

## 📊 中級編（JOIN, GROUP BY, 集計）

### 問題17: 2テーブルの結合｜★★☆☆☆（目安：10分）

問題: sales テーブルと products テーブルを product_id で結合し、以下のカラムを表示してください：sale_id, sale_date, product_name, category, 購入数量（purchase_quantity）, unit_price, 割引後の売上金額（net_amount）。テーブル別名を使い、結果は10件に制限してください。

💡 ヒント
- JOIN ... ON で結合条件を指定します
- テーブル別名（s, p など）を使うと読みやすくなります

> #### ✅ JOIN の効果を確認してみよう
> 
> JOIN を初めて使うときは、結合の前後でデータがどう変わるかを確認しましょう。
> 
> ```sql
> -- sales テーブルの行数
> SELECT COUNT(*) FROM sales;
> 
> -- products テーブルの行数
> SELECT COUNT(*) FROM products;
> 
> -- JOIN 後の行数
> SELECT COUNT(*) 
> FROM sales s 
> JOIN products p ON s.product_id = p.product_id;
> ```
> 
> 内部結合（JOIN）では、結合キー（product_id）が一致する行だけが残ります。
> salesの各行に対して、product_id が一致する products の情報が「横に付く」イメージです。
> 結果の行数は、salesの行数と同じか、それ以下になります。

回答例
```sql
SELECT
      s.sale_id
    , s.sale_date
    , p.product_name
    , p.category
    , s.quantity AS purchase_quantity
    , s.unit_price
    , s.quantity * s.unit_price * (1 - s.discount_rate) AS net_amount
FROM
    sales s
    JOIN products p
        ON s.product_id = p.product_id
LIMIT 10;
```

解説: 
- JOIN で売上と商品の情報を組み合わせることができます
- テーブルの別名（s, p）を使うとクエリが読みやすくなる

---

### 問題18: 3テーブルの結合｜★★☆☆☆（目安：10分）

問題: sales, products, customers の3テーブルを結合して、以下の販売情報を表示してください：sale_date, customer_name, product_name, 購入数量（purchase_quantity）, 割引後の売上金額（net_amount）。結果は10件に制限してください。

💡 ヒント
- JOIN を続けて書くことで、3つ以上のテーブルを結合できます
- それぞれの結合条件（ON句）を正しく指定しましょう

回答例
```sql
SELECT
      s.sale_date
    , c.customer_name
    , p.product_name
    , s.quantity AS purchase_quantity
    , s.quantity * s.unit_price * (1 - s.discount_rate) AS net_amount
FROM
    sales s
    JOIN customers c
        ON s.customer_id = c.customer_id
    JOIN products p
        ON s.product_id = p.product_id
LIMIT 10;
```

解説: 
- JOIN を続けて書くことで、複数のテーブルを次々に繋げられます

---

### 問題19: 重複を除外したリストを作る｜★★☆☆☆（目安：5分）

問題: sales テーブルと products テーブルを結合し、実際に購入されたことがある商品カテゴリの一覧を、重複なしでアルファベット順に表示してください。

💡 ヒント
- SELECT DISTINCT で重複する行を除外できます

回答例
```sql
SELECT DISTINCT
      p.category
FROM
    sales s
    JOIN products p
        ON s.product_id = p.product_id
ORDER BY
    p.category;
```

解説: 
- SELECT DISTINCT で重複する行を除外
- DISTINCTは処理コストが高いので、本当に必要な時だけ使う

---

## 📝 実践編：サブクエリとビュー

### 問題20: サブクエリの基礎（WHERE句内）｜★★☆☆☆（目安：10分）

問題: sales テーブルから、全体の平均売上金額（割引後）よりも高い売上だけを抽出してください。表示するカラムは sale_id, sale_date, customer_id, 売上金額（sales_amount）とし、金額の大きい順で20件に制限してください。

🔍 考え方のステップ
1. **まず「全体の平均売上金額」を計算するクエリを単独で書いてみる** → `SELECT AVG(quantity * unit_price * (1 - discount_rate)) FROM sales`
2. **このクエリの結果（1つの数値）をWHERE句の条件に使いたい** → サブクエリとして () で囲んで WHERE 句に埋め込む
3. **メインクエリで各行の売上金額と比較する** → `WHERE 売上金額 > (サブクエリ)`

💡 ヒント
- WHERE句の中に SELECT 文を書くことができます（サブクエリ）
- サブクエリは () で囲みます
- サブクエリが1つの値を返す場合、比較演算子（>, <, = など）で使えます

回答例
```sql
SELECT
      sale_id
    , sale_date
    , customer_id
    , quantity * unit_price * (1 - discount_rate) AS sales_amount
FROM
    sales
WHERE
    quantity * unit_price * (1 - discount_rate) > (
        SELECT
              AVG(quantity * unit_price * (1 - discount_rate))
        FROM
            sales
    )
ORDER BY
    sales_amount DESC
LIMIT 20;
```

解説: 
- サブクエリは「クエリの中に書くクエリ」です
- WHERE句内のサブクエリは、1つの値（スカラー値）を返す場合に比較演算子で使えます
- この例では、まず全体の平均値を計算し、それより高い売上を抽出しています

---

### 問題21: サブクエリでテーブルを作る（FROM句内）｜★★★☆☆（目安：10分）

問題: 顧客ごとの合計売上金額（total_revenue：割引後）をサブクエリで計算し、その結果と customers テーブルを結合して、customer_name と total_revenue を売上の大きい順に表示してください。

🔍 考え方のステップ
1. **まず顧客ごとの合計売上を計算するクエリを単独で書く** → `SELECT customer_id, SUM(...) AS total_revenue FROM sales GROUP BY customer_id`
2. **このクエリの結果を「仮想的なテーブル」としてFROM句に置く** → FROM句のサブクエリ（導出テーブル）
3. **導出テーブルには必ず AS で名前を付ける**
4. **customers テーブルと JOIN する**

💡 ヒント
- FROM句にサブクエリを書くと、その結果をテーブルのように扱えます（導出テーブル）
- 導出テーブルには必ず AS で別名を付けてください
- この書き方は、後で学ぶ CTE（WITH句）と同じことを実現できます

回答例
```sql
SELECT
      c.customer_name
    , sub.total_revenue
FROM
    (
        SELECT
              customer_id
            , SUM(quantity * unit_price * (1 - discount_rate)) AS total_revenue
        FROM
            sales
        GROUP BY
            customer_id
    ) AS sub
    JOIN customers c
        ON sub.customer_id = c.customer_id
ORDER BY
    sub.total_revenue DESC;
```

解説: 
- FROM句内のサブクエリは「導出テーブル」と呼ばれ、一時的なテーブルとして扱えます
- サブクエリが複雑になると読みにくくなるため、後で学ぶCTE（WITH句）の方が実務では好まれます
- ただし、サブクエリの概念を理解しておくことは、既存コードを読む際に必須です

---

### 問題22: ビューを作成して利用する｜★★☆☆☆（目安：10分）

問題: 以下の2ステップで、ビューの作成と利用を体験してください。

ステップ1: 月次売上サマリのビュー（monthly_sales_summary）を作成してください。ビューには以下のカラムを含めます。
- 年（sale_year）
- 月（sale_month）
- 売上件数（sales_count）
- 合計売上金額：割引後（total_revenue）

ステップ2: 作成したビューから、合計売上金額が大きい月のトップ5を取得してください。

💡 ヒント
- `CREATE VIEW ビュー名 AS SELECT ...` でビューを作成できます
- ビューは「保存されたSELECT文」で、テーブルと同じように SELECT できます
- ビューは実データを持たず、参照するたびに元のSELECT文が実行されます

回答例

ステップ1: ビューの作成
```sql
CREATE OR REPLACE VIEW monthly_sales_summary AS
SELECT
      EXTRACT(YEAR FROM sale_date) AS sale_year
    , EXTRACT(MONTH FROM sale_date) AS sale_month
    , COUNT(*) AS sales_count
    , SUM(quantity * unit_price * (1 - discount_rate)) AS total_revenue
FROM
    sales
GROUP BY
    EXTRACT(YEAR FROM sale_date)
    , EXTRACT(MONTH FROM sale_date);
```

ステップ2: ビューの利用
```sql
SELECT
      sale_year
    , sale_month
    , sales_count
    , total_revenue
FROM
    monthly_sales_summary
ORDER BY
    total_revenue DESC
LIMIT 5;
```

解説: 
- ビューは「名前を付けて保存したクエリ」です
- 一度作成すれば、テーブルと同じように何度でも SELECT できます
- よく使う集計クエリをビューにしておくと、分析が効率的になります
- ビューはデータの実体を持たないため、元テーブルが更新されればビューの結果も変わります
- 実務では、複雑な集計ロジックをビュー化して、分析者に「使いやすいデータの見え方」を提供するのがデータエンジニアの重要な役割です

---

## 🎯 応用編Part1：CASE式マスター

### 🔧 応用問題の取り組み方：積み上げ型アプローチ

応用編からは、複数の構文を組み合わせた複雑なクエリを書くことになります。
いきなり最終形のクエリを書こうとすると、どこでエラーが出たかわからなくなりがちです。

**小さなクエリから段階的に育てていく「積み上げ型」のアプローチ**を心がけてください。

例えば「VIP顧客のカテゴリ別売上を集計する」という問題の場合：

| ステップ | やること | 追加する要素 |
|:---:|:---|:---|
| A | まず sales テーブルだけで売上金額を計算してみる | SELECT + 計算式 |
| B | customers と JOIN して VIP だけに絞り込む | JOIN + WHERE |
| C | products と JOIN してカテゴリ情報を追加する | もう1つ JOIN |
| D | GROUP BY でカテゴリ別に集計する | GROUP BY + 集計関数 |

**各ステップでクエリを実行し、中間結果が正しいことを確認してから次に進みましょう。**
一度に全部書こうとするよりも、結果的に早く・正確にクエリが完成します。

---

### 問題23: CASE式で金額ランク分類｜★★☆☆☆（目安：10分）

問題: 各売上について、割引後の売上金額（sales_amount）を計算し、金額に応じて以下のランク（amount_tier）に分類してください。
- 5,000円以上 → 'High'
- 2,000円以上5,000円未満 → 'Medium'
- 2,000円未満 → 'Low'

売上金額の大きい順に並べ、20件表示してください。

💡 ヒント
- CASE WHEN で条件に応じた値を返せます
- 条件は上から順に評価されるため、大きい値から書くと漏れを防げます

回答例
```sql
SELECT
      sale_id
    , sale_date
    , quantity * unit_price * (1 - discount_rate) AS sales_amount
    , CASE
        WHEN quantity * unit_price * (1 - discount_rate) >= 5000 THEN 'High'
        WHEN quantity * unit_price * (1 - discount_rate) >= 2000 THEN 'Medium'
        ELSE 'Low'
      END AS amount_tier
FROM
    sales
ORDER BY
    sales_amount DESC
LIMIT 20;
```

解説: 
- CASE式で金額に応じたランク付けができます（標準SQL）
- 条件は上から順に評価されます

---

### 問題24: CASE式で複数条件の組み合わせ｜★★★☆☆（目安：15分）

問題: sales と customers を結合し、顧客セグメントと購入金額の組み合わせに基づいて、以下のルールで優先度（priority_level）を判定してください。
- VIPセグメントかつ割引後金額3,000円以上 → 'Top Priority'
- VIPセグメント（金額を問わず）→ 'High Priority'
- Regularセグメントかつ割引後金額5,000円以上 → 'High Priority'
- それ以外 → 'Normal'

表示するカラムは sale_id, sale_date, customer_name, customer_segment, 売上金額（sales_amount）, priority_level です。販売日の新しい順で20件表示してください。

💡 ヒント
- CASE式の条件は上から順に評価されるため、最も限定的な条件を先に書きます
- AND で複数条件を組み合わせられます

回答例
```sql
SELECT
      s.sale_id
    , s.sale_date
    , c.customer_name
    , c.customer_segment
    , s.quantity * s.unit_price * (1 - s.discount_rate) AS sales_amount
    , CASE
        WHEN c.customer_segment = 'VIP' AND s.quantity * s.unit_price * (1 - s.discount_rate) >= 3000 THEN 'Top Priority'
        WHEN c.customer_segment = 'VIP' THEN 'High Priority'
        WHEN c.customer_segment = 'Regular' AND s.quantity * s.unit_price * (1 - s.discount_rate) >= 5000 THEN 'High Priority'
        ELSE 'Normal'
      END AS priority_level
FROM
    sales s
    JOIN customers c
        ON s.customer_id = c.customer_id
ORDER BY
    s.sale_date DESC
LIMIT 20;
```

解説: 
- 実務では複雑なビジネスルールをCASE式で表現
- AND/ORで条件を組み合わせて柔軟な分類が可能

---

### 問題25: CASE式を集計関数内で使う（条件付き集計）｜★★★☆☆（目安：15分）

問題: sales と products を結合し、商品カテゴリごとに以下を集計してください。
- 全体の取引件数（total_transactions）
- 割引ありの売上合計（discounted_sales）：discount_rate > 0 の行のみ割引後金額を合計
- 割引なしの売上合計（full_price_sales）：discount_rate = 0 の行のみ金額を合計
- 全体の売上合計（total_sales）

売上合計の大きい順に並べてください。

💡 ヒント
- SUM(CASE WHEN ... THEN 値 ELSE 0 END) で条件に合う行だけを合計できます
- このパターンは実務で超頻出です

回答例
```sql
SELECT
      p.category
    , COUNT(*) AS total_transactions
    , SUM(
        CASE
            WHEN s.discount_rate > 0 THEN s.quantity * s.unit_price * (1 - s.discount_rate)
            ELSE 0
        END
      ) AS discounted_sales
    , SUM(
        CASE
            WHEN s.discount_rate = 0 THEN s.quantity * s.unit_price
            ELSE 0
        END
      ) AS full_price_sales
    , SUM(s.quantity * s.unit_price * (1 - s.discount_rate)) AS total_sales
FROM
    sales s
    JOIN products p
        ON s.product_id = p.product_id
GROUP BY
    p.category
ORDER BY
    total_sales DESC;
```

解説: 
- 条件付き集計は実務で超頻出
- SUM(CASE WHEN ...) のパターンは必ず覚えましょう

---

### 問題26: CASE式で順序付け（カスタムソート）｜★★☆☆☆（目安：10分）

問題: customers テーブルから customer_id, customer_name, customer_segment, registration_date を表示してください。顧客セグメントを「VIP → Regular → New」のビジネス上の重要度順で並べ、同じセグメント内では登録日の昇順で並べてください。20件に制限してください。

💡 ヒント
- ORDER BY 内でCASE式を使うと、任意の順序で並べ替えができます
- 各セグメントに数値を割り当てることで順序を定義します

回答例
```sql
SELECT
      customer_id
    , customer_name
    , customer_segment
    , registration_date
FROM
    customers
ORDER BY
    CASE
        WHEN customer_segment = 'VIP' THEN 1
        WHEN customer_segment = 'Regular' THEN 2
        WHEN customer_segment = 'New' THEN 3
    END
    , registration_date
LIMIT 20;
```

解説: 
- ビジネスロジックに基づいた並び順を実現
- ORDER BY 内でCASE式を使用（標準SQL）

---

## 🔄 応用編Part2：縦持ち⇔横持ち変換マスター

### 問題27: 縦持ちから横持ちへ（ピボット）｜★★★☆☆（目安：15分）

問題: 年月ごと・カテゴリごとの売上を、「年月」を行、「カテゴリ」を列にしたクロス集計表で表示してください。カテゴリ「家電」の売上列（electronics_sales）、「家具」の売上列（furniture_sales）、および全体の合計列（total_sales）を作成してください。年月の昇順で並べてください。

💡 ヒント
- SUM(CASE WHEN カテゴリ = '...' THEN 金額 ELSE 0 END) で特定カテゴリだけを合計できます
- 各カテゴリごとにCASE式を書くのがピボットの基本パターンです

回答例
```sql
SELECT
      EXTRACT(YEAR FROM s.sale_date) AS sale_year
    , EXTRACT(MONTH FROM s.sale_date) AS sale_month
    , SUM(
        CASE
            WHEN p.category = '家電' THEN s.quantity * s.unit_price * (1 - s.discount_rate)
            ELSE 0
        END
      ) AS electronics_sales
    , SUM(
        CASE
            WHEN p.category = '家具' THEN s.quantity * s.unit_price * (1 - s.discount_rate)
            ELSE 0
        END
      ) AS furniture_sales
    , SUM(s.quantity * s.unit_price * (1 - s.discount_rate)) AS total_sales
FROM
    sales s
    JOIN products p
        ON s.product_id = p.product_id
GROUP BY
    EXTRACT(YEAR FROM s.sale_date)
    , EXTRACT(MONTH FROM s.sale_date)
ORDER BY
    sale_year
    , sale_month;
```

解説: 
- ピボット（縦→横）は、CASE式を集計関数内で使うのが基本
- 完全に標準SQL準拠

---

### 問題28: 複数軸のピボット｜★★★☆☆（目安：15分）

問題: 顧客セグメントを行、商品カテゴリを列にしたクロス集計表を作成してください。カテゴリ「家電」の売上列（electronics_sales）、「家具」の売上列（furniture_sales）、および全体の合計列（total_sales）を表示し、合計売上の大きい順に並べてください。sales, products, customers の3テーブルを結合して集計します。

回答例
```sql
SELECT
      c.customer_segment
    , SUM(
        CASE
            WHEN p.category = '家電' THEN s.quantity * s.unit_price * (1 - s.discount_rate)
            ELSE 0
        END
      ) AS electronics_sales
    , SUM(
        CASE
            WHEN p.category = '家具' THEN s.quantity * s.unit_price * (1 - s.discount_rate)
            ELSE 0
        END
      ) AS furniture_sales
    , SUM(s.quantity * s.unit_price * (1 - s.discount_rate)) AS total_sales
FROM
    sales s
    JOIN products p
        ON s.product_id = p.product_id
    JOIN customers c
        ON s.customer_id = c.customer_id
GROUP BY
    c.customer_segment
ORDER BY
    total_sales DESC;
```

解説: 
- クロス集計は実務で超頻出
- 「どのセグメントが、どのカテゴリを買っているか」が一目でわかる

---

### 問題29: 横持ちから縦持ちへ（アンピボット）｜★★★★☆（目安：20分）

問題: まずCTE（WITH句）を使い、年月ごとに以下の3つの指標を集計してください。
- 売上件数（sales_count）
- 売上金額（revenue：割引後）
- 顧客数（customer_count：ユニーク）

次に、この3指標を横持ち（3列）から縦持ち（metric_name列とmetric_value列の2列）に変換してください。metric_value は DECIMAL(18,2) に型を揃えてください。年月・指標名の昇順で並べてください。

💡 ヒント
- UNION ALL を使うと、複数のSELECT結果を縦に連結できます
- 同じCTEを複数回参照して、各指標を別のSELECTで取り出します
- CAST() で型を合わせます

回答例
```sql
WITH monthly_metrics AS (
    SELECT
          EXTRACT(YEAR FROM sale_date) AS sale_year
        , EXTRACT(MONTH FROM sale_date) AS sale_month
        , COUNT(*) AS sales_count
        , SUM(quantity * unit_price * (1 - discount_rate)) AS revenue
        , COUNT(DISTINCT customer_id) AS customer_count
    FROM
        sales
    GROUP BY
        EXTRACT(YEAR FROM sale_date)
        , EXTRACT(MONTH FROM sale_date)
)
SELECT
      sale_year
    , sale_month
    , 'Sales Count' AS metric_name
    , CAST(sales_count AS DECIMAL(18,2)) AS metric_value
FROM
    monthly_metrics

UNION ALL

SELECT
      sale_year
    , sale_month
    , 'Revenue' AS metric_name
    , revenue AS metric_value
FROM
    monthly_metrics

UNION ALL

SELECT
      sale_year
    , sale_month
    , 'Customer Count' AS metric_name
    , CAST(customer_count AS DECIMAL(18,2)) AS metric_value
FROM
    monthly_metrics

ORDER BY
    sale_year
    , sale_month
    , metric_name;
```

解説: 
- アンピボット（横→縦）は UNION ALL で実現（標準SQL）
- 複数のKPIを縦持ちにすることで、BIツールでの可視化が楽になる

---

## 🪟 応用編Part3：Window関数マスター

### 問題30: ROW_NUMBER vs RANK vs DENSE_RANK｜★★★☆☆（目安：15分）

問題: 商品ごとの合計売上金額（total_sales：割引後）を計算し、売上の大きい順に3種類のランキングを付けてください。
- ROW_NUMBER()：常に連番を振る（row_num）
- RANK()：同点は同順位、次は飛び番号（rank）
- DENSE_RANK()：同点は同順位、次は連番（dense_rank）

売上の大きい順に並べてください。

💡 ヒント
- Window関数は OVER (ORDER BY ...) で順序を指定します
- GROUP BY で商品ごとに集計した後、その集計値にランキングを付けます

回答例
```sql
SELECT
      p.product_name
    , SUM(s.quantity * s.unit_price * (1 - s.discount_rate)) AS total_sales
    , ROW_NUMBER() OVER (ORDER BY SUM(s.quantity * s.unit_price * (1 - s.discount_rate)) DESC) AS row_num
    , RANK() OVER (ORDER BY SUM(s.quantity * s.unit_price * (1 - s.discount_rate)) DESC) AS rank
    , DENSE_RANK() OVER (ORDER BY SUM(s.quantity * s.unit_price * (1 - s.discount_rate)) DESC) AS dense_rank
FROM
    sales s
    JOIN products p
        ON s.product_id = p.product_id
GROUP BY
    p.product_name
ORDER BY
    total_sales DESC;
```

解説: 
- ランキング関数の使い分けは実務で重要（全て標準SQL）
- ROW_NUMBER: 常に連番
- RANK: 同点は同順位、次の順位は飛ぶ
- DENSE_RANK: 同点は同順位、次の順位は連続

---

### 問題31: 顧客別の累積売上（PARTITION BY）｜★★★☆☆（目安：10分）

問題: 各売上レコードについて、顧客ごとに購入日順の累積売上金額（cumulative_revenue：割引後）を計算してください。表示するカラムは customer_id, sale_date, 購入金額（purchase_amount）, cumulative_revenue です。customer_id の昇順、sale_date の昇順で並べ、30件に制限してください。

💡 ヒント
- SUM() OVER (PARTITION BY ... ORDER BY ...) で、グループごとの累積合計を計算できます
- PARTITION BY で顧客ごとに分割し、ORDER BY で日付順に累積していきます

回答例
```sql
SELECT
      customer_id
    , sale_date
    , quantity * unit_price * (1 - discount_rate) AS purchase_amount
    , SUM(quantity * unit_price * (1 - discount_rate)) OVER (
        PARTITION BY customer_id
        ORDER BY sale_date
      ) AS cumulative_revenue
FROM
    sales
ORDER BY
    customer_id
    , sale_date
LIMIT 30;
```

解説: 
- Window関数の SUM() OVER で累積計算（標準SQL）
- PARTITION BY で顧客ごとに分割

---

### 問題32: LAGとLEADで前後の行を参照｜★★★☆☆（目安：10分）

問題: 各顧客の購入履歴について、前回の購入日（previous_purchase_date）と、前回購入からの経過日数（days_since_last）を計算してください。顧客ごと・購入日順で並べ、30件に制限してください。

💡 ヒント
- LAG(列名) OVER (PARTITION BY ... ORDER BY ...) で、1つ前の行の値を参照できます
- 日付の引き算で経過日数が計算できます

回答例
```sql
SELECT
      customer_id
    , sale_date
    , LAG(sale_date) OVER (
        PARTITION BY customer_id
        ORDER BY sale_date
      ) AS previous_purchase_date
    , sale_date - LAG(sale_date) OVER (
        PARTITION BY customer_id
        ORDER BY sale_date
      ) AS days_since_last
FROM
    sales
ORDER BY
    customer_id
    , sale_date
LIMIT 30;
```

解説: 
- LAG() で前の行を参照（標準SQL）
- 購買頻度分析でよく使う

---

### 問題33: 移動平均（ウィンドウフレーム）｜★★★☆☆（目安：10分）

問題: 売上データを販売日順に並べ、各行について、その行を含む直近3件の売上金額（割引後）の移動平均（moving_avg_3）を計算してください。表示するカラムは sale_date, sale_id, 売上金額（sales_amount）, moving_avg_3 です。30件に制限してください。

💡 ヒント
- AVG() OVER (ORDER BY ... ROWS BETWEEN n PRECEDING AND CURRENT ROW) で移動平均を計算できます
- ROWS BETWEEN でウィンドウの範囲（何行前から現在行まで）を指定します

回答例
```sql
SELECT
      sale_date
    , sale_id
    , quantity * unit_price * (1 - discount_rate) AS sales_amount
    , AVG(quantity * unit_price * (1 - discount_rate)) OVER (
        ORDER BY sale_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
      ) AS moving_avg_3
FROM
    sales
ORDER BY
    sale_date
LIMIT 30;
```

解説: 
- 移動平均はトレンド分析の基本（標準SQL）
- ROWS BETWEEN でウィンドウの範囲を制御

---

### 問題34: NTILE（パーセンタイル分割）｜★★★★☆（目安：20分）

問題: 以下の2段階で、顧客を売上金額による四分位グループに分類してください。

ステップ1（CTE）：顧客ごとの合計売上金額（total_revenue：割引後）を計算する。
ステップ2（メインクエリ）：customers テーブルと結合して顧客名を取得し、NTILE(4) で四分位に分割したうえで、以下のラベル（revenue_segment）を付けてください。
- 第1四分位（売上上位25%）→ 'Top 25%'
- 第2四分位 → 'Upper Middle'
- 第3四分位 → 'Lower Middle'
- 第4四分位 → 'Bottom 25%'

売上の大きい順に並べてください。

💡 ヒント
- NTILE(n) OVER (ORDER BY ...) でn等分にグループ分けできます
- CASE式でグループ番号をラベルに変換します

回答例
```sql
WITH customer_revenue AS (
    SELECT
          customer_id
        , SUM(quantity * unit_price * (1 - discount_rate)) AS total_revenue
    FROM
        sales
    GROUP BY
        customer_id
)
SELECT
      cr.customer_id
    , c.customer_name
    , cr.total_revenue
    , NTILE(4) OVER (ORDER BY cr.total_revenue DESC) AS revenue_quartile
    , CASE
        WHEN NTILE(4) OVER (ORDER BY cr.total_revenue DESC) = 1 THEN 'Top 25%'
        WHEN NTILE(4) OVER (ORDER BY cr.total_revenue DESC) = 2 THEN 'Upper Middle'
        WHEN NTILE(4) OVER (ORDER BY cr.total_revenue DESC) = 3 THEN 'Lower Middle'
        ELSE 'Bottom 25%'
      END AS revenue_segment
FROM
    customer_revenue cr
    JOIN customers c
        ON cr.customer_id = c.customer_id
ORDER BY
    cr.total_revenue DESC;
```

解説: 
- NTILE は顧客セグメンテーションでよく使う（標準SQL）
- RFM分析、ABC分析などで活用

---

## 🎓 応用編Part4：CTE（WITH句）マスター

### 問題35: CTEを使った段階的な集計｜★★★☆☆（目安：10分）

問題: CTE（WITH句）を使って、2段階で顧客の売上ランキングを作成してください。

ステップ1（CTE: customer_totals）：sales テーブルから顧客ごとの合計購入金額（total_revenue：割引後）を計算する。
ステップ2（メインクエリ）：CTEの結果と customers テーブルを結合し、customer_name と total_revenue を、売上の大きい順に表示する。

💡 ヒント
- WITH句で中間結果に名前をつけると、メインクエリがシンプルになります

回答例
```sql
WITH customer_totals AS (
    SELECT
          customer_id
        , SUM(quantity * unit_price * (1 - discount_rate)) AS total_revenue
    FROM
        sales
    GROUP BY
        customer_id
)
SELECT
      c.customer_name
    , ct.total_revenue
FROM
    customer_totals ct
    JOIN customers c
        ON ct.customer_id = c.customer_id
ORDER BY
    ct.total_revenue DESC;
```

解説: 
- WITH句で中間結果に名前をつける（標準SQL）
- 複雑な集計を段階的に書ける
- この問題は問題21（FROM句内のサブクエリ）と同じ集計を行っています。見比べてみましょう：
  - サブクエリ版（問題21）: `FROM ( SELECT ... ) AS sub` のようにクエリの中にネストする
  - CTE版（この問題）: `WITH sub AS ( SELECT ... )` で先に名前を付けてからメインクエリで使う
  - CTEの方が「上から下に」読めるため、複雑なクエリほどCTEが好まれます

---

### 問題36: CTEでVIP顧客の購買分析｜★★★☆☆（目安：15分）

問題: CTEを使って、VIP顧客の購買傾向をカテゴリ別に分析してください。

ステップ1（CTE: vip_purchases）：sales と customers を結合し、VIPセグメントの顧客の売上データだけを抽出する（sale_id, customer_id, product_id, 割引後金額 sales_amount）。
ステップ2（メインクエリ）：CTEの結果と products テーブルを結合し、カテゴリごとにVIP購入回数（vip_purchase_count）、VIP合計売上（vip_total_sales）、VIP平均購入金額（vip_avg_purchase）を集計する。合計売上の大きい順に並べてください。

回答例
```sql
WITH vip_purchases AS (
    SELECT
          s.sale_id
        , s.customer_id
        , s.product_id
        , s.quantity * s.unit_price * (1 - s.discount_rate) AS sales_amount
    FROM
        sales s
        JOIN customers c
            ON s.customer_id = c.customer_id
    WHERE
        c.customer_segment = 'VIP'
)
SELECT
      p.category
    , COUNT(*) AS vip_purchase_count
    , SUM(vp.sales_amount) AS vip_total_sales
    , AVG(vp.sales_amount) AS vip_avg_purchase
FROM
    vip_purchases vp
    JOIN products p
        ON vp.product_id = p.product_id
GROUP BY
    p.category
ORDER BY
    vip_total_sales DESC;
```

解説: 
- 複雑な分析は複数のCTEで段階的に組み立てる
- 各CTEで中間結果に名前を付けることで、コードの意図が明確になります

---

## 🎓 チャレンジ問題

### 問題37: 月別コホート分析（新規・既存顧客）｜★★★★★（目安：30分）

問題: 月ごとに、新規顧客と既存顧客の売上・顧客数を分けて集計してください。

「新規顧客」の定義：その月に初めて購入した顧客（初回購入月と売上月が同じ年月）
「既存顧客」の定義：それ以前に購入実績がある顧客（初回購入月と売上月が異なる年月）

以下の指標を年月ごとに集計してください。
- 新規顧客の売上金額（new_customer_revenue：割引後）
- 既存顧客の売上金額（existing_customer_revenue：割引後）
- 新規顧客数（new_customers：ユニーク）
- 既存顧客数（existing_customers：ユニーク）

年月の昇順で並べてください。

🔍 考え方のステップ
1. 「新規顧客」を判定するには、何が必要？ → 各顧客の初回購入日
2. 初回購入日はどうやって求める？ → customer_id で GROUP BY して MIN(sale_date) → これをCTEにする
3. 各売上が新規か既存かを判定するには？ → CTEをJOINし、売上の年月と初回購入の年月を比較
4. 新規/既存で分けて集計するには？ → CASE式 + SUM / COUNT(DISTINCT CASE ...) で条件付き集計
5. 月ごとに集計するには？ → EXTRACT で年月を取り出して GROUP BY

💡 ヒント
- CTEで各顧客の初回購入日を先に求めましょう
- EXTRACT で年月を比較し、CASE式で新規/既存を分類します
- COUNT(DISTINCT CASE WHEN ...) でユニーク数の条件付き集計ができます

回答例
```sql
WITH first_purchase AS (
    SELECT
          customer_id
        , MIN(sale_date) AS first_purchase_date
    FROM
        sales
    GROUP BY
        customer_id
)
SELECT
      EXTRACT(YEAR FROM s.sale_date) AS sale_year
    , EXTRACT(MONTH FROM s.sale_date) AS sale_month
    , SUM(
        CASE
            WHEN EXTRACT(YEAR FROM s.sale_date) = EXTRACT(YEAR FROM fp.first_purchase_date)
                AND EXTRACT(MONTH FROM s.sale_date) = EXTRACT(MONTH FROM fp.first_purchase_date)
            THEN s.quantity * s.unit_price * (1 - s.discount_rate)
            ELSE 0
        END
      ) AS new_customer_revenue
    , SUM(
        CASE
            WHEN EXTRACT(YEAR FROM s.sale_date) != EXTRACT(YEAR FROM fp.first_purchase_date)
                OR EXTRACT(MONTH FROM s.sale_date) != EXTRACT(MONTH FROM fp.first_purchase_date)
            THEN s.quantity * s.unit_price * (1 - s.discount_rate)
            ELSE 0
        END
      ) AS existing_customer_revenue
    , COUNT(DISTINCT
        CASE
            WHEN EXTRACT(YEAR FROM s.sale_date) = EXTRACT(YEAR FROM fp.first_purchase_date)
                AND EXTRACT(MONTH FROM s.sale_date) = EXTRACT(MONTH FROM fp.first_purchase_date)
            THEN s.customer_id
        END
      ) AS new_customers
    , COUNT(DISTINCT
        CASE
            WHEN EXTRACT(YEAR FROM s.sale_date) != EXTRACT(YEAR FROM fp.first_purchase_date)
                OR EXTRACT(MONTH FROM s.sale_date) != EXTRACT(MONTH FROM fp.first_purchase_date)
            THEN s.customer_id
        END
      ) AS existing_customers
FROM
    sales s
    JOIN first_purchase fp
        ON s.customer_id = fp.customer_id
GROUP BY
    EXTRACT(YEAR FROM s.sale_date)
    , EXTRACT(MONTH FROM s.sale_date)
ORDER BY
    sale_year
    , sale_month;
```

解説: 
- コホート分析は実務で重要な分析手法
- CTE + CASE式 + EXTRACT の総合的な活用
- 完全に標準SQL準拠

---

## 🎯 学習の進め方

1. 基礎編（1-6）: SELECT と WHERE に慣れる ← 写経から始めてOK
2. 実務編（7-8）: AS句とビジネスドメイン用語の重要性を理解
3. 関数編（9-16）: 日付・文字列関数をマスター（全て標準SQL）
4. 中級編（17-19）: JOIN と集計をマスター ← 改変で理解を深める
5. 実践編（20-22）: サブクエリとビューの基礎を理解
6. 応用編Part1（23-26）: CASE式で複雑なロジックを表現 ← 自力に挑戦
7. 応用編Part2（27-29）: 縦持ち⇔横持ち変換をマスター
8. 応用編Part3（30-34）: Window関数で高度な分析
9. 応用編Part4（35-36）: CTEで読みやすいクエリを書く技術
10. チャレンジ（37）: 総合的な実践問題

全37問、全て標準SQL準拠です。頑張ってください！
