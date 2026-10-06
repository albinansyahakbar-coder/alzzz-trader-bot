import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Mengambil token dan chat_id dari Environment Variable Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")


def send_telegram_signal(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)


@app.route("/", methods=["GET"])
def home():
    return "Bot AlZzz Trader Aktif!", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if data:
        order_type = data.get("order_type", "-")
        price = data.get("price", "-")
        reason = data.get("reason", "Tidak ada keterangan")
        strength = data.get("strength", "Sideways")

        signal_msg = (
            f"📊 *SINYAL TRADING XAUUSD*\n"
            f"───────────────────\n"
            f"📌 *Order:* {order_type} @ {price}\n"
            f"⚡ *Kekuatan Sinyal:* {strength}\n"
            f"📝 *Alasan:* {reason}\n"
            f"───────────────────"
        )

        send_telegram_signal(signal_msg)
        return "OK", 200
    return "No Data", 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
