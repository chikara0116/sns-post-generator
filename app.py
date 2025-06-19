import streamlit as st
import openai
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# APIキーを設定
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- ここからが変更・追加部分 ---

# 各SNSプラットフォームの特徴を定義した辞書
# この情報をプロンプトに含めることで、AIが各SNSに最適化しやすくなる
PLATFORM_CHARACTERISTICS = {
    "X (Twitter)": "140字以内の短文で、速報性とキャッチーさが重要。関連性の高いハッシュタグを3つ程度含めてください。",
    "Instagram": "画像や動画が主役であることを意識し、共感を呼ぶストーリー性のある文章を作成してください。世界観を表現し、改行や絵文字を効果的に使って読みやすくしてください。ハッシュタグは5つ以上含めてください。",
    "Facebook": "比較的フォーマルで、信頼性が重視されます。ターゲット層に語りかけるような、少し長めの丁寧な文章を作成してください。イベントの告知や詳細な説明にも向いています。",
    "TikTok": "短い動画で使われることを想定した、インパクトのある台本やキャプションを作成してください。若者向けの言葉遣いや、トレンドを意識した内容が効果的です。冒頭の2秒で興味を引く工夫をしてください。",
    "LINE (公式アカウント)": "友だちに送るような、親しみやすいメッセージを作成してください。新商品のお知らせやクーポン配布など、ユーザーにとってお得な情報を伝えるのに適しています。文頭に[お知らせ]のような形式を入れると分かりやすいです。"
}

# --- ここまでが変更・追加部分 ---


# StreamlitアプリのUI部分
st.title("🎯SNS特化型 投稿文生成アプリ") # タイトルを少し変更

# --- ここからが変更・追加部分 ---

# SNSプラットフォームを選択するセレクトボックスを追加
platform = st.selectbox(
    "投稿したいSNSプラットフォームを選択してください",
    list(PLATFORM_CHARACTERISTICS.keys()) # 辞書のキーをリストとして表示
)

# --- ここまでが変更・追加部分 ---

# ユーザーからの入力を受け取る
theme = st.text_input("投稿のテーマを入力してください", "例：新発売のオーガニックコーヒー")
keywords = st.text_input("含めたいキーワードを入力してください（カンマ区切り）", "例：ハンドドリップ, 香り高い, 数量限定")
target = st.text_input("ターゲット層を教えてください", "例：仕事の合間に一息つきたい20代の社会人")
# 任意項目として追加
option = st.text_input("その他、特に伝えたいことや制約があれば入力してください（任意）", "例：キャンペーンは今週末まで")


# 生成ボタン
if st.button("投稿文を生成する"):
    if not theme or not keywords or not target:
        st.error("必須項目（テーマ、キーワード、ターゲット層）を入力してください。")
    else:
        # --- ここからが変更・追加部分 ---
        
        # 選択されたプラットフォームの特徴を取得
        platform_char = PLATFORM_CHARACTERISTICS[platform]

        # AIへの指示（プロンプト）を改善
        prompt = f"""
        あなたはプロのSNSマーケターです。
        以下の情報と、指定されたSNSプラットフォームの特性を最大限に活かして、読者の心に響く魅力的な投稿文を3パターン作成してください。

        # SNSプラットフォーム
        {platform}

        # プラットフォームの特性と指示
        {platform_char}

        # 投稿の基本情報
        - テーマ: {theme}
        - 含めたいキーワード: {keywords}
        - ターゲット層: {target}
        - その他の要望: {option if option else '特になし'}

        ---
        上記の指示に従って、最適な投稿文を3パターン生成してください。
        """
        # --- ここまでが変更・追加部分 ---

        # AIにリクエストを送信
        try:
            with st.spinner(f"{platform}用の投稿文を生成中です..."): # 待機メッセージを動的に変更
                response = openai.chat.completions.create(
                    model="gpt-4o-mini", # より安価で高性能な新モデルに変更するのも良い
                    messages=[
                        {"role": "system", "content": "あなたは、指定されたSNSの特性を理解し、最適な文章を生成するプロのSNSマーケターです。"},
                        {"role": "user", "content": prompt}
                    ]
                )
            
            # 結果を表示
            st.subheader(f"🤖 {platform}用の投稿文はこちらです") # 見出しも動的に変更
            st.write(response.choices[0].message.content)

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")