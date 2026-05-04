import streamlit as st
import google.generativeai as genai

# --- ページ設定とデザイン ---
st.set_page_config(page_title="自己資源・強み発見アシスタント", layout="wide")

st.markdown("""
<style>
h1, h2, h3 { color: #1A5276 !important; }
label p, [data-testid="stWidgetLabel"] p { font-size: 18px !important; color: #2874A6 !important; font-weight: bold !important; }
[data-testid="stFormSubmitButton"] { display: flex; justify-content: center; margin-top: 20px; margin-bottom: 20px; }
[data-testid="stFormSubmitButton"] button { background-color: #27AE60 !important; color: white !important; font-size: 20px !important; font-weight: bold !important; padding: 15px 50px !important; border-radius: 10px !important; border: none !important; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
[data-testid="stFormSubmitButton"] button:hover { background-color: #1E8449 !important; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

st.title("🌱 自己資源・強み発見アシスタント")
st.write("あなたが「なんでもない」と思っている経験や，当たり前に続けていることには，ビジネスで通用する立派な「強み（ポータブルスキル）」が隠れています。AIと一緒に，あなたの魅力を見つけ出しましょう！")

# --- はじめての方へ（APIキー入力） ---
with st.expander("🔑 ご利用には無料のAPIキーが必要です（取得方法はこちら）", expanded=False):
    st.markdown("""
    **Q. 「API（エーピーアイ）」って何ですか？** A. このアプリの画面と，裏側で客観的な視点を提供する「AI（頭脳）」を安全に繋ぐための**「専用の直通電話」**のようなものです。この高性能なAIを無料で利用していただくための**「通行手形」**として，利用者様ご自身に取得をお願いしております。（※もちろん料金が発生することはありませんので，ご安心ください）

    ---
    **【図解】無料APIキーの取得手順（所要時間：約3分）**
    
    **ステップ1：Google AI Studioにアクセス** Googleアカウントにログインした状態で，[Google AI Studio](https://aistudio.google.com/) にアクセスします。

    **ステップ2：APIキーを発行** 画面左側のメニューから「Get API key」を選び，「Create API key」ボタンをクリックして新しいキーを作成します。

    **ステップ3：キーをコピーしてアプリに貼り付け** 画面に表示された `AIza...` から始まる長い文字列をコピーし，このアプリの左側（サイドバー）にある「Gemini APIキー」の入力欄に貼り付けてください。設定はこれだけで完了です！
    """)

st.sidebar.header("🔑 セキュリティ設定")
api_key = st.sidebar.text_input("Gemini APIキー", type="password")

# --- 入力フォーム ---
with st.form("skills_form"):
    # 前回の素晴らしいアイデアを踏襲したお名前入力欄
    user_name_input = st.text_input("お名前（相談結果にてあなたのお名前で表現します。苗字（ひらがなでも可）のみでも構いません）")
    
    st.markdown("---")

    st.subheader("Q1. あなたの「経験」を教えてください。")
    st.caption("仕事，趣味，家事，ボランティア，勉強など，どんなことでも構いません。「ただの事務作業」「毎日お弁当を作った」「ゲームのギルドマスターをした」など，ありのままを書いてみましょう。")
    experience = st.text_area("（例：前職で5年間，データ入力と電話応対をしていました。）")
    
    st.subheader("Q2. その中で，少しでも「工夫したこと」や「気をつけたこと」はありますか？")
    st.caption("「ミスがないように見直した」「なるべく早く返信した」など，小さなことで大丈夫です。")
    effort = st.text_area("（例：入力ミスがないように，最後に必ず指差し確認をしていました。）")
    
    st.markdown("---")
    submit_btn = st.form_submit_button("プロの語彙（強み）に翻訳する ✨")

# --- 実行処理 ---
if submit_btn:
    if not api_key:
        st.error("⚠️ 左側のメニューにAPIキーを入力してください。")
    elif not experience:
        st.warning("⚠️ Q1の「経験」は最低限入力してください。")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        user_name = user_name_input if user_name_input else "あなた"

        prompt = f"""
        あなたは求職者に寄り添う，経験豊富で温かいキャリアコンサルタントです。
        クライアントが「なんでもない」と思っている経験から，ビジネスで通用する「ポータブルスキル（持ち運び可能な能力）」を見つけ出し，自己効力感を高めるサポートをしてください。

        【クライアントの入力情報】
        - 呼称：{user_name}
        - 経験・続けていること：{experience}
        - 工夫したこと・気をつけたこと：{effort}

        【出力要件】
        以下の3つのセクションに分けて，温かく励ますトーンで出力してください。

        1. 【共感と承認】
        まずはクライアントの経験の素晴らしさ，継続や工夫の価値を温かく認めてください。呼びかけには必ず「{user_name}さん」を使用してください。

        2. 【発見されたポータブルスキル（3つ）】
        その経験が，ビジネスの現場でどのような「強み」として活きるのか，プロの語彙（例：課題解決力，継続力，調整力，正確性，ホスピタリティなど）を使って3つ提示し，なぜそう言えるのかを分かりやすく解説してください。

        3. 【履歴書・面接で使える「自己PR」のたたき台】
        発見した強みをもとに，実際の就職活動で使える自己PRの文章（約200〜300文字）を作成してください。

        【AIへの特別な指示（作成のスタンス）】
        ・想像部分の明示（太字化）：求職者の入力情報に具体的な実績や数字が不足しており，説得力を持たせるためにAIが仮のエピソードや成果を想像して補完する場合は，必ずその部分を「**」（Markdownの太字）で囲んで出力すること。（例：「**業務効率化に取り組み，作業時間を20％削減しました**。」）

        【制約条件】
        ・読点：文章中の読点には必ず「，」を使用すること（「、」は使用しないこと）
        ・注意書きの追記：もし太字で想像・補完した箇所がある場合は，文章の最後に改行を入れ，「※【太字】の部分はAIが作成した例文（仮の成果・エピソード）です。必ずご自身の実際の経験に合わせて書き換えてからご使用ください。」と必ず明記すること。
        """

        with st.spinner('キャリアコンサルタントAIがあなたの「強み」を発掘しています...'):
            try:
                response = model.generate_content(prompt)
                st.success("強みの発掘が完了しました！")
                st.markdown("---")
                st.markdown(response.text)

# --- ダウンロード用のテキストを組み立てる ---
                download_text = f"""【あなたの入力内容】
■Q1. 経験・続けていること
{experience}

■Q2. 工夫したこと・気をつけたこと
{effort}

==================================================
【AIからの分析結果】
{response.text}
"""
                
                # --- ダウンロードボタン ---
                st.markdown("---")
                st.download_button(
                    label="📝 入力内容と分析結果を保存（ダウンロード）する",
                    data=download_text,
                    file_name="portable_skills_result.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"エラーが発生しました。詳細: {e}")
