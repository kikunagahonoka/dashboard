# 🛒 小売店向けダッシュボード

このアプリは、CSVファイルまたはテンプレートから売上・顧客データを読み込み、視覚的に分析するための **小売店向け業務ダッシュボード** です。売上・顧客数・目標達成率をグラフと数値でわかりやすく確認できます。

## 🔧 機能一覧

- CSVファイルのアップロード・編集
- 売上、顧客数、目標達成率の自動計算
- 可視化（積み上げ棒グラフ、折れ線グラフなど）
- 時間帯ごとの傾向コメント生成
- 現在時刻から閉店までに必要な売上の逆算（スタッフ人数も考慮）
- 分析データのダウンロード機能（今後追加可能）

## 🖥 使用技術

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly Express](https://plotly.com/python/plotly-express/)

## ▶️ 使い方

1. 必要なパッケージをインストールします：

   ```bash
   pip install streamlit pandas plotly
アプリを起動します：

bash
コピーする
編集する
streamlit run app.py
ブラウザで表示される画面から、CSVをアップロード or テンプレートを編集して「📥 データを読み込む」ボタンをクリック。

## 📂 CSVフォーマット例
```
time,sales_A,sales_B,customers,target_sales
10時,800,400,15,1500
11時,950,600,18,1500
```
