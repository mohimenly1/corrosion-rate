# دليل الإعداد والتشغيل

## المتطلبات الأساسية

### 1. Python 3.8 أو أحدث
```bash
python3 --version
```

### 2. MySQL
قم بتثبيت MySQL على نظامك:
- **macOS**: `brew install mysql`
- **Linux**: `sudo apt-get install mysql-server`
- **Windows**: قم بتحميل MySQL من الموقع الرسمي

### 3. Flutter SDK
قم بتثبيت Flutter من [flutter.dev](https://flutter.dev)

## خطوات الإعداد

### 1. إعداد قاعدة البيانات

```bash
# تسجيل الدخول إلى MySQL
mysql -u root -p

# إنشاء قاعدة البيانات والجداول
source backend/database/schema.sql

# أو مباشرة:
mysql -u root -p < backend/database/schema.sql
```

### 2. إعداد Backend

```bash
cd backend

# إنشاء بيئة افتراضية (اختياري لكن موصى به)
python3 -m venv venv
source venv/bin/activate  # على Windows: venv\Scripts\activate

# تثبيت المكتبات
pip install -r requirements.txt

# إنشاء ملف .env
cp .env.example .env

# تعديل ملف .env وإدخال بيانات قاعدة البيانات
nano .env  # أو استخدم أي محرر نصوص
```

ملف `.env` يجب أن يحتوي على:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=corrosion_db
FLASK_ENV=development
FLASK_PORT=5000
```

### 3. تشغيل Backend

```bash
# من مجلد backend
python app.py

# أو استخدام السكريبت
./run.sh
```

الخادم سيعمل على: `http://localhost:5000`

يمكنك الوصول للوحة التحكم على: `http://localhost:5000/static/dashboard.html`

### 4. إعداد Flutter App

```bash
cd flutter_app

# تثبيت المكتبات
flutter pub get

# للتشغيل على الويب
flutter run -d chrome

# للتشغيل على Android/iOS
flutter run
```

**ملاحظة مهمة**: إذا كنت تشغل Flutter على جهاز محمول، قم بتغيير `baseUrl` في `lib/services/api_service.dart`:

```dart
// استبدل localhost بعنوان IP جهازك
static const String baseUrl = 'http://192.168.1.X:5000/api';
```

يمكنك معرفة عنوان IP جهازك:
- **macOS/Linux**: `ifconfig | grep "inet "`
- **Windows**: `ipconfig`

## اختبار التطبيق

### 1. اختبار Backend API

```bash
# فحص حالة الخادم
curl http://localhost:5000/api/health

# جلب العينات
curl http://localhost:5000/api/samples

# جلب الإحصائيات
curl http://localhost:5000/api/statistics
```

### 2. رفع ملف CSV تجريبي

يمكنك استخدام الملفات الموجودة في المجلد الرئيسي:
- `corrosion_50_points_full.csv`
- `NaCl_50samples_corrosion_table_with_sources.csv`

### 3. اختبار حساب معدل التآكل

استخدم Flutter App أو Dashboard لإدخال البيانات:
- Material: `API-5L X65`
- Temperature: `25`
- pH: `7`
- NaCl %: `3.5`
- Medium: `NaCl`

## استكشاف الأخطاء

### مشكلة: لا يمكن الاتصال بقاعدة البيانات

1. تأكد من تشغيل MySQL:
```bash
# macOS/Linux
sudo service mysql start
# أو
brew services start mysql
```

2. تحقق من بيانات الاتصال في ملف `.env`

3. تأكد من إنشاء قاعدة البيانات والجداول

### مشكلة: Flutter لا يتصل بالخادم

1. تأكد من تشغيل Backend على `localhost:5000`

2. تحقق من `baseUrl` في `api_service.dart`

3. على الأجهزة المحمولة، استخدم عنوان IP بدلاً من `localhost`

4. تأكد من أن Firewall يسمح بالاتصال على المنفذ 5000

### مشكلة: خطأ في رفع ملف CSV

1. تأكد من أن الملف بصيغة CSV

2. تحقق من أن الملف يحتوي على الأعمدة المطلوبة

3. راجع سجلات الخادم للأخطاء

## البنية التحتية

```
corrosion-app/
├── backend/                 # Python Flask Backend
│   ├── app.py              # التطبيق الرئيسي
│   ├── config.py            # الإعدادات
│   ├── requirements.txt    # المكتبات المطلوبة
│   ├── database/
│   │   ├── schema.sql      # هيكل قاعدة البيانات
│   │   └── db_connection.py # اتصال قاعدة البيانات
│   ├── services/
│   │   ├── corrosion_calculator.py  # حساب معدل التآكل
│   │   └── csv_processor.py         # معالجة CSV
│   └── static/
│       └── dashboard.html   # لوحة التحكم
│
├── flutter_app/            # Flutter Frontend
│   ├── lib/
│   │   ├── main.dart       # نقطة البداية
│   │   ├── models/         # نماذج البيانات
│   │   ├── services/       # خدمات API
│   │   ├── providers/      # State Management
│   │   └── screens/        # شاشات التطبيق
│   └── pubspec.yaml        # تبعيات Flutter
│
├── *.csv                   # ملفات البيانات التجريبية
├── README.md               # الوثائق الرئيسية
└── SETUP.md               # هذا الملف
```

## الدعم

إذا واجهت أي مشاكل، راجع:
1. سجلات الخادم (Backend)
2. سجلات Flutter (Frontend)
3. سجلات MySQL

## التطوير المستقبلي

- [ ] إضافة Authentication
- [ ] تحسين واجهة Dashboard
- [ ] إضافة المزيد من المعادلات
- [ ] استخدام Machine Learning
- [ ] تصدير التقارير PDF
- [ ] دعم Real-time updates

