# تغيير المنفذ من 5000 إلى 5001

## المشكلة
المنفذ 5000 مستخدم بواسطة AirPlay Receiver على macOS، لذلك تم تغيير المنفذ إلى **5001**.

## ما تم تحديثه:

### ✅ Backend
- `config.py` - المنفذ الافتراضي: **5001**
- `.env` - `FLASK_PORT=5001`
- `dashboard.html` - API URL: `http://localhost:5001/api`

### ✅ Flutter App
- `api_service.dart` - `baseUrl`: `http://10.0.2.2:5001/api`

## الآن يمكنك:

### 1. تشغيل Backend:
```bash
cd backend
python app.py
```

الخادم سيعمل الآن على: **http://localhost:5001**

### 2. الوصول إلى Dashboard:
افتح المتصفح: **http://localhost:5001/dashboard**

### 3. Flutter App:
التطبيق جاهز للاتصال على المنفذ **5001** ✅

---

## ملاحظة:
إذا أردت استخدام منفذ آخر، غيّر:
1. `FLASK_PORT` في ملف `.env`
2. `baseUrl` في `flutter_app/lib/services/api_service.dart`
3. `API_URL` في `backend/static/dashboard.html`

