# الصلاحيات المطلوبة على Android

## ✅ الصلاحيات المضافة

تم إضافة الصلاحيات التالية في `AndroidManifest.xml`:

### 1. صلاحيات الوصول للملفات:

```xml
<!-- Android 10-12 (API 29-32) -->
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" android:maxSdkVersion="32" />

<!-- Android 13+ (API 33+) -->
<uses-permission android:name="android.permission.READ_MEDIA_IMAGES" />
<uses-permission android:name="android.permission.READ_MEDIA_VIDEO" />
<uses-permission android:name="android.permission.READ_MEDIA_AUDIO" />
<uses-permission android:name="android.permission.READ_MEDIA_VISUAL_USER_SELECTED" />
```

### 2. صلاحيات الشبكة:

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

### 3. Queries للوصول إلى File Picker:

```xml
<queries>
    <intent>
        <action android:name="android.intent.action.GET_CONTENT"/>
    </intent>
    <intent>
        <action android:name="android.intent.action.OPEN_DOCUMENT"/>
    </intent>
</queries>
```

## 🔧 التحسينات المضافة

### 1. استخدام `withData: true`:
- الآن FilePicker يحصل على محتوى الملف مباشرة
- إذا كان `path` غير متاح، يتم حفظ الملف في مجلد مؤقت

### 2. معالجة الملفات المؤقتة:
- استخدام `path_provider` لحفظ الملفات في مجلد مؤقت
- الملفات المحفوظة يمكن الوصول إليها للرفع

## 📱 خطوات التشغيل

### 1. إعادة بناء التطبيق:

```bash
cd flutter_app
flutter clean
flutter pub get
flutter build apk
# أو
flutter run
```

### 2. منح الصلاحيات يدوياً (إذا لزم الأمر):

**على Android 10-12:**
- Settings > Apps > Corrosion App > Permissions
- فعّل "Storage" أو "Files and media"

**على Android 13+:**
- عند اختيار الملف لأول مرة، سيطلب النظام الصلاحيات تلقائياً
- اختر "Allow access to all files" أو "Allow access to selected files"

## 🧪 اختبار

1. افتح التطبيق
2. اذهب إلى شاشة "رفع ملف"
3. اضغط "اختر ملف CSV"
4. اختر ملف CSV من:
   - Downloads
   - Documents
   - أي مجلد آخر
5. يجب أن يتم اختيار الملف ورفعه تلقائياً

## ⚠️ ملاحظات مهمة

1. **Android 13+**: قد تحتاج إلى منح صلاحيات عند الطلب
2. **Scoped Storage**: Android 10+ يستخدم Scoped Storage، FilePicker يتعامل معه تلقائياً
3. **Temporary Files**: الملفات المحفوظة في المجلد المؤقت تُحذف تلقائياً بعد الاستخدام

## 🐛 استكشاف الأخطاء

### المشكلة: لا يفتح File Picker

**الحل:**
- تأكد من إعادة بناء التطبيق بعد إضافة الصلاحيات
- تحقق من أن `queries` موجودة في AndroidManifest.xml

### المشكلة: يفتح لكن لا يمكن اختيار الملف

**الحل:**
- تأكد من منح الصلاحيات في Settings
- جرب اختيار ملف من Downloads أو Documents

### المشكلة: الملف لا يُرفع

**الحل:**
- تحقق من أن Backend يعمل
- تحقق من `baseUrl` في `api_service.dart`
- راجع سجلات التطبيق للأخطاء

---

**تم إضافة جميع الصلاحيات المطلوبة! ✅**

