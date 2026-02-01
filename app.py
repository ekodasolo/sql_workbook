import streamlit as st
import duckdb
import pandas as pd
from pathlib import Path

# ページ設定
st.set_page_config(
    page_title="SQL学習アプリ",
    page_icon="🦆",
    layout="wide"
)

# タイトル
st.title("🦆 Webブラウザで学ぶSQL入門")
st.markdown("---")

# DuckDB接続の初期化
@st.cache_resource
def init_db():
    """DuckDB接続とCSVデータの読み込み"""
    con = duckdb.connect(database=':memory:', read_only=False)
    
    # データディレクトリのパス
    data_dir = Path(__file__).parent / "data"
    
    # CSVファイルからテーブルを作成
    try:
        # 売上トランザクション
        con.execute(f"""
            CREATE TABLE sales AS 
            SELECT * FROM read_csv_auto('{data_dir}/sales.csv')
        """)
        
        # 商品マスタ
        con.execute(f"""
            CREATE TABLE products AS 
            SELECT * FROM read_csv_auto('{data_dir}/products.csv')
        """)
        
        # 顧客マスタ
        con.execute(f"""
            CREATE TABLE customers AS 
            SELECT * FROM read_csv_auto('{data_dir}/customers.csv')
        """)
        
        # 店舗マスタ
        con.execute(f"""
            CREATE TABLE stores AS 
            SELECT * FROM read_csv_auto('{data_dir}/stores.csv')
        """)
        
        st.success("✅ データの読み込みに成功しました")
        
    except Exception as e:
        st.error(f"❌ データ読み込みエラー: {e}")
        st.info("data/フォルダにCSVファイルが配置されているか確認してください")
    
    return con

# データベース接続
con = init_db()

# 利用可能なテーブル一覧を表示
with st.sidebar:
    st.header("📊 利用可能なテーブル")
    tables = con.execute("SHOW TABLES").fetchall()
    
    for table in tables:
        table_name = table[0]
        if st.button(f"📋 {table_name}", key=f"btn_{table_name}"):
            st.session_state['selected_table'] = table_name
    

# メインエリア：2カラムレイアウト
col1, col2 = st.columns([4, 6])

with col1:
    st.header("✍️ SQLエディタ")
    
    # セッションステートにクエリを保存
    if 'sql_input' not in st.session_state:
        st.session_state['sql_input'] = """SELECT product_id, product_name, category
FROM products
FETCH FIRST 10 ROWS ONLY;"""
    
    sql_query = st.text_area(
        "SQLクエリを入力してください",
        value=st.session_state.get('sql_input'),
        height=300
    )
    
    # ボタン群
    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 2])
    
    with btn_col1:
        execute_btn = st.button("▶️ 実行", type="primary", width='stretch')
    
    with btn_col2:
        clear_btn = st.button("🗑️ クリア", width='stretch')
    
    if clear_btn:
        st.session_state['sql_input'] = ""
        st.rerun()

with col2:
    st.header("📊 データビューワー")
    
    # 選択されたテーブルのスキーマ表示
    if 'selected_table' in st.session_state:
        table_name = st.session_state['selected_table']
        st.subheader(f"テーブル: {table_name}")
        
        try:
            schema = con.execute(f"DESCRIBE {table_name}").fetchdf()
            with st.expander("スキーマ情報を表示"):
                st.dataframe(schema, width='stretch')
        except Exception as e:
            st.error(f"スキーマ取得エラー: {e}")
    
    # クエリ実行結果の表示
    if execute_btn:
        if sql_query.strip():
            try:
                # クエリ実行
                result = con.execute(sql_query).fetchdf()
                
                # 結果表示
                st.success(f"✅ クエリ実行成功！ ({len(result)}行取得)")
                st.dataframe(result, width='stretch', height=400)
                
                # 統計情報
                with st.expander("📈 データ統計"):
                    st.write(f"**行数**: {len(result)}")
                    st.write(f"**列数**: {len(result.columns)}")
                    st.write(f"**カラム**: {', '.join(result.columns)}")
                
            except Exception as e:
                st.error(f"❌ エラーが発生しました")
                st.code(str(e), language="text")
                
                # 初学者向けのヒント
                error_msg = str(e).lower()
                if "syntax error" in error_msg:
                    st.info("💡 **ヒント**: SQL構文にエラーがあります。セミコロン、カンマ、括弧などを確認してください。")
                elif "table" in error_msg and "not found" in error_msg:
                    st.info("💡 **ヒント**: テーブル名が正しいか確認してください。左サイドバーで利用可能なテーブルを確認できます。")
                elif "column" in error_msg:
                    st.info("💡 **ヒント**: カラム名が正しいか確認してください。テーブルのスキーマ情報を確認しましょう。")
        else:
            st.warning("⚠️ SQLクエリを入力してください")

# フッター
st.markdown("---")
st.caption("Powered by DuckDB | このアプリでSQLの基礎を学びましょう")
