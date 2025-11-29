# إصلاح مشكلة اختيار الملفات على الهاتف

## المشكلة
عند محاولة اختيار ملف CSV من التطبيق على الهاتف، لا يتم اختيار الملف.

## الحلول المطبقة

### 1. ✅ إضافة الصلاحيات المطلوبة

#### Android (`AndroidManifest.xml`):
- إضافة `queries` للوصول إلى الملفات:
  - `android.intent.action.GET_CONTENT`
  - `android.intent.action.OPEN_DOCUMENT`
- إضافة صلاحيات القراءة:
  - `READ_EXTERNAL_STORAGE` (لـ Android 10-12)
  - `READ_MEDIA_*` (لـ Android 13+)

#### iOS (`Info.plist`):
- إضافة `UISupportsDocumentBrowser`
- إضافة `UIFileSharingEnabled`
- إضافة `LSSupportsOpeningDocumentsInPlace`

### 2. ✅ تحسين معالجة الأخطاء

- التحقق من وجود الملف قبل الرفع
- رسائل خطأ واضحة للمستخدم
- معالجة حالات مختلفة (path null, bytes null, etc.)

### 3. ✅ تحسين إعدادات FilePicker

- `allowMultiple: false` - ملف واحد فقط
- `withData: false` - لا نحتاج البيانات في الذاكرة
- `withReadStream: false` - لا نحتاج stream

## خطوات إضافية قد تكون مطلوبة

### على Android:

1. **إعادة بناء التطبيق:**
   ```bash
   cd flutter_app
   flutter clean
   flutter pub get
   flutter build apk
   ```

2. **التحقق من الصلاحيات في الإعدادات:**
   - اذهب إلى Settings > Apps > Corrosion App > Permissions
   - تأكد من تفعيل "Storage" أو "Files and media"

3. **اختبار على أجهزة مختلفة:**
   - Android 10-12: يحتاج READ_EXTERNAL_STORAGE
   - Android 13+: يحتاج READ_MEDIA_* permissions

### على iOS:

1. **إعادة بناء التطبيق:**
   ```bash
   cd flutter_app
   flutter clean
   flutter pub get
   flutter build ios
   ```

2. **التحقق من Info.plist:**
   - تأكد من وجود جميع المفاتيح المطلوبة

## استكشاف الأخطاء

### المشكلة: لا يفتح file picker

**الحل:**
- تأكد من إعادة بناء التطبيق بعد إضافة الصلاحيات
- تحقق من السجلات (logs) في Android Studio/Xcode

### المشكلة: يفتح picker لكن لا يمكن اختيار الملف

**الحل:**
- تأكد من أن الملف موجود في مكان يمكن الوصول إليه
- جرب اختيار ملف من Downloads أو Documents

### المشكلة: "الملف المختار غير متاح"

**الحل:**
- قد يكون الملف في موقع محمي
- جرب نسخ الملف إلى Downloads أو Documents أولاً
- على Android 13+، قد تحتاج إلى منح صلاحيات إضافية

## ملاحظات مهمة

1. **Android Scoped Storage:**
   - Android 10+ يستخدم Scoped Storage
   - FilePicker يستخدم Storage Access Framework تلقائياً
   - لا حاجة لصلاحيات إضافية في معظم الحالات

2. **iOS Document Picker:**
   - iOS يستخدم UIDocumentPickerViewController
   - يعمل تلقائياً مع الصلاحيات المضافة

3. **اختبار:**
   - اختبر على emulator أولاً
   - ثم اختبر على جهاز حقيقي
   - تأكد من منح الصلاحيات عند الطلب

---

**بعد إجراء هذه التغييرات، أعد بناء التطبيق واختبره مرة أخرى.**

