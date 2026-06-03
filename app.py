import streamlit as st
import google.generativeai as genai

# --- ページ設定とデザイン ---
st.set_page_config(page_title="自己資源・強み発見アシスタント", layout="wide")

# --- カスタムCSS（壁紙・明朝体・桜色テーマ・スマホ対応） ---
st.markdown("""
<style>
/* 1. 全体のフォントを游明朝に統一（アイコン崩れ防止のため span は除外） */
html, body, p, div, a, button, h1, h2, h3, h4, h5, h6, label {
    font-family: 'Yu Mincho', '游明朝', 'YuMincho', 'Hiragino Mincho ProN', 'HGS明朝E', serif !important;
}

/* 2. ページ全体の壁紙（和紙風テクスチャ） */
.stApp {
    background-color: #FCFAFA;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.04'/%3E%3C/svg%3E");
    background-attachment: fixed;
}

/* 3. ヘッダーデザイン（PC用） */
.header-box {
    text-align: center;
    padding: 3rem 1rem;
    background-color: rgba(255, 255, 255, 0.8);
    border-bottom: 2px solid #DB90A0;
    margin-bottom: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.02);
}
.header-title { font-size: 2.2rem; font-weight: 700; color: #3D2D2E; }
.header-subtitle { font-size: 1.1rem; color: #5C4B4D; margin-top: 0.8rem; line-height: 1.6; }

/* 4. 各種コンテナ・ボックスのデザイン */
div[data-testid="stForm"] {
    background-color: rgba(255, 255, 255, 0.9) !important;
    border-radius: 8px !important;
    padding: 30px !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.03) !important;
}
.result-box {
    background-color: #FDFEFE;
    padding: 25px;
    border-radius: 8px;
    border-left: 5px solid #DB90A0;
    margin-top: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    font-size: 1.05rem;
    line-height: 1.8;
}

h1, h2, h3 { color: #3D2D2E !important; }

/* 5. スマートフォン向けの画面表示設定（レスポンシブ対応） */
@media screen and (max-width: 768px) {
    .header-title { font-size: 1.5rem !important; }
    .header-subtitle { font-size: 0.95rem !important; margin-top: 0.8rem !important; }
    .header-box { padding: 2rem 1rem !important; }
    
    div[data-testid="stForm"] { padding: 15px !important; }
    .result-box { padding: 15px !important; font-size: 0.95rem !important; }
    
    h2 { font-size: 1.3rem !important; }
    h3 { font-size: 1.1rem !important; margin-bottom: 0.5rem !important; }
    p, label { font-size: 0.95rem !important; line-height: 1.6 !important; }
    
    /* スマホ用ボタン調整（横幅いっぱい） */
    [data-testid="stFormSubmitButton"] button, 
    .stButton button, 
    [data-testid="stDownloadButton"] button,
    [data-testid="stLinkButton"] a {
        padding: 0.6rem 1rem !important;
        font-size: 1rem !important;
        width: 100% !important;
        text-align: center;
        margin-bottom: 10px !important;
    }
}

/* 6. ボタンのデザイン（PC用ベース） */
[data-testid="stFormSubmitButton"] button, 
.stButton button,
[data-testid="stDownloadButton"] button,
[data-testid="stLinkButton"] a {
    background-color: #DB90A0 !important;
    color: #ffffff !important;
    border-radius: 6px !important;
    padding: 0.7rem 3rem !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    text-align: center;
    text-decoration: none !important;
    transition: all 0.3s ease;
}
[data-testid="stFormSubmitButton"] button:hover,
.stButton button:hover,
[data-testid="stDownloadButton"] button:hover,
[data-testid="stLinkButton"] a:hover {
    background-color: #C27082 !important;
    transform: translateY(-2px);
}
[data-testid="stLinkButton"] a *,
[data-testid="stDownloadButton"] button * {
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# --- タイトル表示 ---
st.markdown('''
<div class="header-box">
    <div class="header-title">🌱 自己資源・強み発見アシスタント</div>
    <div class="header-subtitle">
        あなたが「なんでもない」と思っている経験や、当たり前に続けていることには、ビジネスで通用する立派な「強み（ポータブルスキル）」が隠れています。AIと一緒に、あなたの魅力を見つけ出しましょう！
    </div>
</div>
''', unsafe_allow_html=True)

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
                
                # ★ 出力結果をデザイン枠の中に表示
                st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                st.markdown(response.text)
                st.markdown("</div>", unsafe_allow_html=True)

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

# --- ポータルサイトへ戻るボタン ---
st.markdown("---")
st.link_button("🏠 C.HARIGOMA キャリア支援ポータルへ戻る", "https://harigoma-career.streamlit.app/")
