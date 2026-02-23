# stock_bot.py

import requests
import os
from dotenv import load_dotenv

# ===== 環境変数読み込み =====
load_dotenv()  # .env の内容を反映

API_KEY = "RB_NnjfS0OpIGn5uC6fac9FEgLFZzBKhYjM0_YkkIVQ"
LINE_ACCESS_TOKEN = "4XjMJXwNI8Xm669/RNs69/KICRe9jaG8KmUvMPzsye5969fX61beEK6RUbdKlBuiHSRo/xmiamKxclLylysLY9vjFpPslwKwnyIgKc1s50X/RuK3Plc3/Gc8t2BKK9IIfra1BO9cAIT0/jqKdvUC7gdB04t89/1O/w1cDnyilFU="
LINE_USER_ID = "U3900fb6357ff8ba7767f6f808f85e14a"

# ===== APIキー未設定チェック =====
if not all([API_KEY, LINE_ACCESS_TOKEN, LINE_USER_ID]):
    print("⚠️ APIキーが設定されていません。.envを確認してください。")
    exit()

# ===== J-Quantsから株価取得 =====
headers = {"x-api-key": API_KEY}

response = requests.get(
    "https://api.jquants.com/v1/prices/daily_quotes",
    params={"code": "7203"},  # トヨタの銘柄コード
    headers=headers
)

if response.status_code != 200:
    print("取得エラー:", response.json())
    exit()

quote = response.json()["data"][0]

date = quote["Date"]
open_price = quote["O"]
high_price = quote["H"]
low_price = quote["L"]
close_price = quote["C"]

message = f"""📈 トヨタ株価（{date}）
始値: {open_price}
高値: {high_price}
安値: {low_price}
終値: {close_price}
"""

# ===== LINEへ送信 =====
line_url = "https://api.line.me/v2/bot/message/push"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
}

payload = {
    "to": LINE_USER_ID,
    "messages": [{"type": "text", "text": message}]
}

line_response = requests.post(line_url, headers=headers, json=payload)

if line_response.status_code == 200:
    print("✅ LINE送信成功")
else:
    print("❌ LINE送信失敗:", line_response.status_code, line_response.text)
