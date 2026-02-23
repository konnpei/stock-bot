# stock_bot.py - 完全版
import requests
import os
from dotenv import load_dotenv

# ===== .env 読み込み =====
load_dotenv()

API_KEY = os.getenv("JQUANTS_API_KEY")
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")

# ===== 環境変数確認 =====
print("=== 環境変数確認 ===")
print("B_NnjfS0OpIGn5uC6fac9FEgLFZzBKhYjM0_YkkIVQ", (API_KEY[:10] + "...") if API_KEY else "なし")
print("4XjMJXwNI8Xm669/RNs69/KICRe9jaG8KmUvMPzsye5969fX61beEK6RUbdKlBuiHSRo/xmiamKxclLylysLY9vjFpPslwKwnyIgKc1s50X/RuK3Plc3/Gc8t2BKK9IIfra1BO9cAIT0/jqKdvUC7gdB04t89/1O/w1cDnyilFU=", (LINE_ACCESS_TOKEN[:10] + "...") if LINE_ACCESS_TOKEN else "なし")
print("U3900fb6357ff8ba7767f6f808f85e14a", LINE_USER_ID if LINE_USER_ID else "なし")

# ===== J-Quants 株価取得 =====
print("\n=== J-Quants株価取得開始 ===")
if not API_KEY:
    print("⚠️ J-Quants APIキーが設定されていません")
    exit()

headers = {"x-api-key": API_KEY}
response = requests.get(
    "https://api.jquants.com/v1/prices/daily_quotes",
    params={"code": "72030"},  # トヨタの銘柄コード
    headers=headers
)

print("HTTPステータスコード:", response.status_code)
try:
    data = response.json()
except Exception as e:
    print("JSON変換エラー:", e)
    exit()

if response.status_code != 200:
    print("取得エラー:", data)
    exit()

quote = data["data"][0]
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

print("株価取得成功:\n", message)

# ===== LINE送信 =====
print("\n=== LINE送信開始 ===")
if not LINE_ACCESS_TOKEN or not LINE_USER_ID:
    print("⚠️ LINEトークンまたはユーザーIDが設定されていません")
    exit()

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
print("LINE送信ステータスコード:", line_response.status_code)
if line_response.status_code != 200:
    print("LINE送信エラー:", line_response.text)
else:
    print("LINE送信成功 ✅")
