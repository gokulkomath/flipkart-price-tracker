# 📉 Flipkart Price Tracker

A simple command-line Python tool to monitor the price of a Flipkart product and optionally receive Telegram alerts when the product hits a new **lowest price** since tracking started.

---

## 🚀 Features

- ✅ Track the price of any Flipkart product.
- ✅ Record and timestamp price changes locally.
- ✅ Send Telegram notifications using **CallMeBot** when a new lowest price is detected.
- ✅ View price history.
- ✅ Reset data with a single command.

---

## 🧰 Requirements

```bash
pip install requests beautifulsoup4
```

### 🔔 Enabling Telegram Notifications

To enable Telegram alerts for price drops:

1. Visit 👉 [https://www.callmebot.com/blog/telegram-text-messages/](https://www.callmebot.com/blog/telegram-text-messages/)
2. Follow the instructions on that page to get your **CallMeBot Telegram API link**.
   - You’ll need to send a message to `@CallMeBot` on Telegram and follow the setup steps.
3. During script setup (`--set`), paste your **API URL** when prompted:
