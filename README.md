
# ربات تلگرام فارسی

ربات تلگرام شخصی‌سازی شده با قابلیت‌های زیر:

## ویژگی‌ها
- 🎵 جستجوی موزیک فارسی
- 😂 جک‌های فارسی
- 🗣️ تبدیل متن به صوت
- 💬 گفتگوی هوشمند با AI

## نصب و راه‌اندازی

1. کلون کردن پروژه:
```bash
git clone https://github.com/YOUR_USERNAME/persian-telegram-bot.git
cd persian-telegram-bot
```

2. نصب وابستگی‌ها:
```bash
pip install -r requirements.txt
```

3. تنظیم متغیرهای محیطی:
- فایل `.env.example` را کپی کرده و به نام `.env` ذخیره کنید
- مقادیر مورد نیاز را وارد کنید

4. اجرای ربات:
```bash
python main.py
```

## متغیرهای محیطی مورد نیاز
- `TELEGRAM_TOKEN`: توکن ربات تلگرام
- `GEMINI_API_KEY`: کلید API گوگل جمینی
- `YOUTUBE_API_KEY`: کلید API یوتیوب (اختیاری)
- `ELEVENLABS_API_KEY`: کلید API ElevenLabs (اختیاری)

## دستورات ربات
- `/start` - شروع کار با ربات
- `/help` - راهنمای کامل
- `/song [نام آهنگ]` - جستجوی موزیک
- `/joke` - جک تازه
- `/talk [پیام]` - گفتگو با AI
