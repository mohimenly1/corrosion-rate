# دليل البدء السريع 🚀

## الخطوات السريعة لإعداد وتشغيل المشروع

### 1️⃣ إنشاء قاعدة البيانات (مرة واحدة فقط)

```bash
cd backend
./setup_database.sh
```

أدخل كلمة مرور MySQL عندما يُطلب منك.

**أو يدوياً:**
```bash
mysql -u root -p < backend/database/schema.sql
```

---

### 2️⃣ إعداد ملف .env

```bash
cd backend
nano .env
```

أدخل:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=corrosion_db
FLASK_ENV=development
FLASK_PORT=5000
```

---

### 3️⃣ تثبيت المكتبات (مرة واحدة فقط)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 4️⃣ تشغيل Backend

```bash
cd backend
./start_server.sh
```

أو:
```bash
cd backend
source venv/bin/activate
python app.py
```

✅ الخادم يعمل الآن على: `http://localhost:5000`

---

### 5️⃣ تشغيل Flutter App على Emulator

في Terminal جديد:

```bash
cd flutter_app
flutter run -d emulator-5554
```

---

## ✅ التحقق من أن كل شيء يعمل

### اختبار Backend:
```bash
curl http://localhost:5000/api/health
```

يجب أن يعيد: `{"status":"healthy",...}`

### اختبار من Flutter:
- افتح التطبيق على الـ emulator
- جرب رفع ملف CSV أو حساب معدل التآكل

---

## 🔧 إعدادات الاتصال للـ Emulator

تم إعداد `api_service.dart` لاستخدام `10.0.2.2` للـ Android Emulator.

**إذا كنت تستخدم:**
- ✅ **Android Emulator**: `10.0.2.2` (جاهز بالفعل)
- 📱 **جهاز Android حقيقي**: غيّر إلى عنوان IP المحلي (مثال: `192.168.0.14`)
- 🍎 **iOS Simulator**: استخدم `localhost` أو عنوان IP المحلي
- 🌐 **Web**: استخدم `localhost`

**لتغيير الإعدادات:**
افتح `flutter_app/lib/services/api_service.dart` وعدّل `baseUrl`.

---

## 📍 عنوان IP المحلي لديك

**عنوان IP المحلي**: `192.168.0.14`

استخدمه إذا كنت تستخدم جهاز حقيقي أو iOS Simulator.

---

## 🆘 استكشاف الأخطاء

### Backend لا يعمل؟
```bash
# تحقق من أن MySQL يعمل
mysql -u root -p -e "SELECT 1;"

# تحقق من ملف .env
cat backend/.env
```

### Flutter لا يتصل بالـ Backend؟
1. تأكد من أن Backend يعمل
2. تحقق من `baseUrl` في `api_service.dart`
3. للـ Android Emulator: استخدم `10.0.2.2`
4. للأجهزة الحقيقية: استخدم عنوان IP المحلي

---

## 📚 الملفات المساعدة

- `SETUP_DATABASE.md` - دليل مفصل لإعداد قاعدة البيانات
- `README.md` - الوثائق الكاملة
- `SETUP.md` - دليل الإعداد الشامل

---

**جاهز للبدء! 🎉**

