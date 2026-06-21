DANYA DEV Telegram Bot for Koyeb

Файлы для репозитория:
- main.py
- requirements.txt
- Procfile

Переменные окружения в Koyeb:
BOT_TOKEN = новый токен от BotFather
ADMIN_ID = 1600348576
YOUR_USERNAME = HTML_PRO5
WEBHOOK_SECRET = danya-secret-2026
APP_URL = ссылка Koyeb, например https://your-app.koyeb.app

Важно:
1. Старый токен, который был в коде, уже засветился. Перевыпусти его в BotFather:
   /mybots → твой бот → API Token → Revoke current token
2. Новый токен НЕ вставляй в код. Вставь его только в переменную BOT_TOKEN в Koyeb.
3. После деплоя открой APP_URL в браузере. Должно показать:
   {"status":"DANYA DEV bot is running","webhook":"enabled"}
4. Потом напиши боту /start.
