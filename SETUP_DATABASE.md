# دليل إعداد قاعدة البيانات وتشغيل الباك اند

## الخطوة 1: إعداد قاعدة البيانات MySQL

### الطريقة 1: استخدام السكريبت (الأسهل)

```bash
cd backend
./setup_database.sh
```

سيطلب منك كلمة مرور MySQL (root) ثم يقوم بإنشاء قاعدة البيانات تلقائياً.

### الطريقة 2: يدوياً

```bash
# 1. تسجيل الدخول إلى MySQL
mysql -u root -p

# 2. في MySQL، قم بتشغيل ملف schema
source /path/to/backend/database/schema.sql

# أو مباشرة من Terminal:
mysql -u root -p < backend/database/schema.sql
```

### التحقق من إنشاء قاعدة البيانات

```bash
mysql -u root -p -e "SHOW DATABASES;" | grep corrosion_db
```

إذا ظهر `corrosion_db`، فالقاعدة تم إنشاؤها بنجاح!

---

## الخطوة 2: إعداد ملف .env

قم بإنشاء ملف `.env` في مجلد `backend/`:

```bash
cd backend
nano .env
```

أدخل البيانات التالية (عدّل كلمة المرور حسب إعداداتك):

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=corrosion_db
FLASK_ENV=development
FLASK_PORT=5000
```

**ملاحظة**: إذا لم يكن لديك كلمة مرور لـ MySQL، اترك `DB_PASSWORD=` فارغاً.

---

## الخطوة 3: تثبيت المكتبات المطلوبة

```bash
cd backend

# إنشاء بيئة افتراضية (اختياري لكن موصى به)
python3 -m venv venv
source venv/bin/activate  # على Windows: venv\Scripts\activate

# تثبيت المكتبات
pip install -r requirements.txt
```

---

## الخطوة 4: تشغيل الباك اند

### الطريقة 1: استخدام السكريبت (الأسهل)

```bash
cd backend
./start_server.sh
```

### الطريقة 2: يدوياً

```bash
cd backend
source venv/bin/activate  # إذا كنت تستخدم بيئة افتراضية
python app.py
```

الخادم سيعمل على: `http://localhost:5000`

---

## الخطوة 5: الاتصال من Android Emulator

### المشكلة:
Android Emulator لا يمكنه الوصول إلى `localhost` على جهازك. يجب استخدام عنوان IP المحلي.

### الحل:

#### 1. معرفة عنوان IP المحلي

**على macOS:**
```bash
ipconfig getifaddr en0
# أو
ipconfig getifaddr en1
```

**على Linux:**
```bash
hostname -I | awk '{print $1}'
# أو
ip addr show | grep "inet " | grep -v 127.0.0.1
```

**على Windows:**
```bash
ipconfig
# ابحث عن IPv4 Address
```

#### 2. تعديل Flutter App

افتح ملف `flutter_app/lib/services/api_service.dart` وعدّل:

```dart
class ApiService {
  // استبدل localhost بعنوان IP المحلي
  // مثال: static const String baseUrl = 'http://192.168.1.100:5000/api';
  static const String baseUrl = 'http://YOUR_LOCAL_IP:5000/api';
  
  // للتشغيل على نفس الجهاز (web/desktop):
  // static const String baseUrl = 'http://localhost:5000/api';
```

**مثال:**
```dart
static const String baseUrl = 'http://192.168.1.50:5000/api';
```

#### 3. التأكد من أن Firewall يسمح بالاتصال

**على macOS:**
- System Preferences > Security & Privacy > Firewall
- تأكد من أن Python/Flask مسموح له

**على Linux:**
```bash
sudo ufw allow 5000
```

**على Windows:**
- Windows Defender Firewall > Allow an app
- أضف Python أو Flask

---

## الخطوة 6: اختبار الاتصال

### 1. اختبار Backend من Terminal:

```bash
# فحص حالة الخادم
curl http://localhost:5000/api/health

# يجب أن يعيد: {"status":"healthy","message":"Corrosion Rate API is running"}
```

### 2. اختبار من Android Emulator:

في Flutter App، افتح شاشة "رفع ملف" أو "حساب" وحاول استخدام التطبيق.

إذا ظهرت رسالة خطأ، تحقق من:
- ✅ Backend يعمل على `localhost:5000`
- ✅ عنوان IP صحيح في `api_service.dart`
- ✅ Firewall يسمح بالاتصال
- ✅ الـ emulator والكمبيوتر على نفس الشبكة

---

## استكشاف الأخطاء

### مشكلة: لا يمكن الاتصال بقاعدة البيانات

```bash
# تحقق من أن MySQL يعمل
mysql -u root -p -e "SELECT 1;"

# تحقق من بيانات الاتصال في .env
cat backend/.env
```

### مشكلة: Port 5000 مستخدم

```bash
# ابحث عن العملية التي تستخدم المنفذ
lsof -i :5000

# أو غيّر المنفذ في .env
FLASK_PORT=5001
```

### مشكلة: Android Emulator لا يتصل

1. تأكد من استخدام `10.0.2.2` للوصول إلى localhost من Android Emulator:
   ```dart
   static const String baseUrl = 'http://10.0.2.2:5000/api';
   ```
   
   **ملاحظة**: `10.0.2.2` هو عنوان خاص للـ Android Emulator يشير إلى localhost على جهازك.

2. أو استخدم عنوان IP المحلي كما هو موضح أعلاه.

---

## ملخص الأوامر السريعة

```bash
# 1. إنشاء قاعدة البيانات
cd backend && ./setup_database.sh

# 2. تشغيل الخادم
cd backend && ./start_server.sh

# 3. في Terminal آخر: تشغيل Flutter
cd flutter_app && flutter run -d emulator-5554
```

---

## نصائح إضافية

1. **لتشغيل Backend في الخلفية:**
   ```bash
   nohup python app.py > server.log 2>&1 &
   ```

2. **لإيقاف Backend:**
   ```bash
   pkill -f "python app.py"
   ```

3. **لرؤية سجلات الخادم:**
   ```bash
   tail -f server.log
   ```

4. **لوحة التحكم على الويب:**
   افتح المتصفح واذهب إلى: `http://localhost:5000/dashboard`

---

**تم! الآن يجب أن يعمل كل شيء بشكل صحيح! 🎉**

