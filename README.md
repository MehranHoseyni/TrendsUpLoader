# TrendsUpLoader

سیستم خودکار استخراج ترندهای ایرانی و انتشار ویدیوهای مرتبط در یوتیوب با GitHub Actions.

## راه‌اندازی
1. مخزن را Clone کنید.
2. Secrets زیر را در تنظیمات GitHub > Settings > Secrets and variables تنظیم کنید:
   - YOUTUBE_API_KEY
   - PEXELS_API_KEY
   - PIXABAY_API_KEY
3. درصورت نیاز `requirements.txt` را نصب کنید:
   ```bash
   pip install -r requirements.txt
