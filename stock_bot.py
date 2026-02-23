import requests
import os

API_KEY = os.getenv("JQUANTS_API_KEY")
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")

# ===== J-Quantsから取得 =====
headers = {"x-api-key": API_KEY}

response = requests.get(
    "https://api.jquants.com/v1/prices/daily_quotes",
    params={"code": "72030"},
    headers=headers
)

data = response.json()

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

print("LINE送信:", line_response.status_code)
