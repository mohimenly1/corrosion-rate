# نموذج معدل التآكل - Corrosion Rate Modeling Application

تطبيق شامل لنمذجة وحساب معدل التآكل مع واجهة عصرية ولوحة تحكم.

## المكونات

### 1. Backend (Python Flask)
- **المسار**: `backend/`
- **اللغة**: Python 3.x
- **الإطار**: Flask
- **قاعدة البيانات**: MySQL

### 2. Frontend (Flutter)
- **المسار**: `flutter_app/`
- **اللغة**: Dart
- **الإطار**: Flutter

## متطلبات التشغيل

### Backend
```bash
cd backend
pip install -r requirements.txt
```

### Flutter
```bash
cd flutter_app
flutter pub get
```

## إعداد قاعدة البيانات

1. قم بتثبيت MySQL على جهازك
2. قم بإنشاء قاعدة البيانات:
```bash
mysql -u root -p < backend/database/schema.sql
```

3. قم بإعداد ملف `.env` في مجلد `backend/`:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=corrosion_db
FLASK_ENV=development
FLASK_PORT=5000
```

## تشغيل التطبيق

### 1. تشغيل Backend
```bash
cd backend
python app.py
```

الخادم سيعمل على: `http://localhost:5000`

### 2. تشغيل Flutter App
```bash
cd flutter_app
flutter run
```

## الميزات

### 1. حساب معدل التآكل
- إدخال البيانات يدوياً (نوع العينة، درجة الحرارة، pH، نسبة NaCl، الوسط)
- حساب تلقائي لمعدل التآكل باستخدام معادلات تجريبية
- عرض النتائج بوحدات مختلفة (mm/yr و mpy)

### 2. رفع ملفات CSV
- رفع ملفات CSV تحتوي على بيانات التآكل
- معالجة تلقائية للبيانات
- حفظ البيانات في قاعدة البيانات

### 3. عرض البيانات
- جدول تفاعلي يعرض جميع العينات
- فلترة البيانات حسب المعايير المختلفة
- عرض معدلات التآكل مع ألوان تمييزية

### 4. الإحصائيات والمقارنات
- **معدل التآكل مقابل pH**: رسم بياني خطي
- **معدل التآكل مقابل درجة الحرارة**: رسم بياني خطي
- **معدل التآكل مقابل الوسط**: رسم بياني عمودي
- **مقارنة المواد**: جدول مقارنة بين أنواع العينات المختلفة

## هيكل البيانات

### حقول CSV المطلوبة:
- `Material`: نوع العينة (مثال: API-5L X65, Carbon steel)
- `Temperature` أو `Temp (°C)`: درجة الحرارة
- `pH`: قيمة pH
- `NaCl (%)` أو `NaCl (wt%)`: نسبة كلوريد الصوديوم
- `Medium` أو `Environment`: نوع الوسط
- `Corrosion Rate (mm/yr)` أو `Corrosion_mm_per_yr`: معدل التآكل
- `Corrosion Rate (mpy)` أو `Corrosion_mpy`: معدل التآكل بوحدة mpy

## API Endpoints

### Backend API
- `GET /api/health` - فحص حالة الخادم
- `POST /api/upload-csv` - رفع ملف CSV
- `POST /api/calculate-corrosion-rate` - حساب معدل التآكل
- `GET /api/samples` - جلب العينات (مع فلترة اختيارية)
- `GET /api/statistics` - جلب الإحصائيات
- `GET /api/materials` - جلب قائمة المواد
- `GET /api/mediums` - جلب قائمة الأوساط

## ملاحظات مهمة

1. **للتشغيل على الأجهزة المحمولة**: قم بتغيير `baseUrl` في `flutter_app/lib/services/api_service.dart` إلى عنوان IP جهازك بدلاً من `localhost`

2. **الملفات التجريبية**: يوجد ملفان CSV في المجلد الرئيسي:
   - `corrosion_50_points_full.csv`
   - `NaCl_50samples_corrosion_table_with_sources.csv`

3. **المعادلات المستخدمة**: يستخدم التطبيق معادلات تجريبية متعددة العوامل تأخذ في الاعتبار:
   - تأثير درجة الحرارة (علاقة Arrhenius)
   - تأثير pH (أقل تآكل عند pH 7-8)
   - تأثير تركيز NaCl
   - نوع المادة (API-5L X65 أكثر مقاومة من Carbon steel)
   - نوع الوسط (ماء البحر، أحماض، إلخ)

## التطوير المستقبلي

- إضافة المزيد من المعادلات التجريبية
- استخدام نماذج Machine Learning للتنبؤ
- تصدير التقارير بصيغة PDF
- إضافة المزيد من أنواع الرسوم البيانية
- دعم اللغات المتعددة

## الرخصة

هذا المشروع مفتوح المصدر ومتاح للاستخدام والتطوير.

