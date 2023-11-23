#-----------------------------------------------------------------------
#プロンプト
#https://chat.openai.com/c/743a04ad-4465-4271-bf18-881577314a66
# python streamlit  でチャットボットを開発できますか
# キーワードに対して、決まった文言を返すようにしたい
# 連続した会話にしたい
# 過去のテキストが消えずにテキストを連続で表示するようにしたい
# 過去の履歴がテキストの上に蓄積表示される状態
# テキストに入力したら、返答文章が表示の繰り返し。過去の履歴は消えない
# 送信ボタンを押すと過去の履歴が消えてしまう
# まだ、消えてしまいます
# 過去の履歴が表示されるボタンを追加してください
# 1個前まではそのまま表示させたい
# 直前の10つのメッセージに変更してください
# ユーザーとチャットボットのアイコンを入れたい
# チャットボットのアイコンがへんです
# テキストボックスの幅を狭めたい ⇒NG
# テキスト入力して、enter で実行できるように機能を追加してください⇒NG
# ①準備したEXCELファイル
# C:\Users\AAAA\Desktop\slackBOT\【python】実行環境\◆パーケージ\slakbotTEST.xlsx
# ②A列がキーワードになります
# ③B列が回答文になります。
# ①のファイルを使用して、ユーザーがA列のキーワードを入力してヒットした場合、
# ボットがB列の回答文を回答できるようにしたい
# EXCEL内の改行も反映してほしい
# 上記コードだと、EXCELの改行部分が改行されず1行で表示されています
# あと、httpの場合は、リンクさせたいです
# 例えば
# "日報：
# https://AAAAAAA
# 宜しくお願いします！"
# EXCEL内上記の文字列になっていますが
# ↓
# "日報：#
# https://AAAAAAA#
# 宜しくお願いします！#"
# に書き換えて、
# コード内で、#を改行コードに変換して、
# ボットが表示するときに改行された状態で出力されるようになりますか。
# ▼出力結果
# 日報：
# https://AAAAAAA
# 宜しくお願いします！
# ダブルコーテーションを消したい
# 改行コードは\nではなく\n\nではないでしょうか
# ボットの回答を左に戻してください
# ボットのメッセージに枠を入れることはできますか
# 太文字にできますか⇒保留
# ファイル内のA列をリストボックスで表示したい
# ファイル内で空白で、selectboxで表示されるnanを除外して表示してください

# 上記コードに追加・修正をお願いします。
# ①取込ボタンを追加　
# ②excel_file_path を使用して、取込ボタンでexcel_file_pathのファイルを読み込む
# ③あとは、同じ処理
#-----------------------------------------------------------------------

import streamlit as st
import pandas as pd

#-----------------------------------------------------------------------
# ユーザー入力に対するチャットボットの応答を取得する関数
#-----------------------------------------------------------------------
def chatbot_response(user_input, df):
    matched_answer = df.loc[df['キーワード※値で貼り付け'] == user_input, '返答※値で貼り付け'].values
    if len(matched_answer) > 0:
        return matched_answer[0] # マッチした回答を返す
    else:
        return "すみません、そのキーワードに対する回答は見つかりませんでした。"  # 該当する回答がない場合のデフォルト応答

