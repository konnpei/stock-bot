# stock_bot_direct.py
import requests

# ===== ここにあなたのキーを貼り付ける =====
API_KEY = "RB_NnjfS0OpIGn5uC6fac9FEgLFZzBKhYjM0_YkkIVQ"
LINE_ACCESS_TOKEN = "4XjMJXwNI8Xm669/RNs69/KICRe9jaG8KmUvMPzsye5969fX61beEK6RUbdKlBuiHSRo/xmiamKxclLylysLY9vjFpPslwKwnyIgKc1s50X/RuK3Plc3/Gc8t2BKK9IIfra1BO9cAIT0/jqKdvUC7gdB04t89/1O/w1cDnyilFU="
LINE_USER_ID = "U3900fb6357ff8ba7767f6f808f85e14a"

print("=== キー確認 ===")
print("J-Quants APIキー:", API_KEY[:10] + "...")
print("LINEトークン:", LINE_ACCESS_TOKEN[:10] + "...")
print("LINEユーザーID:", LINE_USER_ID)

# ===== 株価取得 =====
headers = {"x-api-key": API_KEY}
response = requests.get(
    "https://api.jquants.com/v1/prices/daily_quotes",
    params={"code": "72030"},  # トヨタ
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

print("株価取得成功:\n", message)

# ===== LINE送信 =====
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
    print("LINE送信成功 ✅")
else:
    print("LINE送信エラー:", line_response.text)
