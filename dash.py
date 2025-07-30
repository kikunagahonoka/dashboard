import streamlit as st
import pandas as pd
import plotly.express as px
import io
import plotly.io as pio

st.set_page_config(page_title="Dashboard", page_icon="🛒", layout="wide")

# セッション状態の初期化
if "df" not in st.session_state:
    st.session_state.df = None

st.title("🛒 小売店向けダッシュボード")

# 📌 タブUIで構成
tab1, tab2 = st.tabs(["① データ入力", "② 分析とダウンロード"])

# -------------------------------
# 📥 タブ1：データ入力
# -------------------------------
with tab1:
    st.subheader("📥 データを入力してください")
    subtab1, subtab2 = st.tabs(["✅ CSVをアップロード", "✏️ テンプレを使う"])

    with subtab1:
        uploaded_file = st.file_uploader("CSVファイルをアップロード", type="csv")
        if uploaded_file is not None:
            st.session_state.df = pd.read_csv(uploaded_file)
            st.success("✅ CSVを読み込みました")

    with subtab2:
        template = pd.DataFrame({
            "time": ["10時", "11時", "12時", "13時", "14時", "15時", "16時", "17時", "18時", "19時"],
            "sales_A": [800, 950, 1600, 1800, 1500, 1400, 1300, 1700, 2000, 1900],
            "sales_B": [400, 600, 900, 1100, 800, 700, 600, 800, 1000, 950],
            "customers": [15, 18, 25, 30, 28, 26, 24, 29, 32, 31],
            "target_sales": [1500]*10
        })
        edited = st.data_editor(template, num_rows="dynamic", use_container_width=True)
        st.session_state.df = edited


    # -------------------------------
    # ✅ 手動でデータを反映（確定）するボタン
    # -------------------------------
    if st.button("📥 データを読み込む"):
        st.session_state.data_loaded = True
        st.success("📊 データを読み込みました！②タブで確認できます")


# -------------------------------
# 📊 タブ2：分析とダウンロード
# -------------------------------
with tab2:
    st.subheader("📊 データ分析結果とダウンロード")

    if not st.session_state.get("data_loaded", False):
        st.warning("⚠️ まず①タブでデータを入力し、『データを読み込む』ボタンを押してください")
    else:
        df = st.session_state.df.copy()
        df["売上合計"] = df["sales_A"] + df["sales_B"]
        df["達成率"] = df["売上合計"] / df["target_sales"] * 100

        total_sales = df["売上合計"].sum()
        total_customers = df["customers"].sum()
        avg_unit_price = total_sales / total_customers if total_customers else 0
        total_target = df["target_sales"].sum()
        achievement = total_sales / total_target if total_target else 0

        st.subheader("📊 サマリー")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("本日の売上", f"¥{total_sales:,.0f}")
        col2.metric("客数", f"{total_customers:,}人")
        col3.metric("客単価", f"¥{avg_unit_price:,.0f}")
        col4.metric("目標達成率", f"{achievement:.1%}")

        # グラフを3列で表示
        col1, col2, col3 = st.columns(3)

        with col1:
            fig1 = px.bar(df, x="time", y=["sales_A", "sales_B"], barmode="stack",
                            text_auto=True, title="🧾 売上（積み上げ）")
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            fig2 = px.bar(df, x="time", y="customers", text_auto=True,
                            title="👥 客数")
            st.plotly_chart(fig2, use_container_width=True)

        with col3:
            fig3 = px.line(df, x="time", y="達成率", markers=True,
                            title="🎯 予算達成率")
            fig3.update_traces(
                mode="lines+markers+text",
                text=df["達成率"].apply(lambda x: f"{x:.0f}%"),
                textposition="top center"
            )
            st.plotly_chart(fig3, use_container_width=True)

        # 💡 自動コメント
        col4, col5 = st.columns(2)
        with col4:
            st.divider()
            st.markdown("### 💡 時間帯コメント")
            max_time = df.loc[df["売上合計"].idxmax(), "time"]
            worst_time = df.loc[df["達成率"].idxmin(), "time"]
            st.write(f"🕒 一番売れた時間帯：**{max_time}**")
            st.write(f"⚠️ 予算達成率が低かった時間帯：**{worst_time}**")

            if max_time in ["12時", "13時", "14時"]:
                st.write("🍱 昼ピーク帯に強い売上傾向があります。昼前後の商品補充・スタッフ配置の強化が有効かもしれません。")
            elif max_time in ["17時", "18時", "19時"]:
                st.write("🌇 夕方に売上が集中しています。仕事帰りの層を意識した販促が効果的かもしれません。")
            else:
                st.write("🧐 売上が偏っていないので、時間帯ごとのプロモーションの工夫が必要かもしれません。")
        
        
        # 💡 残り時間とスタッフ数に基づく必要売上
        with col5:
            st.divider()
            st.markdown("### 🕒 残り時間から必要売上を逆算")

            import datetime
            now = st.time_input("現在時刻", value=datetime.datetime.now().time())
            closing = st.time_input("閉店時刻", value=datetime.time(20, 0))
            staff_count = st.number_input("現在のスタッフ人数", min_value=1, step=1, value=3)

            now_dt = datetime.datetime.combine(datetime.date.today(), now)
            closing_dt = datetime.datetime.combine(datetime.date.today(), closing)
            remaining_minutes = (closing_dt - now_dt).total_seconds() / 60

            if remaining_minutes <= 0:
                st.error("⚠️ 閉店時刻は現在時刻より後に設定してください")
            else:
                remaining_hours = remaining_minutes / 60
                remaining_target = max(total_target - total_sales, 0)
                per_hour = remaining_target / remaining_hours
                per_staff = per_hour / staff_count

                col1, col2 = st.columns(2)
                col1.metric("1時間あたり必要売上", f"¥{per_hour:,.0f}")
                col2.metric("スタッフ1人あたり必要売上", f"¥{per_staff:,.0f}")