def main():
    st.title("bot") # Streamlitアプリのタイトルを設定

    excel_file_path = None # Excelファイルのパスを初期化

    # ファイル選択用のボタンを追加（サイドバーに配置）
    uploaded_file = st.sidebar.file_uploader("Excelファイルを選択してください", type=['xlsx', 'xls'])

    if uploaded_file:
        excel_file_path = uploaded_file  # 選択されたファイルパスをexcel_file_pathに代入

    if excel_file_path is not None:  # ファイルが選択されている場合の処理
        df = pd.read_excel(excel_file_path) # Pandasを使って選択されたExcelファイルを読み込む

        # キーワードの選択肢をデータフレームから取得　※欠損値(空白)確認
        keyword_options = df.loc[df['キーワード※値で貼り付け'].notna() & (df['キーワード※値で貼り付け'] != ' ')]['キーワード※値で貼り付け']
        
        chat_history = st.session_state.get("chat_history", []) # チャット履歴をsession_stateから取得（初期値は空のリスト）
        show_history = st.checkbox("過去の履歴を表示する") # チェックボックスで過去の履歴を表示するかどうかを選択

        user_input = st.selectbox("ユーザー: メッセージを選択してください", keyword_options) # ユーザーからの選択ボックスを表示

        if st.button("送信"): # 「送信」ボタンが押されたら

            # ユーザーのメッセージを生成
            user_message = f"<img src='https://img.icons8.com/material-outlined/24/000000/user-male-circle.png' style='vertical-align: middle;'> Q: {user_input}"
            # チャット履歴にユーザーのメッセージを追加
            chat_history.append(user_message)

            bot_response = chatbot_response(user_input, df) # チャットボットの応答を取得
            bot_response = bot_response.replace('"', '').replace('#', '\n\n') # 応答の整形

            # チャットボットの応答を表示用のHTMLに整形
            bot_message = f"<div style='text-align: left; padding: 10px; border: 1px solid #ccc; border-radius: 5px;'><img src='https://img.icons8.com/material-outlined/24/000000/bot.png' style='vertical-align: middle;'><span style='vertical-align: middle;'>A:<br><br>{bot_response}</span></div>"

            chat_history.append(bot_message) # チャット履歴にチャットボットの応答を追加
            st.session_state["chat_history"] = chat_history # session_stateにチャット履歴を保存

        if show_history: # 過去のチャット履歴を表示
            start_index = max(0, len(chat_history) - 10)
            st.markdown("<br>".join(chat_history[start_index:]), unsafe_allow_html=True)
        else:            # 最新のチャット履歴を表示
            st.markdown(chat_history[-1] if chat_history else "", unsafe_allow_html=True)
    # else:
    #     st.write("AAExcelファイルを選択してください")

#Pythonのスクリプトが直接実行された場合にのみ、main() 関数が実行
if __name__ == "__main__":
    main()
#-----------------------------------------------------------------------
#requirements.txt
#-----------------------------------------------------------------------
#streamlit==1.28.2
#pandas==2.0.1
#openpyxl==3.1.2
#-----------------------------------------------------------------------
#git hubにリポジトリ作成してプッシュする
#-----------------------------------------------------------------------
#①https://github.com/⇒Top Repositories[New]リポジトリの作成
#②Repository name ⇒ Public(公開) or Private(非公開)⇒[Create repository]
#③ターミナル⇒新しいターミナル
#git init
#git add main.py requirements.txt ⇒アップロードしたいファイルを指定　[add .だと全部アップされてしまう]
#git commit -m "first commit"  ⇒GitHub上のコメント表示(次にコミットするときは違う文言で)

# On branch main
# Untracked files:
#   (use "git add <file>..." to include in what will be committed)
# [main (root-commit) 8fe9b5e] first commit
#  2 files changed, 115 insertions(+)
#  create mode 100644 main.py
#  create mode 100644 requirements.txt

#git branch -M main ⇒ブランチの名前を変更します。
#git remote add origin https://github.com/YMOmame/YMO_BOT_DEV.git ⇒ローカルリポジトリがリモートリポジトリと連携
#git push -u origin main ⇒リモートリポジトリにプッシュします

#④Git HubのサイトをF5するとコミット完了
#⑤https://share.streamlit.io/　⇒[New app]クリック
#⑥各項目に対して、選択or変更入力 Repository/Main file path⇒main.py ⇒[Deploy]
#⑦デプロイされたサイトが開く

#VS CODEでファイルを変更した場合は、再度(add/commit/push)Git hubに更新して、streamlitのサイトを開きなおす
#https://github.com/YMOmame/YMO_BOT_DEV
#-----------------------------------------------------------------------